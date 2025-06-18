import random
import json
import os
from math import floor
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple


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
    location: str = "exchange"
    purchase_records: Dict[str, Dict[str, int]] = field(default_factory=dict)
    total_profit: int = 0
    trades_completed: int = 0
    bounty_points: int = 0
    total_bounty_earned: int = 0  # Track lifetime bounty earned
    bounty_redeemed: int = 0  # Track how many points were redeemed
    

# Define Game structure
@dataclass
class Game:
    player: Player = field(default_factory=Player)
    exchange: Dict[str, Any] = field(default_factory=lambda: {"traders": random.randint(6, 10)})
    running: bool = True


# Procedural generation of goods, pirates, planets, and traders
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


def menu(title: str, options: List[str]) -> str:
    """Display a menu with title and options, return user choice"""
    print(f"\n{title}")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    return input(f"Choose (1-{len(options)}): ")


def cap(s: str) -> str:
    """Capitalize first letter of string"""
    return s[0].upper() + s[1:].lower() if s else ""


def starfield() -> None:
    """Display a simple starfield animation"""
    print("\n  *  .  *")
    print(" . * . * .")
    print("*  .  *  .")
    print(" . * . * *")


def casino(game: Game) -> None:
    """Casino mini-game where player can gamble credits"""
    p = game.player
    print("\n===== Quantum Casino =====")
    print("Welcome to the Quantum Casino")
    print("Here you can test your luck")
    print("with our Asteroid game.")
    print("Your ship must navigate through")
    print("an asteroid field.")
    print("Choose a navigation path (1-3)")
    print("and bet credits.")
    print("Choosing the safe path, doubles your bet!")
    print("If you hit an asteroid, you lose your bet.")

    while True:
        print(f"\nYour credits: {p.credits}")

        bet_str = input("Place your bet (0 to exit): ")
        try:
            bet = int(bet_str)
        except ValueError:
            print("Invalid bet. Please enter a number.")
            continue

        if bet <= 0:
            print("Leaving the casino...")
            break

        if bet > p.credits:
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
        starfield()

        if path == safe_path:
            winnings = bet * 2
            p.credits += bet
            print("\nSuccessful navigation!")
            print("You found a safe path.")
            print(f"You won {bet} cr !")
            print(f"Total winnings: {winnings} cr")
        else:
            p.credits -= bet
            print("\nCRASH! Your ship hit an asteroid")
            print(f"on the {['Alpha', 'Beta', 'Gamma'][int(path) - 1]} Route!")
            print(f"The safe route was: {['Alpha', 'Beta', 'Gamma'][int(safe_path) - 1]} Route")
            print(f"You lost {bet} credits.")

        if p.credits <= 0:
            print("\nYou've lost all your credits!")
            print("The casino security escorts you out.")
            break

        again = input("\nPlay again? 1. Yes 2. No: ")
        if again != "1":
            print("Thanks for playing at the Quantum Casino!")
            break


def bounty_office(game: Game) -> None:
    """Bounty office where players can redeem bounty points for credits"""
    p = game.player
    print("\n===== Galactic Bounty Office =====")
    print("Welcome to the Bounty Office!")
    print("Here you can redeem bounty points")
    print("earned from defeating pirates.")
    print(f"Current bounty points: {p.bounty_points}")

    if p.bounty_points == 0:
        print("No bounty points to redeem.")
        input("Press Enter to continue...")
        return

    # Exchange rate: 1 bounty point = 100 credits
    exchange_rate = 100
    total_value = p.bounty_points * exchange_rate

    print(f"Exchange rate: 1 bounty point = {exchange_rate} cr")
    print(f"Total value: {total_value} cr")
    print("Note: Redeem bounty points to increase your final score.")

    choice = input(f"Redeem bounty points ? (1. Yes 2. No): ")

    if choice == "1":
        p.credits += total_value
        p.bounty_redeemed += p.bounty_points
        print(f"Redeemed {p.bounty_points} bounty points for {total_value} cr!")
        p.bounty_points = 0
        print(f"New credit total: {p.credits} cr")
    else:
        print("Bounty points not redeemed.")

    input("Press Enter to continue...")


