"""What goes in each compost bin, and what each compost tier does.

Composting is the one Farming chain the app could not answer in either
direction: the catalogue had Ultra Compost with an empty recipe list, no
Compost or Super Compost at all, and nothing on a burnt fillet to say it was
worth keeping. This module stamps the link both ways - every compostable item
learns which tier(s) it feeds, and each compost item learns everything that
makes it.

Sources, all checked 2026-10-29:
  - [[Compost Bin]], [[Super Compost Bin]], [[Ultra Compost Bin]] - the build
    recipe, the Farming level that unlocks it, and the "Compostable items"
    section on each page.
  - [[Compost]], [[Super Compost]], [[Ultra Compost]] - the effect each tier
    has when applied to a plot (Farming XP, disease chance, yield multiplier).
  - Individual item pages, for the confirmations and exclusions below.

The regular Compost Bin is the awkward one. Its page lists category rules
("Any burnt food", "Any plants", "Any raw food") rather than item names, and
those rules cannot simply be expanded: the Pumpkin and Watermelon pages both
say outright that they can NOT go in a compost bin, only a super compost bin,
which rules out reading "any plants" as "every plant item". So the categories
that map onto a set the wiki itself enumerates are expanded here, and the two
that do not are carried through as rules for the card to print verbatim. An
unexpanded rule shows up as prose on the Compost card and tags no individual
item - better a rule the player applies themselves than fifty badges that are
wrong about half the game's raw food.
"""

# tier key -> everything about that tier. Order matters: cards and badges are
# rendered in this order, which is also the order you unlock them.
TIERS = [
    ("compost", {
        "item": "Compost",
        "bin": "Compost Bin",
        "binImg": "https://dragonwilds.runescape.wiki/images/Compost_Bin.png?b6a21",
        "unlock": "Level 10 Farming",
        "build": "8 Ash Logs + 4 Stone",
        "effects": [
            {"label": "Farming XP", "value": "10"},
            {"label": "Disease chance", "value": "50%"},
            {"label": "Yield", "value": "1.5x"},
        ],
    }),
    ("super", {
        "item": "Super Compost",
        "bin": "Super Compost Bin",
        "binImg": "https://dragonwilds.runescape.wiki/images/Super_Compost_Bin.png?34e0e",
        "unlock": "Level 60 Farming",
        "build": "8 Willow Logs + 4 Sandstone",
        "effects": [
            {"label": "Farming XP", "value": "50"},
            {"label": "Disease chance", "value": "25%"},
            {"label": "Yield", "value": "1.75x"},
        ],
    }),
    ("ultra", {
        "item": "Ultra Compost",
        "bin": "Ultra Compost Bin",
        "binImg": "https://dragonwilds.runescape.wiki/images/Ultra_Compost_Bin.png?19160",
        "unlock": "Level 69 Farming",
        "build": "8 Yew Logs + 4 Gypsum",
        "effects": [
            {"label": "Farming XP", "value": "50"},
            {"label": "Disease chance", "value": "12.5%"},
            {"label": "Yield", "value": "2.5x"},
        ],
    }),
]
TIER_INFO = dict(TIERS)
TIER_ORDER = [k for k, _ in TIERS]

# Every bin converts one item into 10 units of its compost. The regular bin is
# the only one that pays less for some inputs: raw food is worth 1, not 10.
UNITS_PER_ITEM = 10
RAW_FOOD_UNITS = 1

# --- Compost Bin -----------------------------------------------------------

# Named outright in the Compost Bin page's table, all at +10.
COMPOST_NAMED = [
    "Animal Bone", "Small Animal Fang", "Monstrous Fang", "Antler",
    "Bloodwood Sap", "Anima-Infused Bark", "Shocking Plant Bulb",
    "Feathers", "Wheat", "Ash Logs", "Oak Logs",
]

# Not on the bin's table, but each of these item pages says so in its own
# words - which is also how we know "Any plants" does not mean every plant.
#   Onion:  "Onions can be used to make compost."
#   Potato: "Potatoes can be used to make compost."
#   Weeds:  "can place it into a compost bin to convert to compost"
COMPOST_CONFIRMED = ["Onion", "Potato", "Weeds"]

# "Any [[Herbs|herb]] (except [[irit]])". The seven herbs come from the wiki's
# own Herbs page; irit is dropped here and picked up by the super bin below.
HERBS = ["Marrentil", "Harralander", "Kwuarm", "Snapdragon", "Toadflax", "Avantoe"]

# The category rules that could not be turned into an item list. Printed as-is
# on the Compost card; they tag no individual item. See the module docstring.
COMPOST_RULES = [
    {"text": "Any plants", "units": UNITS_PER_ITEM},
    {"text": "Any raw food", "units": RAW_FOOD_UNITS},
]

