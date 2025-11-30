# Space Trader

### The Attack of Fang on the *Intrepid*

The stars glittered like shards of broken glass across the endless void, as *Reynolds* commanded the *Intrepid*, her trusted starship, through the uncharted regions of the galaxy. Suddenly, alarms blared. Fang, the notorious pirate of the Zarvor Belt, had found them. His ship appeared out of nowhere, engines roaring like a beast let loose. Laser fire lit up the cockpit. Shields were holding, but just barely. Reynolds gritted her teeth as she steered hard, trying to outmaneuver the pirate's barrage. In a moment of brilliance, the *Intrepid*'s weapons fired back, and Fang was gone, retreating into the shadows of space. Victory belonged to the *Intrepid*, but out there in the cold expanse, another battle was always just a heartbeat away...

---

## About the Game

**Space Trader** is a text-based trading and exploration game set in a procedurally generated universe. You take the role of a space trader named *Reynolds*, commanding your starship *Intrepid*.

The game consists of a game engine, game.py, which can be played from a terminal emulator. There is also a server engine, which can host a multiplayer persistent game world. The server engine uses ASCII encoding as it has been designed to be accessed over older clients (such as telnet). There are also three ports with simpler gameplay: micropython versions for the Numworks calculator and M5Stack Cardputer, and a javascript version. 

Your journey begins at the age of 30, and the game ends when you retire, aged 60, from the Trading Guild. Due to hibernation you only age when docked at the Galactic Exchange. Your final score is based on the credits you have accrued.

### Features:
- Procedurally generated encounters including pirates, traders, and planets.
- Ship upgrades: engine, hold, shields, and weapons.
- Boons from planetary encounters that improve your ship.
- Engage in battles with pirates or negotiate trades.
- Manage your resources and goods with the limited hold of your ship.
- Name your ship and captain.
- Gamble at the Quantum Casino
- Receive a rank on retirement
- **NEW**: Persistent game server with player accounts and saved games

---

## How to Play

### Starting Your Journey

You begin your career as a space trader at age 30 with 1000 credits and a basic starship called the *Intrepid*. Your goal is to accumulate as much wealth as possible before mandatory retirement at age 60. Time only passes while you're docked at the Celastra Exchange space station due to hibernation during space travel.

### The Celastra Exchange - Your Home Base

Each turn begins at the Celastra Exchange, a massive space station that serves as your trading hub. Here you can:

#### 1. Trading Operations
- **Buy Goods**: Purchase commodities from visiting traders. Available goods change each turn and include items like Plasma, Void Ore, Warp Cells, Nanites, and more exotic materials.
- **Sell Goods**: Sell your cargo to traders for profit. Prices fluctuate based on supply and demand.
- **Trade Tax**: Each transaction costs 5 credits in trade taxes. Plan your trades carefully!

#### 2. Ship Upgrades
Invest your profits in upgrading your ship's systems:
- **Engine** (500 credits): Increases the number of encounters per exploration turn (1-4 encounters)
- **Hold** (300 credits): Expands cargo capacity, allowing you to carry more goods
- **Shields** (400 credits): Improves defensive capabilities in combat
- **Weapons** (400 credits): Enhances offensive power against pirates

#### 3. Additional Services
- **Quantum Casino**: Test your luck with various gambling games to potentially multiply your credits
- **Bounty Office**: Exchange bounty points earned from defeating pirates for credits (100 credits per point)
- **Ship Computer**: Access ship status, rename your vessel or captain, view trading statistics, and get help

#### 4. Docking Fees
Every time you dock at the Celastra Exchange, you must pay 20 credits in docking fees. If you can't afford this fee, your ship will be impounded and the game ends.

### Space Exploration

When you launch from the exchange, your adventures begin! The number of encounters depends on your engine rating:

#### Types of Encounters

**1. Pirate Attacks**
- Face off against notorious space pirates with names like Havok, Kane, Fang, and Blaze
- Pirates are categorized by difficulty:
  - **Smugglers**: Weaker pirates offering 1-2 bounty points
  - **Raiders**: Medium threat pirates offering 2-4 bounty points  
  - **Warlords**: Dangerous pirates offering 3-6 bounty points
- Combat outcomes depend on your weapons and shields:
  - **Victory**: Earn bounty points and reputation
  - **Escape**: Avoid destruction but may suffer ship damage
  - **Defeat**: Lose cargo and suffer significant ship damage

**2. Trader Encounters**
- Meet traveling merchants in the depths of space
- Opportunity to buy rare goods at potentially better prices than the exchange
- These encounters don't incur the 5-credit trade tax