def manage_ship_stat(game: Game, stat: str, increase: bool = False) -> str:
    """Manage ship statistics - increase or decrease them"""
    p = game.player
    if increase:
        setattr(p, stat, getattr(p, stat) + 1)
        return f"{cap(stat)} increased to {getattr(p, stat)}"

    setattr(p, stat, max(0, getattr(p, stat) - 1))
    if stat == "engine" and getattr(p, stat) == 0:
        print("With no engines, you drift in space. Game over!")
        game.running = False
    elif stat == "hold":
        # Jettison goods if needed
        total = sum(p.goods.values())
        while total > p.hold and p.goods:
            good = random.choice(list(p.goods.keys()))
            p.goods[good] -= 1
            # Record the loss in profit
            if good in p.purchase_records and p.purchase_records[good]:
                # Get the oldest purchase (FIFO)
                purchase_id = list(p.purchase_records[good].keys())[0]
                purchase_price = p.purchase_records[good][purchase_id]
                # Count jettisoned goods as a loss
                p.total_profit -= purchase_price
                # Remove the purchase record
                del p.purchase_records[good][purchase_id]
                if not p.purchase_records[good]:
                    del p.purchase_records[good]
            if p.goods[good] == 0:
                del p.goods[good]
            total -= 1
            print(f"Jettisoned {good} due to hold damage")
    return f"{cap(stat)} reduced to {getattr(p, stat)}"


def trade(game: Game, is_buy: bool = True) -> None:
    """Handle trade transactions - buying or selling goods"""
    p, e = game.player, game.exchange

    if e["traders"] <= 0 and p.location == "exchange":
        print("\nNo traders available")
        return

    e["traders"] -= 1

    if is_buy:
        good = random.choice(goods_list)
        price = random.randint(20, 300)
        action, verb = "Buy", "selling"
    else:
        if not p.goods:
            print("\nNo goods to sell")
            return
        good = random.choice(list(p.goods.keys()))
        price = random.randint(50, 200)
        action, verb = "Sell", "buying"

    trader = random.choice(trader_names)
    print(f"\n{trader} is {verb}:")
    print(f"{good} for {price} cr")
    print(f"{action} {good}?")

    if input("1. Yes 2. No: ") != "1":
        return

    # Handle buy/sell
    if is_buy:
        if p.credits < price:
            print("Not enough credits")
            return
        p.credits -= price
        p.goods[good] = p.goods.get(good, 0) + 1
        # Record purchase for profit tracking
        if good not in p.purchase_records:
            p.purchase_records[good] = {}
        # Create a unique ID for this purchase
        purchase_id = f"{good}_{len(p.purchase_records[good]) + 1}"
        p.purchase_records[good][purchase_id] = price

        print(f"Bought {good}")
    else:
        # Calculate profit for this transaction
        if good in p.purchase_records and p.purchase_records[good]:
            # Get the oldest purchase (FIFO)
            purchase_ids = list(p.purchase_records[good].keys())
            oldest_purchase_id = purchase_ids[0]
            purchase_price = p.purchase_records[good][oldest_purchase_id]
            # Calculate profit and update tracking
            trade_profit = price - purchase_price
            p.total_profit += trade_profit
            p.trades_completed += 1
            p.credits += price

            # Remove the purchase record
            del p.purchase_records[good][oldest_purchase_id]
            if not p.purchase_records[good]:
                del p.purchase_records[good]

            # Remove good from inventory
            p.goods[good] -= 1
            if p.goods[good] == 0:
                del p.goods[good]

            # Display the profit information
            profit_text = "profit" if trade_profit >= 0 else "loss"
            print(f"Sold {good}")
            print(f"for a {profit_text} of {abs(trade_profit)} cr")
        else:
            # Fallback if we don't have purchase records (shouldn't happen)
            p.credits += price
            p.goods[good] -= 1
            if p.goods[good] == 0:
                del p.goods[good]
            print(f"Sold {good}")

    # Exchange tax
    if p.location == "exchange":
        if p.credits < 5:
            print("\nCan't pay trade tax. Ship impounded.")
            game.running = False
            return
        p.credits -= 5
        print("Trade tax of 5 cr paid")


