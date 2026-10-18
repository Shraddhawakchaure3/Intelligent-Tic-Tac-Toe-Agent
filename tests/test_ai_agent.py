"""
tests/test_ai_agent.py
----------------------
Unit tests for the ai_agent module.

Covers:
  - AI wins immediately when a forced win is available.
  - AI blocks an immediate opponent win.
  - AI chooses only legal moves.
  - Alpha-Beta pruning returns the same optimal score as plain Minimax.
  - Hard AI never loses in exhaustive testing against all possible human
    first-move responses.
  - Correct behaviour on near-full boards.

Run with:
    python -m unittest discover -s tests -v
"""

import unittest
import sys
import os
import itertools

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from game_logic import Board, HUMAN, AI, EMPTY
from ai_agent import get_ai_move, _minimax, _minimax_alpha_beta


class TestAILegalMoves(unittest.TestCase):
    """AI must always return a legal move."""

    def test_move_is_in_legal_moves(self):
        board = Board()
        board.cells[0] = HUMAN
        board.cells[4] = AI
        legal = board.legal_moves()
        move, _ = get_ai_move(board, "Hard")
        self.assertIn(move, legal)

    def test_move_on_empty_board(self):
        for difficulty in ("Easy", "Medium", "Hard"):
            board = Board()
            move, _ = get_ai_move(board, difficulty)
            self.assertIn(move, list(range(9)), msg=f"Failed for difficulty {difficulty}")

    def test_single_legal_move(self):
        """When only one cell is empty, all difficulties must choose it."""
        board = Board()
        # Fill all cells except index 7
        board.cells = [HUMAN, AI, HUMAN, AI, AI, HUMAN, AI, EMPTY, HUMAN]
        for difficulty in ("Easy", "Medium", "Hard"):
            b = board.copy()
            move, _ = get_ai_move(b, difficulty)
            self.assertEqual(move, 7, msg=f"Failed for difficulty {difficulty}")


class TestAIWinsImmediately(unittest.TestCase):
    """AI must take an immediate win whenever one is available."""

    def _assert_ai_takes_win(self, cells, winning_move, difficulty="Hard"):
        board = Board()
        board.cells = list(cells)
        move, _ = get_ai_move(board, difficulty)
        self.assertEqual(
            move,
            winning_move,
            msg=f"[{difficulty}] Expected AI to win at {winning_move}, chose {move}.\nBoard:\n{board}",
        )

    def test_ai_wins_top_row(self):
        # O O _ → AI should play index 2
        self._assert_ai_takes_win(
            [AI, AI, EMPTY, HUMAN, HUMAN, EMPTY, EMPTY, EMPTY, EMPTY], 2
        )

    def test_ai_wins_middle_row(self):
        # _ _ _ / O O _ / X X _ → AI should play index 5
        self._assert_ai_takes_win(
            [EMPTY, EMPTY, EMPTY, AI, AI, EMPTY, HUMAN, HUMAN, EMPTY], 5
        )

    def test_ai_wins_left_column(self):
        # O _ X / O _ X / _ _ _ → AI should play index 6
        self._assert_ai_takes_win(
            [AI, EMPTY, HUMAN, AI, EMPTY, HUMAN, EMPTY, EMPTY, EMPTY], 6
        )

    def test_ai_wins_main_diagonal(self):
        # O X _ / X O _ / _ _ _ → AI should play index 8
        self._assert_ai_takes_win(
            [AI, HUMAN, EMPTY, HUMAN, AI, EMPTY, EMPTY, EMPTY, EMPTY], 8
        )

    def test_ai_wins_medium_difficulty(self):
        """Medium AI should also take an immediate win (depth 3 is enough)."""
        board = Board()
        board.cells = [AI, AI, EMPTY, HUMAN, HUMAN, EMPTY, EMPTY, EMPTY, EMPTY]
        move, _ = get_ai_move(board, "Medium")
        self.assertEqual(move, 2, msg="Medium AI missed an immediate win")


