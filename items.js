/* Equipment reference: weapons and armour, organized by material tier. This is
   a curated cross-section, not the full 1,266-item catalog (see crafting.js
   for that caveat) — one or two representative weapons per combat style and a
   representative armour piece or set per tier, not every recipe variant.

   Sourced from dragonwilds.runescape.wiki per-item pages. Where a "note"
   gives numbers (power level, base damage, defence values, Artisan level to
   craft), those were read directly off that item's wiki page and are
   VERIFIED. Where a wiki page didn't expose numbers (mostly rings/amulets,
   whose effect text is the only number given), the note describes the effect
   instead of guessing a stat. Tier ordering follows CLAUDE-facing convention:
   Stone < Bronze < Iron < Steel < Mithril < Adamant < Black metal.

   Two things worth flagging because they cut against the "RS-classic" mental
   model:
   - Fletching (bows/staves) tiers off wood, not metal — ash/oak/willow/
     maple/yew for bows, similar woods for battlestaves. A yew longbow is
     higher-tier than anything bronze or iron could produce.
   - "Black metal" gear is often labeled in-wiki as the "Black Knight" set,
     and reuses some mithril in its recipes (e.g. Black Knight Platebody
     takes 2 Mithril Bars alongside 10 Black Metal Bars). Power level for
     black metal items clusters around 6-7, same range as mithril/adamant/
     obsidian — it's a specialty/quest-gated tier, not strictly "better than
     Adamant" in raw numbers. */

