import unittest
from unittest.mock import patch, MagicMock
import json
import os
import tempfile
import random
from game import (
    Player, Game, menu, cap, starfield, casino, manage_ship_stat, 
    trade, handle_encounter, explore, view_trade_stats, computer,
    log_game, exchange, calculate_final_score
)

class TestPlayer(unittest.TestCase):
    def test_player_initialization(self):
        player = Player()
        self.assertEqual(player.age, 30)
        self.assertEqual(player.credits, 1000)
        self.assertEqual(player.engine, 1)
        self.assertEqual(player.hold, 5)
        self.assertEqual(player.shields, 1)
        self.assertEqual(player.weapons, 1)
        self.assertEqual(player.goods, {})
        self.assertEqual(player.ship_name, "Intrepid")
        self.assertEqual(player.captain_name, "Reynolds")
        self.assertEqual(player.location, "exchange")
        self.assertEqual(player.purchase_records, {})
        self.assertEqual(player.total_profit, 0)
        self.assertEqual(player.trades_completed, 0)
    
    def test_player_custom_values(self):
        player = Player(
            age=35, 
            credits=2000, 
            engine=2, 
            hold=10, 
            shields=3, 
            weapons=2,
            ship_name="Serenity",
            captain_name="Mal"
        )
        self.assertEqual(player.age, 35)
        self.assertEqual(player.credits, 2000)
        self.assertEqual(player.engine, 2)
        self.assertEqual(player.hold, 10)
        self.assertEqual(player.shields, 3)
        self.assertEqual(player.weapons, 2)
        self.assertEqual(player.ship_name, "Serenity")
        self.assertEqual(player.captain_name, "Mal")

class TestGame(unittest.TestCase):
    def test_game_initialization(self):
        # Since exchange has random values, we'll patch random
        with patch('random.randint', return_value=8):
            game = Game()
            self.assertIsInstance(game.player, Player)
            self.assertEqual(game.exchange["traders"], 8)
            self.assertTrue(game.running)

class TestUtilityFunctions(unittest.TestCase):
    def test_cap(self):
        self.assertEqual(cap("hello"), "Hello")
        self.assertEqual(cap("HELLO"), "Hello")
        self.assertEqual(cap(""), "")
        self.assertEqual(cap("h"), "H")
    
    @patch('builtins.print')
    def test_starfield(self, mock_print):
        starfield()
        self.assertEqual(mock_print.call_count, 4)

class TestManageShipStat(unittest.TestCase):
    def test_increase_stat(self):
        game = Game()
        game.player.engine = 2
        result = manage_ship_stat(game, "engine", True)
        self.assertEqual(game.player.engine, 3)
        self.assertEqual(result, "Engine increased to 3")
    
    def test_decrease_stat(self):
        game = Game()
        game.player.shields = 3
        result = manage_ship_stat(game, "shields")
        self.assertEqual(game.player.shields, 2)
        self.assertEqual(result, "Shields reduced to 2")
    
    @patch('builtins.print')
    def test_engine_to_zero(self, mock_print):
        game = Game()
        game.player.engine = 1
        result = manage_ship_stat(game, "engine")
        self.assertEqual(game.player.engine, 0)
        self.assertFalse(game.running)
        mock_print.assert_called_with("With no engines, you drift in space. Game over!")
    
    @patch('random.choice', return_value="Quantum Dust")
    @patch('builtins.print')
    def test_jettison_goods_when_hold_reduced(self, mock_print, mock_choice):
        game = Game()
        game.player.hold = 2
        game.player.goods = {"Quantum Dust": 2}
        game.player.purchase_records = {
            "Quantum Dust": {
                "Quantum_Dust_1": 100
            }
        }
        manage_ship_stat(game, "hold")
        self.assertEqual(game.player.hold, 1)
        self.assertEqual(game.player.goods, {"Quantum Dust": 1})
        mock_print.assert_called_with("Jettisoned Quantum Dust due to hold damage")

class TestCalculateFinalScore(unittest.TestCase):
    def test_calculate_score_basic(self):
        player = Player(age=60, credits=5000, total_profit=2000)
        result = calculate_final_score(player)
        # (60 * 5000 * 2000) / 10000 = 60000
        self.assertEqual(result["enhanced_score"], 60000)
        self.assertEqual(result["rank"], "Legendary Space Mogul")
    
    def test_calculate_score_with_negative_profit(self):
        player = Player(age=60, credits=5000, total_profit=-1000)
        result = calculate_final_score(player)
        # Using minimum profit modifier of 1: (60 * 5000 * 1) / 10000 = 30
        self.assertEqual(result["enhanced_score"], 30)
        self.assertEqual(result["rank"], "Space Rookie")
    
    def test_calculate_score_ranks(self):
        test_cases = [
            {"age": 60, "credits": 1000, "profit": 2000, "expected_rank": "Skilled Trader"},
            {"age": 60, "credits": 5000, "profit": 500, "expected_rank": "Interstellar Merchant"},
            {"age": 35, "credits": 2000, "profit": 100, "expected_rank": "Trader Apprentice"},
        ]
        
        for tc in test_cases:
            player = Player(age=tc["age"], credits=tc["credits"], total_profit=tc["profit"])
            result = calculate_final_score(player)
            self.assertEqual(result["rank"], tc["expected_rank"])

