"""Shelf ordering: which band an item belongs in, and where it sits inside it.

Two separate jobs, deliberately kept apart:

  BAND  - a structural grouping inside a chest ("Raw ingredients", "Cooked",
          "Meals", "Burnt"). Bands never reorder on their own; they are the
          shelves. A band can be marked collapsed, meaning the app hides its
          contents behind a tap - that is how the 35 burnt foods stop being
          35 rows you scroll past.

  RANK  - position WITHIN a band, in the order you actually meet things
          playing the game. The app can sort a band by this or by name, so
          rank has to be a number on every item, even a guessed one.

The progression signal, best first:

  1. Cooking power level. The wiki's Cooking page carries an Ingredients
     table giving every cookable ingredient a power level 1-5 and naming the
     product it cooks into. This is the game's own scale, not an opinion, and
     it is what makes raw rat meat (1) sort before raw monkfish (4).
  2. tierRank, already on the item - metal tier for weapons/armour/ores,
     tree tier for wood, and so on. Bronze before rune.
  3. Region. Ashenfall's five regions are strictly ordered by the wiki's own
     geography section, and sub-regions inherit their parent's number. An
     item first found in Brynmoor outranks one from Umbral Sands.
  4. Nothing - sorts last, alphabetically among its peers.
"""

import json
import re

# Ashenfall's regions in the order you reach them, from the Ashenfall page's
# own "Regions" list, with each region's sub-territories folded in at the
# parent's rank. Sub-regions are listed because item sources name them far
# more often than they name the parent ("Chickens in Bramblemead Valley").
REGION_RANK = {
    "Brynmoor": 1, "Temple Woods": 1, "Bramblemead Valley": 1, "Whispering Swamp": 1,
    "Ghornfell": 2, "Fractured Plains": 2, "Bloodblight Swamp": 2, "Stormtouched Highlands": 2,
    "Fellhollow": 3, "Bleakfields Valley": 3, "Forgotten Temple": 3, "Dragon's Run": 3,
    "Emberwood": 3, "Witchwillow Range": 3, "Hope's Fall": 3, "Lake of Lost Souls": 3,
    "Silverthorn Keep": 3, "Coalridge Pass": 3,
    "Dowdun Reach": 4, "The Approach": 4, "The Courtyard": 4,
    "Umbral Sands": 5,
}
# Longest first, so "Whispering Swamp" is matched before a bare "Swamp" could
# ever be, and sub-regions win over their parent.
_REGION_PATTERNS = sorted(REGION_RANK, key=len, reverse=True)

# Every cookable ingredient's power level, straight off the Cooking page's
# Ingredients table (checked 2026-10-28). The table is the game's own scale:
# an ingredient's power level is what sets the Cooking level needed to cook it
# without burning it, which is why it doubles as a progression order.
# Eight of these (Cabbage, Potato, Tomato, Onion, Pumpkin, Watermelon,
# Cactus Steak, Maple Sap) live in other chests - they stay here anyway so a
# meal built from them can still inherit a level.
COOK_POWER = {
    "Dirty Water": 1, "Egg": 1, "Raw Bird Meat": 1, "Raw Rat Meat": 1, "Redberries": 1,
    "Bag of Flour": 2, "Bittercap Mushroom": 2, "Cabbage": 2, "Potato": 2, "Raw Farm Meat": 2,
    "Raw Game Meat": 2, "Raw Sardine": 2, "Raw Shrimp": 2, "Raw Trout": 2, "Tomato": 2,
    "Dwellberries": 3, "Onion": 3, "Peach": 3, "Raw Anchovies": 3, "Raw Bestial Meat": 3,
    "Raw Herring": 3, "Raw Salmon": 3, "Cadavaberries": 4, "Maple Sap": 4, "Pumpkin": 4,
    "Raw Armoured Catfish": 4, "Raw Beltfish": 4, "Raw Desert Sole": 4, "Raw Giant Krill": 4,
    "Raw Infernal Eel": 4, "Raw Lobster": 4, "Raw Monkfish": 4, "Raw Undead Bass": 4,
    "Raw Undead Eel": 4, "Undead Meat": 4, "Watermelon": 4, "Cactus Steak": 5,
}