window.WILDS_EQUIPMENT = [
  // ---- Stone tier ----
  { tier: "Stone", slot: "Weapon", name: "Stone Pickaxe", style: "Melee", note: "Earliest tool-weapon; predates the Blacksmith's Bench." },
  { tier: "Stone", slot: "Weapon", name: "Stone Hatchet", style: "Melee", note: "Earliest logging tool, doubles as a starter weapon." },

  // ---- Bronze tier ----
  { tier: "Bronze", slot: "Weapon", name: "Bronze Dagger", style: "Melee", note: "Power level 3, Stab, base damage 20-51, durability 1050. Craft: Artisan 60 at Blacksmith's Bench, 6 Bronze Bars + 3 Small Animal Fangs + 1 Wool Thread." },
  { tier: "Bronze", slot: "Weapon", name: "Bronze Sword", style: "Melee", note: "Craft: Blacksmith's Bench, Bronze Bars + basic materials." },
  { tier: "Bronze", slot: "Weapon", name: "Bronze Greatsword", style: "Melee", note: "Two-handed slash weapon, Blacksmith's Bench." },
  { tier: "Bronze", slot: "Weapon", name: "Bronze Warhammer", style: "Melee", note: "Two-handed crush weapon, Blacksmith's Bench." },
  { tier: "Bronze", slot: "Weapon", name: "Bronze Mace", style: "Melee", note: "One-handed crush weapon, Blacksmith's Bench." },
  { tier: "Bronze", slot: "Weapon", name: "Bronze Crossbow", style: "Ranged", note: "Fires Bronze Bolts; Fletching Bench." },
  { tier: "Bronze", slot: "Ammo", name: "Bronze Arrow", style: "Ranged", note: "Base-tier arrow, also comes in Barbed and Fire variants." },
  { tier: "Bronze", slot: "Armour - Head", name: "Bronze Helmet", style: "Melee", note: "Armour Bench, Bronze Bars." },
  { tier: "Bronze", slot: "Armour - Body", name: "Bronze Platebody", style: "Melee", note: "Power level 3: Melee Def 23, Ranged Def 17, Magic Def 15, durability 1250. Craft: Artisan 60 at Armour Bench, 10 Bronze Bars + 4 Hard Leather + 2 Wool Thread." },
  { tier: "Bronze", slot: "Armour - Legs", name: "Bronze Platelegs", style: "Melee", note: "Armour Bench, Bronze Bars." },
  { tier: "Bronze", slot: "Off-hand", name: "Bronze Shield", style: "Melee", note: "Basic tier shield, Armour Bench." },

  // ---- Iron tier ----
  { tier: "Iron", slot: "Weapon", name: "Iron Sword", style: "Melee", note: "Craft: Blacksmith's Bench, 8 Iron Bar + 4 Hard Leather + 1 Wool Thread + 4 Vault Shards, 100 Artisan XP." },
  { tier: "Iron", slot: "Weapon", name: "Iron Greatsword", style: "Melee", note: "Power level 4, Slash, base damage 62-107, block 39.5, durability 1300. Craft: Artisan 100 at Blacksmith's Bench, 10 Iron Bars + 4 Hard Leather + 2 Wool Thread + 4 Vault Shards." },
  { tier: "Iron", slot: "Weapon", name: "Iron Greataxe", style: "Melee", note: "Two-handed slash weapon, Blacksmith's Bench." },
  { tier: "Iron", slot: "Weapon", name: "Iron Dagger", style: "Melee", note: "Blacksmith's Bench, Iron Bars." },
  { tier: "Iron", slot: "Weapon", name: "Iron Crossbow", style: "Ranged", note: "Fires Iron Bolts; Fletching Bench." },
  { tier: "Iron", slot: "Ammo", name: "Iron Arrow", style: "Ranged", note: "Also comes in Barbed and Fire variants." },
  { tier: "Iron", slot: "Armour - Head", name: "Iron Helmet", style: "Melee", note: "Armour Bench, Iron Bars." },
  { tier: "Iron", slot: "Armour - Body", name: "Iron Platebody", style: "Melee", note: "Armour Bench, Iron Bars." },
  { tier: "Iron", slot: "Armour - Legs", name: "Iron Platelegs", style: "Melee", note: "Armour Bench, Iron Bars." },
  { tier: "Iron", slot: "Off-hand", name: "Iron Shield", style: "Melee", note: "Armour Bench, Iron Bars." },

  // ---- Steel tier ----
  { tier: "Steel", slot: "Weapon", name: "Steel Scimitar", style: "Melee", note: "Power level 5, Slash, base damage 49-103, block 26, durability 1300. Craft: Blacksmith's Bench, 10 Steel Bars + 5 Draconic Leather + 2 Fine Cloth + 6 Vault Shards, 100 Artisan XP." },
  { tier: "Steel", slot: "Weapon", name: "Steel Pickaxe", style: "Melee", note: "Craft: Blacksmith's Bench, 8 Steel Bar + 6 Willow Logs + 4 Draconic Leather, 100 Artisan XP." },
  { tier: "Steel", slot: "Weapon", name: "Steel Greataxe", style: "Melee", note: "Two-handed slash weapon, Blacksmith's Bench." },
  { tier: "Steel", slot: "Weapon", name: "Steel Warhammer", style: "Melee", note: "Two-handed crush weapon, Blacksmith's Bench." },
  { tier: "Steel", slot: "Weapon", name: "Steel Crossbow", style: "Ranged", note: "Fires Steel Bolts; Fletching Bench." },
  { tier: "Steel", slot: "Ammo", name: "Steel Arrow", style: "Ranged", note: "Also comes in Barbed and Fire variants." },
  { tier: "Steel", slot: "Armour - Head", name: "Steel Full Helm", style: "Melee", note: "Power level 5: Melee Def 15, Ranged Def 13, Magic Def 12, durability 1500. Craft: Artisan 100 at Armour Bench, 4 Steel Bars + 4 Draconic Leather + 1 Fine Cloth + 1 Sacred Oil + 2 Vault Shards." },
  { tier: "Steel", slot: "Armour - Body", name: "Steel Platebody", style: "Melee", note: "Armour Bench, Steel Bars." },
  { tier: "Steel", slot: "Armour - Legs", name: "Steel Platelegs", style: "Melee", note: "Armour Bench, Steel Bars." },
  { tier: "Steel", slot: "Off-hand", name: "Steel Shield", style: "Melee", note: "Armour Bench, Steel Bars." },

  // ---- Mithril tier ----
  { tier: "Mithril", slot: "Weapon", name: "Mithril Warhammer", style: "Melee", note: "Power level 6, Crush, base damage 126-197, block 44, durability 1600. Craft: Blacksmith's Bench, 16 Mithril Bars + 3 Cursed Leather + 32 Infernal Fragments, 100 Artisan XP." },
  { tier: "Mithril", slot: "Weapon", name: "Mithril Greataxe", style: "Melee", note: "Two-handed slash weapon, Blacksmith's Bench." },
  { tier: "Mithril", slot: "Weapon", name: "Mithril Scimitar", style: "Melee", note: "One-handed slash weapon, Blacksmith's Bench." },
  { tier: "Mithril", slot: "Weapon", name: "Mithril Crossbow", style: "Ranged", note: "Fires Mithril Bolts; Fletching Bench." },
  { tier: "Mithril", slot: "Ammo", name: "Mithril Arrow", style: "Ranged", note: "Also comes in Barbed and Fire variants." },
  { tier: "Mithril", slot: "Armour - Head", name: "Mithril Helmet", style: "Melee", note: "Part of the Mithril set: 1750 durability, Melee Def 18, Ranged Def 16, Magic Def 15." },
  { tier: "Mithril", slot: "Armour - Body", name: "Mithril Platebody", style: "Melee", note: "Power level 6: 1750 durability, Melee Def 45, Ranged Def 39, Magic Def 38. Full 3-piece set totals 90/79/76 and grants block-cost, crit and stagger-damage set bonuses." },
  { tier: "Mithril", slot: "Armour - Legs", name: "Mithril Platelegs", style: "Melee", note: "Part of the Mithril set: 1750 durability, Melee Def 27, Ranged Def 24, Magic Def 23." },
  { tier: "Mithril", slot: "Off-hand", name: "Mithril Shield", style: "Melee", note: "Armour Bench, Mithril Bars." },

  // ---- Adamant tier ----
  { tier: "Adamant", slot: "Weapon", name: "Adamant Warhammer", style: "Melee", note: "Power level 7, Crush, base damage 156-244, block 44, durability 1600. Craft: Blacksmith's Bench, 16 Adamant Bars + 3 Scorch Leather + 4 Gypsum Wax, 100 Artisan XP." },
  { tier: "Adamant", slot: "Weapon", name: "Adamant Sword", style: "Melee", note: "One-handed slash weapon, Blacksmith's Bench." },
  { tier: "Adamant", slot: "Weapon", name: "Adamant Greatsword", style: "Melee", note: "Two-handed slash weapon, Blacksmith's Bench." },
  { tier: "Adamant", slot: "Weapon", name: "Adamant Greataxe", style: "Melee", note: "Two-handed slash weapon, Blacksmith's Bench." },
  { tier: "Adamant", slot: "Weapon", name: "Adamant Scimitar", style: "Melee", note: "One-handed slash weapon, Blacksmith's Bench." },
  { tier: "Adamant", slot: "Weapon", name: "Adamant Crossbow", style: "Ranged", note: "Fires Adamant Bolts; Fletching Bench." },
  { tier: "Adamant", slot: "Ammo", name: "Adamant Arrow", style: "Ranged", note: "Also comes in Barbed and Fire variants." },
  { tier: "Adamant", slot: "Armour - Body", name: "Adamant Platebody", style: "Melee", note: "Power level 7: Melee Def 53, Ranged Def 47, Magic Def 45, durability 1500. Craft: Armour Bench, 10 Adamant Bars + 8 Scorch Leather + 3 Desert Cloth + 3 Refined Obsidian + 3 Gypsum Wax + 3 Garou Weave, repair with 2 Adamant Bars." },
  { tier: "Adamant", slot: "Armour - Head", name: "Adamant Helmet", style: "Melee", note: "Armour Bench, Adamant Bars." },
  { tier: "Adamant", slot: "Armour - Legs", name: "Adamant Platelegs", style: "Melee", note: "Armour Bench, Adamant Bars." },
  { tier: "Adamant", slot: "Off-hand", name: "Adamant Shield", style: "Melee", note: "Armour Bench, Adamant Bars." },

  // ---- Black metal tier (specialty / quest-gated) ----
  { tier: "Black metal", slot: "Weapon", name: "Black Sword", style: "Melee", note: "Power level 6 (7 ascended), Slash, base damage 75-136, durability 1300. Deals +15% damage vs. mage enemies. Craft: Blacksmith's Bench, 10 Black Metal Bar + 5 Cursed Leather + 4 Mystic Thread + 2 Demonic Oil; recipe requires studying the shattered black blade vestige." },
  { tier: "Black metal", slot: "Weapon", name: "Black Greataxe", style: "Melee", note: "Two-handed slash weapon made from Black Metal Bars, Blacksmith's Bench." },
  { tier: "Black metal", slot: "Weapon", name: "Titan's Wrath", style: "Melee", note: "Power level 6 (7 ascended) greatsword, base damage 110-190, block 59, durability 1300. Special \"Baptism of Fire\" AoE burn attack. Reward from the Black Knight's Fortress quest, or craft at Blacksmith's Bench with 12 Black Metal Bars + 5 Blue Dragon Leather + 4 Mystic Cloth + 64 Infernal Fragments + 1 Broken Titan's Wrath (dropped by the Black Knight Titan)." },
  { tier: "Black metal", slot: "Weapon", name: "Zamorak Staff", style: "Magic", note: "Power level 6 (7 ascended), rune damage 6.8/8.3, durability 1600. Passive +33% fire spell damage, but half damage on air/water/earth spells. Craft: Mystic Forge, Artisan 40, 10 Black Metal Bars + 10 Cursed Leather + 6 Demonic Oil + 4 Diamonds + 64 Infernal Fragments. Unlocked via the \"What's Theirs is Mine!\" quest in Dowdun Reach." },
  { tier: "Black metal", slot: "Weapon", name: "Black Crossbow", style: "Ranged", note: "Uses Black Crossbow Limbs; Fletching Bench." },
  { tier: "Black metal", slot: "Off-hand", name: "Black Shield", style: "Melee", note: "Armour Bench, Black Metal Bars." },
  { tier: "Black metal", slot: "Armour - Body", name: "Black Knight Platebody", style: "Melee", note: "Power level 6: Melee Def 45, Ranged Def 39, Magic Def 38. Craft: Armour Bench, Artisan 100, 10 Black Metal Bar + 2 Mithril Bar + 6 Cursed Leather + 4 Mystic Cloth + 3 Demonic Oil; recipe unlocked via the shard of black pauldron vestige from the Evil Emporium." },
  { tier: "Black metal", slot: "Armour - Head", name: "Black Knight Helmet", style: "Melee", note: "Part of the Black Knight set, Armour Bench." },
  { tier: "Black metal", slot: "Armour - Legs", name: "Black Knight Platelegs", style: "Melee", note: "Part of the Black Knight set, Armour Bench." },
  { tier: "Black metal", slot: "Armour - Body", name: "Shadow Body", style: "Ranged", note: "Part of the black-metal Shadow set (Cowl, Body, Chaps)." },
  { tier: "Black metal", slot: "Armour - Body", name: "Zamorak Robes", style: "Magic", note: "Part of the black-metal Zamorak set (Hood, Robes, Robe Legs)." },

  // ---- Fletching (wood-tiered, not metal-tiered) ----
  { tier: "Wood (Fletching)", slot: "Weapon", name: "Ash Shortbow", style: "Ranged", note: "Early fletched bow; Fletching Bench." },
  { tier: "Wood (Fletching)", slot: "Weapon", name: "Willow Longbow", style: "Ranged", note: "Mid-tier fletched bow; Fletching Bench." },
  { tier: "Wood (Fletching)", slot: "Weapon", name: "Maple Longbow", style: "Ranged", note: "Higher-tier fletched bow; Fletching Bench." },
  { tier: "Wood (Fletching)", slot: "Weapon", name: "Yew Longbow", style: "Ranged", note: "Base damage 101, multiplier 4.2, durability 1300. Craft: Fletching Bench, Artisan 60, 16 Yew Logs + 4 Adamant Bars + 8 Desert Thread + 4 Dragonstones + 4 Gypsum Wax. Repair costs 3 Yew Logs." },
  { tier: "Wood (Fletching)", slot: "Weapon", name: "Crystal Bow", style: "Ranged", note: "Masterwork shortbow, power level 3 base up to power level 7 ascended (base damage 20 to 58), durability 1050. Special \"Shattershot\" AoE cone. Craft: Fletching Bench, Artisan 300, reward + recipe from the Heartstrings quest; ascendable at the Mystic Forge." },
  { tier: "Wood (Fletching)", slot: "Weapon", name: "Ash Battlestaff", style: "Magic", note: "Early battlestaff; Mystic Forge." },
  { tier: "Wood (Fletching)", slot: "Weapon", name: "Maple Battlestaff", style: "Magic", note: "Mid-tier battlestaff; Mystic Forge." },
  { tier: "Wood (Fletching)", slot: "Weapon", name: "Splitbark Staff", style: "Magic", note: "Damage multiplier 5.4, attack combo 4, durability 1300. Part of the power-level-5 Splitbark magic set." },
  { tier: "Wood (Fletching)", slot: "Weapon", name: "Necromancer's Staff", style: "Magic", note: "Three power levels (5/6/7), rune damage 5.9/7.3/8.8, durability 1050 at every level. Craft: Mystic Forge, Artisan 250, 24 Undead Bones + 6 Sacred Oil + 4 Fine Thread + 6 Vault Shards. Recipe found via a dragonkin effigy in Vekchenven Kara, Fellhollow." },

  // ---- Obsidian tier (specialty, matches Adamant power level) ----
  { tier: "Obsidian", slot: "Weapon", name: "Toktz-Mej-Tal", style: "Melee", note: "Obsidian-tier melee weapon; base damage in the 93-244 range shared by obsidian melee weapons. Recipe drops from KotHaar enemies in Umbral Sands." },
  { tier: "Obsidian", slot: "Off-hand", name: "TokTz-Ket-Xil", style: "Melee", note: "Obsidian shield, durability 1600. Recipe drops from KotHaar enemies in Umbral Sands." },
  { tier: "Obsidian", slot: "Armour - Body", name: "Obsidian Chest", style: "Melee", note: "Power level 7: Def 53/47/45 (melee/ranged/magic). Full 3-piece set totals 106/94/90. Armour recipes unlock by purchasing vestiges from merchant Beartach with garou chits." },
  { tier: "Obsidian", slot: "Armour - Head", name: "Obsidian Helmet", style: "Melee", note: "Part of the Obsidian set: Def 21/19/18." },
  { tier: "Obsidian", slot: "Armour - Legs", name: "Obsidian Legs", style: "Melee", note: "Part of the Obsidian set: Def 32/28/27." },

  // ---- Dragonhide (ranged armour, leather-based) ----
  { tier: "Dragonhide", slot: "Armour - Body", name: "Blue Dragonhide Body", style: "Ranged", note: "Power level 6 ranged set: full-set Def 79 melee / 99 ranged / 79 magic. Craft: Armour Bench, 20 Blue Dragon Leather + 10 Cursed Leather + 7 Mithril Bars + 6 Demonic Oil across the set." },
  { tier: "Dragonhide", slot: "Armour - Legs", name: "Blue Dragonhide Chaps", style: "Ranged", note: "Part of the Blue Dragonhide set; Armour Bench." },
  { tier: "Dragonhide", slot: "Armour - Head", name: "Blue Dragonhide Coif", style: "Ranged", note: "Part of the Blue Dragonhide set; Armour Bench." },
  { tier: "Dragonhide", slot: "Armour - Body", name: "Green Dragonhide Body", style: "Ranged", note: "Lower-tier dragonhide set than blue; Armour Bench." },
  { tier: "Dragonhide", slot: "Armour - Body", name: "Red Dragonhide Body", style: "Ranged", note: "Higher-tier dragonhide set than blue; Armour Bench." },

  // ---- Mystic / magic armour ----
  { tier: "Mystic", slot: "Armour - Body", name: "Mystic Robes", style: "Magic", note: "Power level 6: Melee Def 38, Ranged Def 39, Magic Def 45, durability 1750. Craft: Armour Bench, Artisan 40, 12 Mystic Cloth + 4 Cursed Leather + 32 Infernal Fragments + 3 Demonic Oil. Set bonuses: stamina-regen delay, magic attack speed, magic crit chance." },
  { tier: "Mystic", slot: "Armour - Head", name: "Mystic Hat", style: "Magic", note: "Part of the Mystic Robes set; Armour Bench." },
  { tier: "Mystic", slot: "Armour - Legs", name: "Mystic Robe Legs", style: "Magic", note: "Part of the Mystic Robes set; Armour Bench." },
  { tier: "Mystic", slot: "Armour - Body", name: "Infinity Robes (Body)", style: "Magic", note: "High-tier magic robe set (Body/Hat/Legs); Mystic Forge / Armour Bench." },
  { tier: "Mystic", slot: "Armour - Body", name: "Splitbark Body", style: "Magic", note: "Power level 5 magic set alongside the Splitbark Staff; full set Def 60/64/76." },

  // ---- Kalphite (ranged, chitin-based) ----
  { tier: "Kalphite", slot: "Armour - Body", name: "Kalphite Carapace (Chest)", style: "Ranged", note: "Power level 7 ranged set, full-set Def 94 melee / 101 ranged / 94 magic. Craft: Armour Bench, 31 Kalphite Shells + 14 Scorch Leather + 6 Gypsum Wax + 12 Garou Weave across the set." },
  { tier: "Kalphite", slot: "Armour - Head", name: "Kalphite Carapace (Helmet)", style: "Ranged", note: "Part of the Kalphite Carapace set; Armour Bench." },
  { tier: "Kalphite", slot: "Armour - Legs", name: "Kalphite Carapace (Legs)", style: "Ranged", note: "Part of the Kalphite Carapace set; Armour Bench." },

  // ---- Trinkets: rings & amulets (Jeweler's Bench) ----
  { tier: "Trinket", slot: "Amulet", name: "Amulet of Magic", style: "Magic", note: "Grants +12.5% magic damage. Craft: Jeweler's Bench." },
  { tier: "Trinket", slot: "Amulet", name: "Amulet of Strength", style: "Melee", note: "Grants +12.5% melee damage with one- and two-handed weapons. Craft: Jeweler's Bench." },
  { tier: "Trinket", slot: "Amulet", name: "Amulet of Defence", style: "Melee", note: "Grants +5 armour value per piece (head/torso/legs) across all three damage types. Craft: Jeweler's Bench." },
  { tier: "Trinket", slot: "Amulet", name: "Amulet of Accuracy", style: "Melee", note: "Accuracy-boosting amulet. Craft: Jeweler's Bench." },
  { tier: "Trinket", slot: "Amulet", name: "Inspiring Amulet of Attack", style: "Melee", note: "Attack-boosting amulet variant. Craft: Jeweler's Bench." },
  { tier: "Trinket", slot: "Amulet", name: "Inspiring Amulet of Ranged", style: "Ranged", note: "Ranged-boosting amulet variant. Craft: Jeweler's Bench." },
  { tier: "Trinket", slot: "Ring", name: "Ring of Life", style: "Any", note: "Automatically teleports the wearer to their bed or bedroll on dropping to 10% health. Craft: Jeweler's Bench." },
  { tier: "Trinket", slot: "Ring", name: "Ring of Pursuit", style: "Any", note: "Reduces animals' awareness of the wearer's presence by 80%. Craft: Jeweler's Bench." },

  // ---- Notable named / quest / unique weapons ----
  { tier: "Unique", slot: "Weapon", name: "Staff of Light", style: "Magic", note: "Named magic staff; Mystic Forge." },
  { tier: "Unique", slot: "Weapon", name: "Master's Staff", style: "Magic", note: "High-tier named magic staff; Mystic Forge." },
  { tier: "Unique", slot: "Weapon", name: "Grieving Moonstaff", style: "Magic", note: "Named magic staff; Mystic Forge." },
  { tier: "Unique", slot: "Weapon", name: "Pharaoh's Sceptre", style: "Magic", note: "Named sceptre-type magic weapon." },
  { tier: "Unique", slot: "Weapon", name: "Bow of Elidinis", style: "Ranged", note: "Named unique bow; Fletching Bench materials plus a quest/vestige recipe unlock (pattern shared by other named weapons)." },
  { tier: "Unique", slot: "Weapon", name: "Ulv's Longbow", style: "Ranged", note: "Named unique longbow." },
  { tier: "Unique", slot: "Weapon", name: "Adventurer's Longbow", style: "Ranged", note: "Named unique longbow." },
  { tier: "Unique", slot: "Weapon", name: "Abyssal Whip", style: "Melee", note: "Named unique one-handed melee weapon, listed on the wiki's weapon category page." },
  { tier: "Unique", slot: "Off-hand", name: "Anti-Dragon Shield", style: "Melee", note: "Named unique shield, listed on the wiki's weapon category page." }
];
