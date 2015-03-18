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

    def test_smart_route_valid_empty(self):
        self.assertFalse(self.game.smart_route_valid())

    def test_smart_route_valid_blocked(self):
        self.simulate_move(0, 0, "C")
        self.simulate_move(1, 0, "P")

        # Noise
        self.simulate_move(2, 2, "C")
        self.simulate_move(1, 2, "C")
        # end Noise

        self.game.smart_route = [(0, 0), (1, 0), (2, 0)]
        self.assertFalse(self.game.smart_route_valid())

    def test_smart_route_valid_all_computers(self):
        self.simulate_move(0, 1, "C")
        self.simulate_move(1, 1, "C")

        # Noise
        self.simulate_move(0, 0, "P")
        self.simulate_move(1, 0, "P")
        # end Noise

        self.game.smart_route = [(0, 1), (1, 1), (2, 1)]
        self.assertTrue(self.game.smart_route_valid())

    def test_smart_route_valid_all_player(self):
        self.simulate_move(0, 1, "P")
        self.simulate_move(1, 1, "P")

        # Noise
        self.simulate_move(2, 2, "C")
        self.simulate_move(0, 0, "C")
        # end Noise

        self.game.smart_route = [(0, 1), (1, 1), (2, 1)]
        self.assertFalse(self.game.smart_route_valid())

    def test_gen_smart_move_empty(self):
        self.assertTrue(isinstance(self.game.gen_smart_move(), list))

    def test_gen_smart_move_valid_smart_route(self):
        self.game.smart_route = [(0, 1), (1, 1), (2, 1)]
        self.assertIsNotNone(self.game.gen_smart_move())

    def test_get_all_moves_player(self):
        self.simulate_move(0, 1, "P")
        self.simulate_move(1, 1, "P")
        self.simulate_move(2, 1, "P")
        self.assertListEqual(self.game.get_all_moves("P"), [(0,1),(1,1),(2,1)])

    def test_get_all_moves_computer(self):
        self.simulate_move(0, 1, "C")
        self.simulate_move(1, 1, "C")
        self.simulate_move(2, 1, "C")
        self.assertListEqual(self.game.get_all_moves("C"), [(0,1),(1,1),(2,1)])

    def test_win(self):
        self.assertTrue(self.game.win(Game.VICTORY_HORIZONTAL,(0,0)))

    def test_line_winner_player(self):
        self.simulate_move(0, 1, "P")
        self.simulate_move(1, 1, "P")
        self.simulate_move(2, 1, "P")
        self.assertEqual(self.game.line_winner([[(0, 1), (1, 1), (2, 1)]]),
                         "P")

    def test_line_winner_computer(self):
        self.simulate_move(0, 1, "C")
        self.simulate_move(1, 1, "C")
        self.simulate_move(2, 1, "C")
        self.assertEqual(self.game.line_winner([[(0, 1), (1, 1), (2, 1)]]),
                         "C")

    def test_line_winner_no_one(self):
        self.simulate_move(0, 1, "C")
        self.simulate_move(1, 1, "P")
        self.simulate_move(2, 1, "P")
        self.assertIsNone(self.game.line_winner([[(0, 1), (1, 1), (2, 1)]]))