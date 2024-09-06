import random
import json
import os
from dataclasses import dataclass, field
from typing import Dict


# Define Player using dataclass
@dataclass
class Player:
    age: int = 30
    credits: int = 1000
    engine: int = 1
    hold: int = 5
    shields: int = 1
    weapons: int = 1
    goods: Dict[str, int] = field(default_factory=dict)
    ship_name: str = "Intrepid"  # Default ship name
    captain_name: str = "Reynolds"  # Default captain name


# Procedural generation of goods, pirates, and planets
goods_list = ["Plasma", "Fuel", "Water", "Titanium", "Food"]
planet_names = ["Zanxor", "Novus", "Kalrix", "Velor", "Gorath"]
pirate_names = ["Rex", "Sly", "Fang", "Blaze", "Havok"]


def print_menu(title, options):
    print(f"\n{title}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("\n")


def buy_goods(player: Player):
    good = random.choice(goods_list)
    price = random.randint(100, 300)
    print(f"Buy {good} for {price} credits?")
    if input("1. Yes 2. No: ") == "1":
        if player.credits >= price:
            player.credits -= price
            if good in player.goods:
                player.goods[good] += 1
            else:
                player.goods[good] = 1
            print(f"Bought {good}")
        else:
            print("Not enough credits.")


def sell_goods(player: Player):
    if not player.goods:
        print("No goods to sell.")
        return
    good = random.choice(list(player.goods.keys()))
    price = random.randint(50, 200)
    print(f"Sell {good} for {price} credits?")
    if input("1. Yes 2. No: ") == "1":
        player.credits += price
        player.goods[good] -= 1
        if player.goods[good] == 0:
            del player.goods[good]
        print(f"Sold {good}")


def upgrade_ship(player: Player):
    print_menu("Upgrade Ship", ["Engine", "Hold", "Shields", "Weapons"])
    choice = input("Upgrade what? ")
    if choice == "1" and player.credits >= 500:
        player.engine += 1
        player.credits -= 500
        print("Upgraded engine!")
    elif choice == "2" and player.credits >= 300:
        player.hold += 1
        player.credits -= 300
        print("Upgraded hold!")
    elif choice == "3" and player.credits >= 400:
        player.shields += 1
        player.credits -= 400
        print("Upgraded shields!")
    elif choice == "4" and player.credits >= 400:
        player.weapons += 1
        player.credits -= 400
        print("Upgraded weapons!")
    else:
        print("Not enough credits.")


def log_game(player: Player, action: str):
    if action == "save":
        with open("savefile.json", "w") as f:
            json.dump(player.__dict__, f)
        print("Game saved.")
    elif action == "load":
        if os.path.exists("savefile.json"):
            with open("savefile.json", "r") as f:
                player_data = json.load(f)
                player.__dict__.update(player_data)
            print("Game loaded.")
        else:
            print("No save file found.")


def decrement_stat(player: Player, stat: str):
    """ Decrement a ship's stat and ensure it doesn't go below 0. Handle the 'hold' and 'engine' cases. """
    if stat == "engine":
        player.engine = max(0, player.engine - 1)
        if player.engine == 0:
            print("With no working engines, you are now adrift in the cold void of space. Game over!")
            exit()
    elif stat == "hold":
        player.hold = max(0, player.hold - 1)
        if len(player.goods) > player.hold:
            jettison_goods(player)
    else:
        setattr(player, stat, max(0, getattr(player, stat) - 1))

    print(f"{stat.capitalize()} has been reduced by 1.")


def jettison_goods(player: Player):
    """ Remove random goods until the number of goods held matches the hold capacity. """
    total_goods = sum(player.goods.values())
    while total_goods > player.hold:
        good = random.choice(list(player.goods.keys()))
        player.goods[good] -= 1
        if player.goods[good] == 0:
            del player.goods[good]
        total_goods -= 1
    print("Due to hold damage, goods had to be jettisoned.")


def pirate_attack(player: Player):
    pirate = random.choice(pirate_names)
    print(f"Pirate {pirate} attacks!")

    # Decide battle outcome based on the player's weapons
    if player.weapons > random.randint(0, 2):
        print("You won the battle!")
    else:
        # Check if the player escapes using shields
        if player.shields > random.randint(0, 2):
            print("You escaped the battle, but your ship took some damage!")
        else:
            print("Lost the battle! Pirates stole your goods and damaged your ship.")
            player.goods.clear()  # Player loses all goods if they fail to escape

        # In both cases (loss or escape), decrement a random ship statistic
        stat = random.choice(["engine", "hold", "shields", "weapons"])
        decrement_stat(player, stat)


def trader_encounter(player: Player):
    print("Met a trader!")
    buy_goods(player)


def planet_encounter(player: Player):
    print(f"Landed on {random.choice(planet_names)}.")
    outcome = random.choice(["boon", "fight", "trade"])
    if outcome == "boon":
        print("Received a boon!")
        upgrade = random.choice(["engine", "hold", "shields", "weapons"])
        setattr(player, upgrade, getattr(player, upgrade) + 1)
        print(f"{upgrade.capitalize()} has been increased by 1!")  # Message showing which stat was incremented
    elif outcome == "fight":
        pirate_attack(player)
    elif outcome == "trade":
        trader_encounter(player)


def exploration(player: Player):
    for _ in range(player.engine):
        encounter = random.choice(["pirate", "trader", "planet", "empty"])
        if encounter == "pirate":
            pirate_attack(player)
        elif encounter == "trader":
            trader_encounter(player)
        elif encounter == "planet":
            planet_encounter(player)
        elif encounter == "empty":
            print("Nothing here...")

        # Ask the player to press Enter to continue
        input("Press Enter to continue exploring...")


def view_ship_status(player: Player):
    # Concatenate the player's stats into a single string, including ship and captain names
    status = (
        f"Ship: {player.ship_name}, Captain: {player.captain_name}, "
        f"Age: {player.age}, Credits: {player.credits}, "
        f"Engine: {player.engine}, Hold: {player.hold}, Shields: {player.shields}, Weapons: {player.weapons}, "
        f"Goods: {', '.join([f'{k} x{v}' for k, v in player.goods.items()]) or 'None'}"
    )
    print(status)


def register_ship_name(player: Player):
    new_name = input("Enter your new ship name: ")
    player.ship_name = new_name
    print(f"Ship renamed to {player.ship_name}")


def register_captain_name(player: Player):
    new_name = input("Enter your new captain name: ")
    player.captain_name = new_name
    print(f"Captain renamed to {player.captain_name}")


def captains_log(player: Player):
    print_menu("Captain's Log",
               ["Save Game", "View Ship Status", "Register Ship Name", "Register Captain Name", "Exit Game"])
    log_choice = input("Choose: ")

    if log_choice == "1":
        log_game(player, "save")
    elif log_choice == "2":
        view_ship_status(player)
    elif log_choice == "3":
        register_ship_name(player)
    elif log_choice == "4":
        register_captain_name(player)
    elif log_choice == "5":
        print("Exiting the game...")
        exit()


def galactic_exchange(player: Player):
    # Display captain and starship names
    print(f"\nCaptain: {player.captain_name}, Starship: {player.ship_name}")
    print(f"Age: {player.age}, Credits: {player.credits}")

    # Display the menu options
    print_menu("Galactic Exchange", ["Buy Goods", "Sell Goods", "Upgrade Ship", "Captain's Log", "Launch Ship"])

    # Get user input
    choice = input("Choose: ")
    if choice == "1":
        buy_goods(player)
    elif choice == "2":
        sell_goods(player)
    elif choice == "3":
        upgrade_ship(player)
    elif choice == "4":
        captains_log(player)  # Open Captain's Log
    elif choice == "5":
        exploration(player)
        player.age += 1


def main():
    player = Player()  # Initialize player object
    while player.age < 60:
        galactic_exchange(player)
    print(f"Game over! Final credits: {player.credits}")


if __name__ == "__main__":
    main()