**3. Planetary Exploration**
Visit mysterious worlds with names like Zanxor, Novus, Kalrix, and Velor. Planet encounters can result in:
- **Beneficial Discoveries**: Receive ship upgrades (engine, hold, shields, or weapons improved by 1)
- **Pirate Ambushes**: Face pirate attacks while exploring
- **Merchant Meetings**: Trade opportunities with planetary merchants

**4. Empty Space**
Sometimes you'll encounter nothing but the vast emptiness of space. These moments provide time to contemplate your next moves.

### Combat System

Combat with pirates involves multiple factors:

#### Combat Capabilities
- **Weapons**: Determine your offensive power and which tier of pirates you can effectively fight
- **Shields**: Provide defensive protection and escape options
- **Reputation**: Your pirate-fighting reputation affects encounter difficulty

#### Combat Hazards
Combat isn't just about winning or losing - various hazards can occur:
- **System Damage**: Ship systems (engine, hold, shields, weapons) can be damaged
- **Cargo Loss**: Defeat may result in losing valuable goods
- **Critical Failures**: Engine damage can leave you stranded in space (game over)

#### Battle Outcomes
- **Dominant Victory**: Complete success with no damage
- **Victory**: Win the fight but may suffer minor damage
- **Narrow Escape**: Avoid destruction but likely suffer damage
- **Defeat**: Lose goods and suffer significant ship damage

### Economy and Trading

#### Market Dynamics
- Goods prices fluctuate between visits to the exchange
- Different traders offer different goods at varying prices
- Space encounters often provide better trading opportunities than the exchange

#### Goods Management
- Your hold capacity limits how much cargo you can carry
- If your hold is damaged and reduced below your current cargo, excess goods are automatically jettisoned
- Keep track of your purchase prices to calculate profits

#### Financial Considerations
- **Trade Tax**: 5 credits per transaction at the exchange
- **Docking Fees**: 20 credits each time you dock
- **Upgrade Costs**: Plan your ship improvements carefully
- **Emergency Funds**: Always maintain enough credits for docking fees

### Progression and Strategy

#### Early Game (Ages 30-40)
- Focus on basic trading to build capital
- Upgrade your hold first to carry more goods
- Avoid high-risk pirate encounters until better equipped

#### Mid Game (Ages 40-50)
- Invest in weapons and shields for profitable pirate hunting
- Upgrade your engine for more encounters per turn
- Take calculated risks for higher rewards

#### Late Game (Ages 50-60)
- Focus on maximizing profit per turn
- Hunt high-value pirates for bounty points
- Balance risk vs. reward as retirement approaches

### Game End and Scoring

The game ends when you reach age 60 or if certain catastrophic events occur:

#### Natural Retirement (Age 60)
- Receive a comprehensive career summary
- View total credits, profit, and trades completed
- Get assigned a trader rank based on performance
- Final score calculated using an enhanced algorithm

#### Game Over Conditions
- Ship impounded for unpaid docking fees
- Ship impounded for unpaid trade taxes
- Engine completely destroyed (stranded in space)

#### Scoring System
Your final score considers:
- Total credits accumulated
- Total profit earned
- Number of successful trades
- Bounty points earned
- Risk-adjusted performance metrics

### Special Commands (Server Mode)

When playing on the persistent server, additional commands are available:
- `/save` - Save your current game progress
- `/quit` - Save and exit the game safely  
- `/help` - Display available commands

### Tips for Success

1. **Manage Your Finances**: Always keep enough credits for docking fees and trade taxes
2. **Diversify Income**: Combine trading profits with bounty hunting
3. **Upgrade Strategically**: Engine and hold upgrades often provide the best return on investment
4. **Know Your Limits**: Don't fight pirates beyond your ship's capabilities
5. **Explore Planets**: Planetary boons can provide valuable free upgrades
6. **Track Market Trends**: Remember profitable trade routes and good prices
7. **Plan for Retirement**: Your final years are crucial for maximizing your score

The galaxy awaits, Captain. Make your fortune among the stars!

---

## Installation

