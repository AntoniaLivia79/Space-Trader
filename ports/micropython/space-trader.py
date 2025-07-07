import random
from math import floor

goods_list = [
    "Stellar Plasma", "Neutronium Ore", "Quantum Dust", "Medical Nanites",
    "Gravitic Particles", "Tachyon Batteries", "Deflector Arrays",
    "Quantum Cores", "Nebula Dust", "Solar Crystals",
    "Dark Matter", "Ion Fuel", "Warp Cells", "Gravitic Particles",
    "Nanite Circuits", "Antimatter Pods", "Star Alloy",
    "Tritium Ore", "Hyperfiber Cloths", "Photon Shields",
    "Cryo Gel", "Plasma Conduits", "ExoFood Rations",
    "Terraforming Seeds", "Gravity Stabilizers", "Void Crystals",
    "Dimensional Fabrics", "Cosmic Silk", "Terraforming Bacteria"
]
planet_names = [
    "Zanxor", "Novus", "Kalrix", "Velor", "Gorath",
    "Zethar", "Avolon", "Krylith", "Dranak", "Phyros",
    "Vespera", "Xenthos", "Lyrin", "Gryphonis", "Vortalis",
    "Thalara", "Nexaris", "Orinth", "Kovarion", "Lysara",
    "Valaxar", "Epsilon-7", "Tarvos", "Veridian",
    "Zenithia", "Novaris", "Helios"
]
pirate_names = [
    "Rex", "Sly", "Fang", "Blaze", "Havok",
    "Ravager", "Scorn", "Widowmaker", "Phantom", "Viper",
    "Blackclaw", "Razor", "Wraith", "Dread", "Inferno",
    "Havok", "Shadowstrike", "Ironfang", "Skullbane",
    "Venom", "Firestorm", "Bloodhawk", "Fangblade",
    "Nightshade", "Thornheart", "Kane", "Bloodfang",
    "Talon", "Hex", "Starkiller", "Deathwing", "Darkstar"
]
trader_names = [
    "Zara Vex", "Maxwell Orion", "Luna Stardust", "Darius Nova",
    "Seraphina Flux", "Jericho Steel", "Thalia Warp", "Cassius Corda",
    "Vesper Gray", "Solomon Quasar", "Lyra Comet", "Drexel Atlas",
    "Astrid Moonglow", "Rigel Amberwing", "Celeste Horizon", "Tiberius Void"
]
game = {
    "player": {
        "age": 30, "credits": 1000, "engine": 1, "hold": 5,
        "shields": 1, "weapons": 1, "goods": {},
        "ship_name": "Intrepid", "captain_name": "Reynolds",
        "location": "exchange",
        "purchase_records": {}, 
        "total_profit": 0,      
        "trades_completed": 0,
        "bounty_points": 0,           
        "total_bounty_earned": 0,
        "bounty_redeemed": 0
    },
    "exchange": {"traders": random.randint(6, 10)},
    "running": True
}

def menu(title, options):
    print("\n" + title)
    for i, opt in enumerate(options, 1):
        print(str(i) + ". " + opt)
    return input("Choose (1-" + str(len(options)) + "): ")

def cap(s): return s[0].upper() + s[1:].lower() if s else ""

def casino():
    p = game["player"]
    print("\n===== Quantum Casino =====")
    print("Test your luck")
    print("with our Asteroid game.")
    print("Choose a navigation path (1-3)")
    print("and bet credits.")
    print("Choosing the safe path, doubles your bet!")
    input("\nPress EXE to continue...")
    while True:
        print("\nYour credits: " + str(p["credits"]))
        bet_str = input("Place your bet (0 to exit): ")
        try:
            bet = int(bet_str)
        except ValueError:
            print("Invalid bet. Please enter a number.")
            continue
        if bet <= 0:
            break
        if bet > p["credits"]:
            print("You don't have enough credits!")
            continue
        print("\nChoose your navigation path:")
        print("1. Alpha Route")
        print("2. Beta Route")
        print("3. Gamma Route")
        path = input("Select path (1-3): ")
        if path not in ["1", "2", "3"]:
            print("Invalid selection. Please choose 1, 2, or 3.")
            continue
        safe_path = str(random.randint(1, 3))
        print("\nNavigating asteroid field...")
        if path == safe_path:
            winnings = bet * 2
            p["credits"] += bet
            print("\nYou found a safe path.")
            print("You won " + str(bet) + " cr !")
            print("Total winnings: " + str(winnings) + " cr")
        else:
            p["credits"] -= bet
            print("\nYour ship hit an asteroid!")
            print("The safe route was: " + ["Alpha", "Beta", "Gamma"][int(safe_path) - 1] + " Route")
            print("You lost " + str(bet) + " credits.")
        if p["credits"] <= 0:
            print("\nYou've lost all your credits!")
            break
        again = input("\nPlay again? 1. Yes 2. No: ")
        if again != "1":
            break
    input("\nPress EXE to return to the Exchange...")

