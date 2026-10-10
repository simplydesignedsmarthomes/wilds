"""Pull every Build Menu recipe into construction.js for the app's
Construction tab: everything placeable from the build menu (crafting
stations, structure pieces, furniture, decorations...) with the materials it
costs, rendered with the same item-chip icons as the Items tab.

Build Menu recipes are already in the recipe bucket alongside every other
recipe - WikiData (normalize_detail.py) parses them the same way, chips and
all, so this script only has to pick out the ones whose facility is "Build
Menu" and group them for browsing. Re-run any time; always reflects whatever
is currently in wiki_buckets.json (run fetch_wiki_data.py first to refresh
that).

Writes construction.js (window.WILDS_CONSTRUCTION), shaped exactly like
storage.js's chest list so the app can reuse its item-grid rendering.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from normalize_detail import WikiData

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

def fetch_wiki_categories(names):
    out = {}
    for i in range(0, len(names), 50):
        chunk = names[i:i + 50]
        d = get({"action": "query", "prop": "categories", "cllimit": "max", "clshow": "!hidden",
                 "format": "json", "formatversion": "2", "redirects": "1", "titles": "|".join(chunk)})
        q = d["query"]
        back = {r["to"]: r["from"] for r in q.get("redirects", [])}
        norm = {n["to"]: n["from"] for n in q.get("normalized", [])}
        for p in q["pages"]:
            t = back.get(p["title"], p["title"])
            out[norm.get(t, t)] = {c["title"].split(":", 1)[1] for c in p.get("categories", [])}
        time.sleep(0.4)
    return out

# Checked in order, first hit wins. Name patterns are the primary signal
# (reliable and specific); the wiki's own "Crafting"/"Decorations" category
# tags fill in the rest where a name alone wouldn't say enough.
GROUP_RULES = [
    ("Crafting stations", r"'s Bench$|'s Table$|Forge$|Range$|Furnace$|Tannery$|Spinning Wheel$|Rune Altar$|Cauldron$|^Kiln$|^Loom$|Grindstone$|Imbuing Barrel$|Cooking Pot$|Pottery Wheel$|Stonecutter$|Sawmill$|Crafting Table$|Fletching (Bench|Table)$"),
    ("Roofs, walls & stairs", r"\bRoof\b|\bWall\b|\bStairs\b|\bBeam\b|\bPillar\b|\bWindow\b|\bDoor\b|\bFloor\b|\bFoundation\b|\bAwning\b|\bArch\b|\bGate\b|\bPalisade|\bFence\b|\bTile\b|\bWell\b"),
    ("Lighting", r"Torch|Chandelier|Lantern|Candle|Brazier|Lightning Rod"),
    ("Furniture & storage", r"Chair|\bBed\b|Table\b|Bookcase|Wardrobe|Shelf|\bStool\b|\bDesk\b|Cabinet|Dresser|Chest\b|Barrel$|\bCrate\b|\bBin\b|Pile$|Rack$|Nugget$|Awning$|Storage$|Mannequin|\bBox\b"),
    ("Banners, flags & trophies", r"Banner|\bFlag\b|Trophy|Pennant|Standard$"),
    ("Decorations", r"\(decoration\)"),  # wiki category fallback for the rest, checked below
    ("Farming & outdoor", r"Farming Plot|Scarecrow|Archery Target|Agility (Flag|Orb)|Barricade"),
]

def group_for(name, wiki_cats):
    for group, rx in GROUP_RULES:
        if rx and re.search(rx, name, re.I):
            return group
    cats = wiki_cats.get(name) or set()
    if "Crafting" in cats:
        return "Crafting stations"
    if "Decorations" in cats:
        return "Decorations"
    if {"Agility", "Attack"} & cats:
        return "Farming & outdoor"
    return "Other builds"

GROUP_ORDER = ["Crafting stations", "Roofs, walls & stairs", "Lighting", "Furniture & storage",
               "Banners, flags & trophies", "Decorations", "Farming & outdoor", "Other builds"]

def main():
    wiki = WikiData()
    b = json.load(open(os.path.join(HERE, "wiki_buckets.json"), encoding="utf-8"))
    names = sorted({r["page_name"] for r in b["recipe"]
                    if r.get("uses_facility") and "Build Menu" in str(r["uses_facility"])})

    wiki_cats = fetch_wiki_categories(names)

    by_group = {}
    skipped = 0
    for name in names:
        recs = wiki.lookup(wiki.recipes_by_output, name)
        rec = next((r for r in recs if r["station"] == "Build Menu"), recs[0] if recs else None)
        if not rec or not rec["materials"]:
            skipped += 1
            continue
        item = {
            "name": name, "img": rec["output"]["img"],
            "materials": [{"name": m["name"], "qty": m["qty"], "img": m["img"]} for m in rec["materials"]],
            "skills": rec["skills"],
        }
        by_group.setdefault(group_for(name, wiki_cats), []).append(item)

    out = []
    total = 0
    for key in GROUP_ORDER:
        items = sorted(by_group.get(key, []), key=lambda it: it["name"].lower())
        if not items:
            continue
        out.append({"key": re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-"), "label": key, "items": items})
        total += len(items)

    header = ("/* Generated by .research/fetch_construction_data.py from the RuneScape: Dragonwilds\n"
              "   Wiki's Build Menu recipes. Do not edit by hand. */\n")
    js = header + "window.WILDS_CONSTRUCTION = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n"
    open(os.path.join(ROOT, "construction.js"), "w", encoding="utf-8").write(js.replace("—", " - "))
    print("construction items: %d (skipped %d with no materials), groups:" % (total, skipped), file=sys.stderr)
    for row in out:
        print("  %-28s %d" % (row["label"], len(row["items"])), file=sys.stderr)

if __name__ == "__main__":
    main()
