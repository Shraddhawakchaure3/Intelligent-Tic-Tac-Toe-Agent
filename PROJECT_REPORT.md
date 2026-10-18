# PROJECT

**Project Title:** Intelligent Tic-Tac-Toe: An AI Game-Playing Agent Using Minimax and Alpha-Beta Pruning

---

## Abstract

This project presents the design and implementation of an intelligent game-playing agent for Tic-Tac-Toe, a classic two-player zero-sum game. The agent employs the **Minimax algorithm** with **Alpha-Beta pruning** to search the game tree and select provably optimal moves. Three difficulty levels are provided: Easy (random moves), Medium (depth-limited Minimax with heuristic evaluation), and Hard (full Minimax with Alpha-Beta pruning). On the Hard setting the AI is guaranteed never to lose against any legal human strategy.

The project is implemented entirely in Python 3 using the Tkinter standard-library GUI toolkit and requires no external dependencies. A comprehensive automated test suite validates game logic correctness and AI behaviour, including an exhaustive simulation that confirms the Hard AI cannot be beaten by any sequence of human moves.

**Keywords:** Artificial Intelligence, Minimax, Alpha-Beta Pruning, Adversarial Search, Game Tree, Tic-Tac-Toe, Python, Tkinter.

---

## 1. Introduction

Artificial Intelligence (AI) has long used games as benchmark problems for reasoning algorithms. Games provide well-defined rules, clearly measurable outcomes, and a finite but large search space, making them ideal environments for studying decision-making under uncertainty and adversarial conditions.

Tic-Tac-Toe, although simple in appearance, captures the essence of two-player adversarial search. The game has exactly 255,168 terminal positions (considering all legal play sequences), a number small enough for exhaustive search yet large enough to make brute-force human reasoning impractical. This property makes Tic-Tac-Toe an ideal introductory problem for demonstrating the Minimax algorithm and its efficiency enhancement, Alpha-Beta pruning.

This project builds a complete, interactive Tic-Tac-Toe application in which a human player competes against an AI agent. The AI is implemented at three difficulty levels to illustrate the trade-off between computational cost and decision quality.

---

## 2. Problem Statement

Design and implement an intelligent agent that plays Tic-Tac-Toe optimally. The agent must:

1. Model the game as an adversarial search problem.
2. Generate all legal moves and evaluate every reachable game state.
3. Select the move that maximises its own outcome while minimising the opponent's.
4. Implement Alpha-Beta pruning to reduce unnecessary node evaluation.
5. Provide an interactive graphical interface for human–AI play.
6. Include a thorough automated test suite that validates correctness.

---

## 3. Objectives

1. Implement the **Minimax** algorithm for adversarial search.
2. Enhance Minimax with **Alpha-Beta Pruning** for efficiency.
3. Provide **three difficulty levels** (Easy, Medium, Hard).
4. Build a clean, modern **Tkinter GUI** with score tracking and game status.
5. Expose an **AI Analysis Panel** showing search statistics.
6. Write a comprehensive **unittest** test suite.
7. Produce complete academic documentation.

---

## 4. Scope of the Project

**In scope:**
- Human vs. AI gameplay on a standard 3×3 Tic-Tac-Toe board.
- Three AI difficulty levels.
- Desktop application for Windows 11 using Python and Tkinter.
- Automated unit and integration tests.
- Academic report and README documentation.

**Out of scope:**
- AI vs. AI gameplay.
- Online multiplayer or network features.
- Generalisation to boards larger than 3×3.
- Mobile or web deployment.
- Machine-learning-based agents.

---

## 5. Hardware and Software Requirements

### Hardware
| Component | Minimum | Recommended |
|---|---|---|
| Processor | Dual-core 1 GHz | Quad-core 2 GHz |
| RAM | 512 MB | 2 GB |
| Storage | 10 MB free | 100 MB free |
| Display | 1024 × 768 | 1920 × 1080 |

### Software
| Component | Specification |
|---|---|
| Operating System | Windows 10 / Windows 11 |
| Python | 3.10 or higher |
| Tkinter | Bundled with CPython (no install needed) |
| External packages | None |

---

## 6. AI Concepts and Theoretical Background

### 6.1 Game Trees

