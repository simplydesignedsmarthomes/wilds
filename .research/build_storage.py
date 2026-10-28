#!/usr/bin/env python3
"""Merge all completed .research/*.json slices into storage.js.
Re-run any time a new research file lands -- safe to run repeatedly."""
import json, html, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from normalize_detail import WikiData
ROOT = os.path.dirname(HERE)

CHEST_LABELS = [
    ("weapons", "Weapons"),
    ("armour", "Armour"),
    ("jewellery", "Jewellery & Trinkets"),
    ("food", "Food & Cooking"),
    ("potions", "Potions & Consumables"),
    ("ores", "Ores & Bars"),
    ("stone", "Stone & Gems"),
    ("pottery", "Clay & Glass"),
    ("textiles", "Threads & Leathers"),
    ("bones", "Bones & Creature Drops"),
    ("wood", "Wood & Planks"),
    ("runes", "Runes & Magic Materials"),
    ("alchemy", "Oils, Waxes & Compounds"),
    ("farming", "Farming & Seeds"),
    ("tools", "Tools"),
    ("ammo", "Ammo"),
    ("vestiges", "Vestiges & Curios"),
    ("progression", "Upgrades, Keys & Currency"),
    # Fallback only: anything a future data refresh can't place lands here
    # (and the chest is hidden while it's empty).
    ("misc", "Miscellaneous"),
]

# Hand placements for items the research passes dumped in Miscellaneous (or
# filed in an odd spot), decided one by one from each item's wiki page: what
# it's made from, what it's used for, and where it drops.
CHEST_OVERRIDES = {
    # Crossbow limbs are smithed weapon parts for crossbows.
    **{m + " Crossbow Limbs": "weapons" for m in
       ["Bronze", "Iron", "Steel", "Black", "Mithril", "Adamant", "Rune", "Blurite", "Bone"]},
    # Cape patterns sit with the capes they unlock.
    **{"PATTERN: " + c + " Cape": "armour" for c in
       ["Bloodblight", "Bramblemead", "Fell", "Fractured", "Stormtouched", "Whispering"]},
    # The whole clay chain (raw, unfired, fired) plus glassware.
    **{n: "pottery" for n in [
        "Clay", "Ground Clay",
        "Clay Decoration (Unfired)", "Clay Decoration", "Clay Mould (Unfired)", "Clay Mould",
        "Clay Vessel (Unfired)", "Clay Vessel", "Clay Slab (Unfired)", "Clay Slab",
        "Molten Glass", "Glass Pane", "Glass Vessel", "Glass Decoration"]},
    # Metal leaf is hammered from bars.
    "Bronze Leaf": "ores", "Silver Leaf": "ores", "Gold Leaf": "ores",
    "Refined Obsidian": "stone",
    # Kiln and cauldron products (and their raw inputs) used as crafting agents.
    **{n: "alchemy" for n in [
        "Adhesive", "Acrid Adhesive", "Charcoal", "Swamp Tar", "Naptha", "Demonic Oil",
        "Sacred Oil", "Draconic Vis Wax", "Gypsum Wax", "Harmonised Compound", "Discordant Residue"]},
    # Monster drops.
    **{n: "bones" for n in [
        "Poison Ichor", "Kalphite Ichor", "Kalphite Shell", "Kalphite Shell Fragments",
        "Vile Ashes", "Shrapnel", "Noxious Draconic Visage", "Zombie Pack"]},
    "Wild Anima": "runes", "Cursed Essence": "runes", "Vault Core": "runes",
    "Amylase Crystal": "potions",
    "Weeds": "farming",
    "Maple Sap": "wood",
    # Weapon upgrades, Nightmare Crucible keys and merchant currencies.
    **{n: "progression" for n in [
        "Ascension Core", "Ascension Shard", "Ascension Shard (Power Level 4)",
        "Ascension Shard (Power Level 5)", "Ascension Shard (Power Level 6)",
        "Ascension Shard (Power Level 8)", "Crucible Engram of Betrayal",
        "Crucible Engram of Helplessness", "Crucible Engram of Humiliation",
        "Crucible Engram of the Hounded", "Garou Chit", "Garou Artefact",
        "Infernal Fragment", "Soul Fragment"]},
}

