"""
main.py
-------
Application entry point for the Intelligent Tic-Tac-Toe game.

Run with:
    python main.py
"""

import tkinter as tk
from gui import TicTacToeGUI


def main() -> None:
    root = tk.Tk()

    # High-DPI awareness on Windows (optional, gracefully skipped if unavailable)
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
