// Space Trader Game - Controller (Game Logic and Event Handling)

// Ship Manual function based on MicroPython script instructions
function shipManual() {
    setScreen(`===== Ship Manual =====<br><br>
        <strong>Space Trader: Trade goods, upgrade ship, explore space.</strong><br><br>

        <strong>Ship Systems:</strong><br>
        • Engine: Determines encounters per exploration (more encounters = more opportunities)<br>
        • Hold: Your cargo capacity (limits how many goods you can carry)<br>
        • Shields & Weapons: Battle survival against pirates<br><br>

        <strong>Game Mechanics:</strong><br>
        • Start with 1000 credits at age 30<br>
        • Game ends at age 60 (mandatory retirement)<br>
        • Age only increases when docked at Celastra Exchange<br>
        • Trade tax: 5 cr per transaction at Exchange<br>
        • Docking fee: 20 cr when returning to Exchange<br><br>

        <strong>How to Play:</strong><br>
        1. Buy and sell goods to make profit<br>
        2. Upgrade your ship systems<br>
        3. Explore space for encounters<br>
        4. Fight pirates for bounty points<br>
        5. Accumulate wealth before retirement<br><br>

        <strong>Exploration Encounters:</strong><br>
        • Pirates: Combat for bounty points<br>
        • Traders: Buy/sell without tax<br>
        • Planets: Beneficial discoveries<br>
        • Empty space: Nothing happens<br><br>

        <strong>Tips:</strong><br>
        • Keep enough credits for docking fees<br>
        • Planet traders don't charge tax<br>
        • Higher engine = more encounters<br>
        • Bounty points = 100 credits each
    `);

    setMenu([
        { text: "Back to Exchange", action: () => exchange() }
    ]);
}

// Game functions
function manageStat(stat, increase = false) {
    const p = game.player;
    if (increase) {
        p[stat] += 1;
        return `${cap(stat)} increased to ${p[stat]}`;
    }
    p[stat] = Math.max(0, p[stat] - 1);

    if (stat === "engine" && p[stat] === 0) {
        log("With no engines, you drift in space. Game over!");
        game.running = false;
        gameOver();
    } else if (stat === "hold") {
        let total = Object.values(p.goods).reduce((a, b) => a + b, 0);
        while (total > p.hold && Object.keys(p.goods).length > 0) {
            const good = randomChoice(Object.keys(p.goods));
            p.goods[good] -= 1;
            if (p.goods[good] <= 0) {
                delete p.goods[good];
            }
            total -= 1;
            log(`Jettisoned ${good} due to hold damage`);
        }
    }
    return `${cap(stat)} reduced to ${p[stat]}`;
}

function trade(isBuy = true) {
    const p = game.player;
    const e = game.exchange;

    if (e.traders <= 0 && p.location === "exchange") {
        log("No traders available");
        return;
    }

    e.traders -= 1;

    if (isBuy) {
        const good = randomChoice(goodsList);
        const price = randomInt(20, 300);
        const trader = randomChoice(traderNames);

        setScreen(`${trader} is selling:<br>${good} for ${price} cr<br><br>Buy ${good}?`);
        setMenu([
            { text: "Yes", action: () => buyGood(good, price) },
            { text: "No", action: () => exchange() }
        ]);
    } else {
        if (Object.keys(p.goods).length === 0) {
            log("No goods to sell");
            exchange();
            return;
        }

        const good = randomChoice(Object.keys(p.goods));
        const price = randomInt(50, 200);
        const trader = randomChoice(traderNames);

        setScreen(`${trader} is buying:<br>${good} for ${price} cr<br><br>Sell ${good}?`);
        setMenu([
            { text: "Yes", action: () => sellGood(good, price) },
            { text: "No", action: () => exchange() }
        ]);
    }
}

function buyGood(good, price, fromSpace = false) {
    const p = game.player;
    if (p.credits < price) {
        log("Not enough credits");
        if (fromSpace) {
            continueExploration();
        } else {
            exchange();
        }
        return;
    }

    // Check cargo hold capacity
    const currentCargo = Object.values(p.goods).reduce((a, b) => a + b, 0);
    if (currentCargo >= p.hold) {
        log("Cargo hold full!");
        if (fromSpace) {
            continueExploration();
        } else {
            exchange();
        }
        return;
    }

    p.credits -= price;
    p.goods[good] = (p.goods[good] || 0) + 1;

    if (!p.purchase_records[good]) {
        p.purchase_records[good] = {};
    }
    const purchaseId = `${good}_${Object.keys(p.purchase_records[good]).length + 1}`;
    p.purchase_records[good][purchaseId] = price;

    log(`Bought ${good}`);

    if (p.location === "exchange") {
        if (p.credits < 5) {
            log("Can't pay trade tax. Ship impounded.");
            game.running = false;
            gameOver();
            return;
        }
        p.credits -= 5;
        log("Trade tax of 5 cr paid");
    }

    updateStatus();

    if (fromSpace) {
        continueExploration();
    } else {
        exchange();
    }
}

