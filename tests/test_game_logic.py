"""
tests/test_game_logic.py
------------------------
Unit tests for the game_logic module.

Run with:
    python -m unittest discover -s tests -v
"""

import unittest
import sys
import os

# Ensure the parent directory is in sys.path so we can import game_logic
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from game_logic import Board, HUMAN, AI, EMPTY, WIN_COMBINATIONS


class TestBoardInitialisation(unittest.TestCase):
    """Tests for Board initialisation and reset."""

    def test_initial_board_is_empty(self):
        """All nine cells should be empty on a fresh board."""
        board = Board()
        self.assertEqual(board.cells, [EMPTY] * 9)

    def test_reset_clears_board(self):
        """After reset, every cell should be empty regardless of previous state."""
        board = Board()
        board.cells[0] = HUMAN
        board.cells[4] = AI
        board.reset()
        self.assertEqual(board.cells, [EMPTY] * 9)

    def test_copy_is_independent(self):
        """Board.copy() should produce an independent snapshot."""
        board = Board()
        board.cells[0] = HUMAN
        copy = board.copy()
        copy.cells[0] = AI
        # Original should be untouched
        self.assertEqual(board.cells[0], HUMAN)


class TestSetCell(unittest.TestCase):
    """Tests for placing and clearing marks."""

    def test_set_cell_places_mark(self):
        board = Board()
        board.set_cell(4, HUMAN)
        self.assertEqual(board.cells[4], HUMAN)

    def test_set_occupied_cell_raises(self):
        board = Board()
        board.set_cell(0, AI)
        with self.assertRaises(ValueError):
            board.set_cell(0, HUMAN)  # already occupied

    def test_set_out_of_range_raises(self):
        board = Board()
        with self.assertRaises(ValueError):
            board.set_cell(9, HUMAN)   # index 9 is out of range

    def test_clear_cell(self):
        board = Board()
        board.cells[3] = AI
        board.clear_cell(3)
        self.assertEqual(board.cells[3], EMPTY)


class TestLegalMoves(unittest.TestCase):
    """Tests for legal_moves generation."""

    def test_all_moves_legal_on_empty_board(self):
        board = Board()
        self.assertEqual(sorted(board.legal_moves()), list(range(9)))

    def test_occupied_cells_excluded(self):
        board = Board()
        board.cells[0] = HUMAN
        board.cells[4] = AI
        legal = board.legal_moves()
        self.assertNotIn(0, legal)
        self.assertNotIn(4, legal)
        self.assertEqual(len(legal), 7)

    def test_full_board_has_no_legal_moves(self):
        board = Board()
        board.cells = [HUMAN, AI, HUMAN, AI, HUMAN, AI, AI, HUMAN, AI]
        self.assertEqual(board.legal_moves(), [])

    def test_is_full_on_full_board(self):
        board = Board()
        board.cells = [HUMAN] * 9
        self.assertTrue(board.is_full())

    def test_is_not_full_on_partial_board(self):
        board = Board()
        board.cells[0] = HUMAN
        self.assertFalse(board.is_full())


class TestWinDetection(unittest.TestCase):
    """Tests for all eight winning combinations."""

    def _make_board_with_winner(self, positions, player) -> Board:
        board = Board()
        for p in positions:
            board.cells[p] = player
        return board

    def test_top_row_win(self):
        board = self._make_board_with_winner([0, 1, 2], HUMAN)
        self.assertEqual(board.check_winner(), HUMAN)

    def test_middle_row_win(self):
        board = self._make_board_with_winner([3, 4, 5], AI)
        self.assertEqual(board.check_winner(), AI)

    def test_bottom_row_win(self):
        board = self._make_board_with_winner([6, 7, 8], HUMAN)
        self.assertEqual(board.check_winner(), HUMAN)

    def test_left_column_win(self):
        board = self._make_board_with_winner([0, 3, 6], AI)
        self.assertEqual(board.check_winner(), AI)

    def test_middle_column_win(self):
        board = self._make_board_with_winner([1, 4, 7], HUMAN)
        self.assertEqual(board.check_winner(), HUMAN)

    def test_right_column_win(self):
        board = self._make_board_with_winner([2, 5, 8], AI)
        self.assertEqual(board.check_winner(), AI)

    def test_main_diagonal_win(self):
        board = self._make_board_with_winner([0, 4, 8], HUMAN)
        self.assertEqual(board.check_winner(), HUMAN)

    def test_anti_diagonal_win(self):
        board = self._make_board_with_winner([2, 4, 6], AI)
        self.assertEqual(board.check_winner(), AI)

    def test_no_winner_on_empty_board(self):
        board = Board()
        self.assertIsNone(board.check_winner())

    def test_no_winner_mid_game(self):
        board = Board()
        board.cells[0] = HUMAN
        board.cells[4] = AI
        self.assertIsNone(board.check_winner())

    def test_winning_line_returned(self):
        board = Board()
        board.cells[0] = board.cells[1] = board.cells[2] = HUMAN
        self.assertEqual(board.get_winning_line(), (0, 1, 2))

    def test_no_winning_line_returns_none(self):
        board = Board()
        self.assertIsNone(board.get_winning_line())


class TestDrawDetection(unittest.TestCase):
    """Tests for draw conditions."""

    def test_draw_on_full_no_winner(self):
        """A standard drawn game: X-O-X / O-O-X / O-X-O."""
        board = Board()
        board.cells = [HUMAN, AI, HUMAN,
                       AI,    AI, HUMAN,
                       AI,    HUMAN, AI]
        self.assertTrue(board.is_draw())
        self.assertIsNone(board.check_winner())

    def test_not_draw_when_winner_exists(self):
        board = Board()
        board.cells = [HUMAN, HUMAN, HUMAN,
                       AI,    AI,    EMPTY,
                       EMPTY, EMPTY, EMPTY]
        self.assertFalse(board.is_draw())

    def test_not_draw_when_board_not_full(self):
        board = Board()
        board.cells[0] = HUMAN
        self.assertFalse(board.is_draw())


class TestGameOver(unittest.TestCase):
    """Tests for is_game_over()."""

    def test_game_over_on_win(self):
        board = Board()
        board.cells[0] = board.cells[1] = board.cells[2] = AI
        self.assertTrue(board.is_game_over())

    def test_game_over_on_full_board(self):
        board = Board()
        board.cells = [HUMAN, AI, HUMAN,
                       AI,    AI, HUMAN,
                       AI,    HUMAN, AI]
        self.assertTrue(board.is_game_over())

    def test_game_not_over_on_empty(self):
        board = Board()
        self.assertFalse(board.is_game_over())


class TestStringRepresentation(unittest.TestCase):
    """Sanity check on __str__."""

    def test_str_does_not_raise(self):
        board = Board()
        board.cells[0] = HUMAN
        board.cells[4] = AI
        s = str(board)
        self.assertIn("X", s)
        self.assertIn("O", s)


if __name__ == "__main__":
    unittest.main(verbosity=2)
