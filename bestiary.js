/* Bestiary. This is a name + faction index pulled from the wiki's monster
   category listing, not a full stat/drop table — those live on each
   creature's own wiki page and weren't pulled in for v1. Faction grouping is
   inferred from naming (e.g. "Vault *", "Skeletal *"); a few one-off names
   without an obvious family sit under "Unique / Named". */

window.WILDS_BESTIARY = [
  { group: "Black Knights", names: [
    "Black Knight Guardian", "Black Knight Sniper", "Black Knight Titan", "Black Knight Warrior",
    "Elite Black Knight", "Houndmaster Rexiton", "Sergeant Blister", "Mage of Zamorak", "Zamorakian Acolyte"
  ]},
  { group: "Garou & wolves", names: [
    "Garou Berserker", "Garou Druid", "Garou Hunter", "Garou King", "Garou Thane",
    "Wolf", "Dire Wolf", "Dragon Wolf", "Ghost Wolf"
  ]},
  { group: "Goblins", names: [
    "Goblin Archer", "Goblin Bruiser", "Goblin Runt", "Goblin Warrior"
  ]},
  { group: "Skeletal & Rotsworn undead", names: [
    "Skeletal Archer", "Skeletal Hoplite", "Skeletal Marauder", "Skeletal Necromancer", "Skeletal Warrior", "Skeleton",
    "Rotsworn Marauder", "Rotsworn Necromancer", "Rotsworn Thrall", "Rotsworn Warrior", "Rotsworn Zombie",
    "Rotridden Cow", "Rotridden Rat", "Zombie", "Zombie Cow", "Zombie Rat", "Undead Giant Rat", "Lost Soul", "Soulstone Sentinel"
  ]},
  { group: "Demons", names: [
    "Abyssal Demon", "Lesser Demon", "Shardbound Lesser Demon"
  ]},
  { group: "Kalphites", names: [
    "Kalphite Guardian", "Kalphite Queen", "Kalphite Soldier", "Kalphite Worker"
  ]},
  { group: "Vault Guardians", names: [
    "Vault Archon", "Vault Corruptor", "Vault Guardian Hulk", "Vault Guardian Sentinel",
    "Vault Guardians", "Vault Incinerator", "Vault Overlord", "Vault Pyroclast", "Vault Striker"
  ]},
  { group: "KotHaar (Umbral Sands lava guardians)", names: [
    "KotHaar-Hur", "KotHaar-Kal", "KotHaar-Ket", "KotHaar-Xil"
  ]},
  { group: "Zogres", names: [
    "Zogre", "Ulgo the Zogre"
  ]},
  { group: "Wild vines (Anima Twist flora)", names: [
    "Wild Jade Vine", "Wild Lapulis Vine", "Wild Ruby Vine"
  ]},
  { group: "Spectral", names: [
    "Spectral Bird", "Spectral Chinchompa"
  ]},
  { group: "Dragons & major bosses", names: [
    "Blue Dragon", "Green Dragon", "Red Dragon", "Velgar", "Imaru", "Fuzan", "Karibdos"
  ]},
  { group: "Huntable wildlife", names: [
    "Chicken", "Cow", "Deer", "Goat", "Ram", "Sheep", "Vulture", "Magpie", "Raven", "Corrupted Raven",
    "Gyrfalcon", "Terrorbird", "Giant Rat", "Kebbit", "Desert Devil Kebbit", "Chinchompa", "Carnivorous Chinchompa"
  ]},
  { group: "Hellspawn & rats", names: [
    "Hellhound", "Hellrat", "Putrid Rat", "Rat King", "Rat Master Skrexis"
  ]},
  { group: "Unique / Named", names: [
    "Boggs", "Blightscale", "Buddy", "Curly", "Delrom", "Fido", "Gnasher", "Lurch",
    "Nosey", "Patch (Hellrat)", "Pip", "Plague King", "Razlem the Deranged", "Reek",
    "Rufus", "Summoner Flament", "Tiny", "Nature Spirit", "Tok-Xil"
  ]}
];