def manage_ship_stat(stat, increase=False):
    p = game["player"]
    if increase:
        p[stat] += 1
        return cap(stat) + " increased to " + str(p[stat])
    p[stat] = max(0, p[stat] - 1)
    if stat == "engine" and p[stat] == 0:
        print("With no engines, you drift in space.")
        print("Game over!")
        game["running"] = False
    elif stat == "hold":
        total = sum(p["goods"].values())
        while total > p["hold"] and p["goods"]:
            good = random.choice(list(p["goods"].keys()))
            p["goods"][good] -= 1
            if good in p["purchase_records"] and p["purchase_records"][good]:
                purchase_id = list(p["purchase_records"][good].keys())[0]
                purchase_price = p["purchase_records"][good][purchase_id]
                p["total_profit"] -= purchase_price
                del p["purchase_records"][good][purchase_id]
                if not p["purchase_records"][good]:
                    del p["purchase_records"][good]
            if p["goods"][good] == 0:
                del p["goods"][good]
            total -= 1
            print("Jettisoned " + good + " due to hold damage")
    return cap(stat) + " reduced to " + str(p[stat])

def trade(is_buy=True):
    p, e = game["player"], game["exchange"]
    if e["traders"] <= 0 and p["location"] == "exchange":
        print("\nNo traders available")
        input("\nPress EXE to continue...")
        return
    e["traders"] -= 1
    if is_buy:
        good = random.choice(goods_list)
        price = random.randint(20, 300)
        action, verb = "Buy", "selling"
    else:
        if not p["goods"]:
            print("\nNo goods to sell")
            input("\nPress EXE to continue...")
            return
        good = random.choice(list(p["goods"].keys()))
        price = random.randint(50, 200)
        action, verb = "Sell", "buying"
    trader = random.choice(trader_names)
    print("\n" + trader + " is " + verb + ":")
    print(good + " for " + str(price) + " cr")
    print(action + " " + good + "?")
    if input("1. Yes 2. No: ") != "1":
        input("\nPress EXE to continue...")
        return
    if is_buy:
        if p["credits"] < price:
            print("Not enough credits")
            input("\nPress EXE to continue...")
            return
        p["credits"] -= price
        p["goods"][good] = p["goods"].get(good, 0) + 1
        if good not in p["purchase_records"]:
            p["purchase_records"][good] = {}
        purchase_id = good + "_" + str(len(p["purchase_records"][good]) + 1)
        p["purchase_records"][good][purchase_id] = price
        print("Bought " + good)
    else:
        if good in p["purchase_records"] and p["purchase_records"][good]:
            purchase_ids = list(p["purchase_records"][good].keys())
            oldest_purchase_id = purchase_ids[0]
            purchase_price = p["purchase_records"][good][oldest_purchase_id]
            trade_profit = price - purchase_price
            p["total_profit"] += trade_profit
            p["trades_completed"] += 1
            p["credits"] += price
            del p["purchase_records"][good][oldest_purchase_id]
            if not p["purchase_records"][good]:
                del p["purchase_records"][good]
            p["goods"][good] -= 1
            if p["goods"][good] == 0:
                del p["goods"][good]
            profit_text = "profit" if trade_profit >= 0 else "loss"
            print("Sold " + good)
            print("for a " + profit_text + " of " + str(abs(trade_profit)) + " cr")
        else:
            p["credits"] += price
            p["goods"][good] -= 1
            if p["goods"][good] == 0:
                del p["goods"][good]
            print("Sold " + good)
    if p["location"] == "exchange":
        if p["credits"] < 5:
            print("\nCan't pay trade tax. Ship impounded.")
            game["running"] = False
            return
        p["credits"] -= 5
        print("Trade tax of 5 cr paid")
    input("\nPress EXE to continue...")

