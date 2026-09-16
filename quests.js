/* Quests. Primary quests are the main line and must be done in order.
   Secondary quests unlock once their region opens up and don't have a
   required order. The wiki doesn't publish reward tables for these, so
   there's no reward column — the tracker just checks them off. */

window.WILDS_QUESTS_PRIMARY = [
  ["First Steps", "Tutorial quest. Starts automatically with a new character."],
  ["Getting Started", "Speak to Doric outside the temple."],
  ["Ratcatcher", "Speak to Vannaka near the old windmill."],
  ["Rune Mysteries", "Speak to Zanik on the path to Bramblemead Valley."],
  ["Dragon Slayer", "Speak to the Wise Old Man in Bramblemead Village."],
  ["Withering Heights", "Speak to the Wise Old Man near Ashien's Watch."],
  ["Black Knight's Fortress", "Speak to Death in the Forgotten Temple."],
  ["Icthlarin's Little Helper", "Interact with the door to Umbral Sands."],
  ["Regicide", "Found in the Scorned Wilderness."]
];

window.WILDS_QUESTS_SECONDARY = {
  "Brynmoor": ["Restless Ghosts", "Goblin Diplomacy", "Highlighting the Problem"],
  "Ghornfell": ["Granite Mauled", "Heartstrings", "Dog Days", "Cook's Assistant", "Animal Magnetism", "A Room With A Garou", "A Melody Remembered"],
  "Fellhollow": ["Even More Restless Ghosts", "The Wild Hunt", "Seeking Salvation", "Things That Go Boom In The Night", "Doric's Quest", "Letters for the Dead", "What Remains is Written", "Mirror Mirror"],
  "Dowdun Reach": ["Biohazard", "Wanted!", "What's Theirs is Mine!"],
  "Umbral Sands": ["Contact!", "Mapping The Sands I", "Mapping The Sands II", "Brink of Extinction"]
};

/* Tertiary quests trigger mid-primary-quest rather than through an NPc,
   so there's no separate name list on the wiki to check off here. */
window.WILDS_QUESTS_NOTE =
  "Tertiary quests activate automatically during specific primary quests " +
  "rather than being started from an NPC, so they aren't tracked as separate items.";