# Metal tier for items moved into a tiered chest, so the power-level filter
# shows them alongside the matching crossbow (same scale as the weapons).
TIER_OVERRIDES = {
    "Bronze Crossbow Limbs": (1, "Bronze"), "Iron Crossbow Limbs": (2, "Iron"),
    "Steel Crossbow Limbs": (3, "Steel"), "Mithril Crossbow Limbs": (4, "Mithril"),
    "Adamant Crossbow Limbs": (5, "Adamant"), "Black Crossbow Limbs": (6, "Black metal"),
    "Rune Crossbow Limbs": (7, "Rune"), "Bronze Leaf": (1, "Bronze"),
}

# Each crop/herb seed grows best in one specific buildable farming plot -
# straight from each plot's own wiki page ("It is the best farming plot to
# plant the following: ..."), checked 2026-10-27. A plot's name doubles as
# its region (Ash = Brynmoor, Oak = Ghornfell, Willow = Fellhollow, Yew =
# Umbral Sands - the Yew Farming Plot page even calls itself "an Umbral
# Sands plot"), but the plot is what you actually place and use, so that's
# what gets shown. Tree seeds ("Plant this directly into the ground") skip
# plots entirely and are left out on purpose - see item_plot()'s "Anywhere"
# fallback below.
SEED_PLOTS = {
    "Cabbage Seeds": "Ash Farming Plot", "Flax Seeds": "Ash Farming Plot",
    "Potato Seeds": "Ash Farming Plot", "Redberry Seeds": "Ash Farming Plot",
    "Wheat Seeds": "Ash Farming Plot", "Marentill Seeds": "Ash Farming Plot",
    "Harralander Seeds": "Ash Farming Plot",
    "Dwellberry Seeds": "Oak Farming Plot", "Tomato Seeds": "Oak Farming Plot",
    "Onion Seeds": "Oak Farming Plot", "Swamp Weed Seeds": "Oak Farming Plot",
    "Kwuarm Seeds": "Oak Farming Plot", "Snapdragon Seeds": "Oak Farming Plot",
    "Toadflax Seeds": "Oak Farming Plot",
    "Cadavaberry Seeds": "Willow Farming Plot", "Watermelon Seeds": "Willow Farming Plot",
    "Pumpkin Seeds": "Willow Farming Plot", "Corpse Cotton Seeds": "Willow Farming Plot",
    "Avantoe Seeds": "Willow Farming Plot", "Irit Seeds": "Willow Farming Plot",
    "Barrel Cactus Seeds": "Yew Farming Plot", "Bunny Cactus Seeds": "Yew Farming Plot",
    "Desert Weed Seeds": "Yew Farming Plot", "Pipe Cactus Seeds": "Yew Farming Plot",
}

# The harvested crop/herb shares its seed's plot - but only where the wiki
# names them so closely that the link is certain (its page title is the
# seed's own name, minus "Seed(s)", give or take the one actual spelling
# quirk - Marrentil the herb vs. "Marentill Seeds" the seed that grows it).
# This doubles as the seed<->harvest cross-link (see growsInto/growsFrom
# below). Left out on purpose: several seeds above (Redberry, Dwellberry,
# Cadavaberry, Corpse Cotton, both cactus seeds) have no standalone
# harvested-item page of their own to tag, and Pipe Cactus Seeds' own linked
# "grows into" page no longer exists - the "Fibrous Pipe Cactus" already in
# this chest is a different, wild-gathered item (its own page describes it
# growing near yew trees, nothing about being farmed), so it's deliberately
# not linked here.
CROP_FOR_SEED = {
    "Potato Seeds": "Potato", "Cabbage Seeds": "Cabbage", "Flax Seeds": "Flax", "Wheat Seeds": "Wheat",
    "Tomato Seeds": "Tomato", "Onion Seeds": "Onion", "Swamp Weed Seeds": "Swamp Weed",
    "Watermelon Seeds": "Watermelon", "Pumpkin Seeds": "Pumpkin",
    "Harralander Seeds": "Harralander", "Kwuarm Seeds": "Kwuarm", "Snapdragon Seeds": "Snapdragon",
    "Toadflax Seeds": "Toadflax", "Avantoe Seeds": "Avantoe", "Irit Seeds": "Irit",
    "Marentill Seeds": "Marrentil",
}
CROP_PLOTS = {crop: SEED_PLOTS[seed] for seed, crop in CROP_FOR_SEED.items()}
SEED_FOR_CROP = {crop: seed for seed, crop in CROP_FOR_SEED.items()}

