import socket
import threading
import sqlite3
import json
import uuid
import bcrypt
from datetime import datetime
from typing import Optional
from game import Game, exchange, calculate_final_score

# Database setup
DB_PATH = "space_trader.db"

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_login TEXT
    )
    ''')
    
    # Create game_states table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_states (
        username TEXT PRIMARY KEY,
        game_data TEXT NOT NULL,
        saved_at TEXT NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    ''')
    
    # Create active sessions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        started_at TEXT NOT NULL,
        last_activity TEXT NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash a password for storing"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verify a stored password against a provided password"""
    return bcrypt.checkpw(provided_password.encode(), stored_hash.encode())

def register_user(username: str, password: str) -> bool:
    """Register a new user in the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False
        
        # Create new user
        password_hash = hash_password(password)
        now = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, password_hash, now)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user against the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result and verify_password(result[0], password):
            # Update last login time
            now = datetime.now().isoformat()
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE username = ?",
                (now, username)
            )
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return False

def create_session(username: str) -> str:
    """Create a new session for a user"""
    try:
        session_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO sessions (session_id, username, started_at, last_activity) VALUES (?, ?, ?, ?)",
            (session_id, username, now, now)
        )
        
        conn.commit()
        conn.close()
        return session_id
    except Exception as e:
        print(f"Error creating session: {e}")
        return ""

def update_session_activity(session_id: str) -> bool:
    """Update the last activity time for a session"""
    try:
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE sessions SET last_activity = ? WHERE session_id = ?",
            (now, session_id)
        )
        
        conn.commit()
        conn.close()

        return True
    except Exception as e:
        print(f"Error updating session: {e}")
        return False

def end_session(session_id: str) -> bool:
    """End a user session"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error ending session: {e}")
        return False

def save_game_state(username: str, game: Game) -> bool:
    """Save the current game state for a user"""
    try:
        # Serialize the game object to JSON
        game_dict = {
            "player": game.player.__dict__,
            "exchange": game.exchange,
            "running": game.running
        }
        game_json = json.dumps(game_dict)
        
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if a save already exists
        cursor.execute("SELECT username FROM game_states WHERE username = ?", (username,))
        if cursor.fetchone():
            # Update existing save
            cursor.execute(
                "UPDATE game_states SET game_data = ?, saved_at = ? WHERE username = ?",
                (game_json, now, username)
            )
        else:
            # Create new save
            cursor.execute(
                "INSERT INTO game_states (username, game_data, saved_at) VALUES (?, ?, ?)",
                (username, game_json, now)
            )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving game state: {e}")
        return False

def delete_player_state(username: str) -> bool:
    """Delete the player's game state (on game loss)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM game_states WHERE username = ?", (username,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting player state: {e}")
        return False

def load_game_state(username: str) -> Optional[Game]:
    """Load a saved game state for a user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT game_data, saved_at FROM game_states WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return None
        
        game_json, saved_at = result
        game_dict = json.loads(game_json)
        
        # Create a new game and populate it with saved data
        game = Game()
        game.running = game_dict["running"]
        game.exchange = game_dict["exchange"]
        game.server_game = True
        
        # Handle player data
        player_dict = game_dict["player"]
        for key, value in player_dict.items():
            setattr(game.player, key, value)
        
        conn.close()
        return game
    except Exception as e:
        print(f"Error loading game state: {e}")
        return None