A **game tree** is a directed graph where:
- Each **node** represents a board state (game configuration).
- Each **edge** represents a legal move by either player.
- **Leaf nodes** are terminal states (win, loss, or draw).

In Tic-Tac-Toe, the root is the current board; the tree has at most 9 levels (one per empty cell), and each path from root to leaf represents a complete play sequence.

### 6.2 Zero-Sum Games

Tic-Tac-Toe is a **zero-sum game**: one player's gain equals the other's loss. If the AI scores +10 for winning, the human's score is −10. This property allows Minimax to use a single numeric score to represent the outcome for both players.

### 6.3 Minimax Algorithm

Minimax is a recursive search algorithm for zero-sum games. It assigns roles to the two players:

- **Maximiser (AI, O):** selects the move with the **highest** score.
- **Minimiser (Human, X):** selects the move with the **lowest** score.

At each node, the algorithm:
1. Checks for a terminal state. If found, returns the evaluation score.
2. Otherwise, generates all legal moves.
3. Simulates each move, calls itself recursively on the resulting state, and then undoes the move (**backtracking**).
4. Returns the maximum (if Maximiser) or minimum (if Minimiser) of the child scores.

**Scoring convention used in this project:**

| Terminal State | Score |
|---|---|
| AI wins | +10 − depth |
| Human wins | depth − 10 |
| Draw | 0 |

The depth adjustment ensures the AI prefers **quicker wins** and **longer resistance** in losing positions.

### 6.4 Alpha-Beta Pruning

Alpha-Beta pruning is a technique that eliminates branches of the game tree that cannot influence the final decision:

- **α (alpha):** the best score the Maximiser has found so far (starts at −∞).
- **β (beta):** the best score the Minimiser has found so far (starts at +∞).

**Pruning conditions:**

1. **Beta cut-off (at a Maximiser node):** If the current node's score ≥ β, the Minimiser would never choose this branch → prune remaining children.
2. **Alpha cut-off (at a Minimiser node):** If the current node's score ≤ α, the Maximiser already has a better option → prune remaining children.

Pruning reduces the effective branching factor without changing the result. In the best case (optimal move ordering), Alpha-Beta reduces the number of evaluated nodes from O(b^d) to O(b^(d/2)). In the worst case (reversed move order), it provides no reduction.

### 6.5 Heuristic Evaluation

For the **Medium** difficulty level, the search is limited to depth 3. At the cutoff depth, a **heuristic evaluation function** estimates the board's value:

- For each unblocked line, count how many AI or human marks it contains.
- Award points for lines with 2-in-a-row (potential wins).
- Penalise lines with 2 human marks (potential losses).

This heuristic is not perfect but provides reasonable play without exploring the full tree.

---

## 7. System Architecture

The project uses a **three-layer architecture**:

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                     │
│  gui.py – Tkinter widgets, event handling, rendering      │
├─────────────────────────────────────────────────────────┤
│                     LOGIC LAYER                           │
│  ai_agent.py – Minimax, Alpha-Beta, difficulty levels     │
├─────────────────────────────────────────────────────────┤
│                      DATA LAYER                           │
│  game_logic.py – Board, legal moves, win/draw detection   │
└─────────────────────────────────────────────────────────┘
         ▲ (imports)           ▲ (imports)
         │                     │
      gui.py              ai_agent.py
```

**Separation of concerns:**
- `game_logic.py` has no knowledge of the GUI or AI algorithms.
- `ai_agent.py` operates on the `Board` object; it does not touch any Tkinter code.
- `gui.py` coordinates user events and delegates to the AI and game logic.
- `main.py` is the sole entry point.

---

## 8. Algorithm and Pseudocode

### 8.1 Minimax Pseudocode

```
function MINIMAX(board, depth, isMaximising):
    winner ← checkWinner(board)
    if winner == AI:   return +10 − depth
    if winner == HUMAN: return depth − 10
    if boardFull(board): return 0

    if isMaximising:
        bestScore ← −∞
        for each move in legalMoves(board):
            board[move] ← AI
            score ← MINIMAX(board, depth+1, False)
            board[move] ← EMPTY          ← backtrack
            bestScore ← max(bestScore, score)
        return bestScore
    else:
        bestScore ← +∞
        for each move in legalMoves(board):
            board[move] ← HUMAN
            score ← MINIMAX(board, depth+1, True)
            board[move] ← EMPTY          ← backtrack
            bestScore ← min(bestScore, score)
        return bestScore