function sellGood(good, price, fromSpace = false) {
    const p = game.player;

    if (p.purchase_records[good] && Object.keys(p.purchase_records[good]).length > 0) {
        const purchaseIds = Object.keys(p.purchase_records[good]);
        const oldestId = purchaseIds[0];
        const purchasePrice = p.purchase_records[good][oldestId];
        const profit = price - purchasePrice;

        p.total_profit += profit;
        p.trades_completed += 1;
        p.credits += price;

        delete p.purchase_records[good][oldestId];
        if (Object.keys(p.purchase_records[good]).length === 0) {
            delete p.purchase_records[good];
        }

        const profitText = profit >= 0 ? "profit" : "loss";
        log(`Sold ${good} for a ${profitText} of ${Math.abs(profit)} cr`);
    } else {
        p.credits += price;
        log(`Sold ${good}`);
    }

    p.goods[good] -= 1;
    if (p.goods[good] <= 0) {
        delete p.goods[good];
    }

    if (p.location === "exchange") {
        if (p.credits < 5) {
            log("Can't pay trade tax. Ship impounded.");
            game.running = false;
            gameOver();
            return;
        }
        p.credits -= 5;
        log("Trade tax of 5 cr paid");
    }

    updateStatus();

    if (fromSpace) {
        continueExploration();
    } else {
        exchange();
    }
}

function casino() {
    setScreen("===== Quantum Casino =====<br>Test your luck with our Asteroid game.<br>Choose a navigation path (1-3) and bet credits.<br>Choosing the safe path doubles your bet!");

    const p = game.player;
    setMenu([
        { text: `Place Bet (Credits: ${p.credits})`, action: () => placeBet() },
        { text: "Exit Casino", action: () => exchange() }
    ]);
}

function placeBet() {
    const bet = parseInt(prompt("Place your bet (0 to exit):"));
    if (!bet || bet <= 0) {
        exchange();
        return;
    }

    const p = game.player;
    if (bet > p.credits) {
        log("You don't have enough credits!");
        casino();
        return;
    }

    setScreen("Choose your navigation path:");
    setMenu([
        { text: "Alpha Route", action: () => playGame(bet, 1) },
        { text: "Beta Route", action: () => playGame(bet, 2) },
        { text: "Gamma Route", action: () => playGame(bet, 3) }
    ]);
}

function playGame(bet, path) {
    const p = game.player;
    const safePath = randomInt(1, 3);
    const routeNames = ["Alpha", "Beta", "Gamma"];

    setScreen("Navigating asteroid field...");

    if (path === safePath) {
        p.credits += bet;
        log(`You found a safe path! You won ${bet} cr! Total winnings: ${bet * 2} cr`);
    } else {
        p.credits -= bet;
        log(`Your ship hit an asteroid! The safe route was: ${routeNames[safePath - 1]} Route. You lost ${bet} credits.`);
    }

    if (p.credits <= 0) {
        log("You've lost all your credits!");
        game.running = false;
        gameOver();
        return;
    }

    updateStatus();
    setMenu([
        { text: "Play Again", action: () => casino() },
        { text: "Exit Casino", action: () => exchange() }
    ]);
}

// Enhanced exploration system
function explore() {
    const p = game.player;
    p.location = "space";
    log("Launching ship...");

    // Generate all encounters for this exploration
    game.exploration.pendingEncounters = [];
    game.exploration.currentEncounter = 0;
    game.exploration.totalEncounters = p.engine;
    game.exploration.betweenEncounters = false;

    for (let i = 0; i < p.engine; i++) {
        game.exploration.pendingEncounters.push(
            randomChoice(["pirate", "trader", "planet", "empty"])
        );
    }

    // Start first encounter
    processNextEncounter();
}

function processNextEncounter() {
    if (!game.running) return;

    const exp = game.exploration;

    if (exp.currentEncounter >= exp.totalEncounters) {
        // All encounters processed, return to exchange
        finishExploration();
        return;
    }

    const encounterType = exp.pendingEncounters[exp.currentEncounter];
    exp.currentEncounter++;

    handleEncounter(encounterType);
}