TREE_SEEDS = {"Ash Tree Seed", "Oak Tree Seed", "Willow Tree Seed", "Maple Tree Seed", "Yew Tree Seed", "Magic Tree Seed"}

def item_plot(name):
    if name in SEED_PLOTS:
        return SEED_PLOTS[name]
    if name in CROP_PLOTS:
        return CROP_PLOTS[name]
    if name in TREE_SEEDS:
        return "Anywhere"
    return ""

# Build-menu structures (crafting stations, furniture) aren't inventory items;
# the app covers them as stations in the "By station" view instead.
BUILD_MENU_PIECES = {"Brewing Cauldron"}

SOURCE_FILES = [
    "weapons.json", "armour.json", "food.json", "potions.json",
    "materials.json", "tools-ammo.json", "vestiges.json", "misc-discovery.json",
    "materials-gap-fill.json", "materials-gap-fill-2.json",
    # New items discover_new_items.py filed with a confident chest guess,
    # straight from a future update - see that script for how.
    "auto-discovered.json",
]

# Full wiki detail (infobox + description), keyed by item name -- re-run this
# script any time a new detail-*.json lands, it merges in automatically.
DETAIL_FILES = [
    "detail-weapons.json", "detail-armour-1.json", "detail-armour-2.json",
    "detail-potions.json", "detail-vestiges.json", "detail-misc-discovery.json",
    "detail-food.json", "detail-materials.json", "detail-tools-ammo.json",
]

# Files whose entries carry their own detail inline (a "detail" key on each
# item) rather than in a separate detail-*.json keyed by name.
EMBEDDED_DETAIL_FILES = ["materials-gap-fill.json", "materials-gap-fill-2.json"]

# Known non-item overview/index pages picked up by research agents -- drop them.
DROP_NAMES = {"Vestige", "Vestiges", "Pickaxes", "Logging Axes", "Spade", "Watering Can",
              "Fishing rod", "Consumable Recipes"}

# Cut from the live game but still sitting in our research files from when
# they were scraped - the wiki itself confirms this with its own
# Category:Discontinued content (checked 2026-10-27, 31 pages; the rest of
# that category - disambiguation pages, perk tiers, a now-merged Ascension
# Shard page - were never scraped into this app in the first place, so there
# was nothing to drop for them). Re-check that category occasionally; it's
# the wiki's own call on what's gone, not a guess made here.
DISCONTINUED_NAMES = {
    "An Ember-Edged Remnant of Cloth", "Berry Compote", "Dwellberry Crunchies (Removed)",
    "Dwellberry Glazed Roast Flank", "Dwellberry Glazed Roast Meat", "Fortifying Crunchies",
    "Fortifying Soup", "Fortifying Stew", "Healing Potion", "Hearty Crunchies",
    "Hearty Fortifying Soup", "Hearty Soup", "Hearty Stew", "Large Wardstone",
    "Lesser Healing Potion", "Medium Wardstone", "Mixed Platter", "Redberry Glazed Roast Flank",
    "Small Wardstone", "Weak Healing Potion",
}
DROP_NAMES |= DISCONTINUED_NAMES

def clean_name(n):
    return html.unescape(n or "").strip()