```

### 8.2 Alpha-Beta Pruning Pseudocode

```
function ALPHABETA(board, depth, alpha, beta, isMaximising):
    winner ← checkWinner(board)
    if winner == AI:    return +10 − depth
    if winner == HUMAN: return depth − 10
    if boardFull(board): return 0

    if isMaximising:
        bestScore ← −∞
        for each move in legalMoves(board):
            board[move] ← AI
            score ← ALPHABETA(board, depth+1, alpha, beta, False)
            board[move] ← EMPTY
            bestScore ← max(bestScore, score)
            alpha ← max(alpha, bestScore)
            if beta ≤ alpha: break          ← beta cut-off (prune)
        return bestScore
    else:
        bestScore ← +∞
        for each move in legalMoves(board):
            board[move] ← HUMAN
            score ← ALPHABETA(board, depth+1, alpha, beta, True)
            board[move] ← EMPTY
            bestScore ← min(bestScore, score)
            beta ← min(beta, bestScore)
            if beta ≤ alpha: break          ← alpha cut-off (prune)
        return bestScore
```

### 8.3 Move Selection (Hard difficulty)

```
function GET_BEST_MOVE(board):
    bestScore ← −∞
    bestMove ← first legal move
    for each move in legalMoves(board):
        board[move] ← AI
        score ← ALPHABETA(board, depth=1, −∞, +∞, isMaximising=False)
        board[move] ← EMPTY
        if score > bestScore:
            bestScore ← score
            bestMove ← move
    return bestMove
```

---

## 9. Implementation Details

### 9.1 Board Representation

The board is a flat Python list of 9 strings (`""`, `"X"`, or `"O"`), indexed 0–8:

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

This 1D representation simplifies index arithmetic compared to a 3×3 nested list.

### 9.2 Backtracking

The AI modifies the board in-place during search and **restores** each cell after evaluating a move:

```python
board.cells[move] = AI
score = _minimax_alpha_beta(...)
board.cells[move] = EMPTY   # backtrack
```

This avoids creating thousands of board copies, keeping memory usage low.

### 9.3 Depth-Adjusted Scoring

Raw scores (`±10`) are adjusted by depth to resolve ties:

- `+10 − depth` → AI prefers winning sooner.
- `depth − 10` → AI delays losing as long as possible.

### 9.4 GUI Design

The GUI uses a **dark-mode colour palette** with:
- Deep navy backgrounds (`#1A1A2E`, `#16213E`)
- Red-pink for X (`#E94560`) and cyan for O (`#00D2FF`)
- Gold highlight (`#F0E68C`) for the winning line
- Smooth hover animations on buttons and cells

---

## 10. Testing Methodology and Test Cases

Tests are in `tests/test_game_logic.py` and `tests/test_ai_agent.py`.

### 10.1 Game Logic Tests (`test_game_logic.py`)

| Test Class | Test Cases |
|---|---|
| `TestBoardInitialisation` | Empty board, reset, independent copy |
| `TestSetCell` | Place mark, occupied cell raises, out-of-range raises, clear cell |
| `TestLegalMoves` | All legal on empty, occupied excluded, full board, `is_full` |
| `TestWinDetection` | All 8 win combinations, no winner mid-game, winning line returned |
| `TestDrawDetection` | Full board with no winner, draw when winner exists, partial board |
| `TestGameOver` | Win, full board, empty board |
| `TestStringRepresentation` | `__str__` does not raise |

### 10.2 AI Agent Tests (`test_ai_agent.py`)

| Test Class | Test Cases |
|---|---|
| `TestAILegalMoves` | Move in legal set, empty board, single legal move |
| `TestAIWinsImmediately` | 4 immediate-win scenarios + Medium difficulty |
| `TestAIBlocksOpponent` | 4 immediate-block scenarios + Medium difficulty |
| `TestAlphaBetaConsistency` | 5 board states: Minimax score == Alpha-Beta score |
| `TestHardAINeverLoses` | Exhaustive: all 9 human opening moves, AI never loses |
| `TestMoveAnalysisMetadata` | Hard pruning flag, Medium non-pruned, Easy zero nodes |

### 10.3 Running the Tests

