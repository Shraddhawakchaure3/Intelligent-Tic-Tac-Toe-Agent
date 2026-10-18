# Intelligent Tic-Tac-Toe: AI Game-Playing Agent

> An AI-powered Tic-Tac-Toe implementation using **Minimax** and **Alpha-Beta Pruning**  
> Built with Python 3.10+ and Tkinter · No external dependencies

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Running the Application](#running-the-application)
6. [Running the Tests](#running-the-tests)
7. [How the AI Works](#how-the-ai-works)
8. [Architecture](#architecture)
9. [Difficulty Levels](#difficulty-levels)
10. [Demonstration Guide](#demonstration-guide)

---

## Project Overview

This project implements an intelligent Tic-Tac-Toe agent that uses the **Minimax algorithm** enhanced with **Alpha-Beta Pruning** to make optimal decisions. It is an academic project for a college AI course and demonstrates core adversarial search concepts.

- **Human plays X**, **AI plays O**
- On **Hard** difficulty the AI is provably optimal and will never lose
- A toggleable **AI Analysis Panel** shows search statistics after each AI move
- An **About / How It Works** section explains the algorithms in plain English

---

## Features

| Feature | Details |
|---|---|
| 3 Difficulty Levels | Easy (random), Medium (depth-limited Minimax), Hard (full Minimax + Alpha-Beta) |
| Win/Draw Detection | All 8 winning lines; draw on full board |
| Invalid-Move Guard | Occupied cells are rejected gracefully |
| Session Scoreboard | Tracks Human wins, AI wins, and draws |
| AI Analysis Panel | Nodes explored, depth, move scores, pruning status |
| About Section | Plain-English explanation of the algorithms |
| Winning Highlight | The winning three cells are highlighted in gold |
| Restart / Reset | New Game and Reset Scores buttons |

---

## Project Structure

```
AI Project/
├── main.py              # Application entry point
├── game_logic.py        # Board, legal moves, win/draw detection
├── ai_agent.py          # Minimax, Alpha-Beta, difficulty levels
├── gui.py               # Tkinter interface and event handling
├── requirements.txt     # No external dependencies
├── README.md            # This file
├── PROJECT_REPORT.md    # Academic project report
└── tests/
    ├── test_game_logic.py   # Game-rule unit tests
    └── test_ai_agent.py     # AI correctness tests
```

---

## Installation

1. Ensure **Python 3.10 or higher** is installed.  
   Download from [python.org](https://www.python.org/downloads/) — on Windows, tick **"Add Python to PATH"** and **"tcl/tk and IDLE"**.

2. No `pip install` is needed — the project uses only the Python standard library.

3. Clone or download this repository to a local folder.

---

## Running the Application

```powershell
# Navigate to the project folder
cd "d:\BTECH_SEM-1\AI Project"

# Launch the game
python main.py
```

The Tic-Tac-Toe window will open. Select a difficulty and click **New Game** to start.

---

## Running the Tests

```powershell
cd "d:\Intelligent-Tic-Tac-Toe-Agent"
python -m unittest discover -s tests -v
```

All tests should pass. The test suite covers:
- All 8 winning combinations
- Draw detection
- Invalid / occupied cell handling
- AI winning on an immediate forced win
- AI blocking an immediate human win
- AI selecting only legal moves
- Alpha-Beta returning the same score as plain Minimax
- Hard AI never losing (exhaustive simulation of all human opening moves)

---

## How the AI Works

### Minimax

The AI models the game as a **game tree**. Each node represents a board state; each edge represents a legal move. The algorithm recursively evaluates every possible future state:

- **Maximiser (AI, O)** — tries to reach the highest score.
- **Minimiser (Human, X)** — tries to reach the lowest score.

**Scores:** AI wins → +10, Human wins → −10, Draw → 0.  
Depth adjustments make the AI prefer quicker wins and delay losses.

### Alpha-Beta Pruning

Alpha-Beta pruning adds two variables to Minimax:

- **α (alpha)** — the best score the Maximiser has guaranteed so far.
- **β (beta)** — the best score the Minimiser has guaranteed so far.

When α ≥ β, the current branch is **pruned** (skipped) because the opponent would never allow it. This typically reduces the number of nodes explored without changing the final decision.

> **Important:** pruning is move-order dependent. In the worst case (worst move order) it provides no benefit over plain Minimax. In the best case it reduces the branching factor from ~b to ~√b.

---

## Architecture

| Module | Responsibility |
|---|---|
| `game_logic.py` | Board state, legal moves, win/draw detection — no GUI, no AI |
| `ai_agent.py` | Search algorithms and difficulty logic — no GUI |
| `gui.py` | Tkinter layout, event handling, rendering — no game logic |
| `main.py` | Creates the root window and launches the GUI |
| `tests/` | Automated tests using `unittest` |

---

## Difficulty Levels

| Level | Algorithm | Max Depth | Notes |
|---|---|---|---|
| Easy | Random choice | 0 | Picks any legal move at random |
| Medium | Depth-limited Minimax | 3 | Heuristic eval at cutoff depth |
| Hard | Full Minimax + Alpha-Beta | 9 (full) | Provably optimal, never loses |

---

## Demonstration Guide

1. **Run** `python main.py`
2. **Select Hard** from the difficulty radio buttons.
3. **Play a game** — try to win. The AI will always block or respond optimally.
4. **Toggle "AI Analysis Panel"** to see how many nodes were explored and what scores each move received.
5. **Switch to Easy** and observe the AI's random, unstrategic behaviour.
6. **Click "New Game"** to reset the board without resetting scores.
7. **Click "Reset Scores"** to zero the scoreboard.
8. **Toggle "About / How It Works"** to read the algorithm explanation.
9. **Run the tests** to demonstrate automated verification:
   ```powershell
   python -m unittest discover -s tests -v
   ```
