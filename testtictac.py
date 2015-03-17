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

    def test_another(self):
        self.assertIsNone(self.game.board.get((0, 0)))
        self.assertNotEqual(self.game.board.get((0, 0)), "P")