def load_details():
    details = {}
    for fname in DETAIL_FILES:
        path = os.path.join(HERE, fname)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for it in data:
            name = clean_name(it.get("name"))
            if not name:
                continue
            infobox = [{"label": clean_name(r.get("label")), "value": clean_name(r.get("value"))}
                       for r in (it.get("infobox") or []) if clean_name(r.get("label"))]
            description = clean_name(it.get("description"))
            if infobox or description:
                details[name] = {"infobox": infobox, "description": description}
    for fname in EMBEDDED_DETAIL_FILES:
        path = os.path.join(HERE, fname)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for it in data:
            name = clean_name(it.get("name"))
            d = it.get("detail")
            if not name or not d:
                continue
            infobox = [{"label": clean_name(r.get("label")), "value": clean_name(r.get("value"))}
                       for r in (d.get("infobox") or []) if clean_name(r.get("label"))]
            description = clean_name(d.get("description"))
            if infobox or description:
                details[name] = {"infobox": infobox, "description": description}
    return details

def load_all(details):
    by_name = {}
    for fname in SOURCE_FILES:
        path = os.path.join(HERE, fname)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for it in data:
            name = clean_name(it.get("name"))
            if not name or name in DROP_NAMES or name in BUILD_MENU_PIECES:
                continue
            chest = it.get("chest") or "misc"
            by_name.setdefault(name, []).append({
                "name": name,
                "img": it.get("img") or "",
                # A bare number (one research pass tagged 8 foods "16", "36"...)
                # isn't a tier name; tierRank still carries it for sorting.
                "tier": "" if re.fullmatch(r"[\d.]+", str(it.get("tier") or "")) else (clean_name(it.get("tier")) if it.get("tier") else ""),
                "tierRank": it.get("tierRank"),
                "chest": chest,
                "note": clean_name(it.get("note")) if it.get("note") else "",
            })

    wiki = WikiData()
    items = []
    for name, candidates in by_name.items():
        rec = candidates[0]
        if len(candidates) > 1:
            chests_seen = set(c["chest"] for c in candidates)
            if len(chests_seen) > 1:
                winner = resolve_chest_conflict(chests_seen)
                rec = next((c for c in candidates if c["chest"] == winner), candidates[0])
            # same chest reported twice (e.g. an overlapping wiki subcategory) -- first one wins, harmless
        rec["chest"] = CHEST_OVERRIDES.get(name, rec["chest"])
        if name in TIER_OVERRIDES:
            rec["tierRank"], rec["tier"] = TIER_OVERRIDES[name]
        old = details.get(name) or {}
        rec["img"] = wiki.item_image(name) or rec["img"]
        rec["detail"] = wiki.detail(name, fallback_description=old.get("description", ""))
        stations = item_stations(rec["detail"])
        if stations:
            rec["stations"] = stations
        plot = item_plot(name)
        if plot:
            rec["plot"] = plot
        if name in CROP_FOR_SEED:
            rec["growsInto"] = CROP_FOR_SEED[name]
        if name in SEED_FOR_CROP:
            rec["growsFrom"] = SEED_FOR_CROP[name]
        items.append(rec)
    return items

# Where an item is MADE comes straight from its own recipes. Raw materials
# with no recipe of their own get tagged with the stations that consume them
# instead ("take this to the Tannery"), but only when that's a short, useful
# list - a hub material like Gold Bar feeds 30 recipes across a dozen
# stations, and tagging it with all of them would just bury those stations'
# real products.
MAX_DOWNSTREAM_STATIONS = 3

# "Build Menu" is the game's own Construction menu, not a crafting station -
# any raw material used in even one building recipe (an ore, a seed) would
# otherwise pick up "Build Menu" as if it were a peer of the Grill or the
# Blacksmith's Bench, complete with a blank icon since it isn't a real,
# buildable thing itself. Construction already has its own dedicated tab
# (see fetch_construction_data.py), so it's excluded from station tagging
# entirely rather than showing up a second time, out of place, here.
# (Cooking Pot - also discontinued, see DISCONTINUED_NAMES above - doesn't
# need an entry here: normalize_detail.py's WikiData.detail() already strips
# it out of every recipe/usedIn list before this function ever sees it.)
NOT_A_STATION = {"Build Menu"}

