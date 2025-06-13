.PHONY: install run test server backup-db docker-build docker-up docker-down docker-logs docker-shell docker-backup

# Install dependencies and set up the project
install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

# Run the game
run:
	@echo "Running Space Trader..."
	@python3 game.py

# Run the persistent server
server:
	@echo "Starting Space Trader server..."
	@python3 server.py

# Backup the game database
backup-db:
	@echo "Backing up database..."
	@cp space_trader.db space_trader_backup_$(shell date +%Y%m%d).db

# Run unit tests
test:
	@echo "Running unit tests..."
	@python3 -m unittest discover -s tests

# Docker commands
# Build the Docker image
docker-build:
	@echo "Building Docker image..."
	@docker-compose build

# Start the Docker container
docker-up:
	@echo "Starting Docker container..."
	@docker-compose up -d
	@echo "Container started on port 3000"

# Stop the Docker container
docker-down:
	@echo "Stopping Docker container..."
	@docker-compose down

# View Docker container logs
docker-logs:
	@echo "Showing container logs..."
	@docker-compose logs -f

# Enter shell in the running container
docker-shell:
	@echo "Opening shell in container..."
	@docker-compose exec space-trader /bin/bash

# Backup the database from the Docker volume
docker-backup:
	@echo "Backing up database from Docker volume..."
	@mkdir -p backups
	@docker-compose exec space-trader cp /data/space_trader.db /data/space_trader_backup_$(shell date +%Y%m%d).db
	@echo "Database backed up to data/space_trader_backup_$(shell date +%Y%m%d).db"

# All-in-one command to build and start
docker-start: docker-build docker-up
	@echo "Space Trader Docker container built and started"