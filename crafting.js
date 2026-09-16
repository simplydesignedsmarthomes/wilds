/* Crafting stations, processing stations, material tiers and a handful of
   verified example recipes. This is a reference, not the full 1,266-item
   database — recipes are illustrative of what each station/tier makes,
   not exhaustive. */

window.WILDS_STATIONS_CRAFTING = [
  ["Armour Bench", "Craft armour pieces."],
  ["Blacksmith's Bench", "Craft weapons at bronze tier and above. Unlocks at Construction 12, needs a bronze bar to place."],
  ["Crafting Table", "General crafting for tools and basic goods."],
  ["Fletching Bench", "Craft bows, crossbow parts and ammunition."],
  ["Mystic Forge", "Craft magic-tier weapons and gear."],
  ["Rune Altar", "Craft runes from rune essence for Runecrafting XP."],
  ["Jeweler's Bench", "Craft rings, amulets and other jewelry."],
  ["Stone Range", "Early cooking station, precursor to the Cooking Range."],
  ["Cooking Range", "Cook food for Cooking XP."],
  ["Pottery Wheel", "Craft pottery and containers."],
  ["Brewing Cauldron", "Brew potions."]
];

window.WILDS_STATIONS_PROCESSING = [
  ["Campfire", "Basic cooking and light."],
  ["Grill", "Cook food."],
  ["Spinning Wheel", "Spin thread from wool or fiber."],
  ["Advanced Spinning Wheel", "Upgraded thread production."],
  ["Tannery", "Turn hides into leather."],
  ["Advanced Tannery", "Upgraded leather production, higher-tier hides."],
  ["Kiln", "Fire clay and pottery."],
  ["Loom", "Weave thread into cloth."],
  ["Furnace", "Smelt ore into bars."],
  ["Blast Furnace", "Higher-tier smelting, needed for mithril and beyond."],
  ["Grindstone", "Sharpen and process materials."],
  ["Sawmill", "Process logs into planks."],
  ["Stonecutter", "Cut stone into blocks."],
  ["Imbuing Barrel", "Imbue items with magical properties."]
];

window.WILDS_STATION_IMPROVEMENTS = [
  ["Tanner's Kit", "Improvement for the Tannery."],
  ["Loom Harness", "Improvement for the Loom."]
];

/* Material tier roughly gates which region you can hold your own in.
   "Power level" numbers are from player-facing patch discussion, not an
   in-game readout, so treat them as approximate. */
window.WILDS_TIERS = [
  ["Stone", 1, "Brynmoor (very early)"],
  ["Bronze", 2, "Brynmoor"],
  ["Iron", 3, "Ghornfell"],
  ["Steel", 5, "Ghornfell → Fellhollow"],
  ["Mithril", 6, "Fellhollow → Dowdun Reach"],
  ["Adamant", 7, "Umbral Sands"],
  ["Black metal", null, "Endgame / specialty"]
];

window.WILDS_RECIPES = [
  ["Bronze Dagger", "Blacksmith's Bench", "2× Bronze Bar", "60 XP"],
  ["Iron Sword", "Blacksmith's Bench", "8× Iron Bar, 4× Hard Leather, 1× Wool Thread, 4× Vault Shards", "100 XP"],
  ["Steel Pickaxe", "Blacksmith's Bench", "8× Steel Bar, 6× Willow Logs, 4× Draconic Leather", "100 XP"],
  ["Mithril Warhammer", "Blacksmith's Bench", "16× Mithril Bar, 3× Cursed Leather, 32× Infernal Fragments", "100 XP"],
  ["Mithril Bar", "Blast Furnace", "3× Mithril Ore, 3× Coal", "—"]
];
