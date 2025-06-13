# Space Trader

### The Attack of Fang on the *Intrepid*

The stars glittered like shards of broken glass across the endless void, as *Reynolds* commanded the *Intrepid*, her trusted starship, through the uncharted regions of the galaxy. Suddenly, alarms blared. Fang, the notorious pirate of the Zarvor Belt, had found them. His ship appeared out of nowhere, engines roaring like a beast let loose. Laser fire lit up the cockpit. Shields were holding, but just barely. Reynolds gritted her teeth as she steered hard, trying to outmaneuver the pirate's barrage. In a moment of brilliance, the *Intrepid*'s weapons fired back, and Fang was gone, retreating into the shadows of space. Victory belonged to the *Intrepid*, but out there in the cold expanse, another battle was always just a heartbeat away...

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
- Gamble at the Quantum Casino
- Receive a rank on retirement
- **NEW**: Persistent game server with player accounts and saved games

---

## How to Play

1. Start with 1000 credits.
2. At each turn, you'll visit the Celastra Exchange space station where you can:
   - Buy Goods
   - Sell Goods
   - Upgrade your Ship
   - Enter the Quantum Casino
   - Use the Ship Computer - Change captain name or ship name and view your stats
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



