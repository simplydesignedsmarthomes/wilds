/* Bestiary detail. Supplemental per-creature reference data keyed by name,
   meant to be merged/looked-up against window.WILDS_BESTIARY (the name index
   in bestiary.js, which this file does NOT modify).

   SOURCING: every entry below was pulled from that creature's own page on
   https://dragonwilds.runescape.wiki/w/<Creature_Name> (fetched Sept 2026).
   The wiki uses "Power Level" (not a classic RuneScape combat level) as its
   difficulty stat, sometimes alongside a raw HP figure -- both are recorded
   here as `level` when the page stated them. `region` is the area/location
   named on the page (vault names are sub-locations inside the "Dragonkin
   Vaults" system, which itself spans multiple overworld regions). `style` is
   only set when the page explicitly described the attack type or listed
   weakness/resistance patterns strongly implying it; where the wiki text was
   ambiguous or silent, the field is omitted rather than guessed. `drop` lists
   one representative notable/guaranteed or rare drop, not the full table.

   CONFIDENCE: high for named bosses and faction trash with a clean infobox
   (Black Knights, Kalphites, Vault Guardians, KotHaar). Lower/partial for a
   few lore-only entries (e.g. Karibdos has no drop table published -- it's
   an ancient, already-slain lore creature) and for a couple of pages with
   internally inconsistent power-level text (noted inline where it occurs).
   Fields not verifiable from the wiki were left out entirely rather than
   invented. Not all ~140 names in bestiary.js appear here -- this file only
   covers the ~45 highest-priority bosses/factions requested (Black Knights,
   Kalphites, Vault Guardians, KotHaar, named bosses, and a few notable
   undead/demon trash tied to those regions). Common wildlife is not covered.
*/