### Requirements
This project uses Python 3.9+ and dependency management is handled by [Poetry](https://python-poetry.org/).

To install dependencies, run:
```shell
poetry install
```
Or if you're not using Poetry:
```shell
pip install -r requirements.txt
```

## Running the Game

### Single-Player Mode
To start the game in single-player mode, run:

```shell
poetry run python game.py
```

### Persistent Server Mode

#### Starting the Server

To start the persistent game server:

```shell
poetry run python server.py
```

Or use the provided shell script

```shell
bash ./start_server.sh
```

To connect to the game server, run:

```shell
telnet bash telnet 127.0.0.1 3000
```

#### Running as a Background Service
To run the server as a background service on Linux:

1. Create a systemd service file:

```shell
sudo nano /etc/systemd/system/spacetrader.service
```

2. Add the following content (update paths as needed):

```shell
[Unit]
Description=Space Trader Game Server
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/spacetrader
ExecStart=/path/to/spacetrader/start_server.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:

```shell
sudo systemctl enable spacetrader.service
sudo systemctl start spacetrader.service

```

4. Check the status:

```shell
sudo systemctl status spacetrader.service
```

#### Database Setup
The server automatically creates and initializes the database the first time it runs. The database file (`space_trader.db`) will be created in the same directory as the server script.

#### Server Configuration
By default, the server runs on port 3000 and binds to all network interfaces (0.0.0.0). To change these settings, modify the `start_server()` function in `server.py`.

### Server Maintenance

#### Database Backup

It's recommended to regularly back-up the database file:

```shell
# Manual backup
cp space_trader.db space_trader_backup_$(date +%Y%m%d).db

# Automated daily backup (add to crontab)
# 0 0 * * * cd /path/to/spacetrader && cp space_trader.db space_trader_backup_$(date +%Y%m%d).db
```

### Server Commands
While the server is running, players can use special commands during gameplay:
- `/save` - Save the current game state
- `/quit` - Save and exit the game
- `/help` - Show available commands

### Monitoring and Troubleshooting

#### Checking Server Status

```shell
ps aux | grep server.py
```

#### Viewing Logs

If running as a systemd service:

```shell
sudo journalctl -u spacetrader.service -f
```

#### Common Issues
1. **Database Locked**: If the server crashes, the database might remain locked. Delete the `.space_trader.db-journal` file if it exists.
2. **Port Already in Use**: If port 3000 is already in use, change the port in . `server.py`
3. **Connection Issues**: Ensure your firewall allows connections on port 3000.

#### Security Considerations
- The server stores passwords securely using bcrypt hashing
- Consider setting up a firewall to restrict access to the server
- For public servers, consider adding rate limiting to prevent brute force attacks

## Docker Implementation

### Running with Docker

Space Trader can be run in a Docker container, providing an isolated and consistent environment across different systems. This is especially useful for running the persistent server mode.

### Requirements
- Docker installed on your system
- Docker Compose (usually included with Docker Desktop)

### Docker Setup

The project includes a Dockerfile and docker-compose.yml configuration for easy containerization.

#### Container Features:
- Lightweight Ubuntu-based image
- Runs the Space Trader server on port 3000
- Persistent database storage using a Docker volume
- Automatic restart on failure

### Running with Docker

We've added Docker commands to the Makefile for easy management:

```shell
# Build and start the container
make docker-start
# Stop the container
make docker-down
# View container logs
make docker-logs
# Open a shell inside the container
make docker-shell
# Backup the database from inside the container
make docker-backup
``` 

### Manual Docker Commands

If you prefer not to use the Makefile, you can use these Docker Compose commands directly:

```shell
# Build the Docker image
docker-compose build
# Start the container in detached mode
docker-compose up -d
# Stop the container
docker-compose down
# View logs
docker-compose logs -f
# Execute commands in the running container
docker-compose exec space-trader /bin/bash
``` 

### Database Persistence

The Docker setup stores the database in a volume mapped to the `./data` directory in your project folder. This ensures your game data persists even if the container is removed.

### Customizing the Docker Setup

To modify the Docker configuration:

1. Edit the `Dockerfile` to change the base image or install additional dependencies
2. Modify `docker-compose.yml` to change port mappings or add environment variables
3. Rebuild the container with `make docker-build` or `docker-compose build`

### Running in Production

For running the dockerized server in production:

1. Consider using a reverse proxy like Nginx for SSL termination
2. Set up proper firewall rules to only expose the necessary port
3. Configure regular database backups using `make docker-backup` in a cron job

```shell
# Example cron job for daily backups (add to crontab)
0 0 * * * cd /path/to/spacetrader && make docker-backup
``` 

### Troubleshooting Docker Setup

#### Container fails to start
Check the logs with `make docker-logs` or `docker-compose logs`

#### Database corruption
1. Stop the container: `make docker-down`
2. Check the data directory for journal files
3. Restore from a backup if necessary
4. Restart the container: `make docker-up`

#### Port conflicts
If port 3000 is already in use, edit the `docker-compose.yml` file to map to a different port:

```yaml
ports:
  - "3001:3000"  # Maps container port 3000 to host port 3001
```

Enjoy your journey through the stars, Captain!