def handle_encounter(game: Game, encounter_type: str) -> None:
    """Handle different types of space encounters"""
    p = game.player

    if encounter_type == "empty":
        starfield()
        print("\nNothing here...")
        return

    if encounter_type == "trader":
        print("\nMet a trader!")
        trade(game, True)
        return

    if encounter_type == "planet":
        planet = random.choice(planet_names)
        print(f"\nLanded on {planet}")
        outcome = random.choice(["boon", "fight", "trade"])

        if outcome == "boon":
            stat = random.choice(["engine", "hold", "shields", "weapons"])
            print(f"Received a boon! {manage_ship_stat(game, stat, True)}")
        elif outcome == "fight":
            handle_encounter(game, "pirate")
        else:
            handle_encounter(game, "trader")
        return

    if encounter_type == "pirate":
        # Different pirate types with different difficulty and rewards
        pirate_types = [
            {"name": "Smuggler", "difficulty": 1, "reward": (1, 2)},
            {"name": "Raider", "difficulty": 2, "reward": (2, 4)},
            {"name": "Warlord", "difficulty": 3, "reward": (3, 6)}
        ]
        
        # Select pirate type based on player's weapons/shields
        player_strength = p.weapons + p.shields
        if player_strength >= 5:
            pirate_type = pirate_types[2]  # Warlord - harder but more rewarding
        elif player_strength >= 3:
            pirate_type = pirate_types[1]  # Raider - medium difficulty and reward
        else:
            pirate_type = pirate_types[0]  # Smuggler - easier but less rewarding
            
        pirate = random.choice(pirate_names)
        print(f"\n{pirate_type['name']} {pirate} attacks!")

        # Combat calculation
        if p.weapons > random.randint(0, pirate_type['difficulty']):
            min_reward, max_reward = pirate_type['reward']
            bounty_reward = random.randint(min_reward, max_reward)
            p.bounty_points += bounty_reward
            p.total_bounty_earned += bounty_reward
            print("You won the battle!")
            print(f"Bounty awarded: {bounty_reward} points")
            print(f"Total bounty points: {p.bounty_points}")
            return

        if p.shields > random.randint(0, pirate_type['difficulty']):
            print("You escaped with damage!")
        else:
            print("Lost! Pirates stole your goods")
            # Record losses from all stolen goods
            for good, quantity in p.goods.items():
                if good in p.purchase_records:
                    for purchase_id, price in p.purchase_records[good].items():
                        p.total_profit -= price
            # Clear goods and purchase records
            p.goods.clear()
            p.purchase_records.clear()

        stat = random.choice(["engine", "hold", "shields", "weapons"])
        print(manage_ship_stat(game, stat))


def explore(game: Game) -> None:
    """Handle exploration sequence"""
    p = game.player
    p.location = "space"

    for _ in range(p.engine):
        if not game.running:
            return

        handle_encounter(game, random.choice(["pirate", "trader", "planet", "empty"]))
        input("\nPress Enter to continue exploring...")

    print("\nDocking at Exchange...")
    p.location = "exchange"

    if p.credits < 20:
        print("Can't pay docking fees. Ship impounded.")
        game.running = False
        return

    game.exchange["traders"] = random.randint(6, 10)
    p.credits -= 20
    print("Docked. Paid 20 cr fee")
    p.age += 1

    if p.age >= 60:
        game.running = False


def view_trade_stats(player: Player) -> None:
    """Display trading statistics including profit/loss and inventory values"""
    print("\nTrading Statistics:")
    print(f"Total Profit/Loss: {player.total_profit} cr")
    print(f"Trades Completed: {player.trades_completed}")

    if player.trades_completed > 0:
        avg_profit = player.total_profit / player.trades_completed
        print(f"Average Profit per Trade: {floor(floor(avg_profit * 10) / 10)} cr")

    # Show current inventory with purchase costs
    if player.goods:
        print("\nCurrent Inventory Values:")
        total_inventory_value = 0

        for good, quantity in player.goods.items():
            if good in player.purchase_records:
                # Calculate average purchase price for this good
                purchase_prices = [price for _, price in player.purchase_records[good].items()]
                if purchase_prices:
                    avg_price = sum(purchase_prices) / len(purchase_prices)
                    total_value = avg_price * quantity
                    total_inventory_value += total_value
                    print(f"{good} x{quantity}")
                    print(f"(avg {floor(avg_price)} cr each)")
            else:
                print(f"{good} x{quantity} (unknown cost)")

        print(f"Estimated inventory value: {floor(total_inventory_value)} cr")


