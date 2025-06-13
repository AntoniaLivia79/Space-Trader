import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import tempfile
import socket
import threading
import json
import sqlite3
import time
from datetime import datetime, timedelta

# Import the server module functions to test
from server import (
    init_database, hash_password, verify_password, 
    register_user, authenticate_user, create_session,
    update_session_activity, end_session, save_game_state,
    load_game_state, handle_client, start_server, DB_PATH
)
from game import Player, Game

class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_db_path = DB_PATH
        
        # Override the DB_PATH temporarily
        import server
        server.DB_PATH = os.path.join(self.temp_dir.name, "test_space_trader.db")
        
        # Initialize the database
        init_database()
    
    def tearDown(self):
        # Restore the original DB_PATH
        import server
        server.DB_PATH = self.old_db_path
        
        # Clean up temp directory
        self.temp_dir.cleanup()
    
    def test_init_database(self):
        # Verify tables were created
        conn = sqlite3.connect(server.DB_PATH)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Check if game_states table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='game_states'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Check if sessions table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sessions'")
        self.assertIsNotNone(cursor.fetchone())
        
        conn.close()
    
    def test_register_and_authenticate_user(self):
        # Register a new user
        self.assertTrue(register_user("testuser", "password123"))
        
        # Try to register the same user again (should fail)
        self.assertFalse(register_user("testuser", "password123"))
        
        # Authenticate with correct credentials
        self.assertTrue(authenticate_user("testuser", "password123"))
        
        # Authenticate with incorrect password
        self.assertFalse(authenticate_user("testuser", "wrongpassword"))
        
        # Authenticate with non-existent user
        self.assertFalse(authenticate_user("nonexistent", "password123"))

class TestPasswordFunctions(unittest.TestCase):
    def test_hash_and_verify_password(self):
        password = "test_password"
        
        # Hash the password
        hashed = hash_password(password)
        
        # Verify the hash is not the original password
        self.assertNotEqual(hashed, password)
        
        # Verify the correct password
        self.assertTrue(verify_password(hashed, password))
        
        # Verify an incorrect password
        self.assertFalse(verify_password(hashed, "wrong_password"))

