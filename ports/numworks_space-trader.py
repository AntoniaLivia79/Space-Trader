import random
from math import floor

goods_list = [
    "Plasma", "Fuel", "Water", "Titanium", "Food",
    "Quantum Core", "Nebula Dust", "Solar Crystals",
    "Dark Matter", "Ion Fuel", "Warp Cells", "Xenon Gas",
    "Nanite Circuits", "Antimatter Pods", "Star Alloy",
    "Tritium Ore", "Hyperfiber Cloth", "Photon Shields",
    "Cryo Gel", "Plasma Conduit", "ExoFood Rations",
    "Terraforming Seeds", "Gravity Stabilizer"
]
planet_names = [
    "Zanxor", "Novus", "Kalrix", "Velor", "Gorath",
    "Zethar", "Avolon", "Krylith", "Dranak", "Phyros",
    "Vespera", "Xenthos", "Lyrin", "Gryphonis", "Vortalis",
    "Thalara", "Nexaris", "Orinth", "Kovarion", "Lysara",
    "Valaxar", "Epsilon-7", "Tarvos"
]
pirate_names = [
    "Rex", "Sly", "Fang", "Blaze", "Havok",
    "Ravager", "Scorn", "Widowmaker", "Phantom", "Viper",
    "Blackclaw", "Razor", "Wraith", "Dread", "Inferno",
    "Havok", "Shadowstrike", "Ironfang", "Skullbane",
    "Venom", "Firestorm", "Bloodhawk", "Fangblade"
]
game_running = True

def print_menu(title, options):
    print("\n=== " + title + " ===")
    for i, option in enumerate(options, 1):
        print(str(i) + ". " + option)
    print("Choose option 1-" + str(len(options)))

def buy_goods(player):
    global goods_list
    good = random.choice(goods_list)
    price = random.randint(20, 300)
    print("\nBuy " + good + " for " + str(price) + " credits?")
    if input("1. Yes 2. No: ") == "1":
        if player["credits"] >= price:
            player["credits"] -= price
            if good in player["goods"]:
                player["goods"][good] += 1
            else:
                player["goods"][good] = 1
            print("Bought " + good)
        else:
            print("Not enough credits.")

def sell_goods(player):
    if not player["goods"]:
        print("\nNo goods to sell.")
        return
    good = random.choice(list(player["goods"].keys()))
    price = random.randint(50, 200)
    print("\nSell " + good + " for " + str(price) + " credits?")
    if input("1. Yes 2. No: ") == "1":
        player["credits"] += price
        player["goods"][good] -= 1
        if player["goods"][good] == 0:
            del player["goods"][good]
        print("Sold " + good)

def upgrade_ship(player):
    print_menu("\nUpgrade Ship", ["Engine", "Hold", "Shields", "Weapons"])
    choice = input("Choose upgrade: ")
    if choice == "1" and player["credits"] >= 500:
        player["engine"] += 1
        player["credits"] -= 500
        print("Upgraded engine!")
    elif choice == "2" and player["credits"] >= 300:
        player["hold"] += 1
        player["credits"] -= 300
        print("Upgraded hold!")
    elif choice == "3" and player["credits"] >= 400:
        player["shields"] += 1
        player["credits"] -= 400
        print("Upgraded shields!")
    elif choice == "4" and player["credits"] >= 400:
        player["weapons"] += 1
        player["credits"] -= 400
        print("Upgraded weapons!")
    else:
        print("Not enough credits.")

def decrement_stat(player, stat):
    global game_running
    """ Decrement a ship's stat and ensure it doesn't go below 0. Handle the 'hold' and 'engine' cases. """
    if stat == "engine":
        player["engine"] = max(0, player["engine"] - 1)
        if player["engine"] == 0:
            print("With no working engines, you are now adrift in the cold void of space. Game over!")
            game_running = False
    elif stat == "hold":
        player["hold"] = max(0, player["hold"] - 1)
        total_goods = sum(player["goods"].values())
        if total_goods > player["hold"]:
            jettison_goods(player)
    else:
        player[stat] = max(0, player[stat] - 1)

    print(stat + " has been reduced by 1.")

def jettison_goods(player):
    """ Remove random goods until the number of goods held matches the hold capacity. """
    total_goods = sum(player["goods"].values())
    while total_goods > player["hold"]:
        good = random.choice(list(player["goods"].keys()))
        player["goods"][good] -= 1
        if player["goods"][good] == 0:
            del player["goods"][good]
        total_goods -= 1
    print("Due to hold damage, goods had to be jettisoned.")

def pirate_attack(player):
    global pirate_names
    pirate = random.choice(pirate_names)
    print("\nPirate " + pirate + " attacks!")

    # Decide battle outcome based on the player's weapons
    if player["weapons"] > random.randint(0, 2):
        print("You won the battle!")
    else:
        # Check if the player escapes using shields
        if player["shields"] > random.randint(0, 2):
            print("You escaped the battle,")
            print("but your ship took some damage!")
        else:
            print("Lost the battle! Pirates stole")
            print("your goods and damaged your ship.")
            player["goods"].clear()  # Player loses all goods if they fail to escape

        # In both cases (loss or escape), decrement a random ship statistic
        stat = random.choice(["engine", "hold", "shields", "weapons"])
        decrement_stat(player, stat)

def trader_encounter(player):
    print("\nMet a trader!")
    buy_goods(player)

