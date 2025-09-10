// Space Trader Game - Model (Data and State)

// Game data constants
const goodsList = [
    "Stellar Plasma", "Neutronium Ore", "Quantum Dust", "Medical Nanites",
    "Gravitic Particles", "Tachyon Batteries", "Deflector Arrays",
    "Quantum Cores", "Nebula Dust", "Solar Crystals", "Dark Matter",
    "Ion Fuel", "Warp Cells", "Nanite Circuits", "Antimatter Pods",
    "Star Alloy", "Tritium Ore", "Hyperfiber Cloths", "Photon Shields",
    "Cryo Gel", "Plasma Conduits", "ExoFood Rations", "Terraforming Seeds",
    "Gravity Stabilizers", "Void Crystals", "Dimensional Fabrics",
    "Cosmic Silk", "Terraforming Bacteria"
];

const planetNames = [
    "Zanxor", "Novus", "Kalrix", "Velor", "Gorath", "Zethar", "Avolon",
    "Krylith", "Dranak", "Phyros", "Vespera", "Xenthos", "Lyrin",
    "Gryphonis", "Vortalis", "Thalara", "Nexaris", "Orinth", "Kovarion",
    "Lysara", "Valaxar", "Epsilon-7", "Tarvos", "Veridian", "Zenithia",
    "Novaris", "Helios"
];

const pirateNames = [
    "Rex", "Sly", "Fang", "Blaze", "Havok", "Ravager", "Scorn",
    "Widowmaker", "Phantom", "Viper", "Blackclaw", "Razor", "Wraith",
    "Dread", "Inferno", "Shadowstrike", "Ironfang", "Skullbane",
    "Venom", "Firestorm", "Bloodhawk", "Fangblade", "Nightshade",
    "Thornheart", "Kane", "Bloodfang", "Talon", "Hex", "Starkiller",
    "Deathwing", "Darkstar"
];

const traderNames = [
    "Zara Vex", "Maxwell Orion", "Luna Stardust", "Darius Nova",
    "Seraphina Flux", "Jericho Steel", "Thalia Warp", "Cassius Corda",
    "Vesper Gray", "Solomon Quasar", "Lyra Comet", "Drexel Atlas",
    "Astrid Moonglow", "Rigel Amberwing", "Celeste Horizon", "Tiberius Void"
];

const planetScenarios = [
    {
        desc: "You discover ruins with an artifact.",
        choices: ["Touch it", "Scan it", "Leave it"],
        outcomes: [
            {stat: "weapons", amount: 2, text: "Energy surge upgrades weapons!"},
            {stat: "engine", amount: 1, text: "Scan data improves navigation!"},
            {credits: 200, text: "Found 200 credits nearby."}
        ]
    },
    {
        desc: "Stranded miners offer to trade.",
        choices: ["Help them", "Negotiate", "Demand payment"],
        outcomes: [
            {stat: "shields", amount: 1, text: "Miners upgrade your shields!"},
            {good: true, text: "Received goods from miners!"},
            {credits: 150, text: "Miners pay 150 credits."}
        ]
    },
    {
        desc: "Energy storm approaches your ship.",
        choices: ["Fly through", "Take shelter", "Study it"],
        outcomes: [
            {stat: "engine", amount: 2, text: "Storm charged your engines!"},
            {stat: "hold", amount: 1, text: "Storage upgrades in shelter!"},
            {credits: 100, stat: "weapons", amount: 1, text: "Analysis yields upgrades!"}
        ]
    }
];

// Game state
let game = {
    player: {
        age: 30, credits: 1000, engine: 1, hold: 5,
        shields: 1, weapons: 1, goods: {},
        ship_name: "Intrepid", captain_name: "Reynolds",
        location: "exchange", purchase_records: {},
        total_profit: 0, trades_completed: 0,
        bounty_points: 0, total_bounty_earned: 0, bounty_redeemed: 0,
        pirates_defeated: 0
    },
    exchange: { traders: randomInt(6, 10) },
    running: true,
    exploration: {
        currentEncounter: 0,
        totalEncounters: 0,
        pendingEncounters: [],
        betweenEncounters: false
    }
};

// Utility functions
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomChoice(array) {
    return array[Math.floor(Math.random() * array.length)];
}

function cap(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}