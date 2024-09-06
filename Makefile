.PHONY: install run test

# Install dependencies and set up the project
install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

# Run the game
run:
	@echo "Running Space Trader..."
	@python3 game.py

# Run unit tests
test:
	@echo "Running unit tests..."
	@python3 -m unittest discover -s tests