def computer(game: Game) -> None:
    """Ship computer interface for various functions"""
    p = game.player
    choice = menu("Ship Computer", ["Instructions", "Ship Status", "Trading Stats", "Bounty Stats", "Rename Ship", "Rename Captain", "Exit Game"])

    if choice == "1":
        print("\nSpace Trader: Trade goods, upgrade ship,")
        print("explore space.")
        print("Engine: Encounter more.")
        print("Hold: Cargo capacity.")
        print("Shields & weapons: Battle survival.")
        print("Taxes: 5cr/trade, 20cr docking.")
        print("Age 60: retire.")

    elif choice == "2":
        print(f"\nShip: {p.ship_name}, Captain: {p.captain_name}")
        print(f"Age: {p.age}, Credits: {p.credits}")
        print(f"Engine: {p.engine}, Hold: {p.hold}")
        print(f"Shields: {p.shields}, Weapons: {p.weapons}")
        print(f"Bounty Points: {p.bounty_points}")

        if p.goods:
            goods_list = []
            for k, v in p.goods.items():
                goods_list.append(f"{k} x{v}")
            print("Goods: ")
            for goods in goods_list:
                print(goods)
        else:
            print("Goods: None")

    elif choice == "3":
        view_trade_stats(p)
        
    elif choice == "4":
        view_bounty_stats(p)

    elif choice == "5":
        p.ship_name = input("\nNew ship name: ")
        print(f"Ship renamed to {p.ship_name}")

    elif choice == "6":
        p.captain_name = input("\nNew captain name: ")
        print(f"Captain renamed to {p.captain_name}")

    elif choice == "7":
        print("\nExiting game...")
        game.running = False
        return


def log_game(player: Player, action: str) -> None:
    """Save or load game state to/from file"""
    if action == "save":
        # Convert player object to dict, handling nested dicts correctly
        player_dict = player.__dict__.copy()
        with open("savefile.json", "w") as f:
            json.dump(player_dict, f)
        print("Game saved.")
    elif action == "load":
        if os.path.exists("savefile.json"):
            with open("savefile.json", "r") as f:
                player_data = json.load(f)
                player.__dict__.update(player_data)
            print("Game loaded.")
        else:
            print("No save file found.")


def exchange(game: Game) -> None:
    """Main exchange interface"""
    p = game.player
    p.location = "exchange"

    print(f"\nCaptain: {p.captain_name}")
    print(f"Starship: {p.ship_name}")
    print(f"Age: {p.age}, Credits: {p.credits}")

    choice = menu("===== Celastra Exchange ======", ["Buy Goods", "Sell Goods", "Upgrade Ship", "Ship Computer", "Casino", "Bounty Office", "Launch Ship"])

    if choice == "1":
        trade(game, True)
    elif choice == "2":
        trade(game, False)
    elif choice == "3":
        upgrades = {"1": ("engine", 500), "2": ("hold", 300),
                    "3": ("shields", 400), "4": ("weapons", 400)}

        opt = menu("Upgrade Ship", ["Engine", "Hold", "Shields", "Weapons"])

        if opt in upgrades:
            stat, cost = upgrades[opt]
            if p.credits >= cost:
                setattr(p, stat, getattr(p, stat) + 1)
                p.credits -= cost
                print(f"Upgraded {cap(stat)}!")
            else:
                print("Not enough credits")
    elif choice == "4":
        computer(game)
    elif choice == "5":
        casino(game)
    elif choice == "6":
        bounty_office(game)
    elif choice == "7":
        explore(game)


