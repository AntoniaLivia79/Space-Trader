import random
import time
from math import floor

goods_list = [
    "Plasma", "Ore", "Dust", "Nanites",
    "Particles", "Batteries", "Arrays",
    "Cores", "Coils", "Crystals",
    "Neutrinos", "Fuel", "Cells", "Particles",
    "Circuits", "Antimatter", "Alloy",
    "Tritium", "Hyperfiber",
    "Cryo Gel", "Conduits", "ExoFood",
    "Seeds", "Stabilizers",
    "Fabrics", "Silk", "Vaccines"
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
    "Ravager", "Scorn", "Phantom", "Viper",
    "Claw", "Razor", "Wraith", "Dread", "Inferno",
    "Havok", "Shadow", "Ironfang", "Skull",
    "Venom", "Storm", "Hawk", "Blade",
    "Shade", "Thorn", "Kane", "Blood",
    "Talon", "Hex", "Darkstar"
]
trader_names = [
    "Zara", "Maxwell", "Luna", "Darius",
    "Seraphina", "Jericho", "Thalia", "Cassius",
    "Vesper", "Solomon", "Lyra", "Drexel",
    "Astrid", "Rigel", "Celeste", "Tiberius"
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
    print(title)
    for i, opt in enumerate(options, 1):
        print(str(i) + ". " + opt)
    return input("Choose (1-" + str(len(options)) + "): ")

def cap(s): return s[0].upper() + s[1:].lower() if s else ""

def casino():
    p = game["player"]
    print("===== Quantum Casino =====")
    print("Play Asteroid game.")
    print("Choose path (1-3)")
    while True:
        print("Your cr: " + str(p["credits"]))
        bet_str = input("Place bet (0 exits): ")
        try:
            bet = int(bet_str)
        except ValueError:
            print("Invalid bet.")
            continue
        if bet <= 0:
            break
        if bet > p["credits"]:
            print("Not enough credits!")
            continue
        print("Choose path:")
        print("1. Alpha Route")
        print("2. Beta Route")
        print("3. Gamma Route")
        path = input("Select path (1-3): ")
        if path not in ["1", "2", "3"]:
            print("Choose 1, 2, or 3.")
            continue
        safe_path = str(random.randint(1, 3))
        print("Navigating asteroids.")
        if path == safe_path:
            winnings = bet * 2
            p["credits"] += bet
            print("Found a safe path.")
            print("Won " + str(bet) + " cr !")
            print("Winnings: " + str(winnings) + " cr")
        else:
            p["credits"] -= bet
            print("Ship hit an asteroid!")
            print("Safe route was: " + ["Alpha", "Beta", "Gamma"][int(safe_path) - 1])
            print("Lost " + str(bet) + " cr.")
        if p["credits"] <= 0:
            print("Lost all your cr!")
            break
        again = input("Again? 1.Yes 2.No: ")
        if again != "1":
            break
    input("Press Enter to exit.")

def manage_ship_stat(stat, increase=False):
    p = game["player"]
    if increase:
        p[stat] += 1
        return cap(stat) + " inc to " + str(p[stat])
    p[stat] = max(0, p[stat] - 1)
    if stat == "engine" and p[stat] == 0:
        print("No engines, you're adrift.")
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
            print("Jettisoned " + good)
    return cap(stat) + " reduced to " + str(p[stat])

def trade(is_buy=True):
    p, e = game["player"], game["exchange"]
    if e["traders"] <= 0 and p["location"] == "exchange":
        print("No traders")
        input("Press Enter...")
        return
    e["traders"] -= 1
    if is_buy:
        good = random.choice(goods_list)
        price = random.randint(20, 300)
        action, verb = "Buy", "selling"
    else:
        if not p["goods"]:
            print("No goods to sell")
            input("Press Enter...")
            return
        good = random.choice(list(p["goods"].keys()))
        price = random.randint(50, 200)
        action, verb = "Sell", "buying"
    trader = random.choice(trader_names)
    print(trader + " is " + verb + ":")
    print(good + " for " + str(price) + " cr")
    print(action + " " + good + "?")
    if input("1.Yes 2.No: ") != "1":
        input("Press Enter...")
        return
    if is_buy:
        if p["credits"] < price:
            print("Not enough cr")
            input("Press Enter...")
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
            print("for " + profit_text + " of " + str(abs(trade_profit)) + " cr")
        else:
            p["credits"] += price
            p["goods"][good] -= 1
            if p["goods"][good] == 0:
                del p["goods"][good]
            print("Sold " + good)
    if p["location"] == "exchange":
        if p["credits"] < 5:
            print("Can't pay tax. Impounded.")
            game["running"] = False
            return
        p["credits"] -= 5
        print("Trade tax of 5 cr")
    input("Press Enter...")

def interactive_boon_encounter(planet):
    """Enhanced boon encounter with scenarios and choices"""
    p = game["player"]
    scenarios = [
        {
            "desc": "Find ruins with artifact.",
            "choices": ["Touch it", "Scan it", "Leave it"],
            "outcomes": [
                {"stat": "weapons", "amount": 2, "text": "Surge upgrades weapons!"},
                {"stat": "engine", "amount": 1, "text": "Scan improves nav!"},
                {"credits": 200, "text": "Found 200 cr."}
            ]
        },
        {
            "desc": "Stranded miners trade.",
            "choices": ["Help them", "Negotiate", "Demand payment"],
            "outcomes": [
                {"stat": "shields", "amount": 1, "text": "They upgrade shields!"},
                {"good": True, "text": "Received goods!"},
                {"credits": 150, "text": "They pay 150 cr."}
            ]
        },
        {
            "desc": "Energy storm.",
            "choices": ["Fly through", "Take shelter", "Study it"],
            "outcomes": [
                {"stat": "engine", "amount": 2, "text": "Storm charged engines!"},
                {"stat": "hold", "amount": 1, "text": "Storage upgrades!"},
                {"credits": 100, "stat": "weapons", "amount": 1, "text": "Yields upgrades!"}
            ]
        }
    ]
    scenario = random.choice(scenarios)
    print("===" + planet + "===")
    choice = menu(scenario["desc"], scenario["choices"])
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(scenario["choices"]):
            outcome = scenario["outcomes"][choice_index]
        else:
            outcome = scenario["outcomes"][0]
    except (ValueError, IndexError):
        outcome = scenario["outcomes"][0]
    print(outcome['text'])
    if "stat" in outcome:
        for _ in range(outcome["amount"]):
            print(manage_ship_stat(outcome["stat"], True))
    if "credits" in outcome:
        p["credits"] += outcome["credits"]
    if "good" in outcome:
        good = random.choice(goods_list)
        p["goods"][good] = p["goods"].get(good, 0) + 1
        print("Added " + good)

def handle_encounter(type_):
    p = game["player"]
    if type_ == "empty":
        print(" *  *       *    *")
        time.sleep(0.4)
        print("      *  *    *   ")
        time.sleep(0.4)
        print("     *       **   ")
        time.sleep(0.4)
        time.sleep(0.2)
        print("Nothing in sector.")
        return
    if type_ == "trader":
        print("Met trader!")
        trade(True)
        return
    if type_ == "planet":
        planet = random.choice(planet_names)
        print("Landed on " + planet)
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
        input("Press Enter...")
        if multi_round_combat(pirate, pirate_type):
            min_reward, max_reward = pirate_type["reward"]
            bounty_reward = random.randint(min_reward, max_reward)
            p["bounty_points"] += bounty_reward
            p["total_bounty_earned"] += bounty_reward
            print("You won!")
            print("Bounty: " + str(bounty_reward))
            print("Total bounty: " + str(p["bounty_points"]))
            return
        if p["shields"] > random.randint(0, 2):
            print("Escaped with damage!")
        else:
            print("Pirates stole goods")
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
            input("Press Enter...")
    if game["running"]:
        print("Docking...")
        p["location"] = "exchange"
        if p["credits"] < 20:
            print("Can't pay fees. Impounded.")
            game["running"] = False
            return
        game["exchange"]["traders"] = random.randint(6, 10)
        p["credits"] -= 20
        print("Docked. Paid 20 cr")
        p["age"] += 1
        if p["age"] >= 60:
            game["running"] = False
    input("Press Enter...")

def view_trade_stats():
    p = game["player"]
    print("Statistics:")
    print("Total Pr/Lss: " + str(p["total_profit"]) + " cr")
    if p["trades_completed"] > 0:
        avg_profit = p["total_profit"] / p["trades_completed"]
        print("Avg profit: " + str(floor(floor(avg_profit * 10) / 10)) + " cr")
    if p["goods"]:
        input("Press Enter...")
        print("Inv Value:")
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
        print("Est inv value: " + str(floor(total_inventory_value)) + " cr")

def view_bounty_stats():
    p = game["player"]
    print("Bounty Stats:")
    print("Points: " + str(p["bounty_points"]))
    print("Points Earned: " + str(p["total_bounty_earned"]))
    print("Redeemed: " + str(p["bounty_redeemed"]))
    credits_earned = p["bounty_redeemed"] * 100
    print("Cr Earned: " + str(credits_earned) + " cr")

def multi_round_combat(pirate, pirate_type):
    p = game["player"]
    rounds = 3
    for round_num in range(1, rounds + 1):
        print("Turn " + str(round_num) + " - ")
        print(pirate_type["name"] + " " + pirate + " attacks!")
        player_attack = p["weapons"] + random.randint(0, 2)
        pirate_defense = pirate_type["difficulty"] + random.randint(0, 2)
        if player_attack > pirate_defense:
            print("Hit pirate!")
        else:
            print("Pirate dodged!")
        pirate_attack = pirate_type["difficulty"] + random.randint(0, 2)
        player_defense = p["shields"] + random.randint(0, 2)
        if pirate_attack > player_defense:
            print("Your ship is hit!")
            stat = random.choice(["shields", "hold", "engine"])
            print(manage_ship_stat(stat))
            if p["shields"] <= 0:
                print("Your shields are down!")
        else:
            print("Blocked attack!")
        if p["shields"] <= 0 or p["engine"] <= 0:
            print("You're' defeated!")
            return False
        input("Press Enter...")
    print("You survived!")
    return True

def registry_menu():
    """Handle the registry submenu for renaming ship and captain"""
    p = game["player"]
    choice = menu("Ship Registry", ["Rename Ship", "Rename Captain", "Back to Computer"])
    if choice == "1":
        p["ship_name"] = input("New ship name: ")
        print("Renamed to " + p["ship_name"])
    elif choice == "2":
        p["captain_name"] = input("New captain name: ")
        print("Renamed to " + p["captain_name"])
    elif choice == "3":
        return

def computer():
    p = game["player"]
    choice = menu("Ship Computer", ["Ship Status", "Trade Stat", "Bounty Stat", "Registry", "Exit Game"])
    if choice == "1":
        print("Ship: " + p["ship_name"])
        print("Cap: " + p["captain_name"])
        print("Age: " + str(p["age"]) + ", Cr: " + str(p["credits"]))
        print("EN: " + str(p["engine"]) + ", HO: " + str(p["hold"]))
        print("SH: " + str(p["shields"]) + ", WP: " + str(p["weapons"]))
        if p["goods"]:
            input("Press Enter...")
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
        registry_menu()
    elif choice == "5":
        print("Exiting game...")
        game["running"] = False
        return
    input("Press Enter...")

def bounty_office():
    p = game["player"]
    print("Bounty Office")

    print("Redeem bounty points")
    print("Bounty points: " + str(p["bounty_points"]))
    if p["bounty_points"] == 0:
        print("No points to redeem.")
        input("Press Enter...")
        return
    exchange_rate = 100
    total_value = p["bounty_points"] * exchange_rate
    choice = input("Redeem ? (1.Yes 2.No): ")
    if choice == "1":
        p["credits"] += total_value
        p["bounty_redeemed"] += p["bounty_points"]
        print(str(p["bounty_points"]) + " for " + str(total_value) + " cr!")
        p["bounty_points"] = 0
    else:
        print("Points not redeemed.")
    input("Press Enter...")

def trade_menu():
    """Handle the trade submenu for buying and selling goods"""
    choice = menu("Trade Menu", ["Buy Goods", "Sell Goods", "Back to Exchange"])
    if choice == "1":
        trade(True)  # Buy goods
    elif choice == "2":
        trade(False)  # Sell goods
    elif choice == "3":
        return  # Go back to main exchange menu

def services_menu():
    """Handle the services submenu for casino and bounty office"""
    choice = menu("Station Services", ["Casino", "Bounty Office", "Back to Exchange"])
    if choice == "1":
        casino()
    elif choice == "2":
        bounty_office()
    elif choice == "3":
        return  # Go back to main exchange menu

def exchange():
    p = game["player"]
    p["location"] = "exchange"
    choice = menu("Celastra Exchange", 
                 ["Trade", "Upgrade Ship", "Ship Computer", 
                  "Services", "Launch Ship"])
    if choice == "1":
        trade_menu()
    elif choice == "2":
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
            input("Press Enter...")
    elif choice == "3":
        computer()
    elif choice == "4":
        services_menu()
    elif choice == "5":
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

while game["running"]:
    exchange()
p = game["player"]
score_data = calculate_final_score()
print("Final Score: " + str(score_data["enhanced_score"]))
print("Trader Rank:")
print(score_data["rank"])