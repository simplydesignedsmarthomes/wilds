"""Find items the wiki has added since the last check, so a future game
update can't silently leave something out of the app.

Compares the wiki's infobox_item bucket (every item page on the wiki) against
known-wiki-items.json, last run's snapshot. Anything new with an unambiguous
item_type (clearly a weapon, armour, food, ...) gets auto-filed into
auto-discovered.json with a best-guess chest, the same way every other
SOURCE_FILES entry works, so build_storage.py picks it straight up.

An item_type alone (Basic Item, Resource, Quest Item, ...) often spans
several chests - but the wiki also tags every page with its own MediaWiki
categories (Category:Farming, Category:Cooking, ...), which are a second,
independently-curated signal. When the type alone isn't enough, a handful of
those categories that map to exactly one chest get checked too (see
CATEGORY_TO_CHEST) - this is what let "Ultra Compost" (type: Resource, but
Category:Farming) and "Burnt Cactus Steak" (type: Basic Item, but
Category:Cooking) file themselves correctly the first time they ever showed
up, with no guess involved - the match is the wiki's own, not ours.

Only once BOTH signals come up empty does an item go to needs-review.json
for a person to place by hand - exactly the judgement call Miscellaneous
items needed (see build_storage.py's CHEST_OVERRIDES comment). That queue is
meant to stay small and rare, not a routine stop on every patch.

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
# Component, Container, Special Material, Pattern, Mount, Unknown, ...)
# spans several chests depending on the individual item, so those fall
# through to the category check below, then to needs-review as a last resort.
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
    # A quest item's mechanical "type" varies wildly (letter, trinket, rock...)
    # but it's never meant to be browsed as gear or a crafting material - it's
    # a narrative/collectible, exactly what Vestiges & Curios already holds
    # (see build_storage.py's CHEST_CONFLICT_RULES, which already prefers
    # vestiges over armour/potions/misc for the same reason).
    "Quest Item": "vestiges",
}

# A second, independent signal for the item_types above that aren't tied to
# one chest: the wiki's own MediaWiki categories, which it already curates
# page by page. Only categories that map to exactly one sensible chest, with
# no real-world exceptions seen so far - checked in this order, first match
# wins, since a page can carry several (a farming tool might also be tagged
# "Category:Tools", which Farming should win over - matches the same
# precedent as the Quest Item rule above).
CATEGORY_TO_CHEST = [
    ("Category:Farming", "farming"),
    ("Category:Cooking", "food"),
    ("Category:Fishing", "food"),
    ("Category:Woodcutting", "wood"),
    ("Category:Mining", "ores"),
    ("Category:Runecrafting", "runes"),
]

def fetch_categories(names):
    """page_name -> set of "Category:X" strings, batched 50 titles per call
    (MediaWiki's own limit for a single query)."""
    out = {}
    names = list(names)
    for i in range(0, len(names), 50):
        batch = names[i:i + 50]
        d = get({"action": "query", "titles": "|".join(batch), "prop": "categories",
                 "cllimit": "50", "format": "json", "formatversion": "2"})
        for page in d.get("query", {}).get("pages", []):
            out[page.get("title", "")] = {c["title"] for c in page.get("categories", [])}
        time.sleep(0.4)
    return out

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

    candidates = []
    for name in sorted(new_names):
        clean = clean_name(name)
        if not clean or clean in DROP_NAMES or clean in BUILD_MENU_PIECES:
            continue
        candidates.append((name, clean, current[name]))

    auto, review, needs_category_check = [], [], []
    for name, clean, item_type in candidates:
        chest = ITEM_TYPE_TO_CHEST.get(item_type)
        if chest:
            auto.append({"name": clean, "img": "", "tier": "", "tierRank": None, "chest": chest, "note": ""})
            print("  auto:   %-40s -> %s (type: %s)" % (clean, chest, item_type), file=sys.stderr)
        else:
            needs_category_check.append((name, clean, item_type))

    if needs_category_check:
        categories = fetch_categories(n for n, _, _ in needs_category_check)
        for name, clean, item_type in needs_category_check:
            cats = categories.get(name, set())
            chest = next((c for cat, c in CATEGORY_TO_CHEST if cat in cats), None)
            if chest:
                auto.append({"name": clean, "img": "", "tier": "", "tierRank": None, "chest": chest, "note": ""})
                matched_cat = next(cat for cat, c in CATEGORY_TO_CHEST if c == chest and cat in cats)
                print("  auto:   %-40s -> %s (%s)" % (clean, chest, matched_cat), file=sys.stderr)
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