def item_stations(detail):
    made = []
    for r in detail["recipes"]:
        st = r["station"]
        if st and st not in NOT_A_STATION and st not in made:
            made.append(st)
    if made:
        return made
    counts, order = {}, []
    for u in detail["usedIn"]:
        st = u["station"]
        if not st or st in NOT_A_STATION:
            continue
        if st not in counts:
            counts[st] = 0
            order.append(st)
        counts[st] += 1
    if not counts:
        return []
    # A raw material used overwhelmingly at one station (most of its real
    # recipes) but only incidentally in a one-off recipe or two elsewhere -
    # a potion herb that also flavors a single cooked dish - belongs with
    # its dominant station alone. Listing every station it ever touches
    # would scatter it across tiles that aren't really "its" station and
    # bury the one that actually defines it.
    top = max(counts, key=lambda s: counts[s])
    rest = sum(c for s, c in counts.items() if s != top)
    if counts[top] >= 3 and counts[top] >= 3 * rest:
        return [top]
    return order if len(order) <= MAX_DOWNSTREAM_STATIONS else []

# A few item types got caught by two different research agents under two
# different chest labels (e.g. an arrow is both "a weapon" and "ammo" by the
# wiki's own category tree). Pick the one chest it actually belongs in, so
# nothing is stored twice.
CHEST_CONFLICT_RULES = {
    frozenset(["ammo", "weapons"]): "ammo",
    frozenset(["armour", "tools"]): "tools",
    frozenset(["armour", "vestiges"]): "vestiges",
    frozenset(["farming", "food"]): "food",
    frozenset(["food", "potions"]): "food",
    frozenset(["farming", "potions"]): "farming",
    frozenset(["potions", "tools"]): "tools",
    frozenset(["potions", "vestiges"]): "vestiges",
    frozenset(["farming", "textiles"]): "textiles",
    frozenset(["misc", "wood"]): "wood",
    frozenset(["misc", "vestiges"]): "vestiges",
}

def resolve_chest_conflict(chests_seen):
    rule = CHEST_CONFLICT_RULES.get(frozenset(chests_seen))
    return rule if rule else sorted(chests_seen)[0]

def sort_key(it):
    tr = it["tierRank"]
    return (0, tr) if isinstance(tr, (int, float)) else (1, it["name"].lower())

def assign_steps(chest_items):
    # Sequential 0,1,2... step per DISTINCT tierRank value actually present in
    # this chest, so "power level" filtering works the same way regardless of
    # whether the chest's native scale is 0-7 (metal) or 1-50 (runes). Items
    # with no tier are usually rare/unique/boss-drop gear (the wiki simply has
    # no material-tier label for them) rather than early-game basics, so in a
    # chest that DOES have a tier chain they're pinned to the top step and
    # only appear once the filter is all the way up. In a chest with no tier
    # chain at all (food, vestiges, ...) there's nothing to gate, so they get
    # step 0 and are always visible.
    distinct = sorted(set(it["tierRank"] for it in chest_items if isinstance(it["tierRank"], (int, float))))
    step_of = {v: i for i, v in enumerate(distinct)}
    untiered_step = len(distinct) - 1 if distinct else 0
    for it in chest_items:
        tr = it["tierRank"]
        it["step"] = step_of[tr] if isinstance(tr, (int, float)) else untiered_step
    return len(distinct)

