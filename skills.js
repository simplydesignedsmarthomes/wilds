/* Skills. Ten released skills, max level 99 each, split into the game's own
   four groupings. Defence, Herblore and Thieving exist in game files but are
   not live yet, so they're flagged rather than omitted. */

window.WILDS_SKILLS = [
  ["Attack", "Combat", "Defeat enemies with melee weapons to level this skill."],
  ["Magic", "Combat", "Defeat enemies with magic, or cast spells, to level this skill."],
  ["Ranged", "Combat", "Defeat enemies with ranged weapons to level this skill."],
  ["Mining", "Gathering", "Mine ore, clay or stone, or gather stones from the floor."],
  ["Woodcutting", "Gathering", "Chop down trees, tear up saplings or collect logs from the floor."],
  ["Farming", "Gathering", "Grow crops to level this skill."],
  ["Fishing", "Gathering", "Catch fish to level this skill."],
  ["Runecrafting", "Artisan", "Gather rune essence and craft runes at a Rune Altar to level this skill."],
  ["Construction", "Artisan", "Build new structures to level this skill."],
  ["Artisan", "Artisan", "Craft new weapons, armour or tools to level this skill."],
  ["Cooking", "Artisan", "Cook food to level this skill."],
  ["Agility", "Support", "Run courses and traverse the world to level this skill."]
];

/* Skills present in game files but not yet released. Shown greyed out in the
   tracker rather than hidden, so a future update doesn't silently add rows. */
window.WILDS_SKILLS_UNRELEASED = ["Defence", "Herblore", "Thieving", "Prayer"];
