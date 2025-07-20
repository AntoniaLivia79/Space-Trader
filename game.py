import random
import json
import os
from math import floor
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple


# Define Player using dataclass with enhanced pirate features
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
    pirate_reputation: int = 0  # Negative = feared by pirates, Positive = hunted by pirates


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


def get_pirate_encounter_difficulty(player: Player) -> dict:
    """Calculate appropriate pirate difficulty based on player progress"""

    # Base difficulty on multiple factors
    wealth_factor = min(3, player.credits // 2000)  # Every 2000 credits adds difficulty
    equipment_factor = (player.weapons + player.shields + player.engine) // 3
    age_factor = min(2, (player.age - 30) // 10)  # Gets harder as you age
    bounty_factor = min(2, player.total_bounty_earned // 10)  # Reputation draws stronger pirates
    reputation_factor = max(0, player.pirate_reputation // 5)  # Positive reputation increases difficulty

    total_difficulty = wealth_factor + equipment_factor + age_factor + bounty_factor + reputation_factor

    return {
        "base_difficulty": min(4, max(1, total_difficulty)),
        "encounter_chance": min(0.4, 0.1 + (total_difficulty * 0.05)),  # Higher chance as difficulty increases
        "fleet_chance": max(0, (total_difficulty - 3) * 0.1)  # Chance of multiple pirates
    }


def update_pirate_reputation(player: Player, action: str, pirate_type: str):
    """Update player's reputation with pirate factions"""
    reputation_changes = {
        "victory": {"Smuggler": -1, "Raider": -2, "Warlord": -3, "Pirate Fleet": -4},
        "defeat": {"Smuggler": 2, "Raider": 3, "Warlord": 4, "Pirate Fleet": 5},
        "escape": {"Smuggler": 1, "Raider": 1, "Warlord": 2, "Pirate Fleet": 2}
    }

    if action in reputation_changes and pirate_type in reputation_changes[action]:
        change = reputation_changes[action][pirate_type]
        player.pirate_reputation += change

        if change < 0:
            if player.pirate_reputation <= -10:
                print(f"Pirates flee at the sight of your ship! (Reputation: {player.pirate_reputation})")
            elif player.pirate_reputation <= -5:
                print(f"Your reputation as a pirate hunter grows! (Reputation: {player.pirate_reputation})")
            else:
                print(f"Pirates are starting to fear you. (Reputation: {player.pirate_reputation})")
        else:
            if player.pirate_reputation >= 10:
                print(
                    f"You're a high-priority target for all pirate factions! (Reputation: {player.pirate_reputation})")
            elif player.pirate_reputation >= 5:
                print(f"Pirates actively hunt you! (Reputation: {player.pirate_reputation})")
            else:
                print(f"Pirates have marked you as a target. (Reputation: {player.pirate_reputation})")


def add_combat_hazards(game: Game, pirate_type: dict) -> dict:
    """Add environmental hazards that affect combat"""
    hazards = [
        {
            "name": "Asteroid Field",
            "effect": "Navigation penalty",
            "player_modifier": -1,
            "enemy_modifier": -1,
            "description": "Floating debris hampers both ships!"
        },
        {
            "name": "Solar Storm",
            "effect": "Shield interference",
            "player_modifier": -2 if game.player.shields < 3 else -1,
            "enemy_modifier": -1,
            "description": "Solar radiation disrupts shield systems!"
        },
        {
            "name": "Nebula",
            "effect": "Sensor confusion",
            "player_modifier": -1,
            "enemy_modifier": -2,  # Pirates less familiar with area
            "description": "Dense gas clouds obscure targeting systems!"
        },
        {
            "name": "Gravity Well",
            "effect": "Movement restriction",
            "player_modifier": -1 if game.player.engine < 3 else 0,
            "enemy_modifier": -1,
            "description": "Strong gravitational forces limit maneuverability!"
        },
        {
            "name": "Ion Storm",
            "effect": "Weapon interference",
            "player_modifier": -1,
            "enemy_modifier": -1,
            "description": "Electrical interference affects weapon systems!"
        }
    ]

    if random.randint(1, 3) == 1:  # 33% chance of hazard
        hazard = random.choice(hazards)
        print(f"\n=== Combat Hazard: {hazard['name']} ===")
        print(hazard['description'])
        return hazard

    return None


def handle_pirate_encounter(game: Game) -> None:
    """Enhanced pirate encounter system with more challenging mechanics"""
    p = game.player

    # Enhanced pirate types with more varied stats
    pirate_types = [
        {
            "name": "Smuggler",
            "difficulty": 1,
            "reward": (1, 2),
            "special": "stealth",  # Harder to detect, surprise attacks
            "health": 1,
            "description": "A nimble ship used for illegal cargo runs"
        },
        {
            "name": "Raider",
            "difficulty": 2,
            "reward": (2, 4),
            "special": "aggressive",  # Multiple attack phases
            "health": 2,
            "description": "A heavily armed vessel built for quick strikes"
        },
        {
            "name": "Warlord",
            "difficulty": 3,
            "reward": (3, 6),
            "special": "fortified",  # Requires multiple hits to defeat
            "health": 3,
            "description": "A battle-hardened flagship with superior armor"
        },
        {
            "name": "Pirate Fleet",
            "difficulty": 4,
            "reward": (5, 10),
            "special": "multiple",  # Multiple enemies
            "health": 2,
            "description": "Multiple pirate ships coordinating their attack"
        }
    ]

    # Get difficulty scaling
    difficulty_info = get_pirate_encounter_difficulty(p)
    base_difficulty = difficulty_info["base_difficulty"]

    # Select pirate based on player strength and some randomness
    player_strength = p.weapons + p.shields

    # Reputation affects encounter chances
    if p.pirate_reputation > 5:
        # High reputation means stronger pirates actively hunt you
        difficulty_modifier = random.randint(0, 1)
    elif p.pirate_reputation < -5:
        # Feared by pirates, sometimes they avoid you
        if random.randint(1, 10) <= 3:
            print("\nPirates detected your ship and fled!")
            print("Your fearsome reputation precedes you.")
            return
        difficulty_modifier = random.randint(-1, 0)
    else:
        difficulty_modifier = random.randint(-1, 1)

    pirate_index = max(0, min(len(pirate_types) - 1, base_difficulty + difficulty_modifier))
    pirate_type = pirate_types[pirate_index]

    pirate = random.choice(pirate_names)
    print(f"\n{'=' * 50}")
    print(f"🏴‍☠️ {pirate_type['name']} {pirate} attacks!")
    print(f"{'=' * 50}")
    print(f"Ship Type: {pirate_type['description']}")
    print(f"Threat Level: {'*' * pirate_type['difficulty']}")

    # Check for environmental hazards
    hazard = add_combat_hazards(game, pirate_type)

    # Special encounter effects
    if pirate_type["special"] == "stealth":
        print(f"\nSURPRISE ATTACK!")
        print("The smuggler appears out of nowhere using stealth technology!")
        if p.shields < 2:
            print("Your shields are compromised by the surprise attack!")
            pirate_type = pirate_type.copy()
            pirate_type["difficulty"] += 1

    elif pirate_type["special"] == "multiple":
        print(f"\nFLEET ENGAGEMENT!")
        print("Multiple pirate ships surround you!")
        print("This will require all your tactical skills...")

    elif pirate_type["special"] == "fortified":
        print(f"\nHEAVY ARMOR DETECTED!")
        print("This ship has reinforced hull plating!")

    elif pirate_type["special"] == "aggressive":
        print(f"\nAGGRESSIVE TACTICS!")
        print("The raider is using hit-and-run tactics!")

    # Multi-phase combat
    pirate_health = pirate_type["health"]
    combat_rounds = 0
    max_rounds = 4

    print(f"\n--- INITIATING COMBAT ---")
    print(f"Enemy Health: {pirate_health}")
    print(f"Your Weapons: {p.weapons} | Your Shields: {p.shields}")

    while pirate_health > 0 and combat_rounds < max_rounds and game.running:
        combat_rounds += 1
        print(f"\n{'=' * 30}")
        print(f"Combat Round {combat_rounds}")
        print(f"{'=' * 30}")

        # Player attack phase
        base_attack = random.randint(1, 6) + p.weapons
        base_defense = random.randint(1, 6) + pirate_type["difficulty"]

        # Apply hazard modifiers
        if hazard:
            base_attack += hazard.get("player_modifier", 0)
            base_defense += hazard.get("enemy_modifier", 0)

        # Special pirate abilities
        if pirate_type["special"] == "stealth" and combat_rounds == 1:
            base_defense += 2  # Harder to hit initially
        elif pirate_type["special"] == "aggressive":
            base_defense += 1  # Evasive maneuvers
        elif pirate_type["special"] == "fortified":
            base_defense += 1  # Heavy armor
        elif pirate_type["special"] == "multiple":
            base_defense += random.randint(0, 1)  # Coordinated defense

        print(f"Your Attack: {base_attack}")
        print(f"Enemy Defense: {base_defense}")

        if base_attack > base_defense:
            pirate_health -= 1
            damage_dealt = base_attack - base_defense
            print(f"DIRECT HIT! Damage: {damage_dealt}")

            if pirate_health > 0:
                print(f"Enemy ship damaged! Health remaining: {pirate_health}")
                if pirate_type["special"] == "multiple" and pirate_health == 1:
                    print("One of the pirate ships is destroyed!")
            else:
                print(f"Enemy ship destroyed!")
        else:
            miss_margin = base_defense - base_attack
            print(f"Attack missed! Defense margin: {miss_margin}")

            if pirate_type["special"] == "stealth":
                print("The smuggler vanishes into the shadows!")
            elif pirate_type["special"] == "aggressive":
                print("The raider evades with superior speed!")

        if pirate_health <= 0:
            break

        # Pirate counter-attack
        print(f"\n--- Enemy Counter-Attack ---")
        pirate_attack = random.randint(1, 6) + pirate_type["difficulty"]
        player_defense = random.randint(1, 6) + p.shields

        # Apply hazard modifiers (reversed for counter-attack)
        if hazard:
            pirate_attack += hazard.get("enemy_modifier", 0)
            player_defense += hazard.get("player_modifier", 0)

        # Special attack bonuses
        if pirate_type["special"] == "aggressive":
            pirate_attack += 1  # Aggressive assault
        elif pirate_type["special"] == "multiple":
            pirate_attack += random.randint(1, 2)  # Multiple ships attacking

        print(f"Enemy Attack: {pirate_attack}")
        print(f"Your Defense: {player_defense}")

        if pirate_attack > player_defense:
            damage_taken = pirate_attack - player_defense
            print(f"HULL BREACH! Damage taken: {damage_taken}")

            # Ship damage - more severe with higher damage
            damage_rolls = min(3, max(1, damage_taken // 2))
            for i in range(damage_rolls):
                damage_stat = random.choice(["engine", "hold", "shields", "weapons"])
                result = manage_ship_stat(game, damage_stat)
                print(f"System Damage: {result}")

                if not game.running:  # Game ended due to engine damage
                    return

            # Special pirate effects on successful hits
            if pirate_type["special"] == "multiple" and random.randint(1, 3) == 1:
                print("Coordinated assault continues!")
            elif pirate_type["special"] == "aggressive":
                print("⚡ Follow-up strike incoming!")

        else:
            defense_margin = player_defense - pirate_attack
            print(f"Shields hold! Defense margin: {defense_margin}")

            if defense_margin >= 3:
                print("Your superior shielding deflects the attack completely!")

        # Check for critical ship damage
        if p.engine <= 0:
            print("CRITICAL: Engine failure detected!")
            break

        # Offer escape option after round 2
        if combat_rounds >= 2 and pirate_health > 0:
            escape_choice = input("\nAttempt to flee? (y/n): ").lower()
            if escape_choice == 'y':
                escape_roll = random.randint(1, 6) + p.engine + p.shields
                pirate_pursuit = random.randint(1, 6) + pirate_type["difficulty"] + pirate_health

                if escape_roll > pirate_pursuit:
                    print("Successfully escaped to hyperspace!")
                    update_pirate_reputation(p, "escape", pirate_type["name"])
                    return
                else:
                    print("Escape failed! Pirates intercept your ship!")
                    print("Taking damage from pursuit fire!")
                    damage_stat = random.choice(["shields", "engine"])
                    print(manage_ship_stat(game, damage_stat))

    # Combat resolution
    if pirate_health <= 0:
        # Victory
        print(f"\n{'=' * 50}")
        print(f"VICTORY! {pirate_type['name']} {pirate} retreats!")
        print(f"{'=' * 50}")

        min_reward, max_reward = pirate_type['reward']
        bounty_reward = random.randint(min_reward, max_reward)

        # Bonus rewards for extended combat
        if combat_rounds > 2:
            bonus = (combat_rounds - 2) * 2
            bounty_reward += bonus
            print(f"Extended Combat Bonus: +{bonus} bounty points!")

        # Reputation bonus
        if p.pirate_reputation < -10:
            reputation_bonus = 2
            bounty_reward += reputation_bonus
            print(f"Legendary Reputation Bonus: +{reputation_bonus} bounty points!")

        p.bounty_points += bounty_reward
        p.total_bounty_earned += bounty_reward
        update_pirate_reputation(p, "victory", pirate_type["name"])

        print(f"Bounty Awarded: {bounty_reward} points")
        print(f"Total Bounty Points: {p.bounty_points}")

        # Chance for rare loot from harder pirates
        loot_chance = pirate_type["difficulty"] * 25  # 25%, 50%, 75%, 100%
        if random.randint(1, 100) <= loot_chance:
            rare_goods = ["Quantum Cores", "Antimatter Pods", "Void Crystals",
                          "Dark Matter", "Dimensional Fabrics", "Tachyon Batteries"]
            loot = random.choice(rare_goods)

            if sum(p.goods.values()) < p.hold:
                p.goods[loot] = p.goods.get(loot, 0) + 1
                print(f"Rare Salvage Found: {loot}!")
                print("(High-value contraband recovered from pirate ship)")
            else:
                print(f"Found {loot} but your cargo hold is full!")
                print("(Consider upgrading your hold capacity)")

        # Special victory rewards for fleet battles
        if pirate_type["special"] == "multiple":
            print("Fleet Victory Achievement Unlocked!")
            bonus_credits = random.randint(200, 500)
            p.credits += bonus_credits
            print(f"Battle Spoils: +{bonus_credits} credits")

    else:
        # Defeat or timeout
        print(f"\n{'=' * 50}")
        print(f"COMBAT DEFEAT")
        print(f"{'=' * 50}")

        # Attempt to escape based on shields and engine
        escape_attempt = random.randint(1, 6) + p.shields + (p.engine // 2)
        pirate_power = random.randint(1, 6) + pirate_type["difficulty"] + pirate_health

        if escape_attempt > pirate_power:
            print("Emergency Escape Successful!")
            print("Your ship limps away with heavy damage...")
            update_pirate_reputation(p, "escape", pirate_type["name"])

            # Escape damage
            for _ in range(2):
                damage_stat = random.choice(["engine", "hold", "shields", "weapons"])
                result = manage_ship_stat(game, damage_stat)
                print(f"Escape Damage: {result}")
                if not game.running:
                    return
        else:
            print("TOTAL DEFEAT! Pirates board your ship!")
            print("Your vessel is completely overwhelmed...")
            update_pirate_reputation(p, "defeat", pirate_type["name"])

            # Severe penalties for total defeat
            goods_lost = len(p.goods)
            credits_stolen = min(p.credits // 2, 1000)  # Pirates steal up to half credits or 1000

            if goods_lost > 0:
                # Record losses from all stolen goods
                for good, quantity in p.goods.items():
                    if good in p.purchase_records:
                        for purchase_id, price in p.purchase_records[good].items():
                            p.total_profit -= price

                p.goods.clear()
                p.purchase_records.clear()
                print(f"Lost all cargo: {goods_lost} different goods stolen!")

            if credits_stolen > 0:
                p.credits -= credits_stolen
                print(f"Credits stolen: {credits_stolen}")

            # Severe ship damage
            damage_systems = random.randint(2, 4)
            print(f"Critical systems damaged: {damage_systems} components")

            for _ in range(damage_systems):
                damage_stat = random.choice(["engine", "hold", "shields", "weapons"])
                result = manage_ship_stat(game, damage_stat)
                print(f"Critical Damage: {result}")
                if not game.running:
                    return

            # Additional consequence - emergency beacon
            if p.credits >= 100:
                p.credits -= 100
                print("Emergency beacon activated: -100 credits")
                print("(Rescue services charge for emergency assistance)")


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


def generate_procedural_encounter(game: Game, planet: str) -> None:
    """Procedurally generate diverse planet encounters"""
    p = game.player

    # Encounter elements for procedural generation
    locations = [
        "ancient ruins", "crashed ship", "mining facility", "research station",
        "energy anomaly", "crystal formations", "underground caverns", "orbital debris",
        "abandoned outpost", "strange monument", "volcanic vents", "ice fields",
        "fungal forests", "metallic structures", "gravity wells", "temporal rifts"
    ]

    entities = [
        "stranded colonists", "automated drones", "alien artifacts", "energy beings",
        "salvage crew", "research team", "mining robots", "security systems",
        "mysterious signals", "holographic recordings", "ancient guardians", "space nomads",
        "rogue AI", "crystalline entities", "plasma storms", "quantum echoes"
    ]

    situations = [
        "requesting assistance", "offering trade", "malfunctioning dangerously",
        "emitting strange energy", "under attack", "sending distress signals",
        "blocking your path", "revealing hidden secrets", "challenging your skills",
        "offering ancient knowledge", "testing your resolve", "sharing valuable intel",
        "warning of danger", "seeking alliance", "guarding treasure", "demanding tribute"
    ]

    # Action templates for different encounter types
    action_sets = [
        {
            "actions": ["Help them", "Negotiate carefully", "Demand payment"],
            "risk_levels": ["low", "medium", "high"],
            "flavor": "social"
        },
        {
            "actions": ["Investigate closely", "Scan from distance", "Avoid completely"],
            "risk_levels": ["high", "medium", "low"],
            "flavor": "exploration"
        },
        {
            "actions": ["Use force", "Try diplomacy", "Retreat quietly"],
            "risk_levels": ["high", "medium", "low"],
            "flavor": "confrontation"
        },
        {
            "actions": ["Accept the challenge", "Propose alternative", "Decline politely"],
            "risk_levels": ["high", "medium", "low"],
            "flavor": "challenge"
        }
    ]

    # Generate the encounter
    location = random.choice(locations)
    entity = random.choice(entities)
    situation = random.choice(situations)
    action_set = random.choice(action_sets)

    # Create the scenario description
    scenario_desc = f"On {planet}, you discover {location} where {entity} are {situation}."

    print(f"\n==={planet}===")
    print(scenario_desc)

    # Generate outcomes based on risk levels and player stats
    outcomes = []
    for i, (action, risk) in enumerate(zip(action_set["actions"], action_set["risk_levels"])):
        outcome = generate_outcome(risk, action_set["flavor"], p)
        outcomes.append(outcome)

    # Present choices to player
    choice = menu("What do you do?", action_set["actions"])

    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(action_set["actions"]):
            selected_outcome = outcomes[choice_index]
        else:
            selected_outcome = outcomes[0]
    except (ValueError, IndexError):
        selected_outcome = outcomes[0]

    # Apply the outcome
    apply_encounter_outcome(game, selected_outcome)


def generate_outcome(risk_level: str, flavor: str, player) -> dict:
    """Generate an outcome based on risk level and encounter flavor"""

    # Base rewards/penalties by risk level
    risk_modifiers = {
        "low": {"credits": (50, 150), "stat_bonus": 0, "failure_chance": 10},
        "medium": {"credits": (100, 300), "stat_bonus": 1, "failure_chance": 25},
        "high": {"credits": (200, 500), "stat_bonus": 2, "failure_chance": 40}
    }

    modifier = risk_modifiers[risk_level]
    success = random.randint(1, 100) > modifier["failure_chance"]

    if success:
        outcome = generate_success_outcome(modifier, flavor, player)
    else:
        outcome = generate_failure_outcome(modifier, flavor, player)

    return outcome


def generate_success_outcome(modifier: dict, flavor: str, player) -> dict:
    """Generate a successful outcome"""
    outcomes = []

    # Credit rewards
    credits = random.randint(modifier["credits"][0], modifier["credits"][1])

    # Flavor-specific success messages and bonuses
    if flavor == "social":
        messages = [
            f"Your diplomatic skills pay off! Gained {credits} credits.",
            f"The locals are grateful and reward you with {credits} credits.",
            f"Successful negotiations earn you {credits} credits and respect."
        ]
        if modifier["stat_bonus"] > 0:
            bonus_stat = random.choice(["shields", "hold"])
            return {
                "type": "success",
                "text": random.choice(messages) + f" They also upgrade your {bonus_stat}!",
                "credits": credits,
                "stat": bonus_stat,
                "stat_amount": modifier["stat_bonus"]
            }

    elif flavor == "exploration":
        messages = [
            f"Your investigation reveals valuable data worth {credits} credits.",
            f"You discover ancient technology! Gained {credits} credits.",
            f"Careful exploration yields {credits} credits in salvage."
        ]
        if modifier["stat_bonus"] > 0:
            bonus_stat = random.choice(["engine", "weapons"])
            return {
                "type": "success",
                "text": random.choice(messages) + f" Your {bonus_stat} system is enhanced!",
                "credits": credits,
                "stat": bonus_stat,
                "stat_amount": modifier["stat_bonus"]
            }

    elif flavor == "confrontation":
        messages = [
            f"You emerge victorious! Claimed {credits} credits in bounty.",
            f"Your show of force succeeds! Earned {credits} credits.",
            f"Decisive action nets you {credits} credits and reputation."
        ]
        if modifier["stat_bonus"] > 0:
            bonus_stat = random.choice(["weapons", "shields"])
            return {
                "type": "success",
                "text": random.choice(messages) + f" Battle experience improves your {bonus_stat}!",
                "credits": credits,
                "stat": bonus_stat,
                "stat_amount": modifier["stat_bonus"]
            }

    elif flavor == "challenge":
        messages = [
            f"You meet the challenge! Rewarded with {credits} credits.",
            f"Your skills impress everyone! Gained {credits} credits.",
            f"Challenge completed successfully! Earned {credits} credits."
        ]
        if modifier["stat_bonus"] > 0 and random.randint(1, 100) <= 30:
            # Chance for rare goods as challenge reward
            return {
                "type": "success",
                "text": random.choice(messages) + " You also receive rare goods!",
                "credits": credits,
                "goods": True
            }

    return {
        "type": "success",
        "text": random.choice(messages),
        "credits": credits
    }


def generate_failure_outcome(modifier: dict, flavor: str, player) -> dict:
    """Generate a failure outcome"""

    # Failure penalties (reduced based on player stats)
    base_penalty = modifier["credits"][0] // 2

    # Player's skills can reduce penalties
    skill_reduction = 0
    if flavor == "social" and player.credits > 5000:
        skill_reduction = base_penalty // 3
    elif flavor == "exploration" and player.engine >= 3:
        skill_reduction = base_penalty // 3
    elif flavor == "confrontation" and player.weapons >= 3:
        skill_reduction = base_penalty // 3
    elif flavor == "challenge" and player.shields >= 3:
        skill_reduction = base_penalty // 3

    penalty = max(0, base_penalty - skill_reduction)

    failure_messages = {
        "social": [
            f"Negotiations fail. Lost {penalty} credits in bribes.",
            f"Cultural misunderstanding costs you {penalty} credits.",
            f"Diplomatic incident results in {penalty} credit fine."
        ],
        "exploration": [
            f"Equipment malfunction costs {penalty} credits to repair.",
            f"Dangerous exploration damages ship. Repair costs {penalty} credits.",
            f"You trigger a trap! Emergency repairs cost {penalty} credits."
        ],
        "confrontation": [
            f"Retreat necessary. Lost {penalty} credits in damages.",
            f"Outmatched! Forced to pay {penalty} credits to escape.",
            f"Combat damage requires {penalty} credits in repairs."
        ],
        "challenge": [
            f"Challenge failed. Penalty of {penalty} credits.",
            f"Unable to complete task. Forfeit {penalty} credits.",
            f"Failure results in {penalty} credit loss."
        ]
    }

    return {
        "type": "failure",
        "text": random.choice(failure_messages[flavor]),
        "credits": -penalty
    }


def apply_encounter_outcome(game: Game, outcome: dict) -> None:
    """Apply the outcome of an encounter to the game state"""
    p = game.player

    print(f"\n{outcome['text']}")

    # Apply credits
    if "credits" in outcome:
        p.credits += outcome["credits"]
        if outcome["credits"] < 0:
            p.credits = max(0, p.credits)  # Don't go negative

    # Apply stat bonuses
    if "stat" in outcome and "stat_amount" in outcome:
        for _ in range(outcome["stat_amount"]):
            print(manage_ship_stat(game, outcome["stat"], True))

    # Apply goods
    if "goods" in outcome and outcome["goods"]:
        good = random.choice(goods_list)
        p.goods[good] = p.goods.get(good, 0) + 1
        print(f"Added {good} to cargo!")

    # Show current status
    print(f"Credits: {p.credits} cr")


def handle_encounter(game: Game, encounter_type: str) -> None:
    """Handle different types of encounters during exploration"""
    if encounter_type == "planet":
        planet = random.choice(planet_names)
        encounter_roll = random.randint(1, 100)

        if encounter_roll <= 20:
            # Pirate encounter on planet
            handle_pirate_encounter(game)
        elif encounter_roll <= 40:
            # Trader encounter on planet
            trader_name = random.choice(trader_names)
            print(f"\nYou encounter {trader_name} on {planet}!")
            trade(game)
        else:
            # Procedural boon encounter (60% chance)
            generate_procedural_encounter(game, planet)

    elif encounter_type == "pirate":
        handle_pirate_encounter(game)

    elif encounter_type == "trader":
        print(f"\nYou encounter a friendly trader out in space!")
        trade(game)

    elif encounter_type == "empty":
        print("\nYou drift through empty space...")
        print("Nothing but stars and silence.")


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
    choice = menu("Ship Computer",
                  ["Instructions", "Ship Status", "Trading Stats", "Bounty Stats", "Pirate Intel", "Rename Ship",
                   "Rename Captain", "Exit Game"])

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
        view_pirate_intel(p)

    elif choice == "6":
        p.ship_name = input("\nNew ship name: ")
        print(f"Ship renamed to {p.ship_name}")

    elif choice == "7":
        p.captain_name = input("\nNew captain name: ")
        print(f"Captain renamed to {p.captain_name}")

    elif choice == "8":
        print("\nExiting game...")
        game.running = False
        return


def view_pirate_intel(player: Player) -> None:
    """Display pirate intelligence and reputation information"""
    print("\n===== Pirate Intelligence Report =====")
    print(f"Pirate Reputation: {player.pirate_reputation}")

    if player.pirate_reputation <= -15:
        rep_status = "LEGENDARY PIRATE HUNTER - Pirates flee at your approach"
    elif player.pirate_reputation <= -10:
        rep_status = "FEARED HUNTER - Well-known pirate killer"
    elif player.pirate_reputation <= -5:
        rep_status = "KNOWN THREAT - Pirates are cautious around you"
    elif player.pirate_reputation >= 15:
        rep_status = "HIGH-VALUE TARGET - All factions actively hunt you"
    elif player.pirate_reputation >= 10:
        rep_status = "MARKED FOR DEATH - Multiple bounties on your head"
    elif player.pirate_reputation >= 5:
        rep_status = "PERSON OF INTEREST - Pirates seek revenge"
    else:
        rep_status = "UNKNOWN - No significant reputation"

    print(f"Status: {rep_status}")

    # Calculate threat assessment
    difficulty_info = get_pirate_encounter_difficulty(player)
    threat_level = difficulty_info["base_difficulty"]

    print(f"\nThreat Assessment Level: {threat_level}/4")
    print(f"Expected Pirate Types:")

    if threat_level >= 4:
        print("  - Pirate Fleets (Multiple coordinated ships)")
        print("  - Warlord Flagships (Heavily armored)")
    if threat_level >= 3:
        print("  - Warlord Ships (Battle-hardened)")
    if threat_level >= 2:
        print("  - Raider Vessels (Aggressive tactics)")
    if threat_level >= 1:
        print("  - Smuggler Ships (Stealth attacks)")

    encounter_chance = int(difficulty_info["encounter_chance"] * 100)
    print(f"\nPirate Encounter Probability: {encounter_chance}%")

    if difficulty_info["fleet_chance"] > 0:
        fleet_chance = int(difficulty_info["fleet_chance"] * 100)
        print(f"Fleet Encounter Chance: {fleet_chance}%")

    print(f"\nCombat Statistics:")
    print(f"Total Bounty Earned: {player.total_bounty_earned}")
    print(f"Current Bounty Points: {player.bounty_points}")
    print(f"Bounty Points Redeemed: {player.bounty_redeemed}")

    input("\nPress Enter to continue...")


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

    choice = menu("===== Celastra Exchange ======",
                  ["Buy Goods", "Sell Goods", "Upgrade Ship", "Ship Computer", "Casino", "Bounty Office",
                   "Launch Ship"])

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

    print("Welcome to Space Trader !")
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

    # Enhanced pirate information
    print(f"\nBounty Hunter Career:")
    print(f"Total Bounty Points Earned: {p.total_bounty_earned}")
    print(f"Bounty Points Redeemed: {p.bounty_redeemed}")
    print(f"Unredeemed Bounty Points: {p.bounty_points}")
    print(f"Final Pirate Reputation: {p.pirate_reputation}")

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