def interactive_boon_encounter(planet):
    """Enhanced boon encounter with scenarios and choices"""
    p = game["player"]
    scenarios = [
        {
            "desc": "You discover ruins with an artifact.",
            "choices": ["Touch it", "Scan it", "Leave it"],
            "outcomes": [
                {"stat": "weapons", "amount": 2, "text": "Energy surge upgrades weapons!"},
                {"stat": "engine", "amount": 1, "text": "Scan data improves navigation!"},
                {"credits": 200, "text": "Found 200 credits nearby."}
            ]
        },
        {
            "desc": "Stranded miners offer to trade.",
            "choices": ["Help them", "Negotiate", "Demand payment"],
            "outcomes": [
                {"stat": "shields", "amount": 1, "text": "Miners upgrade your shields!"},
                {"good": True, "text": "Received goods from miners!"},
                {"credits": 150, "text": "Miners pay 150 credits."}
            ]
        },
        {
            "desc": "Energy storm approaches your ship.",
            "choices": ["Fly through", "Take shelter", "Study it"],
            "outcomes": [
                {"stat": "engine", "amount": 2, "text": "Storm charged your engines!"},
                {"stat": "hold", "amount": 1, "text": "Storage upgrades in shelter!"},
                {"credits": 100, "stat": "weapons", "amount": 1, "text": "Analysis yields upgrades!"}
            ]
        }
    ]
    scenario = random.choice(scenarios)
    print("\n===" + planet + "===")
    choice = menu(scenario["desc"], scenario["choices"])
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(scenario["choices"]):
            outcome = scenario["outcomes"][choice_index]
        else:
            outcome = scenario["outcomes"][0]
    except (ValueError, IndexError):
        outcome = scenario["outcomes"][0]
    print("\n" + outcome['text'])
    if "stat" in outcome:
        for _ in range(outcome["amount"]):
            print(manage_ship_stat(outcome["stat"], True))
    if "credits" in outcome:
        p["credits"] += outcome["credits"]
    if "good" in outcome:
        good = random.choice(goods_list)
        p["goods"][good] = p["goods"].get(good, 0) + 1
        print("Added " + good + " to cargo!")

def handle_encounter(type_):
    p = game["player"]
    if type_ == "empty":
        print("\nNothing in this sector...")
        return
    if type_ == "trader":
        print("\nMet a trader!")
        trade(True)
        return
    if type_ == "planet":
        planet = random.choice(planet_names)
        print("\nLanded on " + planet)
        outcome = random.choice(["boon", "fight", "trade"])
        if outcome == "boon":
            interactive_boon_encounter(planet)
        elif outcome == "fight":
            handle_encounter("pirate")
        else:
            handle_encounter("trader")
        return
    if type_ == "pirate":
        pirate_types = [
            {"name": "Smuggler", "difficulty": 1, "reward": (1, 2)},
            {"name": "Raider", "difficulty": 2, "reward": (2, 4)},
            {"name": "Warlord", "difficulty": 3, "reward": (3, 6)}
        ]
        player_strength = p["weapons"] + p["shields"]
        if player_strength >= 5:
            pirate_type = pirate_types[2]  # Warlord
        elif player_strength >= 3:
            pirate_type = pirate_types[1]  # Raider
        else:
            pirate_type = pirate_types[0]  # Smuggler
        pirate = random.choice(pirate_names)
        print("\n" + pirate_type["name"] + " " + pirate + " attacks!")
        if multi_round_combat(pirate, pirate_type):
            min_reward, max_reward = pirate_type["reward"]
            bounty_reward = random.randint(min_reward, max_reward)
            p["bounty_points"] += bounty_reward
            p["total_bounty_earned"] += bounty_reward
            print("You won the battle!")
            print("Bounty awarded: " + str(bounty_reward) + " points")
            print("Total bounty points: " + str(p["bounty_points"]))
            return
        if p["shields"] > random.randint(0, 2):
            print("You escaped with damage!")
        else:
            print("Lost! Pirates stole your goods")
            for good, quantity in p["goods"].items():
                if good in p["purchase_records"]:
                    for purchase_id, price in p["purchase_records"][good].items():
                        p["total_profit"] -= price
            p["goods"].clear()
            p["purchase_records"].clear()

        stat = random.choice(["engine", "hold", "shields", "weapons"])
        print(manage_ship_stat(stat))

