import unittest
from unittest.mock import patch
from game import Player, buy_goods, sell_goods, decrement_stat, jettison_goods


class TestSpaceTrader(unittest.TestCase):

    def setUp(self):
        """ Set up a default player for use in tests. """
        self.player = Player()

    @patch('builtins.input', return_value='1')  # Mock input to simulate buying goods
    def test_buy_goods(self, mock_input):
        """ Test buying goods reduces player's credits. """
        initial_credits = self.player.credits
        buy_goods(self.player)
        self.assertLess(self.player.credits, initial_credits)

    @patch('builtins.input', return_value='1')  # Mock input to simulate selling goods
    def test_sell_goods(self, mock_input):
        """ Test selling goods increases player's credits and removes the good when sold. """
        self.player.goods = {"Plasma": 1}
        initial_credits = self.player.credits
        sell_goods(self.player)

        # Check that credits have increased
        self.assertGreater(self.player.credits, initial_credits)

        # Check that the good has been removed from the dictionary after selling
        self.assertNotIn("Plasma", self.player.goods)

    def test_decrement_stat_engine(self):
        """ Test decrementing the engine stat reduces the value, or ends game when engine hits 0. """
        self.player.engine = 2
        decrement_stat(self.player, "engine")
        self.assertEqual(self.player.engine, 1)

        # Test game over when engine reaches 0
        self.player.engine = 1
        with self.assertRaises(SystemExit):  # Expect the game to exit
            decrement_stat(self.player, "engine")

    def test_jettison_goods(self):
        """ Test jettisoning goods when the hold capacity is reduced. """
        self.player.goods = {"Plasma": 2, "Fuel": 2}
        self.player.hold = 1
        jettison_goods(self.player)
        total_goods = sum(self.player.goods.values())
        self.assertLessEqual(total_goods, self.player.hold)


if __name__ == '__main__':
    unittest.main()