class TestSessionFunctions(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_db_path = DB_PATH
        
        # Override the DB_PATH temporarily
        import server
        server.DB_PATH = os.path.join(self.temp_dir.name, "test_space_trader.db")
        
        # Initialize the database
        init_database()
        
        # Create a test user
        register_user("testuser", "password123")
    
    def tearDown(self):
        # Restore the original DB_PATH
        import server
        server.DB_PATH = self.old_db_path
        
        # Clean up temp directory
        self.temp_dir.cleanup()
    
    def test_create_session(self):
        session_id = create_session("testuser")
        self.assertTrue(session_id)  # Should return a valid UUID string
        
        # Verify session was created in the database
        conn = sqlite3.connect(server.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM sessions WHERE session_id = ?", (session_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "testuser")
    
    def test_update_session_activity(self):
        # Create a session
        session_id = create_session("testuser")
        
        # Get the initial last_activity time
        conn = sqlite3.connect(server.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT last_activity FROM sessions WHERE session_id = ?", (session_id,))
        initial_activity = cursor.fetchone()[0]
        conn.close()
        
        # Wait a short time to ensure timestamp changes
        time.sleep(0.1)
        
        # Update the session activity
        self.assertTrue(update_session_activity(session_id))
        
        # Get the updated last_activity time
        conn = sqlite3.connect(server.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT last_activity FROM sessions WHERE session_id = ?", (session_id,))
        updated_activity = cursor.fetchone()[0]
        conn.close()
        
        # Verify the timestamp was updated
        self.assertNotEqual(initial_activity, updated_activity)
    
    def test_end_session(self):
        # Create a session
        session_id = create_session("testuser")
        
        # End the session
        self.assertTrue(end_session(session_id))
        
        # Verify the session was removed from the database
        conn = sqlite3.connect(server.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT session_id FROM sessions WHERE session_id = ?", (session_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNone(result)

class TestGameStateFunctions(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_db_path = DB_PATH
        
        # Override the DB_PATH temporarily
        import server
        server.DB_PATH = os.path.join(self.temp_dir.name, "test_space_trader.db")
        
        # Initialize the database
        init_database()
        
        # Create a test user
        register_user("testuser", "password123")
    
    def tearDown(self):
        # Restore the original DB_PATH
        import server
        server.DB_PATH = self.old_db_path
        
        # Clean up temp directory
        self.temp_dir.cleanup()
    
    def test_save_and_load_game_state(self):
        # Create a game with custom values
        game = Game()
        game.player.age = 35
        game.player.credits = 5000
        game.player.ship_name = "TestShip"
        game.player.captain_name = "TestCaptain"
        game.exchange["traders"] = 7
        
        # Save the game state
        self.assertTrue(save_game_state("testuser", game))
        
        # Load the game state
        loaded_game = load_game_state("testuser")
        
        # Verify the loaded game state matches the original
        self.assertIsNotNone(loaded_game)
        self.assertEqual(loaded_game.player.age, 35)
        self.assertEqual(loaded_game.player.credits, 5000)
        self.assertEqual(loaded_game.player.ship_name, "TestShip")
        self.assertEqual(loaded_game.player.captain_name, "TestCaptain")
        self.assertEqual(loaded_game.exchange["traders"], 7)
    
    def test_load_nonexistent_game_state(self):
        # Attempt to load a game state for a user that hasn't saved one
        loaded_game = load_game_state("testuser")
        self.assertIsNone(loaded_game)

class TestHandleClient(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_db_path = DB_PATH
        
        # Override the DB_PATH temporarily
        import server
        server.DB_PATH = os.path.join(self.temp_dir.name, "test_space_trader.db")
        
        # Initialize the database
        init_database()
    
    def tearDown(self):
        # Restore the original DB_PATH
        import server
        server.DB_PATH = self.old_db_path
        
        # Clean up temp directory
        self.temp_dir.cleanup()
    
    @patch('socket.socket')
    def test_handle_client_register(self, mock_socket):
        # Create a mock client socket
        mock_client = MagicMock()
        
        # Mock the receive behavior for registration
        mock_client.recv.side_effect = [
            b"2",  # Choose register
            b"testuser",  # Username
            b"password123",  # Password
            b"/quit"  # Quit command to exit
        ]
        
        # Call the function with the mock socket
        with patch('builtins.print'):  # Suppress print output
            handle_client(mock_client)
        
        # Verify the registration was successful
        conn = sqlite3.connect(server.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", ("testuser",))
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "testuser")
    
    @patch('socket.socket')
    def test_handle_client_login(self, mock_socket):
        # Register a test user first
        register_user("testuser", "password123")
        
        # Create a mock client socket
        mock_client = MagicMock()
        
        # Mock the receive behavior for login
        mock_client.recv.side_effect = [
            b"1",  # Choose login
            b"testuser",  # Username
            b"password123",  # Password
            b"2",  # No to loading saved game
            b"/quit"  # Quit command to exit
        ]
        
        # Call the function with the mock socket
        with patch('builtins.print'):  # Suppress print output
            handle_client(mock_client)
        
        # Verify a session was created and then ended
        conn = sqlite3.connect(server.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE username = ?", ("testuser",))
        count = cursor.fetchone()[0]
        conn.close()
        
        # Since we end the session at the end of handle_client, count should be 0
        self.assertEqual(count, 0)

class TestServerStartup(unittest.TestCase):
    @patch('socket.socket')
    @patch('threading.Thread')
    def test_start_server(self, mock_thread, mock_socket):
        # Mock the socket to avoid actually binding to a port
        mock_server = MagicMock()
        mock_socket.return_value = mock_server
        
        # Mock socket.accept to raise KeyboardInterrupt after first call
        mock_server.accept.side_effect = [
            (MagicMock(), ('127.0.0.1', 12345)),  # First client connects
            KeyboardInterrupt()  # Then we simulate Ctrl+C
        ]
        
        # Call start_server
        with patch('builtins.print'):  # Suppress print output
            start_server()
        
        # Verify the server was set up correctly
        mock_server.setsockopt.assert_called_once_with(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mock_server.bind.assert_called_once_with(('0.0.0.0', 3000))
        mock_server.listen.assert_called_once_with(5)
        
        # Verify a thread was started for the client
        mock_thread.assert_called_once()
        mock_thread.return_value.daemon = True
        mock_thread.return_value.start.assert_called_once()
        
        # Verify the server was closed properly
        mock_server.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()