# Cooked product -> the single ingredient it is made from, same table. This is
# what separates a one-ingredient "Cooked" item from a multi-ingredient "Meal".
COOK_PRODUCT = {
    "Clean Water": "Dirty Water", "Fried Egg": "Egg", "Fillet": "Raw Bird Meat",
    "Rat Roast": "Raw Rat Meat", "Dried Redberries": "Redberries", "Bread": "Bag of Flour",
    "Grilled Mushrooms": "Bittercap Mushroom", "Fried Cabbage": "Cabbage",
    "Baked Potato": "Potato", "Steak": "Raw Farm Meat", "Haunch": "Raw Game Meat",
    "Fried Sardine": "Raw Sardine", "Sauteed Shrimp": "Raw Shrimp",
    "Grilled Trout": "Raw Trout", "Grilled Tomatoes": "Tomato",
    "Dried Dwellberries": "Dwellberries", "Fried Onions": "Onion", "Dried Peach": "Peach",
    "Seared Anchovies": "Raw Anchovies", "Flank Steak": "Raw Bestial Meat",
    "Smoked Herring": "Raw Herring", "Fried Salmon": "Raw Salmon",
    "Dried Cadavaberries": "Cadavaberries", "Maple Syrup": "Maple Sap",
    "Roast Pumpkin": "Pumpkin", "Braised Catfish": "Raw Armoured Catfish",
    "Steamed Beltfish": "Raw Beltfish", "Sun Baked Sole": "Raw Desert Sole",
    "Dried Giant Krill": "Raw Giant Krill", "Smoked Infernal Eel": "Raw Infernal Eel",
    "Roasted Lobster": "Raw Lobster", "Monkfish Fillets": "Raw Monkfish",
    "Grilled Undead Bass": "Raw Undead Bass", "Braised Undead Eel": "Raw Undead Eel",
    "Cauterised Undead Steak": "Undead Meat", "Watermelon Jerky": "Watermelon",
    "Seared Cactus Steak": "Cactus Steak",
}

# Tea is the one cooking chain with no power level of its own - the wiki says
# so outright ("Tea leaves do not have a listed Power Level and are instead
# dried in a kiln and then ground in a grindstone"). Placed by hand so the
# three of them stay a chain instead of falling to the bottom as unknowns.
TEA_CHAIN = {"Tea Leaves": (0, 3), "Dried Tea Leaves": (1, 3), "Ground Tea Leaves": (1, 3)}

# Gem order, cheapest to best, as the Jeweler's Bench recipes climb them.
GEM_RANK = {
    "Opal": 1, "Jade": 2, "Sapphire": 3, "Emerald": 4,
    "Red Topaz": 5, "Ruby": 6, "Diamond": 7, "Dragonstone": 8,
}

# Band layouts per chest: (label, collapsed). A chest absent from here is a
# single unbanded shelf - still progression-sorted, just with no subheadings,
# because splitting e.g. Weapons into stages would be noise.
BAND_LAYOUT = {
    "food":     [("Raw ingredients", False), ("Cooked", False), ("Meals", False), ("Burnt", True)],
    "farming":  [("Seeds", False), ("Crops & herbs", False), ("Supplies", False)],
    "pottery":  [("Raw clay", False), ("Unfired", False), ("Finished", False)],
    "ores":     [("Ore", False), ("Bars", False)],
    "wood":     [("Logs", False), ("Planks & parts", False)],
    "stone":    [("Raw stone", False), ("Processed", False), ("Gems", False)],
    "textiles": [("Raw fibres", False), ("Thread & cloth", False), ("Leather & hide", False)],
}


def _stat(it, label):
    for s in ((it.get("detail") or {}).get("stats") or []):
        if s.get("label") == label:
            return s.get("value") or ""
    return ""


def region_rank(it):
    """Earliest Ashenfall region this item is tied to, or None.

    Earliest, not first-mentioned: an item found in both Brynmoor and Umbral
    Sands is something you meet in Brynmoor, so it sorts there.
    """
    blob = " ".join([
        json.dumps((it.get("detail") or {}).get("sources") or []),
        it.get("note") or "",
        (it.get("detail") or {}).get("description") or "",
    ])
    best = None
    for name in _REGION_PATTERNS:
        if name in blob:
            r = REGION_RANK[name]
            best = r if best is None else min(best, r)
    return best


def _recipe_materials(it):
    rs = (it.get("detail") or {}).get("recipes") or []
    if not rs:
        return []
    return [m.get("name") for m in (rs[0].get("materials") or []) if m.get("name")]