def handle_client(client_socket):
    """Handle a connected client"""
    session_id = None
    username = None
    game = None
    
    # Define the mock I/O functions at the top level so they're available throughout
    def send_message(msg):
        client_socket.send(f"{msg}\r\n".encode('ascii', errors='replace'))
    
    def mock_print(text, **kwargs):
        try:
            client_socket.send((str(text) + "\r\n").encode('ascii', errors='replace'))
        except Exception:
            pass

    def mock_input(prompt=""):

        # Send the prompt
        if prompt and not prompt.endswith('\r\n'):
            prompt += ' '
        client_socket.send(prompt.encode('ascii', errors='replace'))

        # Read data character by character with proper echoing
        data = b""
        while True:
            try:
                chunk = client_socket.recv(1)
                if not chunk:
                    break

                # Handle backspace (ASCII 8 or 127)
                if chunk in [b'\x08', b'\x7f']:
                    if data:
                        data = data[:-1]
                        # Send backspace sequence to erase character on client
                        client_socket.send(b'\x08 \x08')
                    continue

                # Check for line endings
                if chunk in [b'\n', b'\r']:
                    # Send newline back for proper line ending
                    client_socket.send(b'\r\n')
                    break

                # Add to our data buffer
                data += chunk

                # Echo the character back to the client immediately
                client_socket.send(chunk)

            except socket.timeout:
                break
            except Exception:
                break

        response = data.decode('ascii', errors='replace').strip()

        # Auto-save after every input
        if game and game.running:
            save_game_state(username, game)

        # Update session activity
        if session_id:
            update_session_activity(session_id)

        return response

    def receive_input(prompt="", hide_input=False):
        if prompt:
            send_message(prompt)

        # Read data character by character and echo back
        data = b""
        while True:
            try:
                chunk = client_socket.recv(1)
                if not chunk:
                    break

            # Handle backspace (ASCII 8 or 127)
                if chunk in [b'\x08', b'\x7f']:
                    if data:
                        data = data[:-1]
                        # Send backspace sequence to erase character
                        client_socket.send(b'\x08 \x08')
                    continue

                # Check for line endings
                if chunk in [b'\n', b'\r']:
                # Send carriage return/newline after input is complete
                    client_socket.send(b'\r\n')
                    break

                data += chunk

                # Echo the character back to the client (unless hiding input)
                if not hide_input:
                    client_socket.send(chunk)
                else:
                # For hidden input, show asterisk
                    client_socket.send(b'*')

            except socket.timeout:
                break
            except Exception:
                break

        return data.decode('ascii', errors='replace').strip()

    try:
        def receive_input(prompt="", hide_input=False):
            if prompt:
                send_message(prompt)

            # Read data character by character and echo back
            data = b""
            while True:
                try:
                    chunk = client_socket.recv(1)
                    if not chunk:
                        break

                    # Handle backspace (ASCII 8 or 127)
                    if chunk in [b'\x08', b'\x7f']:
                        if data:
                            data = data[:-1]
                            # Send backspace sequence to erase character
                            client_socket.send(b'\x08 \x08')
                        continue

                    # Check for line endings
                    if chunk in [b'\n', b'\r']:
                        break

                    data += chunk

                    # Echo the character back to the client (unless hiding input)
                    if not hide_input:
                        client_socket.send(chunk)
                    else:
                        # For hidden input, show asterisk
                        client_socket.send(b'*')

                except socket.timeout:
                    break
                except Exception:
                    break

            return data.decode('ascii', errors='replace').strip()

        # Welcome message
        send_message("Welcome to Space Trader !")

        # Handle login/registration
        while not username:
            send_message("\nPlease select an option:")
            send_message("1. Login")
            send_message("2. Register")
            send_message("3. View Active Traders")
            send_message("4. Quit")

            choice = receive_input("Choice: ")
            # first input has escape characters at beginning of string
            choice = choice[-1]

            if choice == "1":  # Login
                send_message("\n")
                username_attempt = receive_input("Username: ")
                send_message("\n")
                password = receive_input("Password: ", hide_input=True)
                send_message("\n")

                if authenticate_user(username_attempt, password):
                    username = username_attempt
                    session_id = create_session(username)
                    send_message(f"Welcome back, {username}!")

                    # Check for saved game
                    saved_game = load_game_state(username)
                    if saved_game:
                        send_message("Found a saved game.")
                        send_message("Would you like to continue your saved game?")
                        load_choice = receive_input("1. Yes 2. No: ")
                        send_message("\n")

                        if load_choice == "1":
                            game = saved_game
                            send_message(f"Game loaded!")
                        else:
                            game = Game()  # Start fresh
                            send_message("\nStarting a new game...")
                    else:
                        game = Game()  # No saved game found
                        send_message("No saved game found. Starting a new game...")
                else:
                    send_message("Invalid username or password. Please try again.")

            elif choice == "2":  # Register
                send_message("\n")
                new_username = receive_input("Choose a username: ")
                send_message("\n")
                new_password = receive_input("Choose a password: ", hide_input=True)
                send_message("\n")

                if register_user(new_username, new_password):
                    username = new_username
                    session_id = create_session(username)
                    send_message(f"Registration successful! Welcome, {username}!")
                    game = Game()  # New user gets a fresh game
                else:
                    send_message("Username already taken or registration failed. Please try again.")

            elif choice == "3":  # View Active Traders
                send_message("\n")
                display_user_list(send_message)

            elif choice == "4":  # Quit
                send_message("\n")
                send_message("Goodbye!")
                return

        # Inject our mock I/O functions - do this once and keep them throughout
        import builtins
        original_print = builtins.print
        original_input = builtins.input
        builtins.print = mock_print
        builtins.input = mock_input

        try:
            # Explain the game mechanics
            send_message("Your adventure begins...")

            # Main game loop
            send_message("\nYour mission: explore space and make your fortune")
            input("Press Enter to continue...")

            # Run the game until retirement or game over
            while game.running and game.player.age < 60:
                exchange(game)

                # Check if player chose to log off immediately after the exchange cycle
                if game and hasattr(game, 'game_state') and game.game_state == "offline":
                    if game.running:
                        save_game_state(username, game)
                    # Clean up session
                    if session_id:
                        end_session(session_id)
                    # Exit the game loop cleanly
                    break

                # Check after the exchange cycle for any new loss conditions
                if not game.running:
                    # Player lost during this exchange cycle
                    delete_player_state(username)
                    send_message("\n" + "="*50)
                    send_message("GAME OVER - You have lost everything!")
                    send_message("Your player state has been reset.")
                    send_message("="*50 + "\n")

                    # Show final score for this failed run
                    p = game.player
                    score_data = calculate_final_score(p)
                    send_message(f"Final Score: {score_data['enhanced_score']}")
                    send_message("Overall Rank: " + score_data["overall_rank"])
                    send_message("Trader Rank: " + score_data["trader_rank"])
                    send_message("Bounty Hunter Rank: " + score_data["bounty_rank"])
                    send_message("\nStarting fresh with a new ship and 1000 credits...")
                    input("\nPress Enter to continue with your new career...")

                    # Create a fresh game state
                    game = Game()
                    continue

                # Auto-save if game is still running
                if game.running:
                    save_game_state(username, game)
            
            # Normal game completion (retirement) - save final state
            if game.running and game.game_state != "offline":
                save_game_state(username, game)
            
                # Game over summary for successful retirement
                p = game.player
                send_message(f"\nGame over! You retired at age {p.age}")
                send_message("\nTrading Career Summary:")
                send_message(f"Total Credits: {p.credits} cr")
                send_message(f"Total Profit: {p.total_profit} cr")
                send_message(f"Trades Completed: {p.trades_completed}")

                if p.trades_completed > 0:
                    from math import floor
                    avg_profit = p.total_profit / p.trades_completed
                    send_message(f"Average Profit per Trade: {floor(avg_profit * 10) / 10} cr")

                score_data = calculate_final_score(p)
                send_message(f"\nFinal Score: {score_data['enhanced_score']}")
                send_message("Overall Rank: " + score_data["overall_rank"])
                send_message("Trader Rank: " + score_data["trader_rank"])
                send_message("Bounty Hunter Rank: " + score_data["bounty_rank"])

        finally:
            # Restore original input/output
            builtins.print = original_print
            builtins.input = original_input

    except ConnectionAbortedError:
        # Player chose to quit - connection already handled
        pass
    except Exception as e:
        try:
            # Save game on unexpected error (only if not in losing state)
            if username and game and game.running:
                save_game_state(username, game)
            client_socket.send(f"Error: {str(e)}\r\n".encode())
        except:
            pass
    finally:
        # Clean up session
        if session_id:
            end_session(session_id)
        try:
            client_socket.close()
        except:
            pass