# Things a player will reasonably expect in the regular bin and be wrong about,
# each denied by its own page in so many words. Worth saying out loud on the
# card, because the failure mode is standing at a bin wondering why.
COMPOST_EXCLUDED = [
    {"name": "Pumpkin", "goes": "super"},
    {"name": "Watermelon", "goes": "super"},
    {"name": "Irit", "goes": "super"},
]

# --- Super and Ultra bins --------------------------------------------------

# Both pages enumerate their inputs, so these are straight transcriptions.
SUPER_ITEMS = [
    "Willow Logs", "Maple Logs", "Hollow Bark", "Pumpkin", "Roast Pumpkin",
    "Burnt Pumpkin", "Watermelon", "Cadavaberries", "Dried Cadavaberries",
    "Irit", "Corpse Cotton", "Undead Bone", "Undead Meat", "Raw Giant Krill",
    "Strong Sweet Tea",
]

ULTRA_ITEMS = [
    "Yew Logs", "Magic Logs", "Desert Weed", "Fibrous Pipe Cactus",
    "Cactus Fibres", "Cactus Steak", "Seared Cactus Steak", "Raw Monkfish",
    "Monkfish Fillets", "Raw Beltfish", "Steamed Beltfish", "Raw Desert Sole",
    "Sun Baked Sole", "Tea Leaves", "Dried Tea Leaves", "Ground Tea Leaves",
    "Strong Tea", "Strong Sweet Tea", "Monkfish Skewers", "Swabbie Pie",
    "Umbral Kebab", "Beltfish Broth",
]

# The super bin takes undead meat but not what you cook it into. Called out on
# the card for the same reason as COMPOST_EXCLUDED.
SUPER_EXCLUDED = [{"name": "Cauterised Undead Steak", "goes": None}]


def _burnt_food(by_name):
    """Every burnt food in the catalogue, for "Any burnt food".

    Safe to expand where "Any plants" was not: the Burnt shelf is exactly the
    set of burnt foods, the rule says any, and 17 of those pages carry an
    explicit compostvalue = 10 confirming the figure.
    """
    return sorted(n for n, it in by_name.items()
                  if it.get("chest") == "food" and it.get("bandLabel") == "Burnt")


def _groups(by_name):
    """tier key -> the shelves of items that make it, in display order."""
    burnt = _burnt_food(by_name)
    return {
        "compost": [
            {"label": "Burnt food", "note": "any of them", "items": burnt},
            {"label": "Herbs", "note": "except Irit", "items": list(HERBS)},
            {"label": "Bones, plants & logs", "note": "", "items": COMPOST_NAMED + COMPOST_CONFIRMED},
        ],
        "super": [{"label": "", "note": "", "items": list(SUPER_ITEMS)}],
        "ultra": [{"label": "", "note": "", "items": list(ULTRA_ITEMS)}],
    }


def apply(chests, by_name):
    """Stamp compost links in both directions. Returns a report of what stuck.

    Runs after the chests are assembled so it can look any item up by name
    across chest boundaries - a single bin's inputs are scattered over food,
    farming, wood, textiles, bones and potions.
    """
    groups = _groups(by_name)
    missing = []

    # item -> the tiers it feeds. Built first so an item in two bins (strong
    # sweet tea is in both the super and ultra lists) collects both.
    for tier in TIER_ORDER:
        units = UNITS_PER_ITEM
        for grp in groups[tier]:
            for name in grp["items"]:
                it = by_name.get(name)
                if it is None:
                    missing.append((tier, name))
                    continue
                entry = {"tier": tier, "label": TIER_INFO[tier]["item"],
                         "bin": TIER_INFO[tier]["bin"], "units": units}
                bucket = it.setdefault("compost", [])
                if not any(e["tier"] == tier for e in bucket):
                    bucket.append(entry)

    # tier -> everything that makes it, hung off the compost item itself.
    for tier in TIER_ORDER:
        info = TIER_INFO[tier]
        it = by_name.get(info["item"])
        if it is None:
            missing.append((tier, info["item"]))
            continue
        shelves = [dict(g, items=[n for n in g["items"] if n in by_name])
                   for g in groups[tier]]
        it["compostedFrom"] = {
            "bin": info["bin"],
            "binImg": info["binImg"],
            "unlock": info["unlock"],
            "build": info["build"],
            "effects": info["effects"],
            "units": UNITS_PER_ITEM,
            "groups": [g for g in shelves if g["items"]],
            "rules": COMPOST_RULES if tier == "compost" else [],
            "excluded": (COMPOST_EXCLUDED if tier == "compost"
                         else SUPER_EXCLUDED if tier == "super" else []),
        }

    tagged = sum(1 for it in by_name.values() if it.get("compost"))
    return {"tagged": tagged, "missing": missing,
            "per_tier": {t: sum(len(g["items"]) for g in groups[t]) for t in TIER_ORDER}}