def explore():
    global game_running
    p = game["player"]
    p["location"] = "space"
    for _ in range(p["engine"]):
        if not game["running"]:
            return
        handle_encounter(random.choice(["pirate", "trader", "planet", "empty"]))
        if game["running"]:
            input("\nPress EXE to continue exploring...")
    if game["running"]:
        print("\nDocking at Exchange...")
        p["location"] = "exchange"
        if p["credits"] < 20:
            print("Can't pay docking fees. Ship impounded.")
            game["running"] = False
            return
        game["exchange"]["traders"] = random.randint(6, 10)
        p["credits"] -= 20
        print("Docked. Paid 20 cr fee")
        p["age"] += 1
        if p["age"] >= 60:
            game["running"] = False
    input("\nPress EXE to continue...")

def view_trade_stats():
    p = game["player"]
    print("\nTrading Statistics:")
    print("Total Profit/Loss: " + str(p["total_profit"]) + " cr")
    print("Trades Completed: " + str(p["trades_completed"]))
    if p["trades_completed"] > 0:
        avg_profit = p["total_profit"] / p["trades_completed"]
        print("Average Profit per Trade: " + str(floor(floor(avg_profit * 10) / 10)) + " cr")
    if p["goods"]:
        print("\nCurrent Inventory Values:")
        total_inventory_value = 0
        for good, quantity in p["goods"].items():
            if good in p["purchase_records"]:
                purchase_prices = [price for _, price in p["purchase_records"][good].items()]
                if purchase_prices:
                    avg_price = sum(purchase_prices) / len(purchase_prices)
                    total_value = avg_price * quantity
                    total_inventory_value += total_value
                    print(good + " x" + str(quantity))
                    print("(avg " + str(floor(avg_price)) + " cr each)")
            else:
                print(good + " x" + str(quantity) + " (unknown cost)")
        print("Estimated inventory value: " + str(floor(total_inventory_value)) + " cr")

def computer():
    p = game["player"]
    choice = menu("Ship Computer", ["Ship Status", "Trading Stats", "Bounty Stats", "Rename Ship", "Rename Captain", "Exit Game"])
    if choice == "1":
        print("\nShip: " + p["ship_name"] + ", Captain: " + p["captain_name"])
        print("Age: " + str(p["age"]) + ", Credits: " + str(p["credits"]))
        print("Engine: " + str(p["engine"]) + ", Hold: " + str(p["hold"]))
        print("Shields: " + str(p["shields"]) + ", Weapons: " + str(p["weapons"]))
        if p["goods"]:
            goods_list = []
            for k, v in p["goods"].items():
                goods_list.append(k + " x" + str(v))
            print("Goods: ")
            for goods in goods_list:
                print(goods)
        else:
            print("Goods: None")
    elif choice == "2":
        view_trade_stats()
    elif choice == "3":
        view_bounty_stats()
    elif choice == "4":
        p["ship_name"] = input("\nNew ship name: ")
        print("Ship renamed to " + p["ship_name"])
    elif choice == "5":
        p["captain_name"] = input("\nNew captain name: ")
        print("Captain renamed to " + p["captain_name"])
    elif choice == "6":
        print("\nExiting game...")
        game["running"] = False
        return
    input("\nPress EXE to continue...")

def bounty_office():
    p = game["player"]
    print("\n===== Galactic Bounty Office =====")
    print("Welcome to the Bounty Office!")
    print("Here you can redeem bounty points")
    print("for credits.")
    print("Current bounty points: " + str(p["bounty_points"]))
    if p["bounty_points"] == 0:
        print("No bounty points to redeem.")
        input("\nPress EXE to continue...")
        return
    exchange_rate = 100
    total_value = p["bounty_points"] * exchange_rate
    choice = input("Redeem bounty points ? (1. Yes 2. No): ")
    if choice == "1":
        p["credits"] += total_value
        p["bounty_redeemed"] += p["bounty_points"]
        print("Redeemed " + str(p["bounty_points"]) + " points for " + str(total_value) + " cr!")
        p["bounty_points"] = 0
    else:
        print("Bounty points not redeemed.")
    input("\nPress EXE to continue...")

