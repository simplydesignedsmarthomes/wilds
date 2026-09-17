/* Skills. Twelve released skills, max level 99 each. The "category" field
   is the game's own grouping (Combat/Gathering/Artisan/Support), shown as
   a badge, but the array order itself follows the skill order Jagex used
   for the Steam achievement list (Attack, Magic, Ranged, Mining,
   Woodcutting, Artisan, Construction, Cooking, Runecrafting, Farming,
   Fishing, Agility) — the closest confirmed proxy available for "the
   order it's in the game" short of a screenshot of the skills panel
   itself. */

window.WILDS_SKILLS = [
  ["Attack", "Combat", "Defeat enemies with melee weapons to level this skill."],
  ["Magic", "Combat", "Defeat enemies with magic, or cast spells, to level this skill."],
  ["Ranged", "Combat", "Defeat enemies with ranged weapons to level this skill."],
  ["Mining", "Gathering", "Mine ore, clay or stone, or gather stones from the floor."],
  ["Woodcutting", "Gathering", "Chop down trees, tear up saplings or collect logs from the floor."],
  ["Artisan", "Artisan", "Craft new weapons, armour or tools to level this skill."],
  ["Construction", "Artisan", "Build new structures to level this skill."],
  ["Cooking", "Artisan", "Cook food to level this skill."],
  ["Runecrafting", "Artisan", "Gather rune essence and craft runes at a Rune Altar to level this skill."],
  ["Farming", "Gathering", "Grow crops to level this skill."],
  ["Fishing", "Gathering", "Catch fish to level this skill."],
  ["Agility", "Support", "Run courses and traverse the world to level this skill."]
];