def cooking_power(name, by_name, _depth=0, _seen=None):
    """Highest cooking power level anywhere in this item's ingredient tree.

    A meal is gated by its most advanced ingredient, so monkfish skewers
    (monkfish, power 4 + cactus steak, power 5) land at 5 and sort after a
    shrimp omelette, which is exactly the order you can first make them in.
    """
    _seen = _seen or set()
    if name in COOK_POWER:
        return COOK_POWER[name]
    if _depth > 4 or name in _seen:
        return 0
    _seen = _seen | {name}
    if name in COOK_PRODUCT:
        return COOK_POWER.get(COOK_PRODUCT[name], 0)
    it = by_name.get(name)
    if not it:
        return 0
    best = 0
    for m in _recipe_materials(it):
        best = max(best, cooking_power(m, by_name, _depth + 1, _seen))
    return best


def _food_band(name, it, by_name):
    if name.startswith("Burnt "):
        return 3
    if name in TEA_CHAIN:
        return TEA_CHAIN[name][0]
    if name in COOK_PRODUCT:
        return 1
    if (_stat(it, "Type") == "Raw Ingredient" or name in COOK_POWER
            or name.startswith("Raw ") or name.startswith("Pristine ")
            or name == "Unusual Trout"):
        return 0
    return 2


def _chain_band(name, it, chest):
    """Processing-stage band for the chests that have an obvious chain."""
    if chest == "farming":
        if "Seed" in name:
            return 0
        if name in ("Weeds", "Ultra Compost", "Large Compost Bucket",
                    "Shocking Plant Bulb", "Cactus Water"):
            return 2
        return 1
    if chest == "pottery":
        if "(Unfired)" in name:
            return 1
        if name in ("Clay", "Ground Clay"):
            return 0
        return 2
    if chest == "ores":
        return 1 if name.endswith("Bar") else 0
    if chest == "wood":
        return 1 if ("Plank" in name or "Log" not in name) else 0
    if chest == "stone":
        if name in GEM_RANK or name.endswith("Emblem"):
            return 2
        if name.startswith("Ground ") or name.startswith("Refined ") or "Block" in name:
            return 1
        return 0
    if chest == "textiles":
        if "Leather" in name or "Hide" in name:
            return 2
        if "Thread" in name or "Cloth" in name or "Rope" in name:
            return 1
        return 0
    return 0


def band_for(name, it, chest, by_name):
    if chest not in BAND_LAYOUT:
        return 0
    if chest == "food":
        return _food_band(name, it, by_name)
    return _chain_band(name, it, chest)


def rank_for(name, it, chest, by_name):
    """A number for 'how far into the game before you meet this'. Lower first.

    Unknowns return a deliberately large number rather than 0, so an item we
    could not place sinks to the bottom of its band instead of masquerading
    as a starter item.
    """
    UNKNOWN = 99
    if chest == "food":
        if name in TEA_CHAIN:
            return TEA_CHAIN[name][1]
        p = cooking_power(name, by_name)
        if p:
            return p
        # Pristine/Unusual fish mirror their plain counterpart's level.
        m = re.match(r"^(?:Pristine|Unusual) (.+)$", name)
        if m:
            for cand in ("Raw " + m.group(1), m.group(1)):
                if cand in COOK_POWER:
                    return COOK_POWER[cand]
        # Last resort for food whose only recipe was at a dropped station
        # (Redberry Crunchies lost its Cooking Pot recipe and so has no
        # ingredient tree left): borrow the level of any ingredient whose
        # name it still carries. "Redberries" has to match "Redberry", hence
        # the -ies/-y stem alongside the plain singular.
        for ing, lvl in COOK_POWER.items():
            base = ing.replace("Raw ", "")
            stems = {base, base.rstrip("s")}
            if base.endswith("ies"):
                stems.add(base[:-3] + "y")
            if any(s and s in name for s in stems):
                return lvl
    if chest == "stone" and name in GEM_RANK:
        return GEM_RANK[name]
    tr = it.get("tierRank")
    if isinstance(tr, (int, float)):
        return tr
    r = region_rank(it)
    if r is not None:
        return r
    return UNKNOWN


def apply(chests, by_name):
    """Stamp band/rank onto every item and sort each chest into shelf order."""
    for chest in chests:
        key = chest["key"]
        layout = BAND_LAYOUT.get(key)
        for it in chest["items"]:
            name = it["name"]
            b = band_for(name, it, key, by_name)
            it["band"] = b
            it["rank"] = rank_for(name, it, key, by_name)
            if layout:
                it["bandLabel"] = layout[b][0]
        chest["items"].sort(key=lambda i: (i["band"], i["rank"], i["name"].lower()))
        if layout:
            # Only advertise bands that actually have something in them.
            used = sorted({i["band"] for i in chest["items"]})
            chest["bands"] = [{"band": b, "label": layout[b][0],
                               "collapsed": layout[b][1]} for b in used]
    return chests
