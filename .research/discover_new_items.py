"""Find items the wiki has added since the last check, so a future game
update can't silently leave something out of the app.

Compares the wiki's infobox_item bucket (every item page on the wiki) against
known-wiki-items.json, last run's snapshot. Anything new with an unambiguous
item_type (clearly a weapon, armour, food, ...) gets auto-filed into
auto-discovered.json with a best-guess chest, the same way every other
SOURCE_FILES entry works, so build_storage.py picks it straight up. Anything
without a confident type is left out of storage entirely (same as an item no
research pass has reached yet) and listed in needs-review.json instead, for a
person to place by hand - exactly the judgement call Miscellaneous items
needed (see build_storage.py's CHEST_OVERRIDES comment).

Always rewrites known-wiki-items.json to the current full list, whether or
not anything new was found, so the next run's diff is against today.

  python3 .research/discover_new_items.py
"""
import json, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_storage import clean_name, DROP_NAMES, BUILD_MENU_PIECES

API = "https://dragonwilds.runescape.wiki/api.php"
UA = "wilds-companion-data-refresh/1.0 (personal fan companion app)"

def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"user-agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 + attempt * 3)

def fetch_infobox_items():
    rows, offset, page = [], 0, 500
    sel = "'page_name','item_name','json'"
    while True:
        q = "bucket('infobox_item').select(%s).limit(%d).offset(%d).run()" % (sel, page, offset)
        d = get({"action": "bucket", "format": "json", "query": q})
        batch = d.get("bucket", [])
        rows.extend(batch)
        if len(batch) < page:
            break
        offset += page
        time.sleep(0.4)
    out = {}
    for r in rows:
        try:
            out[r["page_name"]] = json.loads(r["json"]).get("item_type") or ""
        except ValueError:
            continue
    return out

# Only item_types the wiki uses unambiguously for one chest. Everything else
# (Basic Item, Basic Material, Processed Material, Resource, Raw Ingredient,
# Component, Container, Quest Item, Special Material, Pattern, Mount,
# Unknown, ...) spans several chests depending on the individual item, so a
# new one of those always goes to needs-review instead of a guess.
ITEM_TYPE_TO_CHEST = {
    "Melee Weapon": "weapons", "Ranged Weapon": "weapons", "Magic Weapon": "weapons", "Bow": "weapons",
    "Melee Armour": "armour", "Ranged Armour": "armour", "Mage Armour": "armour",
    "Armour": "armour", "Shield": "armour", "Cape": "armour",
    "Trinket": "jewellery",
    "Food": "food",
    "Potion": "potions", "Drink": "potions", "Tome": "potions", "Consumable Tome": "potions",
    "Tool": "tools",
    "Arrow": "ammo", "Ammo": "ammo",
    "Seed": "farming",
    "Rune": "runes",
    "Vestige": "vestiges",
}

def main():
    known_path = os.path.join(HERE, "known-wiki-items.json")
    discovered_path = os.path.join(HERE, "auto-discovered.json")
    review_path = os.path.join(HERE, "needs-review.json")

    known = {}
    if os.path.exists(known_path):
        known = {r["name"]: r.get("type", "") for r in json.load(open(known_path, encoding="utf-8"))}
    already_discovered = set()
    if os.path.exists(discovered_path):
        already_discovered = {r["name"] for r in json.load(open(discovered_path, encoding="utf-8"))}

    current = fetch_infobox_items()
    new_names = [n for n in current if n not in known and n not in already_discovered]

    auto, review = [], []
    for name in sorted(new_names):
        clean = clean_name(name)
        if not clean or clean in DROP_NAMES or clean in BUILD_MENU_PIECES:
            continue
        item_type = current[name]
        chest = ITEM_TYPE_TO_CHEST.get(item_type)
        if chest:
            auto.append({"name": clean, "img": "", "tier": "", "tierRank": None, "chest": chest, "note": ""})
            print("  auto:   %-40s -> %s (%s)" % (clean, chest, item_type), file=sys.stderr)
        else:
            review.append({"name": clean, "type": item_type or "(none)",
                            "wikiUrl": "https://dragonwilds.runescape.wiki/w/" + urllib.parse.quote(name.replace(" ", "_"))})

    if auto:
        existing = json.load(open(discovered_path, encoding="utf-8")) if os.path.exists(discovered_path) else []
        json.dump(existing + auto, open(discovered_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    json.dump(review, open(review_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    snapshot = [{"name": n, "type": t} for n, t in sorted(current.items())]
    json.dump(snapshot, open(known_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    print("new wiki items: %d (%d auto-filed, %d need review)" % (len(new_names), len(auto), len(review)), file=sys.stderr)
    for r in review:
        print("  REVIEW: %-40s %s" % (r["name"], r["type"]), file=sys.stderr)

if __name__ == "__main__":
    main()
