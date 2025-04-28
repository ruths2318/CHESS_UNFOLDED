# tests/test_visualizer.py
import os

from game_analyzer.game import ChessGame, Move
from game_analyzer.visualizer import plot_time_deltas


def test_plot_time_deltas_creates_file():
    game = ChessGame("White", "Black", "1-0", "600+5")
    game.add_move(Move(1, "e4", 600))
    game.add_move(Move(2, "e5", 590))

    plot_time_deltas(game, save_path="test_time_plot.png")

    assert os.path.exists("test_time_plot.png")

    # Clean up (remove the test file after checking)
    os.remove("test_time_plot.png")
