/* Quest walkthroughs. Step-by-step completion guides for all 9 primary and
   25 secondary quests, sourced from each quest's own wiki page
   (dragonwilds.runescape.wiki/w/<Quest_Name>). Requirements/rewards are
   whatever the page listed; steps are a condensed, concrete ordered list,
   not verbatim wiki prose. A `stub: true` entry means the wiki page itself
   didn't have a full walkthrough documented yet — that's a gap in the
   source, not a guess filled in here. Keys must match the quest name
   strings in quests.js exactly. */

window.WILDS_QUEST_WALKTHROUGHS = {
  "First Steps": {
    requirements: null,
    rewards: "1 Tome of Runecrafting - Vol 1",
    steps: [
      "Speak to the Wise Old Man in the Temple at Temple Woods to begin your adventure.",
      "Accept his offer of training, which sends you to Doric outside the Temple to start Getting Started.",
      "Complete Getting Started, Ratcatcher, and Rune Mysteries as directed by Doric, Vannaka, and Zanik.",
      "Travel to Bramblemead Village and find the Wise Old Man on the first floor of a ruined building at the far end of the village.",
      "Speak to him to finish the quest and learn about your next steps."
    ]
  },
  "Getting Started": {
    requirements: "Complete First Steps",
    rewards: "1 vegetable soup",
    steps: [
      "Speak to Doric outside the Temple.",
      "Travel to a pond and enter the water to collect at least 1 dirty water, then return to Doric.",
      "Gather ash logs and stones, then build a crafting table (4 ash logs).",
      "Use the crafting table to craft a stone club (6 ash logs and 8 stones).",
      "Speak to Doric again with the club to complete the quest; he sends you to Vannaka to start Ratcatcher."
    ]
  },
  "Ratcatcher": {
    requirements: "Complete Getting Started",
    rewards: "1 stone logging axe, 1 stone dagger",
    steps: [
      "Speak to Vannaka, located south of the windmill, northeast of Doric.",
      "Travel north to the windmill and kill 4 giant rats to collect 4 raw rat meat.",
      "Gather 4 ash logs and 4 stones to build a campfire.",
      "Cook the raw rat meat on the campfire to make 2 rat roasts.",
      "Bring the rat roasts to Vannaka to complete the quest; he sends you to Zanik to start Rune Mysteries."
    ]
  },
  "Rune Mysteries": {
    requirements: "Complete Ratcatcher",
    rewards: "1 stone pickaxe, 50 air runes, 50 astral runes, 1 Tome of Woodcutting - Vol 1",
    steps: [
      "Travel east from Vannaka along the road to find Zanik.",
      "Collect 50 ash logs and return them to Zanik.",
      "Receive a stone pickaxe, then mine rune essence from a geyser by striking the surrounding rocks with a ranged or magic weapon.",
      "Gather 12 stones and 4 rune essence to build a rune altar (Building menu, Crafting tab).",
      "Craft some air runes and astral runes, then return to Zanik.",
      "Speak to Zanik to complete the quest; she sends you to the Wise Old Man to begin the next primary quest."
    ]
  },
  "Dragon Slayer": {
    requirements: "Complete First Steps; iron pickaxe and iron logging axe needed for later steps",
    rewards: "Tome of Construction - Vol 1 (mid-quest); Dragon Slayer reward pack: Tome of the Dragon Slayer, noxious draconic visage, anti-dragon shield; plus a pack of 3 clay, 3 redberries, 3 harralander",
    steps: [
      "Build a shelter (foundation, 3 walls, ceiling, and a bed roll).",
      "Hunt deer for antlers to help track down the missing adventurer Cathan.",
      "Travel to the Keep of Blue Flames and fight through the goblins inside.",
      "Find Cathan's Journal at the top of the castle.",
      "Explore the Vertentis Kara dragonkin vault and speak to Spitfoot.",
      "Report back to the Wise Old Man, then travel to Ghornfell's Fractured Plains to investigate Velgar's Rise.",
      "Meet Cathan's ghost, who gives you a challenge horn recipe.",
      "Mine a dragon tooth from skull teeth in the Stormtouched Highlands using an iron pickaxe.",
      "Harvest bloodwood sap from a tree at the Bloodblight Swamp castle using an iron logging axe.",
      "Combine the dragon tooth, bloodwood sap, and 5 bronze bars to craft the challenge horn.",
      "Place the horn on the dragonkin altar at Velgar's Rise to start the fight with Velgar.",
      "Defeat Velgar across four health phases, watching for poison attacks as he moves between three corners.",
      "Retrieve Velgar's head and return it to the Wise Old Man to complete the quest."
    ]
  },
  "Withering Heights": {
    requirements: "Complete Dragon Slayer",
    rewards: "Tome of the Undying, Undead Draconic Visage, Dragoncurse Shield, access to the dragoncurse shield masterwork recipe",
    steps: [
      "Meet the Wise Old Man near Ashien's Watch and open the door marked with necromantic runes into the Forgotten Temple.",
      "Speak to Death about Imaru and the Fellhollow situation.",
      "Speak to Postie Pete about entering the region, then cross the wither water with him.",
      "Quickly find a purifying fountain after entering the soul rift state to cleanse yourself before tormented souls appear.",
      "Find Cathan on a cliff near three stone tablets.",
      "Collect the Grief fragment in Emberwood by activating the four shrine altars (Guthix, Saradomin, Armadyl, Zamorak) in any order.",
      "Collect the Rage fragment in the Lake of Lost Souls by defeating a zogre in the Vekchenven Kara vault beneath a waterfall.",
      "Collect the Despair fragment in Silverthorn Keep by fighting through zombies and skeletons and defeating a green dragon.",
      "Bring all three curse fragments to Imaru's Tower in Hope's Fall and dispel the curse seal.",
      "Defeat Imaru, who phases between soul-rift states and tries to self-heal.",
      "Take Imaru's head back to Death to complete the quest."
    ]
  },
  "Black Knight's Fortress": {
    requirements: "Complete Withering Heights; level 41 Cooking (to make maple syrup, or obtain a maple toastie from salvage); Steel/Undead Spade, Steel/Mithril Pickaxe, and Mithril Logging Axe",
    rewards: "Black Knight's Fortress reward pack: Tome of the Titan (+750 XP to Magic, Ranged, Attack) and Titan's Wrath weapon; recipe for crafting the Titan's Wrath 2h sword",
    steps: [
      "Speak to Death at the Forgotten Temple, then to Cathan near Silverthorn Keep's gatehouse.",
      "Enter the ominous door to reach the Approach and the Courtyard.",
      "Meet the Wise Old Man in the Courtyard and set up a base camp.",
      "Head to the Nexus and speak to Doric about repairing a broken stone artifact.",
      "Collect all 13 Shards of Dreaming Stone scattered across Dowdun Reach (some require combat, puzzles, digging, or NPC interactions; 3 are underground in the Crypt, Demon Gate, and Lake).",
      "Interact with the restored Dreaming Stone, revealed to be Avisk, and make the case against its enslavement.",
      "Travel to the Bastion and defeat the Black Knight Titan boss.",
      "Speak to Avisk again to complete the quest."
    ]
  },
  "Icthlarin's Little Helper": {
    requirements: "Complete Black Knight's Fortress; Mithril pickaxe or better, Adamant logging axe or better, a spade (Adamant recommended), 1 clean water, 3 adamant bars, 3 raw farm meat, 3 kalphite shell fragments, 3 cactus steaks",
    rewards: "Reward pack: anti-dragon masterwork shield crafting ability, dragonfire shield, Tome of Volcano, smouldering draconic visage; plus 3 Moon Garou packs, full access to the Fight Caves (with a chance at the fire cape), and full access to the Nightmare Crucible",
    steps: [
      "Enter the Umbral Sands through the Door to Umbral Sands.",
      "At Alcarrid Oasis: find three moonstones under gypsum nodes for Domri, deliver 3 adamant bars to Valas to repair mirrors, and bring Lagra 3 raw farm meat, 3 kalphite shell fragments, and 3 cactus steaks.",
      "At Manafem Plains: enter the Dragonkin Vault with a scarab staff to transcribe ancient garou lyrics for Laguna, find clues and defeat a red dragon for Hedric, and give clean water to Efina to break the Dearg Due's curse for Manathep.",
      "At the Dunes of Uzzer: dig up four forbidden scrolls for Lehran, collect statue inscriptions from four rocky spires and locate the Nightmare Crucible entrance for Laguna, and convince three councillors to abandon Mark Day for Shangruuh.",
      "Use the collected mirrors to direct sunlight at Fuzan's tower, opening the Fight Caves at the Burning Spire.",
      "Complete ten waves of trials in the Fight Caves and defeat Fuzan.",
      "Return Fuzan's head to Icthlarin to complete the quest."
    ]
  },
  "Regicide": {
    requirements: "Complete Icthlarin's Little Helper",
    rewards: "Regicide Reward Pack: Dragon Kiteshield, Dragonslayer's Cape, Queenslayer's Reward Pack; full access to the Scorned Wilderness raid including Kuldra's Sanctum",
    steps: [
      "Travel northwest of Velgar's Rise in the Fractured Plains to find the Dragon Gate.",
      "Interact with the gate and choose to enter the Scorned Wilderness.",
      "Speak to Commander Zilyana at Rasthin's Rest; she explains she needs help since Kuldra's presence weakens her.",
      "Build a base camp at Rasthin's Rest.",
      "Speak to Zilyana again to start the raid at Dragontail Vines.",
      "Defeat Kuldra.",
      "Return with Zilyana to Rasthin's Rest to receive your rewards and complete the quest."
    ]
  },

  "Restless Ghosts": {
    requirements: "20 Woodcutting; 5 air runes for Windstep (or means to cross a large gap); any axe, or 10 air runes + 5 astral runes for Axtral Projection",
    rewards: "Ability to speak with ghosts; Restless Ghosts reward pack (Tome of Cooking Vol 1, Tome of Woodcutting Vol 1, Tome of the Artisan Vol 1, Tome of Mining Vol 1)",
    steps: [
      "Find the crumbling well in the ruined village northwest of the Wise Old Man and interact with it to get the ghostspeak amulet.",
      "Find Warren's spirit in a dilapidated house at the southwest corner of the ruined village.",
      "Find Lazina's spirit in a broken house southeast of the windmill in Temple Woods, along the walking path.",
      "Cast Windstep and chop the thorny vines to reach Finn's spirit in a cave southeast of the Wise Old Man.",
      "Find Kay's spirit in a ruined house in Whispering Swamp along the Bramblemead Valley border.",
      "Go to the Remembrance Shrine at the southwest corner of the starting church and interact with the stone flower vase sculpture to remember all four ghosts."
    ]
  },
  "Goblin Diplomacy": {
    requirements: "Rune Mysteries completed; a logging axe and 20 Woodcutting, or one steak to bribe a caged goblin",
    rewards: "Goblin war banner",
    steps: [
      "Talk to Zanik in Bramblemead Valley; she points to Outlook Ruins (northeast) and the Adventurer's Guild (south), both overrun with goblins.",
      "Go to one location and retrieve an amulet from its reliquary (Outlook Ruins reliquary is tucked in a corner; the Adventurer's Guild reliquary needs thorny vines cut with 20 Woodcutting). Optionally bribe the caged goblin there (Bilegut at the ruins, Wormelbow at the guild) with a steak for help finding it.",
      "Go to the other location, clear the goblins, and speak to the caged goblin to learn a garou-beastman took the second amulet to a cave in the Whispering Swamp.",
      "Travel to the cave at the bottom of the swamp and defeat the garou druid (uses potent poison thorns; use ranged or magic and dodge).",
      "Return to Zanik with both amulets to finish the quest."
    ]
  },
  "Highlighting the Problem": {
    requirements: "First Steps completed",
    rewards: "Recipe for the staff of light",
    steps: [
      "Travel to the Thishepen Kara vault at the cliff base near the guild and use Windstep to reach a room with four giant rats.",
      "Find the glowing blue statue on an elevated path inside and take note of the password: pthentorok.",
      "Return to the wizard statue in the Runecrafting Guild and give it the password to receive an uncharged mysterious orb.",
      "Use Windstep to reach the three pedestals on towers surrounding the guild's main tower, using rubble and scenery to navigate, and interact with each to charge the orb.",
      "Return to the statue with the charged orb to receive the recipe for the staff of light."
    ]
  },
  "Granite Mauled": {
    requirements: "First Steps completed; one free inventory slot; 5+ air runes for Windstep, or ash logs to cross a bridge",
    rewards: "Recipe for the granite maul (66-95 damage, 4 Combo, Special: Battering Ram); imbued granite maul head (crafting also needs imbued leather wrappings and an ornate maul handle)",
    steps: [
      "Speak to Doric northeast of Fractured Plains, south of Ashien's Watch; he asks for help recovering relics from a vault he was chased away from.",
      "Activate all four statues around Ashien's Watch to open the Skeklac Kara vault.",
      "Enter the vault; bring antipoison since putrid rats and exploding poison gas bubbles are inside, and watch for blind spots where gas pools.",
      "At the lever, defeat the vault corruptor (hits hard and poisons, spawns putrid rats) — ranged or magic recommended.",
      "Interact with the final statue to get a blueprint, then return it to Doric."
    ]
  },
  "Heartstrings": {
    requirements: "Getting Started completed",
    rewards: "Crystal bow; recipe for the crystal bow (requires a free inventory slot to receive the bow)",
    steps: [
      "Go to Fractured Plains to the large tree with blue leaves atop the first dungeon, reached by casting Windstep up the rocks beside the dungeon entrance.",
      "Interact with the glowing blue memorial stone at the first tree to receive a crystal seed.",
      "Head east to find and interact with the next memorial stone, then continue finding stones 2 through 7 in order heading east, fighting wolves and garou along the way.",
      "At the seventh and final tree, sing the bard's song to complete the quest."
    ],
    stub: true
  },
  "Dog Days": {
    requirements: null,
    rewards: "Garou highborn's cloak",
    steps: [
      "Speak to Vannaka under a cliff in the eastern Stormtouched Highlands.",
      "Find the lore book beneath a wyrm corpse, approaching from the north to avoid enemies, and read it near a Garou thane.",
      "Travel to the castle in the north-west of the Highlands and defeat the Garou King (use Windstep to avoid enemies en route and to safely attack via the temple arches) to obtain the tainted token.",
      "Return the tainted token to Vannaka, then travel north to Lougrim's Shrine.",
      "Defeat the Garou druids at the shrine, then kill rams and wild lapulis vines to collect 2 ram horns and 3 shocking plant bulbs.",
      "Perform the purification ritual to receive a purified token, then return it to Vannaka to complete the quest."
    ]
  },
  "Cook's Assistant": {
    requirements: "Farming unlocked",
    rewards: "Recipe to bake the Victoria sponge cake",
    steps: [
      "Speak to Slopfinger in southwestern Fractured Plains, near Stormtouched Highlands; he asks for 4 eggs, 6 wheat, and 1 bucket of milk to bake a cake for Manktongue.",
      "Get milk from the cow in the pen outside — go through the dialogue options without choosing to milk it; it gives milk willingly.",
      "Collect eggs by killing chickens or chopping trees for bird nests.",
      "Get wheat seeds from goblins or chests and farm the wheat.",
      "Return all ingredients to Slopfinger, then speak to him again to have him bake the cake.",
      "Speak to Slopfinger again so he can show the cake to Manktongue, then talk to him one final time to complete the quest."
    ]
  },
  "Animal Magnetism": {
    requirements: null,
    rewards: "Ava's accumulator; ability to craft additional accumulators",
    steps: [
      "Speak to Manktongue in southwestern Fractured Plains; he relays a message from Ava with crafting instructions.",
      "Take an iron bar and 5 law runes to Pulpknuckle, upstairs in the same cabin, to have him craft a magnet.",
      "Find an undead chicken in Stormtouched Highlands (north of the quest area), near an iron ore node on the wall.",
      "Get undead twigs south of the Bloodblight Swamp entrance by interacting with an undead tree (an abyssal demon roams this area — be careful).",
      "Return the undead chicken, undead twigs, and magnet to Manktongue, who creates the device for you."
    ]
  },
  "A Room With A Garou": {
    requirements: null,
    rewards: "Unlocks building decorations: Hanging Tools, Pots on a Bench, Sawhorse",
    steps: [
      "Speak to Caratacus, a blind elder garou grieving his late wife Cliodhna, in the northwestern corner of the Fractured Plains.",
      "Build a house around him using ash logs or another building material — four walls and one 45-degree roof (about 20 ash logs minimum) is the quickest way.",
      "Return and speak to Caratacus again to complete the quest."
    ]
  },
  "A Melody Remembered": {
    requirements: "An inspiring ring of Runecrafting (or craft one: 1 clay mould, 2 silver bars, 2 opals, 3 vault shards) and an Amulet of Magic (or craft one: 1 clay mould, 2 gold bars, 2 silver bars, 4 sapphires, 6 vault shards) — crafted at a Jeweler's bench (or build one: 12 oak planks, 8 ground sandstone, 2 gold bars, 2 silver bars, 1 vault core)",
    rewards: "Ravanna's ring (includes the recipe to craft more)",
    steps: [
      "Find the music box on a desk in a ruined building south of the Garou King's fortress.",
      "Interact with the music box and give it an inspiring ring of Runecrafting.",
      "Later, give it an Amulet of Magic (distinct from the inspiring amulet of Magic) to complete the quest."
    ]
  },

  "Even More Restless Ghosts": {
    requirements: "Withering Heights (partial completion, to unlock Fellhollow); Restless Ghosts must be started (not necessarily completed)",
    rewards: "Recipe for the Dorgeshuun crossbow",
    steps: [
      "Speak to Zanik in the ruins east of Cathan's location, near three standing stones in Fellhollow, to start the quest.",
      "Find the Windswept Ghost in the ruined village on the northeast outskirts of Emberwood.",
      "Gather 24 ash logs and build a house around the ghost: a square foundation, four walls, and one floor piece as the roof, then close the door.",
      "Travel to Hope's Fall, north of the dragon spire, to find the Reminiscing Ghost.",
      "Give the ghost an unfired clay decoration to settle it.",
      "Head to the area northeast of the tainted river, between the Lake of Lost Souls and Coalridge Pass, to find the Paint-Spattered Ghost.",
      "Enter the nearby cave and mine through the granite deposits covering a coal node to uncover a skeleton and its sketchbook.",
      "Return the sketchbook to the Paint-Spattered Ghost.",
      "Return to Zanik in Bleakfields Valley to complete the quest."
    ]
  },
  "The Wild Hunt": {
    requirements: "Withering Heights (partial completion, to unlock Fellhollow)",
    rewards: "Access to a terrorbird mount (summon with ALT); 50x soul fragments for extra hearts",
    steps: [
      "Speak to Vannaka, west of Cathan's location in Bleakfields Valley, to start the quest.",
      "Hunt the nature spirits, which appear as white glowing terrorbirds, in willow groves across western Fellhollow: near the druid's circle in Emberwood, in the Dragon's Run area, and in the southern Witchwillow Range.",
      "Defeat three nature spirits and collect a primordial heart from each.",
      "Return the three primordial hearts to Vannaka.",
      "Watch Vannaka perform the old garou ritual to imbue you with the spirits' essence and complete the quest."
    ]
  },
  "Seeking Salvation": {
    requirements: "Withering Heights (partial completion, to unlock Fellhollow)",
    rewards: "1 salve crystal (unlocks a permanent purchase option from Death's Exchange for 25 soul fragments each); recipe to craft a salve amulet",
    steps: [
      "Speak to Doric, found east of the Lake of Lost Souls inside a cave, to start the quest.",
      "Activate the statue outside the cave entrance.",
      "Activate the statue southwest of Doric, behind the giant pillar (bring a torch or use Fire Spirit for the dark).",
      "Activate the statue atop the pillar directly west of Doric, using Windstep or built stairs to reach it.",
      "Activate the final statue northwest of Doric, near a rotted, cracked wall, using Windstep or stairs to reach it and a pickaxe to break through.",
      "With all four statues active, enter the Skekven Kara vault with food and water.",
      "Proceed to the central staircase and climb to the second-highest level.",
      "Use Windstep to reach the opening and interact with the dragonkin statue to reveal its secrets and complete the quest."
    ]
  },
  "Things That Go Boom In The Night": {
    requirements: "Withering Heights (partial completion, to unlock Fellhollow); completion of The Wild Hunt",
    rewards: "1x spectral chinchompa cape",
    steps: [
      "Speak to Vannaka, west of Cathan's location in Bleakfields Valley, to start the quest.",
      "Hunt spectral chinchompas and collect ten spectral chinchompa skulls; attack quickly, as they vanish fast.",
      "Check known spawn spots: south of Emberwood's druid circle, the willow tree grove in Witchwillow Range, the willow grove north of Hope's Fall, west of Doric's camp near the first statue and the Lake of Lost Souls shore, the southeastern wood of Silverthorn Keep, another willow grove in Silverthorn Keep, and the eastern purification pool area of Silverthorn Keep.",
      "Once you have all ten skulls, return to Vannaka to complete the quest."
    ]
  },
  "Doric's Quest": {
    requirements: "Withering Heights (partial completion, to unlock Fellhollow); completion of Seeking Salvation",
    rewards: "1x Doric's smithing supplies; 1x Doric's superior smithing supplies; recipe to craft the zombie axe",
    steps: [
      "Speak to Doric to start the quest.",
      "Enter the Skekven Kara vault and locate a dragonkin effigy to obtain the undead ranger's bow recipe.",
      "Craft the undead ranger's bow and return it to Doric (existing copies are kept).",
      "Enter the Vekchenven Kara vault and locate a dragonkin effigy to obtain the necromancer's staff recipe.",
      "Craft the necromancer's staff and return it to Doric.",
      "Kill a Zogre for a rare drop: the shadow sword recipe. Zogres spawn in the Emberwood cave east of Silverthorn Keep and as the vault boss of Vekchenven Kara.",
      "Craft the shadow sword and return it to Doric to complete the quest."
    ]
  },
  "Letters for the Dead": {
    requirements: "Withering Heights (partial completion, to unlock Fellhollow)",
    rewards: "1x buildable postbox scenery item; access to an expanding, repeatable activity",
    steps: [
      "Speak to Postie Pete in the Forgotten Temple and choose option 2 to start the quest; he explains three letters were stolen and a suspicious figure was seen near Fellhollow's entrance.",
      "Find the animated skeleton northeast of Fellhollow's entrance and talk to it: choose option 3, then option 1 twice, to make it hand over a letter.",
      "Deliver the letter to the red deposit box northwest of Vannaka's camp, revealing a strange leaf that fades into the spirit realm.",
      "Collect a letter from the glowing wall torch southeast of Cathan's location near the standing stones.",
      "Deliver that letter to the nearby deposit box, revealing ghostly fluff that looks like unspun wool.",
      "Find the ghostly sheep, Shaun, west of that deposit box, and take the ghostly letter.",
      "Deliver the ghostly letter to the postbox in front of Imaru's Tower.",
      "Return to Postie Pete, meet Parcel Pete, and complete the quest."
    ]
  },
  "What Remains is Written": {
    requirements: "Withering Heights (partial completion) and Restless Ghosts; full necromancer gear (crown, robe top, robe bottom) and a ghostspeak amulet recommended",
    rewards: "1x Abraxus ring trinket and its recipe unlock",
    steps: [
      "Speak to Abraxus the Eternal in Coalridge Pass, wearing full necromancer gear, to start the quest.",
      "Agree to recover his ransacked library's stolen tomes from the eastern sub-regions.",
      "Collect five ancient books across Silverthorn Keep: The Pride of the Avernic (second level of the keep), The Importance of Chaos (near the ominous gateway), Aetheric Fundamentals a Primordial Primer (near the stone bridge), The Wrath of Baba Potterington (in a crumbled house near the nature grove), and Leonard the Bound (northwest of the gateway, on a pedestal).",
      "Return all five books to Abraxus.",
      "Defeat Razlem the Deranged, east of the gateway, to obtain the scroll Eventide - A New Spawn.",
      "Defeat Ulgo the zogre, in Coalridge Pass, to obtain the scroll Coclear Malificarum.",
      "Defeat Blightscale, a green dragon near the Keep's cliffs, to obtain the scroll The Binding of Ib.",
      "Return all three scrolls to Abraxus to complete the quest."
    ]
  },
  "Mirror Mirror": {
    requirements: "Withering Heights (partial completion, to unlock Fellhollow)",
    rewards: "1x Ulv's longbow and its recipe",
    steps: [
      "Speak to the mirror west of Emberwood Village to start the quest.",
      "Find a bedraggled spellbook in the destroyed windmill within Emberwood Village.",
      "Find Edna's skeleton in Dragon's Run, near a crumbling stone house by a willow grove, for instructions on crafting spectral silver thread.",
      "Gather the materials (1 silver bar, 1 fine thread, 1 sacred oil, 6 soul fragments, and dragon blood from a green dragon or dragon wolf) and craft the spectral silver thread.",
      "Deliver the spellbook and spectral silver thread to the mirror.",
      "Light memorial candles scattered across six regions: Fellhollow, Fractured Plains, Stormtouched Highlands, Bloodblight Swamp, Whispering Swamp, and Bramblemead Valley (for example, next to a small lake south-southeast of Velgar's Rise, and west of the garou encampment).",
      "Speak to the mirror again; it begins a week-long ritual but grants its reward immediately."
    ]
  },

  "Biohazard": {
    requirements: "Partial completion of Black Knight's Fortress; 10 corrupted essence samples, dragon blood, unholy water, twilight lily; recommended ranged weapon and good armor",
    rewards: "Zamorak cape recipe, 50 infernal fragments (from trading samples with Putrilius)",
    steps: [
      "Speak to Zanik beneath The Approach in Dowdun Reach to start the quest.",
      "Kill corrupted ravens scattered across the region until you have 10 corrupted essence samples.",
      "Get dragon blood by slaying any dragon or a dragon wolf in Dowdun Reach.",
      "Get a twilight lily glowing blue in front of an anima tree in The Lake.",
      "Get unholy water from behind The Cathedral, southwest of the three Zamorakian acolytes (no need to fight them).",
      "Return all items to Zanik.",
      "Travel to The Nexus, make your way to The Grand Hall, and use Windstep to climb to the roof.",
      "Confront Putrilius (a corrupted chicken) and complete the dialogue.",
      "Return to Zanik to report your findings and receive your rewards."
    ]
  },
  "Wanted!": {
    requirements: "Partial completion of Black Knight's Fortress; no required items; recommended tier-appropriate armor, weapons, and food",
    rewards: "Corroded jewellery vestige, needed to craft the unholy symbol",
    steps: [
      "Speak to Vannaka by the tent in front of The Library in Dowdun Reach to start the quest.",
      "Travel southwest to The Menagerie and defeat the Rat Master (Skrexis) and his pack of hellrats.",
      "Pick up his journal from the rock behind where he stood, to the left of the statue.",
      "Head to The Garrison's lower floors and defeat the Hound Master (Rexiton) and his entire dog pack.",
      "Pick up his journal from the table in the central kennel.",
      "Travel south to The Cathedral and descend into the crypts to fight the Summoner (Flament).",
      "Pick up his journal from the plinth at the back wall, below the demon gargoyle.",
      "Return all three journals to Vannaka to complete the quest."
    ]
  },
  "What's Theirs is Mine!": {
    requirements: "Partial completion of Black Knight's Fortress; no required items; recommended tier-appropriate armor, weapons, and food",
    rewards: "Zamorak staff recipe; optional portal reward pack (Tome of the Artisan Vol 2, Tome of Construction Vol 2, Tome of Magic Vol 2, Tome of Mining Vol 2) for activating all nodestones",
    steps: [
      "Meet Doric at The Nexus, where a red-robed mage steals his bronze dog keychain.",
      "Follow the mage's trail through the portals, activating nodestones along the way.",
      "At The Cathedral, use Windstep to reach the nodestone on the northwest wing's upper ledge and activate it, then return to Doric.",
      "At The Garrison, find the nodestone on the first floor of the turreted building and activate it, then report back.",
      "Head underground to The Demon Gate and defeat two shardbound lesser demons.",
      "Search the body of the dead Zamorak mage beyond them to retrieve a crumpled schematic.",
      "Return to Doric to report your findings and learn the Zamorak staff recipe.",
      "Optionally activate the remaining nodestones for the bonus portal reward pack."
    ]
  },
  "Contact!": {
    requirements: "Partial completion of Icthlarin's Little Helper; 1 shovel, 1 pickaxe, 4 vault shards; recommended plenty of food/drink",
    rewards: "Icthlarian fetish, a vestige used to create the pharaoh's sceptre",
    steps: [
      "Speak to the Avisk crystal in Umbral Sands to start the quest.",
      "Talk to Vault Guardian Prime in the nearby cave; he needs 3 crystal helix remains recovered.",
      "Follow the red lights through the tunnels opposite Vault Guardian Prime's chamber to the large cavern and take the guardian remains (Helix 1) on the left-hand side.",
      "Head to the kalphite eggs outside the cave; the Helix there is missing — look for footprints leading east.",
      "Speak to Zanik at the oasis camp east of the kalphites; she trades you the crystal helix (Helix 2) for your help.",
      "Find the ruined building with the buried guardian and use a shovel to excavate it.",
      "With 4 vault shards in your inventory, reactivate the buried guardian to get the Helix (Helix 3).",
      "Return all three crystal helix fragments to Vault Guardian Prime and use them to pass the barrier.",
      "Interact with the Avisk crystals and Veins of Consciousness, then speak to Zanik to finish the quest."
    ]
  },
  "Mapping The Sands I": {
    requirements: "Partial completion of Icthlarin's Little Helper",
    rewards: "Blue desert cape",
    steps: [
      "Speak to Moon Sprite Shaman Anamcara at Alcarrid Camp, next to the pond, in Umbral Sands to start the quest.",
      "Discover Moon Sprites atop tall locations around Alcarrid Camp to map the Umbral Sands.",
      "Return to Anamcara once the sprites are found to complete the quest."
    ],
    stub: true
  },
  "Mapping The Sands II": {
    requirements: "Completion of Mapping The Sands I; partial completion of Icthlarin's Little Helper",
    rewards: "Bow of Elidinis recipe unlocked",
    steps: [
      "Speak to Moon Sprite Shaman Anamcara at Alcarrid Camp, next to the pond, in Umbral Sands to start the quest.",
      "Visit the 8 Moon Sprite locations marked on the map across the Umbral Sands region.",
      "Return to Anamcara at Alcarrid Camp, next to the pond, to complete the quest."
    ]
  },
  "Brink of Extinction": {
    requirements: "Partial completion of Icthlarin's Little Helper; 3 raw beltfish, 1 cactus steak",
    rewards: "Plate of pure obsidian, unlocks the obsidian cape recipe",
    steps: [
      "Speak to KotHaar-Zi in The Burning Spire, southeast of the Sinking Pyramid on the L-shaped island in Umbral Sands, to start the quest.",
      "Gather 3 raw beltfish and 1 cactus steak and bring them back to KotHaar-Zi.",
      "Interact with all four pedestals around the Burning Spire: east of the Sunken Pyramid on a rock structure, north behind KotHaar-Zi, west of the Sunken Pyramid, and south/southwest of KotHaar-Zi.",
      "Return to KotHaar-Zi after activating all four pillars.",
      "Head to the Cave of Screams entrance in the top-left corner of The Burning Spire.",
      "Read the scroll from the dialogue and answer the KotHaar Bouncer's password riddle (\"Two triangles separated by a line?\").",
      "Enter the cave and defeat two KotHaar-Xil and one Reforged Zi.",
      "Collect the Zi core that drops after the fight and exit the cave.",
      "Speak to the bouncer again to complete the quest and receive your reward."
    ]
  }
};