def calculate_final_score(player: Player) -> dict:
    """Calculate final score and determine player rank"""
    # Profit modifier (avoid division by zero)
    profit_modifier = max(1, player.total_profit) if player.total_profit > 0 else 1
    
    # Simplified bounty points calculation - only count redeemed points
    bounty_bonus = player.bounty_redeemed * 50  # 50 points per redeemed bounty point
    
    # Enhanced score formula: (Age * Credits * Total Profit) / 10000 + bounty bonuses
    enhanced_score = floor((player.age * player.credits * profit_modifier) / 10000) + bounty_bonus

    # Separate trader score component (based on profits and trades)
    trader_score = floor((player.age * player.credits * profit_modifier) / 10000)
    
    # Determine trader rank based on trading performance
    trader_rank = "Rookie Trader"
    if trader_score >= 50000:
        trader_rank = "Legendary Space Mogul"
    elif trader_score >= 30000:
        trader_rank = "Galactic Trade Master"
    elif trader_score >= 15000:
        trader_rank = "Interstellar Merchant"
    elif trader_score >= 7500:
        trader_rank = "Established Trader"
    elif trader_score >= 3000:
        trader_rank = "Skilled Trader"
    elif trader_score >= 1000:
        trader_rank = "Trader Apprentice"
    
    # Determine bounty hunter rank based on total redeemed bounty points
    bounty_rank = "Amateur Bounty Hunter"
    if player.bounty_redeemed >= 50:
        bounty_rank = "Legendary Bounty Hunter"
    elif player.bounty_redeemed >= 30:
        bounty_rank = "Master Bounty Hunter"
    elif player.bounty_redeemed >= 20:
        bounty_rank = "Elite Bounty Hunter"
    elif player.bounty_redeemed >= 15:
        bounty_rank = "Professional Bounty Hunter"
    elif player.bounty_redeemed >= 10:
        bounty_rank = "Seasoned Bounty Hunter"
    elif player.bounty_redeemed >= 5:
        bounty_rank = "Novice Bounty Hunter"

    # Calculate overall rank based on combined score
    overall_rank = "Space Rookie"
    if enhanced_score >= 50000:
        overall_rank = "Legendary Space Captain"
    elif enhanced_score >= 30000:
        overall_rank = "Galactic Champion"
    elif enhanced_score >= 15000:
        overall_rank = "Interstellar Ace"
    elif enhanced_score >= 7500:
        overall_rank = "Established Space Captain"
    elif enhanced_score >= 3000:
        overall_rank = "Skilled Space Captain"
    elif enhanced_score >= 1000:
        overall_rank = "Space Apprentice"

    return {
        "enhanced_score": enhanced_score,
        "trader_score": trader_score,
        "bounty_contribution": bounty_bonus,
        "overall_rank": overall_rank,
        "trader_rank": trader_rank,
        "bounty_rank": bounty_rank
    }

def view_bounty_stats(player: Player) -> None:
    """Display bounty hunting statistics without showing ranks"""
    print("\nBounty Hunter Statistics:")
    print(f"Current Bounty Points: {player.bounty_points}")
    print(f"Total Bounty Points Earned: {player.total_bounty_earned}")
    print(f"Bounty Points Redeemed: {player.bounty_redeemed}")
    
    # Calculate credits earned from bounty redemptions
    credits_earned = player.bounty_redeemed * 100  # 100 credits per point
    print(f"Credits Earned from Bounties: {credits_earned} cr")


def main():
    """Main game function"""
    game = Game()  # Initialize game with default player
    
    print("Welcome to Space Trader v0.0.1!")
    print("\nYour mission: explore space")
    print("and make your fortune")

    while game.running:
        exchange(game)

    p = game.player
    print(f"\nGame over! You retired at age {p.age}")
    print("\nTrading Career Summary:")
    print(f"Total Credits: {p.credits} cr")
    print(f"Total Profit: {p.total_profit} cr")
    print(f"Trades Completed: {p.trades_completed}")
    
    # Update pirate information to include more detail
    print(f"\nBounty Hunter Career:")
    print(f"Total Bounty Points Earned: {p.total_bounty_earned}")
    print(f"Bounty Points Redeemed: {p.bounty_redeemed}")
    print(f"Unredeemed Bounty Points: {p.bounty_points}")

    if p.trades_completed > 0:
        avg_profit = p.total_profit / p.trades_completed
        print(f"\nAverage Profit per Trade: {floor(avg_profit * 10) / 10} cr")

    score_data = calculate_final_score(p)

    print(f"\nFinal Score: {score_data['enhanced_score']}")
    print("Score Breakdown:")
    print(f"- Trading: {score_data['trader_score']}")
    print(f"- Bounty Hunting: {score_data['bounty_contribution']}")
    
    print("\n==== FINAL RANKINGS ====")
    print(f"Overall Rank: {score_data['overall_rank']}")
    print(f"Trader Rank: {score_data['trader_rank']}")
    print(f"Bounty Hunter Rank: {score_data['bounty_rank']}")
    
    input("\nPress Enter to leave the game.")


if __name__ == "__main__":
    main()