/* Per-skill level unlocks: the spells, passives and recipes each of the 12
   trainable skills grants as you level it, straight from each skill's own
   "Levelling" table on the wiki (dragonwilds.runescape.wiki/w/<Skill>). Every
   entry below was read directly off that table - nothing here is guessed or
   interpolated between known levels. An entry with level "All" is a
   per-level scaling passive (e.g. "-0.5% stamina drain per level") rather
   than something that unlocks once.

   Two structural notes from the wiki itself:
   - "type" is left null where the wiki's own Type column was blank for that
     row (a handful of Artisan rows). That's a gap in the wiki, not this file.
   - Resource/tool tiers (which ore a pickaxe can mine, which fish a rod can
     catch, which pickaxe/axe "power level" you have) are gated by the TOOL's
     tier, not by a Mining/Woodcutting/Fishing skill level - the wiki is
     explicit that it doesn't list per-fish or per-ore level gates, so those
     are intentionally not represented here as skill-level unlocks.

   Skill max level is 99. Coverage is uneven because the source material is:
   most skills have a full table through level 99; Ranged and Fishing are
   comparatively newer/thinner skills in-game and their tables are shorter
   because that's genuinely all that's documented, not because entries were
   cut. */

window.WILDS_LEVEL_UNLOCKS = {
  "Attack": [
    { level: "All", name: "Reduced Melee Stamina Drain", type: "Passive", note: "Reduces the stamina cost of melee weapons by 0.5% per level, up to 49% at level 99." },
    { level: 5, name: "Parry", type: "Passive", note: "Block attacks at the last moment to stagger enemies and deal increased damage." },
    { level: 8, name: "Melee Weapon Special Actions", type: "Passive", note: "Unlocks unique special actions for melee weapons." },
    { level: 11, name: "Tempest Shield", type: "Spell", note: "Conjure a shield of air magic that prevents all damage while blocking, then bursts when the spell ends." },
    { level: 13, name: "Sprint Attacks", type: "Passive", note: "Unlocks a unique sprint attack after sprinting for a short distance." },
    { level: 16, name: "Weapon Expertise", type: "Passive", note: "Unlocks additional attacks for all melee weapons." },
    { level: 20, name: "Enchant Weapon: Fire", type: "Spell", note: "Enchant your melee weapon with fire; critical hits apply Burning." },
    { level: 23, name: "Adaptability", type: "Passive", note: "Evading or blocking no longer interrupts melee combos." },
    { level: 27, name: "Weapon Rack", type: "Recipe", note: "Build a weapon rack to display your weapons." },
    { level: 30, name: "Enchant Weapon: Air", type: "Spell", note: "Enchant your melee weapon with air; increases attack speed." },
    { level: 34, name: "Lesser Attack Potion", type: "Recipe", note: "Craft the Lesser Attack Potion at the brewing cauldron." },
    { level: 37, name: "Training Dummy", type: "Recipe", note: "Build a training dummy to test melee weapons on." },
    { level: 40, name: "Whetstone", type: "Recipe", note: "Craft whetstones at the crafting table to sharpen melee weapons for increased damage." },
    { level: 50, name: "Enchant Weapon: Water", type: "Spell", note: "Enchant your melee weapon with water; deals water damage and occasionally creates healing orbs." },
    { level: 65, name: "Tempest Shield Upgrade", type: "Passive", note: "Tempest Shield lasts longer." },
    { level: 99, name: "Attack Skillcape", type: "Recipe", note: "Craft and wear the Attack skillcape and its trimmed variant." }
  ],

  "Magic": [
    { level: "All", name: "Reduced Magic Stamina", type: "Passive", note: "Reduces the stamina cost of magic by 0.5% per level." },
    { level: 1, name: "Air Magic", type: "Passive", note: "Equip air runes for high single-target damage that knocks enemies down." },
    { level: 5, name: "Secondary Attacks", type: "Passive", note: "Charge up and release powerful secondary staff spells." },
    { level: 7, name: "Water Magic", type: "Passive", note: "Equip water runes to damage/slow enemies while healing yourself and allies; kills can spawn water orbs." },
    { level: 11, name: "Surge", type: "Spell", note: "Channel arcane power into your dodges, travelling further and evading longer." },
    { level: 16, name: "Arcane Expertise", type: "Passive", note: "Unlocks an additional powerful magical attack at the end of staff combos." },
    { level: 20, name: "Runic Refund", type: "Passive", note: "30% chance to preserve runes when attacking with magic." },
    { level: 21, name: "Fire Magic", type: "Passive", note: "Equip fire runes to damage enemies in a large area and build up Burning." },
    { level: 25, name: "Afterimage", type: "Passive", note: "Leaves behind an illusionary image for a short time when using your first Surge charge." },
    { level: 30, name: "Confuse", type: "Spell", note: "Makes lesser enemies unable to distinguish friend from foe for a limited time." },
    { level: 34, name: "Magic Potion", type: "Recipe", note: "Unlocks the recipe for the (Lesser) Magic Potion at the brewing cauldron." },
    { level: 39, name: "Magic Focus", type: "Recipe", note: "Craft Magic Focus at the crafting table to imbue a staff with bonus damage." },
    { level: 44, name: "Greater Confuse", type: "Passive", note: "Confuse now works on a wider variety of creatures." },
    { level: 61, name: "Enfeeble", type: "Spell", note: "Weakens the attacks of the targeted opponent." },
    { level: 80, name: "Vengeance", type: "Spell", note: "Reflects incoming damage back at enemies." },
    { level: 99, name: "Magic Skillcape", type: "Unlock", note: "Craft and wear the Magic skillcape and its trimmed variant." }
  ],

  "Ranged": [
    { level: "All", name: "Ammo Recovery Chance", type: "Passive", note: "Increases the chance to recover ammo (bolts/arrows) per level." },
    { level: 3, name: "Quick Action", type: "Passive", note: "Perform Quick Actions with ranged weapons using the Primary Action button." },
    { level: 5, name: "Archery Target", type: "Recipe", note: "Build an archery target to practice Ranged accuracy against." },
    { level: 8, name: "Trick Shot", type: "Passive", note: "Fire a follow-up shot at exactly the right time after a fully drawn arrow for 15% increased damage." },
    { level: 12, name: "Snare", type: "Spell", note: "Lay an earth-magic trap that roots enemies caught inside it for a short time." },
    { level: 15, name: "Toxic Behaviour", type: "Recipe", note: "Unlocks weapon poison, used to imbue melee weapons with Poison or craft Poisonous arrows." },
    { level: 18, name: "Hunter's Sense", type: "Passive", note: "Crouch briefly to sense nearby creatures and enemies." },
    { level: 22, name: "Make 'Em Bleed", type: "Recipe", note: "Unlocks weapon barbs, used to imbue melee weapons with Bleed or craft Barbed arrows." },
    { level: 25, name: "Spectral Arrows", type: "Spell", note: "Enchant your bow with astral magic so arrows penetrate multiple targets." },
    { level: 30, name: "Crossbow Trick Shot", type: "Passive", note: "Trick Shot now applies to crossbows: fire at the right time to instantly finish reloading." },
    { level: 35, name: "Enchanted Crossbow Bolts", type: "Recipe", note: "Craft Enchanted Crossbow Bolts, which have a chance to trigger unique magical effects." },
    { level: 40, name: "Venomous Trapper", type: "Passive/Spell", note: "The Snare trap now also triggers a poison cloud on activation." },
    { level: 45, name: "Fire Starter", type: "Recipe", note: "Unlocks fire oil and fire arrow recipes." },
    { level: 60, name: "Lucky Bolts", type: "Passive", note: "Increases the chance for enchanted crossbow bolts to trigger their magical effects." },
    { level: 99, name: "Ranged Skillcape", type: "Recipe", note: "Craft and wear the Ranged skillcape and its trimmed variant." }
  ],

  "Mining": [
    { level: "All", name: "Increased Mining Critical Chance", type: "Passive", note: "Increases mining critical hit chance by 0.5% per level." },
    { level: 5, name: "Lift With Your Hips", type: "Passive", note: "Reduces the weight of stone, clay and sand by 25%." },
    { level: 11, name: "Rocksplosion", type: "Spell", note: "Conjure a blast that breaks apart stone boulders and ore in a 5m radius." },
    { level: 16, name: "Gem Prospector", type: "Passive", note: "Mining ore now sometimes produces gemstones from the previous tier." },
    { level: 20, name: "Mine Crumbled Walls", type: "Passive", note: "Knock down crumbled walls with a pickaxe to access hidden or blocked areas." },
    { level: 24, name: "Summon Stone Spirits", type: "Spell", note: "Call a spirit that guides you to the nearest mineable clay or ore node, up to 200m away." },
    { level: 36, name: "Not-So-Heavy Metal", type: "Passive", note: "Reduces the weight of metal ores by 25%." },
    { level: 62, name: "Ore & Stone Storage", type: "Recipe", note: "Unlocks the ore & stone storage building piece." },
    { level: 69, name: "Ultimate Burst", type: "Passive", note: "Increases Rocksplosion's area of effect." },
    { level: 71, name: "Ingot Weight Reduction", type: "Passive", note: "Reduces the weight of bars by 50%." },
    { level: 80, name: "Divine Rock", type: "Spell", note: "Turn 5 dropped ore into a personal floating mining vein." },
    { level: 90, name: "Accelerated Veins", type: "Passive", note: "Divine Rock now has a chance to drop gemstones." },
    { level: 99, name: "Mining Cape", type: "Recipe", note: "Craft and wear the Mining skillcape." }
  ],

  "Woodcutting": [
    { level: 4, name: "Overhead Chop", type: "Ability", note: "Deals greater damage against fallen logs, but very little against standing trees." },
    { level: 11, name: "Axtral Projection", type: "Spell", note: "Launch an astral axe forward, instantly chopping down trees in its path. Upgrades at level 88." },
    { level: 16, name: "Bird Nest", type: "Passive", note: "Chance to find bird nests (containing useful items) while felling trees." },
    { level: 20, name: "Chop Thorny Vines", type: "Passive", note: "Cut down thorny vines with a hatchet to access hidden or blocked areas." },
    { level: 27, name: "Splinter", type: "Spell", note: "Chops fallen trees into logs; can be cast on multiple logs to maximise logs per cast." },
    { level: 40, name: "Lumber Storage", type: "Recipe", note: "Build lumber storage, a high-capacity store for logs and planks." },
    { level: 52, name: "Trunk Totem", type: "Spell", note: "Transmutes fallen trees into a wooden totem for easier chopping." },
    { level: 67, name: "Wood Weight Reduction", type: "Passive", note: "Reduces the carry weight of wood by 50%." },
    { level: 78, name: "Lumber Backpack", type: "Recipe", note: "Craft the lumber backpack: +10% Woodcutting XP, +10% wood from chopping, +15% special drop chance, -10% wood weight." },
    { level: 88, name: "Axtral Projection Upgrade", type: "Passive", note: "Axtral Projection now fires 3 spectral axes for a bigger area of effect." },
    { level: 99, name: "Woodcutting Cape", type: "Passive", note: "Craft and wear the Woodcutting skillcape and its trimmed variant." }
  ],

  "Artisan": [
    { level: "All", name: "Reduced Durability Loss on Equipment", type: "Passive", note: "Reduces durability loss on equipment by 0.5% per level, up to 49% at level 99." },
    { level: 11, name: "Bark To Bones", type: "Spell", note: "Transmute a tree into a stack of bones." },
    { level: 20, name: "Superheat", type: null, note: "Cast on fire-based processing stations to empower them, boosting processing speed for a while. (Wiki left the Type column blank for this row.)" },
    { level: 28, name: "Storage Ledger", type: "Item", note: "Unlocks the Storage Ledger building piece." },
    { level: 40, name: "Decorated Adventurer", type: "Recipe", note: "Unlocks the armour mannequin and cape rack, for displaying armour sets and capes." },
    { level: 48, name: "Overdrive", type: "Spell", note: "Cast on mechanical processing stations to empower them, boosting processing speed for a while." },
    { level: 56, name: "Magical Mending", type: null, note: "Throw items down to repair them instantly through nature magic. (Wiki left the Type column blank for this row.)" },
    { level: 66, name: "Superheat Upgrade", type: "Passive", note: "Superheat's speed boost lasts even longer." },
    { level: 80, name: "Overdrive Upgrade", type: null, note: "Upgrades Overdrive. (Wiki left the Type column and description blank for this row.)" },
    { level: 90, name: "Magical Mending Upgrade", type: null, note: "Restores even more durability when using Magical Mending. (Wiki left the Type column blank for this row.)" },
    { level: 99, name: "Artisan Skillcape", type: "Recipe", note: "Craft and wear the Artisan skillcape." }
  ],

  "Construction": [
    { level: 3, name: "Middle Ground", type: "Recipe", note: "Unlocks medium-sized building pieces." },
    { level: 5, name: "Fine Details", type: "Recipe", note: "Unlocks small building pieces." },
    { level: 8, name: "Sacred Geometry", type: "Recipe", note: "Unlocks triangular building pieces." },
    { level: 11, name: "Eye of Oculus", type: "Spell", note: "Become the Eye of Oculus for an easier build perspective." },
    { level: 16, name: "Creature Comforts", type: "Recipe", note: "Unlocks an assortment of furniture and decorations." },
    { level: 18, name: "Mighty Oak", type: "Recipe", note: "Unlocks the next (Oak) tier of building pieces." },
    { level: 20, name: "Summon Shelter", type: "Spell", note: "Conjure a temporary shelter (with a bed) through astral magic." },
    { level: 22, name: "Countryside", type: "Recipe", note: "Unlocks Thatched Roofs." },
    { level: 30, name: "Bastion", type: "Recipe", note: "Unlocks additional stone building pieces." },
    { level: 35, name: "Baroque Stone", type: "Recipe", note: "Unlocks additional stone building pieces." },
    { level: 40, name: "Personal Chest", type: "Spell", note: "Access your personal storage chest from anywhere." },
    { level: 45, name: "Desert Dweller", type: "Recipe", note: "Unlocks additional Kharidian building pieces." },
    { level: 99, name: "Construction cape", type: "Recipe", note: "Craft and wear the Construction skillcape." }
  ],

  "Cooking": [
    { level: "All", name: "Culinary Confidence", type: "Passive", note: "Reduces the chance to burn ingredients." },
    { level: 1, name: "Culinary Confidence: Power Level 1", type: "Passive", note: "Reduces the chance to burn power level 1 ingredients by 50%." },
    { level: 11, name: "Fancy Cookware", type: "Recipe", note: "Unlocks the pan rack furniture piece in the building menu." },
    { level: 12, name: "Culinary Confidence: Power Level 2", type: "Passive", note: "Reduces the chance to burn power level 2 ingredients by 50%." },
    { level: 14, name: "Teamonger", type: "Recipe", note: "Unlocks a collection of perk-granting recipes at the Stone Range and Cooking Range." },
    { level: 16, name: "Amateur Culinaromancer", type: "Recipe", note: "Unlocks a collection of perk-granting recipes at the Stone Range and Cooking Range." },
    { level: 20, name: "Internal Alchemy", type: "Spell", note: "Refreshes any active food and drink buffs." },
    { level: 26, name: "Grill Master", type: "Recipe", note: "Unlocks the Grill station." },
    { level: 27, name: "Culinary Confidence: Power Level 3", type: "Passive", note: "Reduces the chance to burn power level 3 ingredients by 50%." },
    { level: 28, name: "Bones to Peaches", type: "Spell", note: "Transmute bones on the ground into fresh peaches." },
    { level: 36, name: "Adept Culinaromancer", type: "Recipe", note: "Unlocks a collection of perk-granting recipes at the Stone Range and Cooking Range." },
    { level: 40, name: "Yes, Chef!", type: "Recipe", note: "Unlocks the recipe for the chef's hat, craftable at the crafting station." },
    { level: 41, name: "Culinary Confidence: Power Level 4", type: "Passive", note: "Reduces the chance to burn power level 4 ingredients by 50%." },
    { level: 50, name: "Culinary Confidence: Power Level 5", type: "Passive", note: "Reduces the chance to burn power level 5 ingredients by 50%." },
    { level: 75, name: "Culinary Confidence: Power Level 6", type: "Passive", note: "Reduces the chance to burn power level 6 ingredients by 50%." },
    { level: 99, name: "Cooking Skillcape", type: "Recipe", note: "Craft and wear the Cooking skillcape; also prevents burning food of any power level while worn." }
  ],

  "Runecrafting": [
    { level: "All", name: "Attunement Phase Duration", type: "Passive", note: "Increases the Attunement phase duration by 0.6% per level, up to 58.8% at level 99." },
    { level: 1, name: "Air Rune", type: "Recipe", note: "Craft Air runes at the rune altar." },
    { level: 3, name: "Astral Rune", type: "Recipe", note: "Craft Astral runes at the rune altar." },
    { level: 11, name: "Water Rune", type: "Recipe", note: "Craft Water runes at the rune altar." },
    { level: 15, name: "Earth Rune", type: "Recipe", note: "Craft Earth runes at the rune altar." },
    { level: 17, name: "Lesser Infusion Duration", type: "Passive", note: "Reduces the Infusion phase duration." },
    { level: 19, name: "Summon Elemental Spirits", type: "Spell", note: "Call wisps that guide you to nearby anima vents you can siphon." },
    { level: 22, name: "Air Efficiency", type: "Passive", note: "Better yield when auto-crafting Air runes." },
    { level: 25, name: "Fire Rune", type: "Recipe", note: "Craft Fire runes at the rune altar." },
    { level: 27, name: "Runes To Rune Essence", type: "Spell", note: "Convert runes on the ground back into 40% of their rune essence." },
    { level: 30, name: "Astral Efficiency", type: "Passive", note: "Better yield when auto-crafting Astral runes." },
    { level: 34, name: "Pure Essence", type: "Passive", note: "Chance for a Pure Essence Stone to appear while siphoning an anima vent." },
    { level: 38, name: "Nature Rune", type: "Recipe", note: "Craft Nature runes at the rune altar." },
    { level: 42, name: "Fire Spirit", type: "Spell", note: "Conjure a fire spirit to light your way." },
    { level: 46, name: "Lesser Anima Siphoning", type: "Passive", note: "Each anima vent siphon consumes 1 rune essence to produce 12 runes." },
    { level: 48, name: "Better Infusion Duration", type: "Passive", note: "Further reduces the Infusion phase duration." },
    { level: 50, name: "Law Rune", type: "Recipe", note: "Craft Law runes at the rune altar." },
    { level: 53, name: "Essential Strength", type: "Passive", note: "Reduces the weight of rune essence by 50%." },
    { level: 58, name: "Water Efficiency", type: "Passive", note: "Better yield when auto-crafting Water runes." },
    { level: 64, name: "Greater Elemental Spirits", type: "Spell", note: "Summon Elemental Spirits now also indicates which anima vents are Concentrated." },
    { level: 68, name: "Earth Efficiency", type: "Passive", note: "Better yield when auto-crafting Earth runes." },
    { level: 71, name: "Greater Anima Siphoning", type: "Passive", note: "Each anima vent siphon consumes 1 rune essence to produce 15 runes." },
    { level: 75, name: "Fire Efficiency", type: "Passive", note: "Better yield when auto-crafting Fire runes." },
    { level: 78, name: "Greater Infusion Duration", type: "Passive", note: "Reduces the Infusion phase duration to its minimum." },
    { level: 81, name: "Runes To Rune Essence Upgrade", type: "Spell", note: "Runes To Rune Essence now returns 60% of the rune essence." },
    { level: 87, name: "Nature Efficiency", type: "Passive", note: "Better yield when auto-crafting Nature runes." },
    { level: 94, name: "Law Efficiency", type: "Passive", note: "Better yield when auto-crafting Law runes." },
    { level: 99, name: "Runecrafting Skillcape", type: "Recipe", note: "Craft and wear the Runecrafting skillcape." }
  ],

  "Farming": [
    { level: "All", name: "Seed Gathering", type: "Passive", note: "Increases the chance to gather seeds from all plants by 0.3% per level, up to 29.4% at level 99." },
    { level: 3, name: "Plant Cure", type: "Recipe", note: "Craft plant cures at the cooking range to heal diseased plants." },
    { level: 6, name: "Rain Catcher", type: "Recipe", note: "Passively collects and filters rainwater into clean water over time." },
    { level: 10, name: "Compost Bin / Compost Bucket", type: "Recipe", note: "Craft compost (and super compost later) to boost yield and disease resistance of plots." },
    { level: 15, name: "Uproot", type: "Spell", note: "Instantly harvest all fully grown crops and wild plants within a small radius." },
    { level: 20, name: "Tree Farming", type: "Passive", note: "Unlocks planting trees directly into the ground; tree seeds can be found chopping trees or from bird nests." },
    { level: 24, name: "Water Barrel", type: "Recipe", note: "Stores dirty or clean water collected from watering cans for later use." },
    { level: 28, name: "Humidify", type: "Spell", note: "Conjure a rain cloud that waters any farming plot it passes over with clean water." },
    { level: 32, name: "Well", type: "Recipe", note: "Build a well that passively collects a limited amount of clean water each day." },
    { level: 36, name: "Harvester", type: "Passive", note: "Expands Uproot's range to a wider radius." },
    { level: 39, name: "Speedy Farmer", type: "Passive", note: "Reduces the movement speed penalty while watering and composting." },
    { level: 42, name: "Iron Secateurs", type: "Recipe", note: "Craft secateurs that boost harvesting yield while equipped." },
    { level: 46, name: "Large Water Barrel", type: "Recipe", note: "Stores even more dirty or clean water than the Water Barrel." },
    { level: 50, name: "Cleansing Rain", type: "Passive", note: "Upgrades Humidify so its rain cloud also cures diseased plants it passes over." },
    { level: 55, name: "Scarecrow", type: "Recipe", note: "Protects crops from birds." },
    { level: 60, name: "Super Compost Bin", type: "Recipe", note: "Produces super compost for an even better yield/disease-resistance boost." },
    { level: 74, name: "Rapid Growth", type: "Spell", note: "Advances a plant's growth by one stage; cannot be reapplied until it grows further." },
    { level: 80, name: "Mucksplosion", type: "Spell", note: "Summons a compost volcano that fertilizes plots in the area." },
    { level: 90, name: "Overgrowth Aura", type: "Passive", note: "Increases the range of the Rapid Growth spell." },
    { level: 99, name: "Farming Skillcape", type: "Recipe", note: "Craft and wear the Farming skillcape." }
  ],

  "Fishing": [
    { level: "All", name: "Increased Fish Stamina Drain Rate", type: "Passive", note: "Increases the stamina drain rate of hooked fish by 1% per level." },
    { level: 3, name: "Fishing Rod", type: "Passive", note: "Unlocks the ability to craft fishing rods." },
    { level: 10, name: "Fishing Frenzy", type: "Spell", note: "Enchant a fishing node so each successful catch yields an extra fish of the same type while it lasts." },
    { level: 17, name: "Pristine Fish", type: "Passive", note: "Unlocks the chance to catch rare Pristine fish (more food when cooked, or usable as a decoration)." },
    { level: 23, name: "Fish Weight Reduction", type: "Passive", note: "Reduces the carry weight of all fish by 25%." },
    { level: 30, name: "Infernal Rod", type: "Spell", note: "Enchant your equipped rod with fire for 2 minutes; fish caught during the effect are instantly cooked." },
    { level: 34, name: "Fish Barrel Storage", type: "Passive", note: "Unlocks the fishing barrel, a high-capacity storage structure for fish." },
    { level: 39, name: "Tackle box", type: "Passive", note: "Unlocks the recipe to build a storage box for bait." },
    { level: 43, name: "Troubled Waters", type: "Passive", note: "Fishing Frenzy now also reduces the hooked fish's maximum stamina by 15% while active." },
    { level: 49, name: "Increase Net Fishing Catch Chance", type: "Passive", note: "Increases the net fishing catch chance to 75%." },
    { level: 55, name: "Fishnado", type: "Spell", note: "Conjure a tornado that pulls up to 5 fish out of a fishing node at once." },
    { level: 60, name: "Greater Fishnado", type: "Passive", note: "Reduces the cooldown of the Fishnado spell." },
    { level: 70, name: "Experienced Angler", type: "Passive", note: "Unlocks the fishing hat recipe; grants a 10% chance per catch to not deplete the fishing spot." },
    { level: 99, name: "Fishing Skillcape", type: "Passive", note: "Craft and wear the Fishing skillcape and its trimmed variant." }
  ],

  "Agility": [
    { level: "All", name: "Sprinting Stamina Reduction", type: "Passive", note: "Reduces the stamina drain of sprinting by 0.085% per level, up to 8.415% at level 99." },
    { level: 1, name: "Brynmoor Courses", type: "Unlock", note: "Unlocks Agility courses in Brynmoor (e.g. Chasm Dash), the lowest-level course region." },
    { level: 5, name: "Windstep", type: "Spell", note: "A movement spell (reclassified from Runecrafting to Agility)." },
    { level: 10, name: "Double Jump", type: "Ability", note: "Perform a second jump mid-air; can be chained into an Air Dash." },
    { level: 15, name: "Ghornfell Courses", type: "Unlock", note: "Unlocks Agility courses in Ghornfell." },
    { level: 22, name: "Hopper", type: "Passive", note: "Reduces the stamina cost of jumping." },
    { level: 27, name: "Common Burrower", type: "Shortcut", note: "Unlocks use of the Brynmoor and Ghornfell kebbit-burrow shortcut networks." },
    { level: 30, name: "Fellhollow Courses", type: "Unlock", note: "Unlocks Agility courses in Fellhollow." },
    { level: 32, name: "Air Dash", type: "Ability", note: "A short horizontal aerial dash to cross gaps or evade attacks in combat." },
    { level: 35, name: "Breakfall", type: "Passive", note: "Automatically rolls out of high falls to reduce landing damage." },
    { level: 40, name: "Wind Stomp", type: "Ability", note: "Landing from Windstep now staggers nearby enemies." },
    { level: 42, name: "Wild Burrower", type: "Shortcut", note: "Unlocks the Fellhollow burrow network, with reduced chance and amount of damage taken." },
    { level: 44, name: "Phase Dash", type: "Spell", note: "Allows a second dash while airborne." },
    { level: 48, name: "Nomad", type: "Passive", note: "Increases passive exploration XP from 50 to 200." },
    { level: 50, name: "Backpacker", type: "Passive", note: "Increases maximum carry weight by 75." },
    { level: 51, name: "Dowdun Reach Courses", type: "Unlock", note: "Unlocks Agility courses in Dowdun Reach." },
    { level: 53, name: "Stamina Potion", type: "Recipe", note: "Craft stamina potions that stop stamina drain while running." },
    { level: 54, name: "Greater Breakfall", type: "Passive", note: "Further reduces fall damage." },
    { level: 55, name: "Dark Burrower", type: "Shortcut", note: "Unlocks the Dowdun Reach burrow network." },
    { level: 57, name: "Recall", type: "Spell", note: "Leaves a runic marker; recasting teleports you back to it. A fatal fall while tethered teleports you back safely instead, consuming the tether." },
    { level: 65, name: "Umbral Sands Courses", type: "Unlock", note: "Unlocks Agility courses in Umbral Sands." },
    { level: 67, name: "Desert Burrower", type: "Shortcut", note: "Unlocks the Umbral Sands burrow network." },
    { level: 70, name: "Reactive Recall", type: "Spell", note: "Recall now triggers automatically on fatal fall damage, protecting the caster." },
    { level: 75, name: "Explorer", type: "Passive", note: "Increases maximum carry weight by a further 75." },
    { level: 80, name: "Razor-backed Burrower", type: "Shortcut", note: "Further reduces the chance and amount of damage taken while using kebbit burrows." },
    { level: 85, name: "Trailblazer", type: "Passive", note: "Increases passive exploration XP from 200 to 400." },
    { level: 99, name: "Agility Skillcape", type: "Recipe", note: "Craft and wear the Agility skillcape and its trimmed variant." }
  ]
};
