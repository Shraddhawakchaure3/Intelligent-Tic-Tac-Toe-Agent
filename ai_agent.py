"""
ai_agent.py
-----------
Implements the AI game-playing agent for Tic-Tac-Toe.

Difficulty levels
-----------------
  Easy   – picks a random legal move.
  Medium – uses depth-limited Minimax (depth ≤ 3) with a heuristic
           evaluation function for non-terminal states.
  Hard   – uses full Minimax with Alpha-Beta pruning; the AI is
           provably optimal and will never lose.

Scoring convention
------------------
  +10  – AI (O) wins
  -10  – Human (X) wins
    0  – Draw

Scores are adjusted by depth so the AI prefers quicker wins and
delays losses as long as possible.
"""

import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from game_logic import Board, AI, HUMAN, EMPTY


# ---------------------------------------------------------------------------
# Data class for carrying analysis metadata back to the GUI panel
# ---------------------------------------------------------------------------

@dataclass
class MoveAnalysis:
    """Captures statistics from a single AI move calculation."""
    difficulty: str = ""
    chosen_move: int = -1
    score: float = 0.0
    nodes_explored: int = 0
    depth_reached: int = 0
    move_scores: List[Tuple[int, float]] = field(default_factory=list)
    pruning_used: bool = False


# ---------------------------------------------------------------------------
# Heuristic evaluation for Medium difficulty (non-terminal states)
# ---------------------------------------------------------------------------

def _heuristic_evaluate(board: Board) -> float:
    """
    A lightweight heuristic that scores a non-terminal board position
    by counting 'two-in-a-row' patterns for both players.

    Scoring per line:
      AI has 2, line open  → +3
      AI has 1, line open  → +1
      Human has 2, open    → -3
      Human has 1, open    → -1
    """
    from game_logic import WIN_COMBINATIONS

    score = 0.0
    for a, b, c in WIN_COMBINATIONS:
        line = [board.cells[a], board.cells[b], board.cells[c]]
        ai_count = line.count(AI)
        human_count = line.count(HUMAN)
        empty_count = line.count(EMPTY)

        # Only score lines that are still winnable by exactly one player
        if ai_count > 0 and human_count > 0:
            continue  # blocked line – no value
        if ai_count == 2 and empty_count == 1:
            score += 3
        elif ai_count == 1 and empty_count == 2:
            score += 1
        elif human_count == 2 and empty_count == 1:
            score -= 3
        elif human_count == 1 and empty_count == 2:
            score -= 1
    return score


# ---------------------------------------------------------------------------
# Core Minimax (no pruning)
# ---------------------------------------------------------------------------

def _minimax(
    board: Board,
    depth: int,
    is_maximising: bool,
    counter: List[int],
) -> float:
    """
    Standard Minimax algorithm with recursive game-tree search.

    Parameters
    ----------
    board          : current board state (modified in-place, then restored)
    depth          : current depth (increases with each recursive call)
    is_maximising  : True when it is the AI's turn to move
    counter        : single-element list used to count explored nodes

    Returns
    -------
    float – the evaluated score for the current board state
    """
    counter[0] += 1  # count every node visit

    winner = board.check_winner()
    if winner == AI:
        return 10 - depth   # prefer quicker wins
    if winner == HUMAN:
        return depth - 10   # prefer delaying losses
    if board.is_full():
        return 0             # draw

    moves = board.legal_moves()

    if is_maximising:
        # AI's turn – maximise the score
        best = float("-inf")
        for move in moves:
            board.cells[move] = AI
            score = _minimax(board, depth + 1, False, counter)
            board.cells[move] = EMPTY  # backtrack
            best = max(best, score)
        return best
    else:
        # Human's turn – minimise the score
        best = float("inf")
        for move in moves:
            board.cells[move] = HUMAN
            score = _minimax(board, depth + 1, True, counter)
            board.cells[move] = EMPTY  # backtrack
            best = min(best, score)
        return best


# ---------------------------------------------------------------------------
# Minimax with Alpha-Beta Pruning (Hard difficulty)
# ---------------------------------------------------------------------------

