"""
gui.py
------
Redesigned Tkinter GUI for the Intelligent Tic-Tac-Toe game.

Theme  : Dark navy + teal — professional AI application aesthetic.
Layout : Fixed two-column layout (board left, controls right).
         Collapsible AI Analysis and How It Works panels below.

All game logic, AI callbacks, and method interfaces are fully
preserved from the original implementation. Only presentation
code has changed.
"""

import tkinter as tk
from tkinter import font as tkfont
import sys

from game_logic import Board, HUMAN, AI, EMPTY
from ai_agent import get_ai_move, MoveAnalysis

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
C_BG          = "#0B1120"   # main window background
C_PANEL       = "#111C30"   # side panel / card background
C_CARD        = "#17243A"   # elevated card inside panel
C_ACCENT      = "#2DD4BF"   # primary teal accent
C_ACCENT2     = "#60A5FA"   # secondary blue accent
C_TEXT        = "#F1F5F9"   # primary text
C_TEXT2       = "#94A3B8"   # secondary / muted text
C_BORDER      = "#28364D"   # subtle borders / dividers
C_SUCCESS     = "#34D399"   # green — human win
C_ERROR       = "#FB7185"   # red — AI win / error
C_WIN_BG      = "#1E3A2F"   # winning-cell background (dark green tint)
C_WIN_FG      = "#34D399"   # winning-cell text

# Cell states
C_CELL_EMPTY  = "#17243A"   # resting empty cell
C_CELL_HOVER  = "#1F3352"   # hover over empty cell
C_CELL_X      = "#2DD4BF"   # X mark colour
C_CELL_O      = "#60A5FA"   # O mark colour

# Button colours
C_BTN_PRI     = "#2DD4BF"   # primary button (New Game)
C_BTN_PRI_H   = "#22B3A4"
C_BTN_SEC     = "#1E2D45"   # secondary button (Reset)
C_BTN_SEC_H   = "#28364D"

AI_DELAY_MS   = 450         # ms before AI responds


# ---------------------------------------------------------------------------
# Small helper: bordered card frame
# ---------------------------------------------------------------------------
def _card(parent, **kw) -> tk.Frame:
    """Return a Frame styled as a bordered card."""
    defaults = dict(bg=C_CARD, bd=1, relief="flat", highlightthickness=1,
                    highlightbackground=C_BORDER, highlightcolor=C_BORDER)
    defaults.update(kw)
    return tk.Frame(parent, **defaults)