class TestLogGame(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_dir = os.getcwd()
        os.chdir(self.temp_dir.name)
    
    def tearDown(self):
        os.chdir(self.old_dir)
        self.temp_dir.cleanup()
    
    @patch('builtins.print')
    def test_save_and_load_game(self, mock_print):
        player = Player(
            age=40, 
            credits=5000, 
            ship_name="TestShip", 
            captain_name="TestCaptain"
        )
        
        # Test save
        log_game(player, "save")
        self.assertTrue(os.path.exists("savefile.json"))
        mock_print.assert_called_with("Game saved.")
        
        # Modify player
        player.age = 50
        player.credits = 1000
        
        # Test load
        log_game(player, "load")
        self.assertEqual(player.age, 40)
        self.assertEqual(player.credits, 5000)
        self.assertEqual(player.ship_name, "TestShip")
        self.assertEqual(player.captain_name, "TestCaptain")
        mock_print.assert_called_with("Game loaded.")
    
    @patch('builtins.print')
    def test_load_game_no_save_file(self, mock_print):
        player = Player()
        log_game(player, "load")
        mock_print.assert_called_with("No save file found.")

class TestTrade(unittest.TestCase):
    @patch('random.choice', side_effect=["Quantum Dust", "Luna Stardust"])
    @patch('random.randint', return_value=100)
    @patch('builtins.input', return_value="1")  # User chooses to buy
    @patch('builtins.print')
    def test_buy_goods(self, mock_print, mock_input, mock_randint, mock_choice):
        game = Game()
        game.player.credits = 200
        
        trade(game, is_buy=True)
        
        self.assertEqual(game.player.credits, 95)  # 200 - 100 - 5 (tax)
        self.assertEqual(game.player.goods, {"Quantum Dust": 1})
        self.assertTrue("Quantum Dust" in game.player.purchase_records)
        self.assertEqual(len(game.player.purchase_records["Quantum Dust"]), 1)
        self.assertEqual(list(game.player.purchase_records["Quantum Dust"].values())[0], 100)
    
    @patch('random.choice', side_effect=["Quantum Dust", "Luna Stardust"])
    @patch('random.randint', return_value=150)
    @patch('builtins.input', return_value="1")  # User chooses to sell
    @patch('builtins.print')
    def test_sell_goods(self, mock_print, mock_input, mock_randint, mock_choice):
        game = Game()
        game.player.credits = 100
        game.player.goods = {"Quantum Dust": 1}
        game.player.purchase_records = {
            "Quantum Dust": {"Quantum_Dust_1": 100}
        }
        
        trade(game, is_buy=False)
        
        self.assertEqual(game.player.credits, 245)  # 100 + 150 - 5 (tax)
        self.assertEqual(game.player.goods, {})
        self.assertEqual(game.player.purchase_records, {})
        self.assertEqual(game.player.total_profit, 50)  # 150 - 100
        self.assertEqual(game.player.trades_completed, 1)

class TestEncounters(unittest.TestCase):
    @patch('builtins.print')
    def test_empty_encounter(self, mock_print):
        game = Game()
        handle_encounter(game, "empty")
        # We'll just verify it doesn't crash and calls print
        self.assertTrue(mock_print.called)
    
    @patch('game.trade')
    @patch('builtins.print')
    def test_trader_encounter(self, mock_print, mock_trade):
        game = Game()
        handle_encounter(game, "trader")
        mock_trade.assert_called_once_with(game, True)
    
    @patch('random.choice', side_effect=["Zanxor", "boon", "engine"])
    @patch('game.manage_ship_stat')
    @patch('builtins.print')
    def test_planet_encounter_boon(self, mock_print, mock_manage_stat, mock_choice):
        game = Game()
        handle_encounter(game, "planet")
        mock_manage_stat.assert_called_once_with(game, "engine", True)
    
    @patch('random.choice', side_effect=["Rex", 1, 1, "shields"])
    @patch('builtins.print')
    def test_pirate_encounter_win(self, mock_print, mock_choice):
        game = Game()
        game.player.weapons = 2  # Ensure victory
        handle_encounter(game, "pirate")
        mock_print.assert_any_call("You won the battle!")

if __name__ == '__main__':
    unittest.main()