def main():
    details = load_details()
    items = load_all(details)
    with_detail = sum(1 for it in items if "detail" in it)
    by_chest = {}
    for it in items:
        by_chest.setdefault(it["chest"], []).append(it)
    for chest in by_chest:
        by_chest[chest].sort(key=sort_key)

    out = []
    total = 0
    max_step = 0
    for key, label in CHEST_LABELS:
        chest_items = by_chest.pop(key, [])
        total += len(chest_items)
        max_step = max(max_step, assign_steps(chest_items))
        out.append({"key": key, "label": label, "items": chest_items})
    # anything with an unrecognized chest key -> dump into misc so nothing is silently lost
    leftover = []
    for key, chest_items in by_chest.items():
        leftover.extend(chest_items)
    if leftover:
        for row in out:
            if row["key"] == "misc":
                row["items"].extend(leftover)
                row["items"].sort(key=sort_key)
                total += len(leftover)
                max_step = max(max_step, assign_steps(row["items"]))
    out = [row for row in out if row["items"] or row["key"] != "misc"]

    # A small personal touch: each chest tile shows one representative
    # item's icon, picked by hand where there's an obvious one, falling
    # back to the first item that actually has an icon otherwise.
    CHEST_ICON_ITEM = {
        "weapons": "Bronze Sword", "armour": "Bronze Platebody", "jewellery": "Amulet of Strength",
        "food": "Cheeky Fryup", "potions": "Weak Healing Potion", "ores": "Iron Ore",
        "stone": "Stone", "pottery": "Clay Vessel", "textiles": "Leather", "bones": "Animal Bone",
        "wood": "Oak Logs", "runes": "Air Rune", "alchemy": "Adhesive", "farming": "Cabbage Seeds",
        "tools": "Bronze Pickaxe", "ammo": "Bronze Arrow", "progression": "Vault Core",
    }
    for row in out:
        wanted = CHEST_ICON_ITEM.get(row["key"])
        by_name = {it["name"]: it for it in row["items"]}
        pick = by_name.get(wanted) or next((it for it in row["items"] if it.get("img")), None)
        row["img"] = pick["img"] if pick else ""

    # A station and its "Advanced" upgrade make the same family of goods at
    # a higher tier, so they browse as one combined entry rather than two
    # near-empty boxes. Item-level station tags stay specific (an item still
    # says "Made at: Advanced Tannery"), only the browsing list merges them.
    STATION_GROUPS = [
        ("Tannery", ["Tannery", "Advanced Tannery"]),
        ("Spinning Wheel", ["Spinning Wheel", "Advanced Spinning Wheel"]),
    ]
    member_to_group = {}
    for group_name, members in STATION_GROUPS:
        for m in members:
            member_to_group[m] = group_name

    station_counts = {}
    station_members = {}
    for row in out:
        for it in row["items"]:
            for s in it.get("stations", []):
                display = member_to_group.get(s, s)
                station_counts[display] = station_counts.get(display, 0) + 1
                station_members.setdefault(display, set()).add(s)
    # A station is itself something you build, so its icon comes from its
    # own Build Menu recipe (the same way Construction resolves icons)
    # rather than a regular item infobox, which stations don't have.
    station_wiki = WikiData()
    def station_icon(name):
        recs = station_wiki.lookup(station_wiki.recipes_by_output, name)
        if recs and recs[0]["output"]["img"]:
            return recs[0]["output"]["img"]
        return station_wiki.item_image(name) or ""
    stations_out = [{"name": k, "count": v, "members": sorted(station_members[k]),
                      "img": station_icon(sorted(station_members[k])[0])}
                     for k, v in sorted(station_counts.items(), key=lambda kv: (-kv[1], kv[0]))]

    # Research data (wiki descriptions, infobox labels) comes from many source
    # files and regenerates on every build, so em dashes sneak back in even
    # after a one-time sweep of the hand-written app files. Strip them here,
    # at the single point everything funnels through, so this never regresses.
    def strip_em_dashes(obj):
        if isinstance(obj, str):
            return re.sub(r"\s*—\s*", " - ", obj)
        if isinstance(obj, list):
            return [strip_em_dashes(v) for v in obj]
        if isinstance(obj, dict):
            return {k: strip_em_dashes(v) for k, v in obj.items()}
        return obj
    out = strip_em_dashes(out)
    stations_out = strip_em_dashes(stations_out)

    js = "window.WILDS_STORAGE = " + json.dumps(out, indent=2, ensure_ascii=False) + ";\n"
    js += "window.WILDS_STORAGE_MAX_STEP = " + str(max_step) + ";\n"
    js += "window.WILDS_STATIONS = " + json.dumps(stations_out, indent=2, ensure_ascii=False) + ";\n"
    with open(os.path.join(ROOT, "storage.js"), "w", encoding="utf-8") as f:
        f.write(js)

    print("Total items:", total, "  (with full detail:", with_detail, ")")
    for row in out:
        print(f"  {row['label']:<28} {len(row['items'])}")
    print("Stations:", len(stations_out))
    for s in stations_out:
        print(f"  {s['name']:<22} {s['count']}")

if __name__ == "__main__":
    main()