class TicTacToeGUI:
    """Main application window — redesigned with dark navy / teal theme."""

    # -----------------------------------------------------------------------
    # Construction
    # -----------------------------------------------------------------------

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Intelligent Tic-Tac-Toe — Minimax & Alpha-Beta Pruning")
        self.root.configure(bg=C_BG)
        self.root.resizable(True, True)
        self.root.minsize(780, 560)

        # Game state
        self.board = Board()
        self.current_player: str = HUMAN
        self.game_active: bool = False
        self.difficulty: str = "Hard"

        # Scores
        self.score_human: int = 0
        self.score_ai:    int = 0
        self.score_draws: int = 0

        # UI references
        self.cell_buttons: list = []
        self.analysis_visible: tk.BooleanVar = tk.BooleanVar(value=False)
        self.about_visible:    tk.BooleanVar = tk.BooleanVar(value=False)

        self._setup_fonts()
        self._build_ui()
        self._start_new_game()

    # -----------------------------------------------------------------------
    # Fonts
    # -----------------------------------------------------------------------

    def _setup_fonts(self) -> None:
        self.font_title   = tkfont.Font(family="Segoe UI", size=17, weight="bold")
        self.font_sub     = tkfont.Font(family="Segoe UI", size=9)
        self.font_badge   = tkfont.Font(family="Segoe UI", size=8, weight="bold")
        self.font_cell    = tkfont.Font(family="Segoe UI", size=36, weight="bold")
        self.font_section = tkfont.Font(family="Segoe UI", size=9,  weight="bold")
        self.font_label   = tkfont.Font(family="Segoe UI", size=10)
        self.font_bold    = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.font_turn    = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.font_score_n = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.font_score_l = tkfont.Font(family="Segoe UI", size=9)
        self.font_btn     = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.font_mono    = tkfont.Font(family="Consolas",  size=9)
        self.font_diff    = tkfont.Font(family="Segoe UI", size=9,  weight="bold")

    # -----------------------------------------------------------------------
    # Master layout
    # -----------------------------------------------------------------------

    def _build_ui(self) -> None:
        self._build_header()

        # Thin accent divider
        tk.Frame(self.root, bg=C_ACCENT, height=2).pack(fill="x")

        # Main area
        body = tk.Frame(self.root, bg=C_BG)
        body.pack(fill="both", expand=True, padx=20, pady=14)
        body.columnconfigure(0, weight=5, minsize=340)
        body.columnconfigure(1, weight=3, minsize=240)
        body.rowconfigure(0, weight=1)

        # Left — game board
        left = tk.Frame(body, bg=C_BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        left.rowconfigure(0, weight=1)
        left.columnconfigure(0, weight=1)
        self._build_board(left)

        # Right — control panel
        right = tk.Frame(body, bg=C_PANEL,
                         highlightthickness=1, highlightbackground=C_BORDER)
        right.grid(row=0, column=1, sticky="nsew")
        self._build_side_panel(right)

        # Collapsible panels (below main area)
        self._build_analysis_panel()
        self._build_about_panel()

    # -----------------------------------------------------------------------
    # Header
    # -----------------------------------------------------------------------

    def _build_header(self) -> None:
        hdr = tk.Frame(self.root, bg=C_BG, pady=14)
        hdr.pack(fill="x", padx=20)

        # Left cluster: icon + title + subtitle
        title_col = tk.Frame(hdr, bg=C_BG)
        title_col.pack(side="left")

        icon_lbl = tk.Label(title_col, text="◈", font=tkfont.Font(family="Segoe UI", size=22),
                            bg=C_BG, fg=C_ACCENT)
        icon_lbl.pack(side="left", padx=(0, 10))

        text_col = tk.Frame(title_col, bg=C_BG)
        text_col.pack(side="left")

        tk.Label(text_col, text="Intelligent Tic-Tac-Toe",
                 font=self.font_title, bg=C_BG, fg=C_TEXT).pack(anchor="w")
        tk.Label(text_col,
                 text="AI Game-Playing Agent  |  Minimax + Alpha-Beta Pruning",
                 font=self.font_sub, bg=C_BG, fg=C_TEXT2).pack(anchor="w")

        # Right cluster: status badge
        badge_frame = tk.Frame(hdr, bg=C_BG)
        badge_frame.pack(side="right", anchor="n", pady=4)

        self.badge_dot  = tk.Label(badge_frame, text="●", font=self.font_badge,
                                   bg=C_BG, fg=C_ACCENT)
        self.badge_dot.pack(side="left")
        self.badge_text = tk.Label(badge_frame, text="READY",
                                   font=self.font_badge, bg=C_BG, fg=C_TEXT2)
        self.badge_text.pack(side="left", padx=(2, 0))

    def _set_badge(self, label: str, colour: str) -> None:
        self.badge_dot.configure(fg=colour)
        self.badge_text.configure(text=label)

    # -----------------------------------------------------------------------
    # Board
    # -----------------------------------------------------------------------

    def _build_board(self, parent: tk.Frame) -> None:
        """Build the 3×3 grid of cell buttons, centred in *parent*."""
        # Outer centering frame
        outer = tk.Frame(parent, bg=C_BG)
        outer.grid(row=0, column=0)

        # Board background card
        board_bg = tk.Frame(outer, bg=C_BORDER, padx=3, pady=3)
        board_bg.pack()

        # Inner grid
        grid_frame = tk.Frame(board_bg, bg=C_BORDER)
        grid_frame.pack()

        self.cell_buttons = []
        for i in range(9):
            r, c = divmod(i, 3)
            btn = tk.Button(
                grid_frame,
                text="",
                font=self.font_cell,
                width=3,
                height=1,
                bg=C_CELL_EMPTY,
                fg=C_TEXT,
                activebackground=C_CELL_HOVER,
                activeforeground=C_TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda idx=i: self._on_cell_click(idx),
            )
            btn.grid(row=r, column=c, padx=2, pady=2, ipadx=6, ipady=8)
            btn.bind("<Enter>", lambda e, b=btn: self._on_cell_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self._on_cell_leave(b))
            self.cell_buttons.append(btn)

    def _on_cell_enter(self, btn: tk.Button) -> None:
        if btn["text"] == "" and self.game_active and self.current_player == HUMAN:
            btn.configure(bg=C_CELL_HOVER)

    def _on_cell_leave(self, btn: tk.Button) -> None:
        if btn["text"] == "":
            btn.configure(bg=C_CELL_EMPTY)

    # -----------------------------------------------------------------------
    # Side panel
    # -----------------------------------------------------------------------

    def _build_side_panel(self, parent: tk.Frame) -> None:
        # Pad the whole panel
        inner = tk.Frame(parent, bg=C_PANEL)
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        # ── Difficulty ──────────────────────────────────────────────────────
        self._section_label(inner, "DIFFICULTY")

        self.diff_var = tk.StringVar(value=self.difficulty)
        diff_row = tk.Frame(inner, bg=C_PANEL)
        diff_row.pack(fill="x", pady=(4, 0))

        self._diff_btns: dict = {}
        for level in ("Easy", "Medium", "Hard"):
            b = tk.Button(
                diff_row,
                text=level,
                font=self.font_diff,
                relief="flat", bd=0,
                padx=10, pady=5,
                cursor="hand2",
                command=lambda lv=level: self._select_difficulty(lv),
            )
            b.pack(side="left", padx=(0, 4))
            self._diff_btns[level] = b

        self._refresh_diff_buttons()

        self._divider(inner)

        # ── Turn indicator ──────────────────────────────────────────────────
        self._section_label(inner, "CURRENT TURN")

        turn_card = _card(inner)
        turn_card.pack(fill="x", pady=(4, 0))

        self.turn_var = tk.StringVar(value="")
        self.turn_label = tk.Label(
            turn_card,
            textvariable=self.turn_var,
            font=self.font_turn,
            bg=C_CARD, fg=C_ACCENT,
            padx=10, pady=8,
            anchor="w",
        )
        self.turn_label.pack(fill="x")

        self._divider(inner)

        # ── Status ──────────────────────────────────────────────────────────
        self._section_label(inner, "STATUS")

        status_card = _card(inner)
        status_card.pack(fill="x", pady=(4, 0))

        self.status_var = tk.StringVar(value="")
        self.status_label = tk.Label(
            status_card,
            textvariable=self.status_var,
            font=self.font_label,
            bg=C_CARD, fg=C_TEXT2,
            wraplength=210,
            justify="left",
            padx=10, pady=8,
            anchor="w",
        )
        self.status_label.pack(fill="x")

        self._divider(inner)

        # ── Scoreboard ──────────────────────────────────────────────────────
        self._section_label(inner, "SCOREBOARD")

        score_row = tk.Frame(inner, bg=C_PANEL)
        score_row.pack(fill="x", pady=(6, 0))
        score_row.columnconfigure((0, 1, 2), weight=1)

        score_defs = [
            ("You", "X", C_ACCENT,  "human"),
            ("AI",  "O", C_ACCENT2, "ai"),
            ("Draw","—", C_TEXT2,   "draws"),
        ]
        self.score_vars: dict = {}
        for col, (label, mark, clr, key) in enumerate(score_defs):
            sc = _card(score_row)
            sc.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 4, 0))

            tk.Label(sc, text=mark, font=self.font_turn,
                     bg=C_CARD, fg=clr, pady=4).pack()

            var = tk.StringVar(value="0")
            self.score_vars[key] = var
            tk.Label(sc, textvariable=var, font=self.font_score_n,
                     bg=C_CARD, fg=clr).pack()

            tk.Label(sc, text=label, font=self.font_score_l,
                     bg=C_CARD, fg=C_TEXT2, pady=4).pack()

        self._divider(inner)

        # ── Action buttons ──────────────────────────────────────────────────
        new_btn = self._primary_button(inner, "New Game", self._start_new_game)
        new_btn.pack(fill="x", pady=(0, 6))

        reset_btn = self._secondary_button(inner, "Reset Scores", self._reset_scores)
        reset_btn.pack(fill="x")

        self._divider(inner)

        # ── Collapsible toggle buttons ───────────────────────────────────────
        self._toggle_btn(inner, "AI Analysis", self.analysis_visible).pack(
            fill="x", pady=(0, 4))
        self._toggle_btn(inner, "How It Works", self.about_visible).pack(fill="x")

    # -----------------------------------------------------------------------
    # Difficulty button logic
    # -----------------------------------------------------------------------

    def _select_difficulty(self, level: str) -> None:
        self.diff_var.set(level)
        self._refresh_diff_buttons()
        self._on_difficulty_change()

    def _refresh_diff_buttons(self) -> None:
        selected = self.diff_var.get()
        colours = {
            "Easy":   (C_SUCCESS,  "#0B1120"),
            "Medium": (C_ACCENT2,  "#0B1120"),
            "Hard":   (C_ERROR,    "#0B1120"),
        }
        for level, btn in self._diff_btns.items():
            if level == selected:
                bg, fg = colours[level]
                btn.configure(bg=bg, fg=fg,
                              activebackground=bg, activeforeground=fg)
            else:
                btn.configure(bg=C_CARD, fg=C_TEXT2,
                              activebackground=C_CARD, activeforeground=C_TEXT)

    # -----------------------------------------------------------------------
    # Widget helpers
    # -----------------------------------------------------------------------

    def _section_label(self, parent, text: str) -> tk.Label:
        lbl = tk.Label(parent, text=text, font=self.font_section,
                       bg=C_PANEL, fg=C_TEXT2, anchor="w")
        lbl.pack(fill="x", pady=(10, 0))
        return lbl

    def _divider(self, parent) -> tk.Frame:
        line = tk.Frame(parent, bg=C_BORDER, height=1)
        line.pack(fill="x", pady=10)
        return line

    def _primary_button(self, parent, text: str, command) -> tk.Button:
        btn = tk.Button(
            parent, text=text, font=self.font_btn,
            bg=C_BTN_PRI, fg="#0B1120",
            activebackground=C_BTN_PRI_H, activeforeground="#0B1120",
            relief="flat", bd=0, pady=8,
            cursor="hand2", command=command,
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=C_BTN_PRI_H))
        btn.bind("<Leave>", lambda e: btn.configure(bg=C_BTN_PRI))
        return btn

    def _secondary_button(self, parent, text: str, command) -> tk.Button:
        btn = tk.Button(
            parent, text=text, font=self.font_btn,
            bg=C_BTN_SEC, fg=C_TEXT2,
            activebackground=C_BTN_SEC_H, activeforeground=C_TEXT,
            relief="flat", bd=0, pady=7,
            cursor="hand2", command=command,
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=C_BTN_SEC_H, fg=C_TEXT))
        btn.bind("<Leave>", lambda e: btn.configure(bg=C_BTN_SEC, fg=C_TEXT2))
        return btn

    def _toggle_btn(self, parent, text: str, var: tk.BooleanVar) -> tk.Button:
        # Store original text for label refresh
        btn = tk.Button(
            parent,
            text=f"▸  {text}",
            font=self.font_diff,
            bg=C_PANEL, fg=C_TEXT2,
            activebackground=C_CARD, activeforeground=C_TEXT,
            relief="flat", bd=0, pady=5,
            cursor="hand2", anchor="w",
            command=lambda v=var, t=text, container=[None]: self._toggle_panel(v, t),
        )
        btn.bind("<Enter>", lambda e: btn.configure(fg=C_TEXT))
        btn.bind("<Leave>", lambda e: btn.configure(fg=C_TEXT2))

        # Keep reference to update arrow on toggle
        if text == "AI Analysis":
            self._analysis_toggle_btn = btn
        else:
            self._about_toggle_btn = btn

        return btn

    # -----------------------------------------------------------------------
    # AI Analysis panel
    # -----------------------------------------------------------------------

    def _build_analysis_panel(self) -> None:
        self.analysis_frame = tk.Frame(self.root, bg=C_PANEL,
                                       highlightthickness=1,
                                       highlightbackground=C_BORDER)

        header = tk.Frame(self.analysis_frame, bg=C_PANEL)
        header.pack(fill="x", padx=16, pady=(10, 4))

        tk.Label(header, text="AI ANALYSIS", font=self.font_section,
                 bg=C_PANEL, fg=C_ACCENT).pack(side="left")

        # Stats grid
        stats_outer = tk.Frame(self.analysis_frame, bg=C_PANEL)
        stats_outer.pack(fill="x", padx=16, pady=(0, 6))

        # Top row: key stats
        self._stat_labels: dict = {}
        stat_defs = [
            ("chosen_move",    "Chosen Move",  "—"),
            ("score",          "Score",        "—"),
            ("nodes",          "Nodes",        "—"),
            ("depth",          "Max Depth",    "—"),
            ("pruning",        "Pruning",      "—"),
        ]
        stats_row = tk.Frame(stats_outer, bg=C_PANEL)
        stats_row.pack(fill="x", pady=(0, 6))

        for col, (key, label, default) in enumerate(stat_defs):
            sc = _card(stats_row)
            sc.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 4, 0))
            stats_row.columnconfigure(col, weight=1)

            val_var = tk.StringVar(value=default)
            self._stat_labels[key] = val_var

            tk.Label(sc, textvariable=val_var,
                     font=self.font_bold, bg=C_CARD, fg=C_ACCENT,
                     padx=6, pady=4).pack()
            tk.Label(sc, text=label,
                     font=self.font_score_l, bg=C_CARD, fg=C_TEXT2,
                     padx=6, pady=2).pack()

        # Move evaluations text box
        tk.Label(self.analysis_frame, text="Move Evaluations  (best first)",
                 font=self.font_section, bg=C_PANEL, fg=C_TEXT2,
                 anchor="w").pack(fill="x", padx=16, pady=(2, 2))

        self.analysis_text = tk.Text(
            self.analysis_frame,
            height=4,
            bg=C_CARD,
            fg=C_TEXT,
            font=self.font_mono,
            relief="flat",
            bd=0,
            state="disabled",
            wrap="word",
            padx=8,
            pady=6,
            highlightthickness=1,
            highlightbackground=C_BORDER,
        )
        self.analysis_text.pack(fill="x", padx=16, pady=(0, 10))

    def _update_analysis(self, analysis: MoveAnalysis) -> None:
        """Populate the analysis panel with the latest AI move data."""
        cell_map = {i: f"R{i//3+1}C{i%3+1}" for i in range(9)}
        chosen   = cell_map.get(analysis.chosen_move, "?")
        pruning  = "Yes" if analysis.pruning_used else "No"

        self._stat_labels["chosen_move"].set(chosen)
        self._stat_labels["score"].set(f"{analysis.score:+.1f}")
        self._stat_labels["nodes"].set(str(analysis.nodes_explored))
        self._stat_labels["depth"].set(str(analysis.depth_reached))
        self._stat_labels["pruning"].set(pruning)

        sorted_moves = sorted(analysis.move_scores, key=lambda x: -x[1])
        lines = [
            f"  {cell_map[m]:6s}  score={s:+.1f}"
            for m, s in sorted_moves
        ]

        self.analysis_text.configure(state="normal")
        self.analysis_text.delete("1.0", "end")
        self.analysis_text.insert("end", "\n".join(lines) if lines else "—")
        self.analysis_text.configure(state="disabled")

    def _clear_analysis(self) -> None:
        for key in self._stat_labels:
            self._stat_labels[key].set("—")
        self.analysis_text.configure(state="normal")
        self.analysis_text.delete("1.0", "end")
        self.analysis_text.configure(state="disabled")

    # -----------------------------------------------------------------------
    # How It Works panel
    # -----------------------------------------------------------------------

    def _build_about_panel(self) -> None:
        self.about_frame = tk.Frame(self.root, bg=C_PANEL,
                                    highlightthickness=1,
                                    highlightbackground=C_BORDER)

        tk.Label(self.about_frame, text="HOW IT WORKS",
                 font=self.font_section, bg=C_PANEL, fg=C_ACCENT,
                 anchor="w").pack(fill="x", padx=16, pady=(10, 4))

        about_text = (
            "WHAT IS A GAME-PLAYING AGENT?\n"
            "  An agent that perceives board states and selects actions (moves) to maximise\n"
            "  its own outcome. In Tic-Tac-Toe the agent (AI, O) is the Maximiser.\n\n"
            "MINIMAX\n"
            "  Recursively evaluates every reachable game state. The AI assumes the human\n"
            "  always plays optimally (Minimiser). Terminal scores: AI wins +10, human wins\n"
            "  -10, draw 0 — each adjusted by depth so quicker wins score higher.\n\n"
            "ALPHA-BETA PRUNING\n"
            "  Enhances Minimax with two bounds: alpha (Maximiser's best so far) and beta\n"
            "  (Minimiser's best so far). A branch is pruned when alpha >= beta, because\n"
            "  the opponent would never allow it. Fewer nodes explored, same decision.\n\n"
            "DIFFICULTY LEVELS\n"
            "  Easy   — Random legal move. No strategy.\n"
            "  Medium — Depth-limited Minimax (depth <= 3) with heuristic evaluation.\n"
            "  Hard   — Full Minimax + Alpha-Beta. Provably optimal; cannot lose.\n\n"
            "WHY HARD CANNOT LOSE\n"
            "  Tic-Tac-Toe is a solved game. With perfect play, the outcome is always\n"
            "  a draw or a win for the first mover in certain positions. The Minimax\n"
            "  algorithm with full depth explores all paths and always picks the optimal."
        )

        about_box = tk.Text(
            self.about_frame,
            height=13,
            bg=C_CARD,
            fg=C_TEXT2,
            font=self.font_mono,
            relief="flat",
            bd=0,
            state="disabled",
            wrap="none",
            padx=10,
            pady=8,
            highlightthickness=1,
            highlightbackground=C_BORDER,
        )
        about_box.pack(fill="x", padx=16, pady=(0, 10))
        about_box.configure(state="normal")
        about_box.insert("end", about_text)
        about_box.configure(state="disabled")

    # -----------------------------------------------------------------------
    # Panel toggle
    # -----------------------------------------------------------------------

    def _toggle_panel(self, var: tk.BooleanVar, name: str) -> None:
        var.set(not var.get())
        is_open = var.get()

        if name == "AI Analysis":
            btn = self._analysis_toggle_btn
            frame = self.analysis_frame
        else:
            btn = self._about_toggle_btn
            frame = self.about_frame

        arrow = "▾" if is_open else "▸"
        btn.configure(text=f"{arrow}  {name}")

        if is_open:
            frame.pack(fill="x", padx=20, pady=(0, 8))
        else:
            frame.pack_forget()

    # -----------------------------------------------------------------------
    # Game flow  (all method signatures preserved from original)
    # -----------------------------------------------------------------------

    def _start_new_game(self) -> None:
        """Reset board state and begin a new game (Human always goes first)."""
        self.board.reset()
        self.current_player = HUMAN
        self.game_active = True
        self.difficulty = self.diff_var.get()

        for btn in self.cell_buttons:
            btn.configure(
                text="", fg=C_TEXT, bg=C_CELL_EMPTY,
                state="normal", relief="flat",
            )

        self._update_turn_label()
        self.status_var.set("Your move — click a cell to place X.")
        self.status_label.configure(fg=C_TEXT2)
        self._set_badge("IN PROGRESS", C_ACCENT)
        self._clear_analysis()

    def _on_difficulty_change(self) -> None:
        """Apply difficulty change and restart the game."""
        self.difficulty = self.diff_var.get()
        self._start_new_game()

    def _on_cell_click(self, index: int) -> None:
        """Handle human player clicking a cell."""
        if not self.game_active:
            return
        if self.current_player != HUMAN:
            return
        if not self.board.is_cell_empty(index):
            self.status_var.set("That cell is occupied — choose an empty one.")
            self.status_label.configure(fg=C_ERROR)
            return

        # Place human mark
        self.board.set_cell(index, HUMAN)
        self.cell_buttons[index].configure(text="X", fg=C_CELL_X)

        if self._check_game_over():
            return

        # Switch to AI
        self.current_player = AI
        self._update_turn_label()
        self.status_var.set("AI is thinking…")
        self.status_label.configure(fg=C_TEXT2)

        self._set_board_enabled(False)
        self.root.after(AI_DELAY_MS, self._ai_turn)

    def _ai_turn(self) -> None:
        """Execute the AI's turn."""
        if not self.game_active:
            return

        move, analysis = get_ai_move(self.board, self.difficulty)
        self.board.set_cell(move, AI)
        self.cell_buttons[move].configure(text="O", fg=C_CELL_O)

        if self.analysis_visible.get():
            self._update_analysis(analysis)

        if self._check_game_over():
            return

        self.current_player = HUMAN
        self._update_turn_label()
        self.status_var.set("Your move — click a cell to place X.")
        self.status_label.configure(fg=C_TEXT2)
        self._set_board_enabled(True)

    def _check_game_over(self) -> bool:
        """Return True if the game has ended; update UI accordingly."""
        winner = self.board.check_winner()
        if winner:
            winning_line = self.board.get_winning_line()
            if winning_line:
                for idx in winning_line:
                    self.cell_buttons[idx].configure(bg=C_WIN_BG, fg=C_WIN_FG)
            self._set_board_enabled(False)
            self.game_active = False

            if winner == HUMAN:
                self.score_human += 1
                self.score_vars["human"].set(str(self.score_human))
                self.status_var.set("You win! Well played.")
                self.status_label.configure(fg=C_SUCCESS)
                self.turn_var.set("You Win!")
                self.turn_label.configure(fg=C_SUCCESS)
                self._set_badge("YOU WIN", C_SUCCESS)
            else:
                self.score_ai += 1
                self.score_vars["ai"].set(str(self.score_ai))
                self.status_var.set("AI wins! Try a different strategy.")
                self.status_label.configure(fg=C_ERROR)
                self.turn_var.set("AI Wins")
                self.turn_label.configure(fg=C_ERROR)
                self._set_badge("AI WINS", C_ERROR)
            return True

        if self.board.is_draw():
            self._set_board_enabled(False)
            self.game_active = False
            self.score_draws += 1
            self.score_vars["draws"].set(str(self.score_draws))
            self.status_var.set("It's a draw — perfect play from both sides.")
            self.status_label.configure(fg=C_TEXT2)
            self.turn_var.set("Draw")
            self.turn_label.configure(fg=C_TEXT2)
            self._set_badge("DRAW", C_TEXT2)
            return True

        return False

    def _set_board_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for btn in self.cell_buttons:
            if btn["text"] == "":
                btn.configure(state=state)

    def _update_turn_label(self) -> None:
        if self.current_player == HUMAN:
            self.turn_var.set("Your Turn  (X)")
            self.turn_label.configure(fg=C_CELL_X)
        else:
            self.turn_var.set("AI's Turn  (O)")
            self.turn_label.configure(fg=C_CELL_O)

    def _reset_scores(self) -> None:
        self.score_human = 0
        self.score_ai    = 0
        self.score_draws = 0
        for key in self.score_vars:
            self.score_vars[key].set("0")
        self.status_var.set("Scores reset.")
        self.status_label.configure(fg=C_TEXT2)