def _minimax_alpha_beta(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    is_maximising: bool,
    counter: List[int],
) -> float:
    """
    Minimax enhanced with Alpha-Beta pruning.

    Alpha-Beta pruning eliminates branches that cannot affect the final
    decision, often dramatically reducing the number of nodes explored.
    However, pruning is order-dependent – in the worst case (already
    sorted in the worst order) it provides no benefit over plain Minimax.

    Parameters
    ----------
    board          : current board state (modified in-place, then restored)
    depth          : current depth in the game tree
    alpha          : best score the maximiser can guarantee so far
    beta           : best score the minimiser can guarantee so far
    is_maximising  : True when it is the AI's (maximiser's) turn
    counter        : single-element list used to count explored nodes

    Returns
    -------
    float – the evaluated score for the current board state

    Pruning logic
    -------------
    Maximiser prunes when it finds a move scoring ≥ beta
      (the minimiser would never allow this branch).
    Minimiser prunes when it finds a move scoring ≤ alpha
      (the maximiser already has a better option).
    """
    counter[0] += 1

    winner = board.check_winner()
    if winner == AI:
        return 10 - depth
    if winner == HUMAN:
        return depth - 10
    if board.is_full():
        return 0

    moves = board.legal_moves()

    if is_maximising:
        best = float("-inf")
        for move in moves:
            board.cells[move] = AI
            score = _minimax_alpha_beta(board, depth + 1, alpha, beta, False, counter)
            board.cells[move] = EMPTY  # backtrack

            best = max(best, score)
            alpha = max(alpha, best)

            if beta <= alpha:
                # Beta cut-off: minimiser will never choose this branch
                break
        return best
    else:
        best = float("inf")
        for move in moves:
            board.cells[move] = HUMAN
            score = _minimax_alpha_beta(board, depth + 1, alpha, beta, True, counter)
            board.cells[move] = EMPTY  # backtrack

            best = min(best, score)
            beta = min(beta, best)

            if beta <= alpha:
                # Alpha cut-off: maximiser already has a better option
                break
        return best


# ---------------------------------------------------------------------------
# Depth-limited Minimax for Medium difficulty
# ---------------------------------------------------------------------------

def _minimax_depth_limited(
    board: Board,
    depth: int,
    max_depth: int,
    is_maximising: bool,
    counter: List[int],
) -> float:
    """
    Depth-limited Minimax with a heuristic evaluation at the cutoff depth.

    When *depth* reaches *max_depth* and the game is not over, we call
    _heuristic_evaluate() instead of continuing the search.
    """
    counter[0] += 1

    winner = board.check_winner()
    if winner == AI:
        return 10 - depth
    if winner == HUMAN:
        return depth - 10
    if board.is_full():
        return 0
    if depth >= max_depth:
        return _heuristic_evaluate(board)

    moves = board.legal_moves()

    if is_maximising:
        best = float("-inf")
        for move in moves:
            board.cells[move] = AI
            score = _minimax_depth_limited(board, depth + 1, max_depth, False, counter)
            board.cells[move] = EMPTY
            best = max(best, score)
        return best
    else:
        best = float("inf")
        for move in moves:
            board.cells[move] = HUMAN
            score = _minimax_depth_limited(board, depth + 1, max_depth, True, counter)
            board.cells[move] = EMPTY
            best = min(best, score)
        return best


# ---------------------------------------------------------------------------
# Public API – get_ai_move
# ---------------------------------------------------------------------------

def get_ai_move(board: Board, difficulty: str) -> Tuple[int, MoveAnalysis]:
    """
    Select the best move for the AI based on the chosen difficulty.

    Parameters
    ----------
    board      : current Board instance
    difficulty : "Easy", "Medium", or "Hard"

    Returns
    -------
    (chosen_move_index, MoveAnalysis)
    """
    legal = board.legal_moves()
    if not legal:
        raise ValueError("No legal moves available – the board is already full.")

    analysis = MoveAnalysis(difficulty=difficulty)

    # ---- Easy ---------------------------------------------------------------
    if difficulty == "Easy":
        analysis.chosen_move = random.choice(legal)
        analysis.nodes_explored = 0
        analysis.depth_reached = 0
        return analysis.chosen_move, analysis

    # ---- Medium -------------------------------------------------------------
    if difficulty == "Medium":
        MAX_DEPTH = 3
        best_score = float("-inf")
        best_move = legal[0]
        counter = [0]
        move_scores: List[Tuple[int, float]] = []

        for move in legal:
            board.cells[move] = AI
            score = _minimax_depth_limited(board, 1, MAX_DEPTH, False, counter)
            board.cells[move] = EMPTY
            move_scores.append((move, round(score, 2)))
            if score > best_score:
                best_score = score
                best_move = move

        analysis.chosen_move = best_move
        analysis.score = round(best_score, 2)
        analysis.nodes_explored = counter[0]
        analysis.depth_reached = MAX_DEPTH
        analysis.move_scores = move_scores
        analysis.pruning_used = False
        return best_move, analysis

    # ---- Hard (default) -----------------------------------------------------
    best_score = float("-inf")
    best_move = legal[0]
    counter = [0]
    move_scores: List[Tuple[int, float]] = []

    for move in legal:
        board.cells[move] = AI
        score = _minimax_alpha_beta(
            board,
            depth=1,
            alpha=float("-inf"),
            beta=float("inf"),
            is_maximising=False,
            counter=counter,
        )
        board.cells[move] = EMPTY
        move_scores.append((move, round(score, 2)))
        if score > best_score:
            best_score = score
            best_move = move

    analysis.chosen_move = best_move
    analysis.score = round(best_score, 2)
    analysis.nodes_explored = counter[0]
    analysis.depth_reached = 9  # full depth
    analysis.move_scores = move_scores
    analysis.pruning_used = True
    return best_move, analysis