class TestAIBlocksOpponent(unittest.TestCase):
    """AI must block an immediate human win when no AI win is available."""

    def _assert_ai_blocks(self, cells, blocking_move, difficulty="Hard"):
        board = Board()
        board.cells = list(cells)
        move, _ = get_ai_move(board, difficulty)
        self.assertEqual(
            move,
            blocking_move,
            msg=f"[{difficulty}] Expected block at {blocking_move}, chose {move}.\nBoard:\n{board}",
        )

    def test_blocks_top_row(self):
        # X X _ / O _ _ / _ _ _ → AI must block at 2
        self._assert_ai_blocks(
            [HUMAN, HUMAN, EMPTY, AI, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY], 2
        )

    def test_blocks_bottom_row(self):
        # O _ _ / _ _ _ / X X _ → AI must block at 8
        self._assert_ai_blocks(
            [AI, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, HUMAN, HUMAN, EMPTY], 8
        )

    def test_blocks_right_column(self):
        # _ _ X / O _ X / _ _ _ → AI must block at 8
        self._assert_ai_blocks(
            [EMPTY, EMPTY, HUMAN, AI, EMPTY, HUMAN, EMPTY, EMPTY, EMPTY], 8
        )

    def test_blocks_anti_diagonal(self):
        # _ _ X / _ X _ / _ _ _ / (O somewhere) → AI must block at 6
        self._assert_ai_blocks(
            [EMPTY, EMPTY, HUMAN, EMPTY, HUMAN, EMPTY, EMPTY, EMPTY, AI], 6
        )

    def test_blocks_medium_difficulty(self):
        """Medium AI should also block an immediate opponent win."""
        board = Board()
        board.cells = [HUMAN, HUMAN, EMPTY, AI, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        move, _ = get_ai_move(board, "Medium")
        self.assertEqual(move, 2, msg="Medium AI failed to block opponent win")


class TestAlphaBetaConsistency(unittest.TestCase):
    """Alpha-Beta must return the same optimal score as plain Minimax."""

    def _compare_scores(self, cells, is_maximising=True):
        """Return (minimax_score, ab_score) for the given board state."""
        board = Board()
        board.cells = list(cells)
        counter_mm = [0]
        counter_ab = [0]
        mm_score = _minimax(board, 0, is_maximising, counter_mm)
        ab_score = _minimax_alpha_beta(
            board, 0, float("-inf"), float("inf"), is_maximising, counter_ab
        )
        return mm_score, ab_score

    def test_empty_board_scores_equal(self):
        mm, ab = self._compare_scores([EMPTY] * 9)
        self.assertEqual(mm, ab, msg="Scores differ on empty board")

    def test_near_win_ai_scores_equal(self):
        cells = [AI, AI, EMPTY, HUMAN, HUMAN, EMPTY, EMPTY, EMPTY, EMPTY]
        mm, ab = self._compare_scores(cells, is_maximising=True)
        self.assertEqual(mm, ab)

    def test_near_win_human_scores_equal(self):
        cells = [HUMAN, HUMAN, EMPTY, AI, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        mm, ab = self._compare_scores(cells, is_maximising=True)
        self.assertEqual(mm, ab)

    def test_mid_game_state_scores_equal(self):
        cells = [HUMAN, AI, HUMAN, EMPTY, AI, EMPTY, EMPTY, EMPTY, EMPTY]
        mm, ab = self._compare_scores(cells, is_maximising=True)
        self.assertEqual(mm, ab)

    def test_multiple_states_scores_equal(self):
        """Check a dozen random-ish mid-game positions for consistency."""
        test_positions = [
            [HUMAN, AI, EMPTY, EMPTY, AI, EMPTY, HUMAN, EMPTY, EMPTY],
            [EMPTY, AI, HUMAN, EMPTY, AI, EMPTY, EMPTY, HUMAN, EMPTY],
            [AI, EMPTY, HUMAN, EMPTY, HUMAN, EMPTY, AI, EMPTY, EMPTY],
            [HUMAN, EMPTY, AI, EMPTY, HUMAN, EMPTY, AI, EMPTY, EMPTY],
        ]
        for cells in test_positions:
            mm, ab = self._compare_scores(cells, is_maximising=True)
            self.assertEqual(mm, ab, msg=f"Score mismatch for state: {cells}")


class TestHardAINeverLoses(unittest.TestCase):
    """
    Exhaustive test: simulate every possible game where human moves first and
    the Hard AI responds optimally. The AI should never lose.

    Since Tic-Tac-Toe has at most 9! / duplicates ≈ 362,880 paths but the
    tree is pruned early, this is computationally tractable.
    """

    def _collect_outcomes(self, board: Board, is_human_turn: bool, outcomes: list) -> None:
        """
        Recursively explore all game paths.

        - When it is the human's turn, branch on every legal human move.
        - When it is the AI's turn, apply the Hard AI's chosen move (single branch).
        - At each terminal state, append the result to *outcomes*.
        """
        winner = board.check_winner()
        if winner:
            outcomes.append(winner)
            return
        if board.is_full():
            outcomes.append("Draw")
            return

        if is_human_turn:
            # Explore ALL possible human moves
            for move in board.legal_moves():
                b = board.copy()
                b.cells[move] = HUMAN
                self._collect_outcomes(b, False, outcomes)
        else:
            # AI responds optimally (single chosen move)
            move, _ = get_ai_move(board, "Hard")
            b = board.copy()
            b.cells[move] = AI
            self._collect_outcomes(b, True, outcomes)

    def test_hard_ai_never_loses_exhaustive(self):
        """
        Verify that for every possible human first move, no game-tree branch
        results in the human winning (the AI either wins or draws).
        """
        for human_first_move in range(9):
            board = Board()
            board.cells[human_first_move] = HUMAN

            outcomes: list = []
            self._collect_outcomes(board, False, outcomes)

            for result in outcomes:
                self.assertNotEqual(
                    result,
                    HUMAN,
                    msg=(
                        f"Hard AI lost when human opened at cell {human_first_move}!\n"
                        f"Outcome: {result}"
                    ),
                )


class TestMoveAnalysisMetadata(unittest.TestCase):
    """MoveAnalysis dataclass should be populated correctly."""

    def test_hard_analysis_contains_move_scores(self):
        board = Board()
        board.cells[0] = HUMAN  # Give it a partly-filled board
        _, analysis = get_ai_move(board, "Hard")
        self.assertTrue(analysis.pruning_used)
        self.assertGreater(analysis.nodes_explored, 0)
        self.assertEqual(len(analysis.move_scores), len(board.legal_moves()))

    def test_medium_analysis_not_pruned(self):
        board = Board()
        _, analysis = get_ai_move(board, "Medium")
        self.assertFalse(analysis.pruning_used)
        self.assertGreater(analysis.nodes_explored, 0)

    def test_easy_analysis_zero_nodes(self):
        board = Board()
        _, analysis = get_ai_move(board, "Easy")
        self.assertEqual(analysis.nodes_explored, 0)
        self.assertIn(analysis.chosen_move, range(9))


if __name__ == "__main__":
    unittest.main(verbosity=2)
