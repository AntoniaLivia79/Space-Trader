# Space Trader

### The Attack of Fang on the *Intrepid*

The stars glittered like shards of broken glass across the endless void, as *Reynolds* commanded the *Intrepid*, her trusted starship, through the uncharted regions of the galaxy. Suddenly, alarms blared. Fang, the notorious pirate of the Zarvor Belt, had found them. His ship appeared out of nowhere, engines roaring like a beast let loose. Laser fire lit up the cockpit. Shields were holding, but just barely. Reynolds gritted her teeth as she steered hard, trying to outmaneuver the pirate’s barrage. In a moment of brilliance, the *Intrepid*’s weapons fired back, and Fang was gone, retreating into the shadows of space. Victory belonged to the *Intrepid*, but out there in the cold expanse, another battle was always just a heartbeat away...

---

## About the Game

**Space Trader** is a terminal-based, text-based trading and exploration game set in a procedurally generated universe. You take the role of a space trader named *Reynolds*, commanding your starship *Intrepid*.

Your journey begins at the age of 30, and the game ends when you retire, aged 60, from the Trading Guild. Due to hibernation you only age when docked at the Galactic Exchange. Your final score is based on the credits you have accrued.

### Features:
- Procedurally generated encounters including pirates, traders, and planets.
- Ship upgrades: engine, hold, shields, and weapons.
- Boons from planetary encounters that improve your ship.
- Engage in battles with pirates or negotiate trades.
- Manage your resources and goods with the limited hold of your ship.
- Name your ship and captain.

---

## How to Play

1. Start with 1000 credits.
2. At each turn, you'll visit the Galactic Exchange where you can:
   - Buy Goods
   - Sell Goods
   - Upgrade your Ship
   - Edit the Captain's Log - Save/Load your game, change captain name or ship name and view your stats
   - Launch your ship to begin exploration
3. During exploration, you'll face 1 to 4 encounters based on your engine stat:
   - Pirate Attack
   - Meet a Trader
   - Explore a Planet (you may encounter pirates, traders, or receive a boon)
   - Empty Space

### Ship Stats:
- **Engine**: Determines the number of encounters per turn.
- **Hold**: Dictates how many goods you can carry.
- **Shields**: Helps defend your ship in battle.
- **Weapons**: Affects your offensive power in battles.

## Installation

### Requirements
This project uses Python 3.9+ and dependency management is handled by [Poetry](https://python-poetry.org/).

To install dependencies, run:
```bash
poetry install
```

## Running the Game

To start the game, run:
```bash
poetry run python -m game.py
```  

To start the server, run:
```bash
poetry run python -m server.py
```

To connect to game server, run:
```bash
telnet 127.0.0.1 3000
```