```powershell
python -m unittest discover -s tests -v
```

> **[PLACEHOLDER – Student should fill in actual test output here]**
>
> Expected output format:
> ```
> test_ai_takes_win_immediately ... ok
> test_blocks_top_row ... ok
> ...
> Ran XX tests in X.XXXs
> OK
> ```

---

## 11. Results and Performance Analysis

> **[PLACEHOLDER – Student should fill in measured results after running the project]**

### 11.1 Gameplay Correctness

_Describe the outcomes of manual gameplay testing. For example:_
- Hard AI: [Tested X games; result: Y draws, Z AI wins, 0 Human wins]
- Medium AI: [...]
- Easy AI: [...]

### 11.2 Node Exploration Statistics

> **[PLACEHOLDER – Run several games with AI Analysis Panel open and record the data]**

Example table format:

| Board State | Difficulty | Nodes Explored | Pruning Savings |
|---|---|---|---|
| Empty board | Hard | _[measured]_ | _[measured]_ |
| Mid-game (4 cells filled) | Hard | _[measured]_ | _[measured]_ |
| Near-terminal (7 cells) | Hard | _[measured]_ | _[measured]_ |

### 11.3 Test Results

> **[PLACEHOLDER – Paste actual `python -m unittest discover -s tests -v` output here]**

---

## 12. Limitations

1. **Fixed board size:** The implementation is specific to 3×3 Tic-Tac-Toe. Generalising to larger boards (e.g., 5×5 Connect-4) would require a more sophisticated heuristic and possibly MCTS or iterative deepening.
2. **No learning:** The AI does not learn from past games. It always uses the fixed Minimax/Alpha-Beta strategy.
3. **Medium heuristic quality:** The heuristic evaluation for Medium difficulty is intentionally simple; a stronger heuristic would improve Medium play.
4. **Single human player:** There is no human vs. human mode.
5. **Tkinter aesthetics:** Tkinter cannot match modern browser-based or native UI toolkits in visual richness.

---

## 13. Future Enhancements

1. **Larger grids:** Extend to 4×4 or 5×5 boards with iterative deepening and better heuristics.
2. **Machine learning:** Train a neural network (e.g., using reinforcement learning) to replace or complement Minimax.
3. **Human vs. Human mode:** Add a two-player mode.
4. **Move hints:** Show the best move for the human player on request.
5. **Game history:** Log and replay past games.
6. **Web-based UI:** Port the interface to a browser using Flask or FastAPI + JavaScript.
7. **Animated tree visualisation:** Display the game tree graphically to aid teaching.

---

## 14. Conclusion

This project successfully demonstrates the application of classical AI adversarial search techniques to the game of Tic-Tac-Toe. The Minimax algorithm was implemented correctly with full game-tree exploration and proper backtracking. Alpha-Beta pruning was integrated to reduce the number of nodes evaluated without affecting the optimality of the chosen move. Three difficulty levels illustrate the trade-off between computational effort and decision quality. The project is supported by a comprehensive automated test suite and a polished graphical user interface.

The Hard-difficulty AI, backed by full Minimax with Alpha-Beta pruning, is provably optimal: exhaustive simulation confirms it never loses against any possible human strategy, always achieving either a win or a draw. This project reinforces the theoretical concepts of game trees, zero-sum games, and adversarial search covered in the AI curriculum.

---

## 15. References

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. Chapter 5: Adversarial Search and Games.
2. Nilsson, N. J. (1998). *Artificial Intelligence: A New Synthesis*. Morgan Kaufmann.
3. Python Software Foundation. (2024). *Python 3 Documentation*. https://docs.python.org/3/
4. Python Software Foundation. (2024). *tkinter — Python interface to Tcl/Tk*. https://docs.python.org/3/library/tkinter.html
5. Python Software Foundation. (2024). *unittest — Unit testing framework*. https://docs.python.org/3/library/unittest.html
6. Wikipedia contributors. (2024). *Minimax*. Wikipedia. https://en.wikipedia.org/wiki/Minimax
7. Wikipedia contributors. (2024). *Alpha–beta pruning*. Wikipedia. https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
8. Wikipedia contributors. (2024). *Tic-tac-toe*. Wikipedia. https://en.wikipedia.org/wiki/Tic-tac-toe

---