window.WILDS_BESTIARY_DETAIL = {
  // ---- Named bosses ----
  "Velgar": {
    region: "Velgar's Rise, Fractured Plains",
    level: "Power Level 4 (6,000 HP)",
    style: "Magic (poison breath and meteor barrages while airborne)",
    drop: "Ascension Shard (Power Level 4), 30-40 -- always"
  },
  "Imaru": {
    region: "Imaru's Tower, Hope's Fall (Fellhollow)",
    level: "Power Level 5 (14,000 HP)",
    style: "Magic (elemental / anima-infused attacks)",
    drop: "Serrated Claw -- 1/10"
  },
  "Fuzan": {
    region: "Umbral Sands",
    level: "Power Level 7 (16,000 HP)",
    style: "Fire breath attacks",
    drop: "Fuzan's Head -- always"
  },
  "Karibdos": {
    region: "Beneath the Umbral Sands (Ashenfall) -- an ancient, already-slain lore boss",
    style: "Melee (dragged prey into a sand vortex, swallowed whole)"
    // No power level or drop table is published on the wiki for this one.
  },
  "Black Knight Titan": {
    region: "Black Knight's Fortress, Dowdun Reach",
    level: "Power Level 6",
    style: "Melee (weak to crush/water; resists fire/slash; immune to burn, bleed, poison)",
    drop: "Broken Titan's Wrath -- always; Ascension Shard (Power Level 6), 20-30 -- always"
  },
  "Kalphite Queen": {
    region: "End of the vault, Umbral Sands",
    level: "Power Level 7 (5,500 HP)",
    style: "Hybrid -- cycles red/blue/green shades that block melee, magic, or ranged in turn",
    drop: "Greater Kalphite Wings (2-4) -- always; Ornate Golden Scarab and Moonsilk Weave mount -- rare"
  },
  "Plague King": {
    region: "Whispering Swamp, Bloodblight Swamp, and Vertentis Kara vault",
    level: "Power Level 2 (Whispering Swamp) / Power Level 3 (Bloodblight Swamp)",
    style: "Melee (crush weakness, stab resistance implied)",
    drop: "Poison Ichor -- always"
  },
  "Rat King": {
    region: "Vertentis Kara and Kalistrakthen Kara vaults",
    level: "Power Level 2 (280 HP)",
    style: "Melee (weak to stab, resists crush)",
    drop: "Raw Rat Meat (3x) -- always"
  },
  "Rat Master Skrexis": {
    region: "Dowdun Reach (spawns with six accompanying Hellrats)",
    level: "Power Level 6 (840 HP)",
    style: "Magic (fire spells, short teleport, calls Flames of Zamorak)",
    drop: "Zamorakian Mage Pack (2x) -- always"
  },
  "Razlem the Deranged": {
    region: "South-east Silverthorn Keep, Fellhollow (page title \"Razlem, the Deranged\")",
    level: "Power Level 5 (862 HP)",
    style: "Magic (necromancer-like moveset; weak to crush, resists air/fire)"
    // Guards the "Eventide - A New Spawn" quest scroll; no separate item drop table published.
  },
  "Summoner Flament": {
    region: "Dowdun Reach, under the Cathedral near The Lake",
    level: "Power Level 6 (840 HP)",
    style: "Magic (fire spells, short-distance teleport, Flames of Zamorak)",
    drop: "Zamorakian Mage Pack (2x) -- always"
  },
  "Ulgo the Zogre": {
    region: "Coalridge Pass (guards the Coclear Malificarum scroll)",
    level: "Power Level 5 (4,200 HP)",
    style: "Melee (weak to crush; resists slash, stab, air)",
    drop: "Zogre Pack -- always; Springdown Runner / Grassfoot Screecher / Leafwood Strider mounts -- 1/100 each"
  },
  "Garou King": {
    region: "Highlands Castle, Stormtouched Highlands",
    level: "Power Level 5 (1,035 HP)",
    style: "Melee (tower shield, stance-breaking mechanic; weak to crush, resists stab)",
    drop: "Tainted King's Token -- always (Dog Days quest item); Garou Pack -- always"
  },

  // ---- Black Knights (Dowdun Reach) ----
  "Houndmaster Rexiton": {
    region: "The Garrison, Dowdun Reach",
    level: "Power Level 6 (150 HP)",
    style: "Melee (weak to crush/earth, resists slash/stab)",
    drop: "Zamorakian Warrior Pack -- always"
  },
  "Sergeant Blister": {
    region: "The Garrison, beneath Dowdun Reach",
    level: "Power Level 6 (wiki text also calls it a \"power level 7 variant of the Black Knight Guardian\" -- inconsistent on the page)",
    drop: "Zamorakian Warrior Pack -- always; drops a Dreaming Stone Shard"
  },
  "Mage of Zamorak": {
    region: "Dowdun Reach",
    level: "Power Level 6 (840 HP)",
    style: "Magic (fire spells, short teleport, Flames of Zamorak; weak to slash/ranged, resists air/fire)",
    drop: "Zamorakian Mage Pack (2x) -- always"
  },
  "Zamorakian Acolyte": {
    region: "Dowdun Reach",
    level: "Power Level 6 (560 HP)",
    style: "Hybrid melee/magic (fire spell plus dagger attacks)",
    drop: "Zamorakian Mage Pack -- always"
  },
  "Black Knight Guardian": {
    region: "Dowdun Reach (Black Knight's Fortress)",
    level: "Power Level 6",
    style: "Melee, shield-bearer (weak to crush/earth, resists slash/stab)",
    drop: "Zamorakian Warrior Pack -- always"
  },
  "Black Knight Sniper": {
    region: "Dowdun Reach",
    level: "Power Level 6 (560 HP)",
    style: "Ranged (crossbow; weak to stab/fire, resists bolts/arrows)",
    drop: "Steel Arrows (4-8) -- always; Zamorakian Warrior Pack -- always"
  },
  "Black Knight Warrior": {
    region: "Dowdun Reach (Black Knight's Fortress)",
    level: "Power Level 6 (630 HP)",
    style: "Melee (weak to crush/earth, resists slash/stab)",
    drop: "Zamorakian Warrior Pack -- always"
  },
  "Elite Black Knight": {
    region: "Dowdun Reach",
    level: "Power Level 6",
    style: "Melee (weak to air magic, resists slash/stab)",
    drop: "Zamorakian Warrior Pack (2x) -- always; Eclipseborn Sharpbeak / Summerbellied Wagtail / Sunkissed Clawfoot mounts -- 1/100 each"
  },

  // ---- Kalphites (Umbral Sands) ----
  "Kalphite Guardian": {
    region: "Umbral Sands",
    level: "Power Level 7 (2,475 HP)",
    style: "Hybrid -- cycles color-phase immunities, similar to the Kalphite Queen",
    drop: "Greater Kalphite Wing and 1-2 Kalphite Shell Fragments -- always"
  },
  "Kalphite Soldier": {
    region: "Umbral Sands",
    level: "Power Level 7 (825 HP)",
    style: "Melee (resists crush, slash, stab, ranged, air, water)",
    drop: "Kalphite Wing (1x) and Kalphite Shell Fragments (2-4x) -- always"
  },
  "Kalphite Worker": {
    region: "Umbral Sands",
    level: "Power Level 7 (495 HP)",
    style: "Melee (resists crush, slash, stab, ranged, air, water)",
    drop: "Stunted Kalphite Wing (1x) -- always"
  },

  // ---- Vault Guardians (Dragonkin Vaults, spanning Brynmoor / Ghornfell / Fellhollow / Umbral Sands) ----
  "Vault Guardians": {
    region: "Ancient dragonkin vaults scattered across Ashenfall (Brynmoor, Ghornfell, Fellhollow, Umbral Sands)",
    style: "Anima-animated constructs; melee-based, individual variants add fire/poison/shock",
    drop: "Stone, Rune Essence, and Vault Shards are the common currency-like drops across the whole faction"
    // Umbrella faction term, not a single fightable creature -- see the specific variants below for stats.
  },
  "Vault Archon": {
    region: "Dragonkin Vaults (Brynmoor, Ghornfell, Fellhollow, Umbral Sands)",
    level: "Power Level 2 (3,100 HP)",
    style: "Ranged",
    drop: "Stone (5x) -- always"
  },
  "Vault Corruptor": {
    region: "Skeklac Kara vault",
    level: "Power Level 4 (2,925 HP)",
    style: "Melee plus poison (weak to water, resists fire; immune to poison/bleed/burn)",
    drop: "Stone (30x) -- always"
  },
  "Vault Guardian Hulk": {
    region: "Vaults in Brynmoor, Ghornfell, and Fellhollow",
    level: "Power Level 2-5 (390-690 HP depending on tier)",
    style: "Melee (weak to crush; immune to poison/bleed/burn)",
    drop: "Stone (5x) -- always"
  },
  "Vault Guardian Sentinel": {
    region: "Vaults in Brynmoor, Ghornfell, and Fellhollow",
    level: "Power Level 2-4",
    style: "Ranged/magic (Magic Missile and underground spike-trap projectiles)",
    drop: "Stone (15x) -- always"
  },
  "Vault Incinerator": {
    region: "Takla Kara vault, Ghornfell",
    level: "Power Level 3",
    style: "Melee plus fire (weak to water, resists fire; immune to poison/bleed/burn)",
    drop: "Stone (30x, plus 5x possible) -- always"
  },
  "Vault Overlord": {
    region: "Crasorak Kara and Skekven Kara vaults",
    level: "Power Level 2 (1,300 HP)",
    style: "Melee (oversized Vault Guardian Hulk variant; immune to poison/bleed/burn)",
    drop: "Stone (15x) -- always"
  },
  "Vault Pyroclast": {
    region: "Chaktan Kara vault, Ghornfell",
    level: "Power Level 4 (2,925 HP)",
    style: "Melee plus fire (weak to water, resists fire; immune to poison/bleed/burn)",
    drop: "Stone (30x) -- always"
  },
  "Vault Striker": {
    region: "Kalistrakthen Kara vault, Fellhollow",
    level: "Power Level 5 (3,738 HP)",
    style: "Melee plus shock/electric",
    drop: "Stone (30x, plus 5x possible) -- always"
  },

  // ---- KotHaar (Umbral Sands lava guardians) ----
  "KotHaar-Hur": {
    region: "Umbral Sands",
    level: "Power Level 7 (660 HP)",
    style: "Melee, unarmed two-swing combo (weak to water, resists ranged; immune to fire/burn)",
    drop: "Kot Pack -- always"
  },
  "KotHaar-Kal": {
    region: "Umbral Sands",
    level: "Power Level 7 (2,475 HP)",
    style: "Hybrid ranged/melee (ring attacks and stabbing; immune to fire/burn)",
    drop: "Kot Pack (2x) -- always"
  },
  "KotHaar-Ket": {
    region: "Umbral Sands",
    level: "Power Level 7",
    style: "Melee, hammer-wielder (sweeping strikes, earth spikes, double-hammer slam)",
    drop: "Kot Pack -- always"
  },
  "KotHaar-Xil": {
    region: "Umbral Sands",
    level: "Power Level 7",
    style: "Ranged (thrown weapons)",
    drop: "Kot Pack -- always"
  },
  "Tok-Xil": {
    region: "Umbral Sands, Ashenfall",
    level: "Power Level 7",
    style: "Melee (weak to water, resists ranged; immune to fire/burn)",
    drop: "Kot Pack (3x) -- always"
  },

  // ---- Zogres, Garou, demons, undead (mixed regions) ----
  "Zogre": {
    region: "Hope's Fall, Vekchenven Kara, Silverthorn Keep, Dowdun Reach, Fellhollow",
    level: "Power Level 5 (4,200 HP) or Power Level 6 (6,000 HP) variant",
    style: "Melee (belly flops, charges, rock throws; weak to crush, resists slash/stab/air)",
    drop: "Zogre Pack -- always"
  },
  "Garou Thane": {
    region: "Bloodblight Swamp and Stormtouched Highlands",
    level: "Power Level 3-4",
    style: "Melee, tower shield with a breakable defensive stance (weak to crush, resists stab)",
    drop: "Garou Pack -- always"
  },
  "Hellhound": {
    region: "Dowdun Reach (named variants include Fido, Gnasher, Lurch, Rufus, Tiny)",
    level: "Power Level 6 (420 HP)",
    style: "Melee (demon; weak to water, resists fire, immune to burn)",
    drop: "Small Ash Pile -- always"
  },
  "Abyssal Demon": {
    region: "Whispering Swamp and Bloodblight Swamp (also spawns unintentionally in Fractured Plains)",
    level: "Power Level 4 (1,500 HP)",
    style: "Melee plus magic, teleporting (weak to slash, resists air magic)",
    drop: "Abyssal Spine (1x), Abyssal Ashes (3x) -- always"
  },
  "Lesser Demon": {
    region: "Dowdun Reach (Demon Gate, under The Library, under The Cathedral near The Lake)",
    level: "Power Level 6 (2,100 HP)",
    style: "Melee (weak to stab/water, resists crush/fire/air, immune to burn)",
    drop: "Ash Pile (2x) -- always"
  },
  "Delrom": {
    region: "Beneath Dowdun Reach, near The Lake (under the Cathedral) -- a named Lesser Demon",
    level: "Power Level 6 (2,100 HP)",
    style: "Melee (weak to stab/water, resists crush/fire/air)",
    drop: "Ash Pile -- always"
  },
  "Blightscale": {
    region: "South side of the cliffs leading to Silverthorn Keep, north-east of the ominous gateway (Fellhollow) -- a named Green Dragon",
    level: "Power Level 5 (2,800 HP)",
    drop: "Dragon Blood (8x), Green Dragon Hide (6-8x), Dragon Tooth (3-5x), Soul Fragment (40-50x) -- always"
    // Wiki: "has the same attacks and drops as a normal Green Dragon" -- doesn't itself name a melee/ranged/magic style.
  },
  "Soulstone Sentinel": {
    region: "Fellhollow, behind spectral doors",
    level: "Power Level 5 (1,380 HP)",
    style: "Melee, similar to Skeletal Hoplites (weak to crush/air, resists slash/stab/fire)",
    drop: "Ectoplasm -- 1/4"
  }
};
