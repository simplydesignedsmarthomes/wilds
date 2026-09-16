/* Regions of Ashenfall, roughly in the order the main quest opens them up.
   Sub-areas and features are drawn from the region's own wiki page; treat
   the "features" line as flavor/orientation, not a complete gazetteer. */

window.WILDS_REGIONS = [
  {
    name: "Brynmoor",
    order: 1,
    tier: "Bronze",
    blurb: "The most accessible region and the primary human settlement area.",
    areas: ["Temple Woods", "Bramblemead Valley", "Whispering Swamp"],
    features: "Home to the Keep of Blue Flames and the first human settlements. The Whispering Swamp is a natural buffer — muddy water that's slow and dangerous to fight in."
  },
  {
    name: "Ghornfell",
    order: 2,
    tier: "Iron / Steel",
    blurb: "Mountainous northern territory originally claimed by the garou, rich in iron.",
    areas: ["Fractured Plains", "Bloodblight Swamp", "Stormtouched Highlands"],
    features: "Bloodblight Swamp formed when the dragon general Velgar spilled his poisoned blood across fertile plains. The Stormtouched Highlands hold a perpetual magical storm full of fractured spirits."
  },
  {
    name: "Fellhollow",
    order: 3,
    tier: "Mithril",
    blurb: "Remote far-northern territory, once protected by the dragons Imaru and Xikotal, now an undead-infested wasteland.",
    areas: ["Bleakfields Valley", "Forgotten Temple", "Dragon's Run", "Emberwood", "Witchwillow Range", "Hope's Fall", "Lake of Lost Souls", "Silverthorn Keep", "Coalridge Pass"],
    features: "Currently ruled by the undead dragon Imaru. The Forgotten Temple is the way into Death's domain. Silverthorn Keep shelters the Wild Knights."
  },
  {
    name: "Dowdun Reach",
    order: 4,
    tier: "Mithril / Adamant",
    blurb: "Mountainous ground between Fellhollow and Ghornfell, fortified and controlled by the Black Knights.",
    areas: ["The Approach", "The Courtyard", "The Nexus", "The Library", "The Grand Hall", "The Garrison", "The Pastures", "The Menagerie", "The Bastion"],
    features: "Contains the main Black Knight Fortress, its research facilities, and the shattered remains of the Dreaming Stone. The region exists to seal off Fellhollow's undead threat."
  },
  {
    name: "Umbral Sands",
    order: 5,
    tier: "Adamant",
    blurb: "Far south-eastern desert, home to the Moon Garou's remnant civilization, ruled by the dragon Fuzan.",
    areas: ["Alcarrid Oasis", "Dunes of Uzzer", "Manafem Plains", "The Burning Spire"],
    features: "Holds the ruins of the Old Kingdom's cities and monuments. Fuzan's manipulation of the Lens keeps raising the temperature, and KotHaar lava creatures guard its sacred sites."
  },
  {
    name: "Scorned Wilderness",
    order: 6,
    tier: "Endgame",
    blurb: "Where the Regicide storyline plays out.",
    areas: [],
    features: ""
  }
];

/* Not a real region — a world-wide effect. The further inland you travel,
   the stronger it gets, mutating flora and fauna into elemental Amalgamated
   creatures. */
window.WILDS_ANIMA_TWIST =
  "Anima Twist grows stronger the further you travel inland, making the " +
  "geography wilder and more dangerous and creating Amalgamated creatures " +
  "with elemental properties.";