function continueExploration() {
    // Set state to show we're between encounters
    game.exploration.betweenEncounters = true;
    
    const exp = game.exploration;
    const isLastEncounter = exp.currentEncounter >= exp.totalEncounters;
    
    if (isLastEncounter) {
        // Show return message
        log("Returning to the Celastra Exchange");
        setScreen("Returning to the Celastra Exchange");
        setMenu([{ text: "Continue", action: () => proceedAfterEncounter() }]);
    } else {
        // Show travel message
        log("Travelling to next sector...");
        setScreen("Travelling to next sector...");
        setMenu([{ text: "Continue", action: () => proceedAfterEncounter() }]);
    }
}

function proceedAfterEncounter() {
    // Reset between encounters state
    game.exploration.betweenEncounters = false;
    
    const exp = game.exploration;
    
    if (exp.currentEncounter >= exp.totalEncounters) {
        // All encounters processed, return to exchange
        finishExploration();
    } else {
        // Continue to next encounter
        processNextEncounter();
    }
}

function finishExploration() {
    const p = game.player;
    log("Docking at Exchange...");
    p.location = "exchange";

    if (p.credits < 20) {
        log("Can't pay docking fees. Ship impounded.");
        game.running = false;
        gameOver();
        return;
    }

    game.exchange.traders = randomInt(6, 10);
    p.credits -= 20;
    log("Docked. Paid 20 cr fee");
    p.age += 1;

    if (p.age >= 60) {
        game.running = false;
        gameOver();
        return;
    }

    updateStatus();
    exchange();
}

function handleEncounter(type) {
    const p = game.player;

    switch(type) {
        case "empty":
            log("Nothing in this sector...");
            continueExploration();
            break;

        case "trader":
            encounterTrader();
            break;

        case "planet":
            encounterPlanet();
            break;

        case "pirate":
            const pirate = randomChoice(pirateNames);
            log(`Pirate ${pirate} attacks!`);
            if (p.weapons + p.shields > randomInt(1, 4)) {
                const bounty = randomInt(1, 3);
                p.bounty_points += bounty;
                p.total_bounty_earned += bounty;
                log(`You won the battle! Bounty awarded: ${bounty} points`);
                updateStatus();
            } else {
                log("Lost! Pirates damaged your ship");
                const stat = randomChoice(["engine", "hold", "shields", "weapons"]);
                log(manageStat(stat));
                updateStatus();
            }
            continueExploration();
            break;
    }
}

// Enhanced planet encounter system matching the original MicroPython
function encounterPlanet() {
    const planet = randomChoice(planetNames);
    log(`Landed on ${planet}`);

    // Determine encounter type: 60% chance for boon, 20% fight, 20% trade
    const roll = randomInt(1, 100);

    if (roll <= 60) {
        // Interactive boon encounter
        interactiveBoonEncounter(planet);
    } else if (roll <= 80) {
        // Fight encounter (pirate ambush on planet)
        log("Pirate ambush on the planet!");
        const pirate = randomChoice(pirateNames);
        log(`Pirate ${pirate} attacks!`);
        if (game.player.weapons + game.player.shields > randomInt(1, 4)) {
            const bounty = randomInt(1, 3);
            game.player.bounty_points += bounty;
            game.player.total_bounty_earned += bounty;
            log(`You won the battle! Bounty awarded: ${bounty} points`);
            updateStatus();
        } else {
            log("Lost! Pirates damaged your ship");
            const stat = randomChoice(["engine", "hold", "shields", "weapons"]);
            log(manageStat(stat));
            updateStatus();
        }
        continueExploration();
    } else {
        // Trade encounter on planet
        const trader = randomChoice(traderNames);
        log(`You encounter ${trader} on ${planet}!`);
        encounterTrader();
    }
}

function interactiveBoonEncounter(planet) {
    const scenario = randomChoice(planetScenarios);

    setScreen(`===${planet}===<br><br>${scenario.desc}<br><br>What do you choose?`);

    const menuOptions = scenario.choices.map((choice, index) => ({
        text: choice,
        action: () => processBoonOutcome(scenario.outcomes[index])
    }));

    setMenu(menuOptions);
}

function processBoonOutcome(outcome) {
    const p = game.player;

    log(outcome.text);

    if (outcome.stat) {
        for (let i = 0; i < outcome.amount; i++) {
            log(manageStat(outcome.stat, true));
        }
    }

    if (outcome.credits) {
        p.credits += outcome.credits;
        updateStatus();
    }

    if (outcome.good) {
        const good = randomChoice(goodsList);
        p.goods[good] = (p.goods[good] || 0) + 1;
        log(`Added ${good} to cargo!`);
    }

    updateStatus();
    continueExploration();
}

