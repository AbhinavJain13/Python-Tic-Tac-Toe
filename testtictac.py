import unittest
import tkinter
from tictac import *

class TestTicTac(unittest.TestCase):
    def setUp(self):
        self.game = Game(tkinter.Tk())

    def tearDown(self):
        self.game = Game(tkinter.Tk())

    def simulate_move(self, column, row, player):
        self.game.board[(column, row)] = player

    def test_simulate_move(self):
        self.simulate_move(0, 0, "P")
        self.assertIsNotNone(self.game.board[(0, 0)])
        self.assertEqual(self.game.board[0, 0], "P")

    def test_will_tear_down(self):
        self.assertIsNone(self.game.board.get((0, 0)))
        self.assertNotEqual(self.game.board.get((0, 0)), "P")

    def test_smart_route_valid(self):
        self.simulate_move(0, 0, "C")
        self.simulate_move(1, 0, "P")
        self.game.smart_route = [(0, 0), (1, 0), (2, 0)]
        self.assertFalse(self.game.smart_route_valid())

        self.simulate_move(0, 1, "C")
        self.simulate_move(1, 1, "C")
        self.game.smart_route = [(0, 1), (1, 1), (2, 1)]
        self.assertTrue(self.game.smart_route_valid())