def exchange():
    p = game["player"]
    p["location"] = "exchange"
    print("\nCaptain: " + p["captain_name"])
    print("Starship: " + p["ship_name"])
    print("Age: " + str(p["age"]) + ", Credits: " + str(p["credits"]))
    choice = menu("===== Celastra Exchange ======", 
                 ["Buy Goods", "Sell Goods", "Upgrade Ship", "Ship Computer", 
                  "Casino", "Bounty Office", "Launch Ship"])
    if choice == "1":
        trade(True)
    elif choice == "2":
        trade(False)
    elif choice == "3":
        upgrades = {"1": ("engine", 500), "2": ("hold", 300),
                    "3": ("shields", 400), "4": ("weapons", 400)}
        opt = menu("Upgrade Ship", ["Engine", "Hold", "Shields", "Weapons"])
        if opt in upgrades:
            stat, cost = upgrades[opt]
            if p["credits"] >= cost:
                p[stat] += 1
                p["credits"] -= cost
                print("Upgraded " + cap(stat) + "!")
            else:
                print("Not enough credits")
            input("\nPress EXE to continue...")
    elif choice == "4":
        computer()
    elif choice == "5":
        casino()
    elif choice == "6":
        bounty_office()
    elif choice == "7":
        explore()

def calculate_final_score():
    p = game["player"]
    profit_modifier = max(1, p["total_profit"]) if p["total_profit"] > 0 else 1
    bounty_bonus = p["bounty_redeemed"] * 50
    enhanced_score = floor((p["age"] * p["credits"] * profit_modifier) / 10000) + bounty_bonus
    rank = "Space Rookie"
    if enhanced_score >= 5000:
        rank = "Legendary Space Captain"
    elif enhanced_score >= 3000:
        rank = "Galactic Champion"
    elif enhanced_score >= 1500:
        rank = "Interstellar Ace"
    elif enhanced_score >= 750:
        rank = "Famous Space Captain"
    elif enhanced_score >= 300:
        rank = "Space Captain"
    elif enhanced_score >= 100:
        rank = "Apprentice"
    return {
        "enhanced_score": enhanced_score,
        "rank": rank
    }

def view_bounty_stats():
    p = game["player"]
    print("\nBounty Hunter Statistics:")
    print("Current Bounty Points: " + str(p["bounty_points"]))
    print("Total Bounty Points Earned: " + str(p["total_bounty_earned"]))
    print("Bounty Points Redeemed: " + str(p["bounty_redeemed"]))
    credits_earned = p["bounty_redeemed"] * 100
    print("Credits Earned: " + str(credits_earned) + " cr")

def multi_round_combat(pirate, pirate_type):
    p = game["player"]
    rounds = 3
    for round_num in range(1, rounds + 1):
        print("\nRound " + str(round_num) + " - " + pirate_type["name"] + " " + pirate + " attacks!")
        player_attack = p["weapons"] + random.randint(0, 2)
        pirate_defense = pirate_type["difficulty"] + random.randint(0, 2)
        if player_attack > pirate_defense:
            print("You hit the pirate ship!")
        else:
            print("The pirate dodged your attack!")
        pirate_attack = pirate_type["difficulty"] + random.randint(0, 2)
        player_defense = p["shields"] + random.randint(0, 2)
        if pirate_attack > player_defense:
            print("The pirate hit your ship!")
            stat = random.choice(["shields", "hold", "engine"])
            print(manage_ship_stat(stat))
            if p["shields"] <= 0:
                print("Your shields are down!")
        else:
            print("You blocked the pirate's attack!")
        if p["shields"] <= 0 or p["engine"] <= 0:
            print("You have been defeated!")
            return False
        input("\nPress EXE to continue...")
    print("\nYou survived the battle!")
    return True

print("Welcome to Space Trader !")
while game["running"]:
    exchange()
p = game["player"]
print("\nGame over! You retired at age " + str(p["age"]))
score_data = calculate_final_score()
print("\nFinal Score: " + str(score_data["enhanced_score"]))
print("Trader Rank:")
print(score_data["rank"])