def planet_encounter(player):
    global planet_names
    planet = random.choice(planet_names)
    print("\nLanded on " + planet + ".")
    outcome = random.choice(["boon", "fight", "trade"])
    if outcome == "boon":
        print("Received a boon!")
        upgrade = random.choice(["engine", "hold", "shields", "weapons"])
        player[upgrade] += 1
        print(upgrade + " has been increased by 1!")
    elif outcome == "fight":
        pirate_attack(player)
    elif outcome == "trade":
        trader_encounter(player)

def exploration(player):
    for _ in range(player["engine"]):
        encounter = random.choice(["pirate", "trader", "planet", "empty"])
        if encounter == "pirate":
            pirate_attack(player)
        elif encounter == "trader":
            trader_encounter(player)
        elif encounter == "planet":
            planet_encounter(player)
        elif encounter == "empty":
            print("\nNothing here...")
        input("\nPress EXE to continue exploring...")

def instructions():
    print("\nAbout the Game:")
    print("\nYou take the role of a space")
    print("trader named Reynolds,")
    print("commanding your starship")
    print("Intrepid.")
    input("\nPress EXE to continue...")
    print("\nYour journey begins at the")
    print("age of 30, and the game")
    print("ends when you retire, aged")
    print("60, from the Trading Guild.")
    print("\nDue to hibernation you only")
    print("age when docked at the")
    print("Galactic Exchange. Your")
    print("final score is based on the")
    print("credits you have accrued.")
    input("\nPress EXE to continue...")
    print("\nHow to Play:")
    print("\n1. Start with 1000 credits.")
    print("2. At each turn, you'll visit")
    print("the Galactic Exchange where you can:")
    print("\n - Buy Goods")
    print(" - Sell Goods")
    print(" - Upgrade your Ship")
    input("\nPress EXE to continue...")
    print("\n3. During exploration, you'll")
    print("face 1 to 4 encounters based")
    print("on your engine stat:")
    print("\n - Pirate Attack")
    print(" - Meet a Trader")
    print(" - Explore a Planet (you may")
    print("   encounter pirates, traders")
    print("   or receive a boon)")
    print(" - Explore empty space")
    input("\nPress EXE to continue...")
    print("\nShip Stats:")
    print("\nEngine: Number of encounters")
    print("per turn.")
    print("Hold: How many goods you can")
    print("carry.")
    print("Shields: Helps defend your")
    print("ship in battle.")
    print("Weapons: Affects your")
    print("offensive power in battles.")
    input("\nPress EXE to return to the game")

def view_ship_status(player):
    print("Ship: " + player["ship_name"])
    print("Captain: " + player["captain_name"])
    print("Age: " + str(player["age"]))
    print("Credits: " + str(player["credits"]))
    print("Engine: " + str(player["engine"]))
    print("Hold: " + str(player["hold"]))
    print("Shields: " + str(player["shields"]))
    print("Weapons: " + str(player["weapons"]))

    # Handle the goods display
    if player["goods"]:
        print("Goods:")
        for k, v in player["goods"].items():
            print(" - " + k + " x" + str(v))
    else:
        print("Goods: None")
    input("\nPress EXE to continue...")

def register_ship_name(player):
    new_name = input("Enter your new ship name: ")
    player["ship_name"] = new_name
    print("Ship renamed to " + player["ship_name"])

def register_captain_name(player):
    new_name = input("Enter your new captain name: ")
    player["captain_name"] = new_name
    print("Captain renamed to " + player["captain_name"])

def ship_computer(player):
    global game_running
    print_menu("Ship Computer",
               ["Instructions", "View Ship Status", "Register Ship Name", "Register Captain Name", "Exit Game"])
    log_choice = input(": ")

    if log_choice == "1":
        instructions()
    elif log_choice == "2":
        view_ship_status(player)
    elif log_choice == "3":
        register_ship_name(player)
    elif log_choice == "4":
        register_captain_name(player)
    elif log_choice == "5":
        print("\nExiting the game...")
        game_running = False

def galactic_exchange(player):
    global game_running
    # Display captain and starship names
    print("\nCaptain: " + player["captain_name"])
    print("Starship: " + player["ship_name"])
    print("Age: " + str(player["age"]))
    print("Credits: " + str(player["credits"]))

    # Display the menu options
    print_menu("Galactic Exchange", ["Buy Goods", "Sell Goods", "Upgrade Ship", "Ship Computer", "Launch Ship"])

    # Get user input
    choice = input(": ")
    if choice == "1":
        buy_goods(player)
    elif choice == "2":
        sell_goods(player)
    elif choice == "3":
        upgrade_ship(player)
    elif choice == "4":
        ship_computer(player)
    elif choice == "5":
        exploration(player)
        player["age"] += 1
        if player["age"] == 60:
            game_running = False

# Initialize player as a dictionary instead of dataclass
player = {
    "age": 30,
    "credits": 1000,
    "engine": 1,
    "hold": 5,
    "shields": 1,
    "weapons": 1,
    "goods": {},
    "ship_name": "Intrepid",
    "captain_name": "Reynolds"
}

print("Welcome to Space Trader !")
print("\nYour mission is to explore")
print("the galaxy and make your")
print("fortune.")
input("\nPress EXE to continue...")

while game_running :
    galactic_exchange(player)

print("\nGame over! You retired")
print("Final score: " + str(floor((player["age"] * player["credits"])/1000)))
