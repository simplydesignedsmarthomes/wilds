"""Pull the wiki's interactive-map marker data into map-data.js.

The wiki's map (MediaWiki:Gadget-maps.js + Module:Map) is Leaflet over
https://maps.runescape.wiki/dw/tiles, with markers stored one category per
page at Module:Map/<Category>.json as [{x, y, name, description?, icon?}].
This fetches every category, groups them for the app's filter panel, and
also pulls each quest page's own {{Map|...}} template (which categories it
shows, plus its center/zoom) so quest guides can embed the same map.

Writes map-data.js (window.WILDS_MAP, loaded on demand) and quest-maps.js
(window.WILDS_QUEST_MAPS, loaded up front). Re-run to refresh.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from normalize_detail import clean, templates

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

def list_category_pages():
    titles, cont = [], {}
    while True:
        d = get(dict({"action": "query", "list": "allpages", "apnamespace": "828", "apprefix": "Map/",
                      "aplimit": "500", "format": "json"}, **cont))
        titles += [p["title"] for p in d["query"]["allpages"]]
        if "continue" not in d:
            return titles
        cont = d["continue"]

def fetch_contents(titles):
    out = {}
    for i in range(0, len(titles), 50):
        d = get({"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
                 "format": "json", "formatversion": "2", "titles": "|".join(titles[i:i + 50])})
        for p in d["query"]["pages"]:
            if "revisions" in p:
                out[p["title"]] = p["revisions"][0]["slots"]["main"]["content"]
        time.sleep(0.4)
    return out

# Scratch pages, docs and test data, not real map content.
SKIP = re.compile(r"(sandbox|^test$|^doc$|test\.json$|^HealingPotionTest$|^chests$|^abyssalwhipstatue$|^zogre$)", re.I)

def fetch_wiki_categories(names):
    """The wiki's own (non-hidden) page categories for each marker category's page."""
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

# Wiki page category -> app group, checked in this order (first hit wins).
WIKI_CATEGORY_GROUPS = [
    ({"Lore Scraps", "Journal"}, "Lore & books"),
    ({"Bosses"}, "Bosses"),
    ({"Monsters"}, "Creatures"),
    ({"Non-player characters"}, "Merchants & NPCs"),
    ({"Dragonkin Vaults"}, "Dragonkin vaults"),
    ({"Salvage Hotspots"}, "Salvage"),
    ({"Agility", "Agility Course", "Activities"}, "Agility & activities"),
    ({"Mining nodes", "Mining"}, "Ores & rocks"),
    ({"Woodcutting"}, "Trees"),
    ({"Quest Items", "Vestiges"}, "Quest items & vestiges"),
]

# Hand placements where the wiki's own category tagging points the wrong way
# for a map filter (e.g. Buried Treasure is tagged "Activities").
GROUP_OVERRIDES = {
    "Buried Treasure": "Treasure", "X Marks the Spot": "Treasure", "Scarecrow Scavenging": "Treasure",
    "Fight Cave": "Landmarks & fast travel", "Lava Fields": "Landmarks & fast travel",
    "Statues of Saradomin": "Landmarks & fast travel", "Bramblemead Locations": "Landmarks & fast travel",
    "Exploding Plant Trap": "Creatures", "Kalphite Queen Egg": "Creatures", "Magical Raven": "Creatures",
    "Razlem the Deranged": "Creatures", "Skeletal Marauder (Dowdun Reach)": "Creatures",
    "Skeletal Warrior (Dowdun Reach)": "Creatures", "Mark Day": "Merchants & NPCs",
}

def group_for(cat, quest_names, merchants, wiki_cats):
    c = cat.lower()
    if cat in quest_names:
        return "Quests"
    if cat in GROUP_OVERRIDES:
        return GROUP_OVERRIDES[cat]
    # Things only visible while soul-rifted.
    if c.startswith("spectral "):
        return "Soul rift"
    if c.startswith("recipe:"):
        return "Lore & books"
    if cat in merchants or re.search(r" - the (merchant|hunter)$", c):
        return "Merchants & NPCs"
    wc = wiki_cats.get(cat) or set()
    for keys, group in WIKI_CATEGORY_GROUPS:
        if wc & keys:
            return group
    rules = [
        ("Anima vents", r"anima vent|rune essence geyser"),
        ("Ores & rocks", r"ore node|deposit|rock$|node$|^clay node|limestone|sandstone|gypsum"),
        ("Trees", r"\btree$|root$"),
        ("Plants & crops", r"bush|cactus|plant$|weed|vine$|mushroom|flax|cabbage|onion|potato|pumpkin|snapdragon|harralander|marrentil|toadflax|irit|cotton|swamp tar|bloodwood sap|anima-infused bark"),
        ("Fishing", r"fishing spot"),
        ("Salvage", r"salvage"),
        ("Treasure", r"treasure|chest|reliquary|jewellery box|x marks the spot|sanguine urn|scarecrow scavenging|threadbare grain sack|emblem$|cape$"),
        ("Dragonkin vaults", r" kara$|^vaults$|nightmare crucible|velgar|keep of blue flames|bloodblight castle|highlands castle"),
        ("Creatures", r"burrow|kothaar"),
        ("Lore & books", r"journal|diary|tome|note|book|scroll|page|parchment|ledger|letter|scrawl|scribble|memoirs|gospel|saga|tale|recipe|text|log$|primer|report|storybook|writings|binding|importance|pride of|wrath of|plan \(|lore scraps|malificarum|riddle|doodle"),
        ("Landmarks & fast travel", r"lodestone|nodestone|shrine|guild|statue|temple|windmill|watch$|ruins|well$|postbox|orb stand|door$|lava fields|fight cave|transport network|makeshift table|torn tapestry|outlook"),
        ("Agility & activities", r"agility|course|dash|climb|run$|assault|difficulties"),
    ]
    for name, rx in rules:
        if re.search(rx, c):
            return name
    if wc & {"Items", "Basic Items", "Resources", "Raw Ingredients", "Basic Materials"}:
        return "Quest items & vestiges"
    return "Other"

def main():
    titles = [t for t in list_category_pages() if t.endswith(".json")]
    contents = fetch_contents(titles)

    qsrc = open(os.path.join(ROOT, "quests.js"), encoding="utf-8").read()
    primary = re.search(r"WILDS_QUESTS_PRIMARY\s*=\s*\[(.*?)\];", qsrc, re.S).group(1)
    secondary = re.search(r"WILDS_QUESTS_SECONDARY\s*=\s*\{(.*?)\};", qsrc, re.S).group(1)
    quest_names = set(re.findall(r'\[\s*"([^"]+)"\s*,', primary))
    for arr in re.findall(r":\s*\[(.*?)\]", secondary, re.S):
        quest_names.update(re.findall(r'"([^"]+)"', arr))

    merchants = {"Beartach - The Merchant", "Domri - The Merchant", "Iasadair - The Merchant",
                 "Hedric - The Hunter", "Death", "Edna", "Postie Pete", "Doric", "Vannaka", "Zanik", "Wise Old Man"}

    names = [t[len("Module:Map/"):-len(".json")] for t in contents]
    wiki_cats = fetch_wiki_categories([n for n in names if not SKIP.search(n)])

    categories, total = [], 0
    for t in sorted(contents):
        name = t[len("Module:Map/"):-len(".json")]
        if SKIP.search(name):
            continue
        try:
            data = json.loads(contents[t])
        except ValueError:
            print("  skipped unparseable:", name, file=sys.stderr)
            continue
        pts = []
        for s in data if isinstance(data, list) else []:
            try:
                x, y = float(s["x"]), float(s["y"])
            except (KeyError, TypeError, ValueError):
                continue
            p = [round(x, 1), round(y, 1)]
            label = clean(s.get("name") or "")
            desc = clean(s.get("description") or "")
            if label and label != name:
                p.append(label)
            if desc:
                if len(p) == 2:
                    p.append("")
                p.append(desc)
            pts.append(p)
        if not pts:
            continue
        total += len(pts)
        categories.append({"id": name, "group": group_for(name, quest_names, merchants, wiki_cats), "points": pts})

    # Each quest page's own {{Map|Cat1,Cat2|center=y,x|zoom=n}} templates.
    qpages = fetch_contents(sorted(quest_names))
    known = {c["id"] for c in categories}
    quest_maps = {}
    for qname, wt in qpages.items():
        maps = []
        for _, p, _, _ in templates(wt, r"Map"):
            cats = [c.strip() for c in (p.get("1") or "").split(",") if c.strip() and c.strip() in known]
            if not cats:
                continue
            entry = {"categories": cats}
            if p.get("center"):
                try:
                    a, b = [float(v) for v in re.split(r"\s*,\s*", p["center"])[:2]]
                    entry["center"] = [a, b]
                except ValueError:
                    pass
            if p.get("zoom"):
                try:
                    entry["zoom"] = float(p["zoom"])
                except ValueError:
                    pass
            maps.append(entry)
        if maps:
            quest_maps[qname] = maps

    groups = {}
    for c in categories:
        groups[c["group"]] = groups.get(c["group"], 0) + 1
    header = ("/* Generated by .research/fetch_map_data.py from the RuneScape: Dragonwilds Wiki's\n"
              "   interactive map data (Module:Map/*.json). Do not edit by hand. */\n")
    # The 15k markers load only when a map is opened; the quest list is tiny
    # and loads up front so quest guides know straight away which have a map.
    big = {"tiles": "https://maps.runescape.wiki/dw/tiles/{z}/{x}_{y}.png", "categories": categories}
    for fname, var, payload in [("map-data.js", "WILDS_MAP", big), ("quest-maps.js", "WILDS_QUEST_MAPS", quest_maps)]:
        js = header + "window." + var + " = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n"
        open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(js.replace("—", " - "))
    print("categories: %d, markers: %d, quest maps: %d" % (len(categories), total, len(quest_maps)), file=sys.stderr)
    for g, n in sorted(groups.items(), key=lambda kv: -kv[1]):
        print("  %-26s %d" % (g, n), file=sys.stderr)

if __name__ == "__main__":
    main()