def get_users_with_login_status():
    """Get all users with their current login status"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all users with their login status
        cursor.execute('''
        SELECT u.username,
               CASE WHEN s.username IS NOT NULL THEN 'Online' ELSE 'Offline' END as status
        FROM users u
        LEFT JOIN sessions s ON u.username = s.username
        GROUP BY u.username,
                 CASE WHEN s.username IS NOT NULL THEN 'Online' ELSE 'Offline' END
        ORDER BY u.username
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Error getting users: {e}")
        return None

def display_user_list(send_message):
    """Display the list of users with their login status"""
    users = get_users_with_login_status()
    
    if users is None:
        send_message("\nThe user list is temporarily unavailable. Please try again later.")
        return
    
    if not users:
        send_message("\nNo registered users found.")
        return
    
    send_message("\n" + "="*30)
    send_message("REGISTERED SPACE TRADERS")
    send_message("="*30)
    send_message(f"{'Username':<20} {'Status':<12}")
    send_message("-"*30)
    
    for username, status in users:
        send_message(f"{username:<20} {status:<12}")
    
    send_message("="*30)


def start_server():
    """Start the server and listen for connections"""
    # Initialize database
    init_database()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 3000))
    server.listen(5)
    print("Space Trader server started on port 3000")
    print("Persistent universe ready for explorers")

    try:
        while True:
            try:
                client, addr = server.accept()
                print(f"New connection from {addr}")
                client_handler = threading.Thread(target=handle_client, args=(client,))
                client_handler.daemon = True
                client_handler.start()
            except Exception as e:
                print(f"Error accepting connection: {e}")
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()