// Trader encounter in space
function encounterTrader() {
    const trader = randomChoice(traderNames);
    const good = randomChoice(goodsList);
    const price = randomInt(15, 250);

    log(`Encountered trader ${trader} in space!`);

    setScreen(`Space Trader Encounter<br><br>${trader} hails your ship:<br>"Greetings, Captain! I have ${good} for sale.<br>Price: ${price} credits"<br><br>What do you want to do?`);

    const p = game.player;
    const menuOptions = [];

    // Check if player can afford and has cargo space
    const currentCargo = Object.values(p.goods).reduce((a, b) => a + b, 0);
    const canBuy = p.credits >= price && currentCargo < p.hold;

    if (canBuy) {
        menuOptions.push({
            text: `Buy ${good} for ${price} cr`,
            action: () => buyGood(good, price, true)
        });
    } else if (p.credits < price) {
        menuOptions.push({
            text: `Buy ${good} for ${price} cr (Not enough credits)`,
            action: () => {
                log("Not enough credits for this trade");
                continueExploration();
            }
        });
    } else {
        menuOptions.push({
            text: `Buy ${good} for ${price} cr (Cargo hold full)`,
            action: () => {
                log("Cargo hold is full");
                continueExploration();
            }
        });
    }

    // Option to try to sell something if player has goods
    if (Object.keys(p.goods).length > 0) {
        menuOptions.push({
            text: "Try to sell goods to trader",
            action: () => tryToSellToTrader(trader)
        });
    }

    menuOptions.push({
        text: "Decline and continue",
        action: () => {
            log("Declined the trade offer");
            continueExploration();
        }
    });

    setMenu(menuOptions);
}

function tryToSellToTrader(traderName) {
    const p = game.player;
    const playerGoods = Object.keys(p.goods);

    if (playerGoods.length === 0) {
        log("You have no goods to sell");
        continueExploration();
        return;
    }

    // Trader might be interested in one of the player's goods
    const interestedGood = randomChoice(playerGoods);
    const offerPrice = randomInt(30, 180);

    setScreen(`${traderName} examines your cargo:<br><br>"I'm interested in your ${interestedGood}.<br>I'll pay ${offerPrice} credits for it."<br><br>Sell ${interestedGood}?`);

    setMenu([
        {
            text: `Sell ${interestedGood} for ${offerPrice} cr`,
            action: () => sellGood(interestedGood, offerPrice, true)
        },
        {
            text: "Decline and continue",
            action: () => {
                log("Declined the sale");
                continueExploration();
            }
        }
    ]);
}

// Ship Computer functions
function shipComputer() {
    setScreen("===== Ship Computer =====");
    setMenu([
        { text: "Ship Status", action: () => showShipStatus() },
        { text: "Trading Stats", action: () => viewTradeStats() },
        { text: "Bounty Stats", action: () => viewBountyStats() },
        { text: "Rename Ship", action: () => renameShip() },
        { text: "Rename Captain", action: () => renameCaptain() },
        { text: "Exit Game", action: () => gameOver() },
        { text: "Back", action: () => exchange() }
    ]);
}

function showShipStatus() {
    const p = game.player;
    let content = `Ship: ${p.ship_name}, Captain: ${p.captain_name}<br>`;
    content += `Age: ${p.age}, Credits: ${p.credits}<br>`;
    content += `Engine: ${p.engine}, Hold: ${p.hold}<br>`;
    content += `Shields: ${p.shields}, Weapons: ${p.weapons}<br>`;

    if (Object.keys(p.goods).length > 0) {
        content += "Goods:<br>";
        for (const [good, qty] of Object.entries(p.goods)) {
            content += `${good} x${qty}<br>`;
        }
    } else {
        content += "Goods: None";
    }

    setScreen(content);
    setMenu([{ text: "Back", action: () => shipComputer() }]);
}

function viewTradeStats() {
    const p = game.player;
    let content = "Trading Statistics:<br>";
    content += `Total Profit/Loss: ${p.total_profit} cr<br>`;
    content += `Trades Completed: ${p.trades_completed}<br>`;

    if (p.trades_completed > 0) {
        const avgProfit = Math.floor(p.total_profit / p.trades_completed);
        content += `Average Profit per Trade: ${avgProfit} cr<br>`;
    }

    setScreen(content);
    setMenu([{ text: "Back", action: () => shipComputer() }]);
}

