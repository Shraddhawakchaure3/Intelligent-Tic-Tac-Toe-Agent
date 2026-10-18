"""
game_logic.py
-------------
Handles all Tic-Tac-Toe board management, legal move generation,
win/draw detection, and board state queries.

This module is intentionally kept separate from the GUI and AI code
so each layer can be tested independently.
"""

from typing import List, Optional, Tuple

# Cell values
EMPTY: str = ""
HUMAN: str = "X"
AI: str = "O"

# All eight winning combinations (rows, columns, diagonals)
WIN_COMBINATIONS: List[Tuple[int, int, int]] = [
    (0, 1, 2),  # Top row
    (3, 4, 5),  # Middle row
    (6, 7, 8),  # Bottom row
    (0, 3, 6),  # Left column
    (1, 4, 7),  # Middle column
    (2, 5, 8),  # Right column
    (0, 4, 8),  # Main diagonal
    (2, 4, 6),  # Anti-diagonal
]


class Board:
    """
    Represents a Tic-Tac-Toe board as a flat list of 9 cells (indices 0–8).

    Layout:
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8

    Each cell contains EMPTY (""), HUMAN ("X"), or AI ("O").
    """

    def __init__(self) -> None:
        """Initialise an empty 3×3 board."""
        self.cells: List[str] = [EMPTY] * 9

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Reset the board to the initial empty state."""
        self.cells = [EMPTY] * 9

    def copy(self) -> "Board":
        """Return a deep copy of the current board (used by the AI)."""
        new_board = Board()
        new_board.cells = self.cells[:]
        return new_board

    def get_cell(self, index: int) -> str:
        """Return the value at position *index* (0–8)."""
        return self.cells[index]

    def set_cell(self, index: int, player: str) -> None:
        """Place *player*'s mark at *index*. Raises ValueError if occupied."""
        if not (0 <= index <= 8):
            raise ValueError(f"Cell index {index} is out of range (0–8).")
        if self.cells[index] != EMPTY:
            raise ValueError(f"Cell {index} is already occupied by '{self.cells[index]}'.")
        self.cells[index] = player

    def clear_cell(self, index: int) -> None:
        """Remove the mark at *index* (used internally by the AI for backtracking)."""
        self.cells[index] = EMPTY

    def is_cell_empty(self, index: int) -> bool:
        """Return True if cell at *index* is unoccupied."""
        return self.cells[index] == EMPTY

    # ------------------------------------------------------------------
    # Legal move generation
    # ------------------------------------------------------------------

    def legal_moves(self) -> List[int]:
        """Return a list of indices for all empty (legal) cells."""
        return [i for i in range(9) if self.cells[i] == EMPTY]

    def is_full(self) -> bool:
        """Return True when no empty cell remains on the board."""
        return EMPTY not in self.cells

    # ------------------------------------------------------------------
    # Terminal-state detection
    # ------------------------------------------------------------------

    def check_winner(self) -> Optional[str]:
        """
        Return the winner ("X" or "O") if one exists, otherwise None.
        Scans all eight winning lines.
        """
        for a, b, c in WIN_COMBINATIONS:
            if (
                self.cells[a] != EMPTY
                and self.cells[a] == self.cells[b] == self.cells[c]
            ):
                return self.cells[a]
        return None

    def is_draw(self) -> bool:
        """Return True if the board is full and there is no winner."""
        return self.is_full() and self.check_winner() is None

    def is_game_over(self) -> bool:
        """Return True if the game has ended (win or draw)."""
        return self.check_winner() is not None or self.is_full()

    def get_winning_line(self) -> Optional[Tuple[int, int, int]]:
        """
        Return the triple of indices forming the winning line, or None.
        Useful for highlighting the winning cells in the GUI.
        """
        for a, b, c in WIN_COMBINATIONS:
            if (
                self.cells[a] != EMPTY
                and self.cells[a] == self.cells[b] == self.cells[c]
            ):
                return (a, b, c)
        return None

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Human-readable string representation of the board."""
        def fmt(v: str) -> str:
            return v if v else "."

        rows = []
        for row in range(3):
            start = row * 3
            rows.append(" | ".join(fmt(self.cells[start + col]) for col in range(3)))
        return "\n---------\n".join(rows)