function viewBountyStats() {
    const p = game.player;
    let content = "Bounty Hunter Statistics:<br>";
    content += `Current Bounty Points: ${p.bounty_points}<br>`;
    content += `Total Bounty Points Earned: ${p.total_bounty_earned}<br>`;
    content += `Bounty Points Redeemed: ${p.bounty_redeemed}<br>`;
    content += `Credits Earned: ${p.bounty_redeemed * 100} cr<br>`;

    setScreen(content);
    setMenu([{ text: "Back", action: () => shipComputer() }]);
}

function renameShip() {
    const newName = prompt("New ship name:");
    if (newName) {
        game.player.ship_name = newName;
        log(`Ship renamed to ${newName}`);
        updateStatus();
    }
    shipComputer();
}

function renameCaptain() {
    const newName = prompt("New captain name:");
    if (newName) {
        game.player.captain_name = newName;
        log(`Captain renamed to ${newName}`);
        updateStatus();
    }
    shipComputer();
}

function bountyOffice() {
    const p = game.player;
    const exchangeRate = 100;
    const totalValue = p.bounty_points * exchangeRate;

    setScreen(`===== Galactic Bounty Office =====<br>Welcome to the Bounty Office!<br>Here you can redeem bounty points for credits.<br><br>Current bounty points: ${p.bounty_points}<br>Exchange rate: ${exchangeRate} cr per point<br>Total value: ${totalValue} cr`);

    if (p.bounty_points === 0) {
        setMenu([{ text: "Back", action: () => exchange() }]);
    } else {
        setMenu([
            { text: "Redeem Points", action: () => redeemBounty() },
            { text: "Back", action: () => exchange() }
        ]);
    }
}

function redeemBounty() {
    const p = game.player;
    const exchangeRate = 100;
    const totalValue = p.bounty_points * exchangeRate;

    p.credits += totalValue;
    p.bounty_redeemed += p.bounty_points;
    log(`Redeemed ${p.bounty_points} points for ${totalValue} cr!`);
    p.bounty_points = 0;

    updateStatus();
    exchange();
}

function upgradeShip() {
    const p = game.player;
    const upgrades = {
        "engine": 500,
        "hold": 300,
        "shields": 400,
        "weapons": 400
    };

    setScreen("Ship Upgrades:");
    const menuOptions = [];

    for (const [stat, cost] of Object.entries(upgrades)) {
        const canAfford = p.credits >= cost ? "" : " (Can't afford)";
        menuOptions.push({
            text: `${cap(stat)} - ${cost} cr${canAfford}`,
            action: () => buyUpgrade(stat, cost)
        });
    }

    menuOptions.push({ text: "Back", action: () => exchange() });
    setMenu(menuOptions);
}

function buyUpgrade(stat, cost) {
    const p = game.player;
    if (p.credits >= cost) {
        p[stat] += 1;
        p.credits -= cost;
        log(`Upgraded ${cap(stat)}!`);
        updateStatus();
    } else {
        log("Not enough credits");
    }
    exchange();
}

function exchange() {
    const p = game.player;
    p.location = "exchange";

    setScreen(`===== Celastra Exchange =====<br>Captain: ${p.captain_name}<br>Starship: ${p.ship_name}<br>Age: ${p.age}, Credits: ${p.credits}`);

    setMenu([
        { text: "Buy Goods", action: () => trade(true) },
        { text: "Sell Goods", action: () => trade(false) },
        { text: "Upgrade Ship", action: () => upgradeShip() },
        { text: "Ship Computer", action: () => shipComputer() },
        { text: "Ship Manual", action: () => shipManual() },
        { text: "Casino", action: () => casino() },
        { text: "Bounty Office", action: () => bountyOffice() },
        { text: "Launch Ship", action: () => explore() }
    ]);
}

function gameOver() {
    const p = game.player;
    let profitModifier = Math.max(1, p.total_profit);
    if (p.total_profit <= 0) profitModifier = 1;

    const bountyBonus = p.bounty_redeemed * 50;
    const enhancedScore = Math.floor((p.age * p.credits * profitModifier) / 10000) + bountyBonus;

    let rank = "Space Rookie";
    if (enhancedScore >= 5000) rank = "Legendary Space Captain";
    else if (enhancedScore >= 3000) rank = "Galactic Champion";
    else if (enhancedScore >= 1500) rank = "Interstellar Ace";
    else if (enhancedScore >= 750) rank = "Famous Space Captain";
    else if (enhancedScore >= 300) rank = "Space Captain";
    else if (enhancedScore >= 100) rank = "Apprentice";

    setScreen(`Game Over!<br><br>You retired at age ${p.age}<br><br>Final Score: ${enhancedScore}<br>Trader Rank: ${rank}<br><br>Thank you for playing Space Trader!`);

    setMenu([
        { text: "New Game", action: () => location.reload() }
    ]);
}