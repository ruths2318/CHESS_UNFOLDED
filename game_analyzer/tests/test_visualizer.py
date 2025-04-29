# game_analyzer/tests/test_visualizer.py

import os
from game_analyzer.visualizer import plot_time_deltas
from game_analyzer.game import ChessGame, Move

def test_plot_time_deltas_creates_file(tmp_path):
    game = ChessGame(
        white="White",
        black="Black",
        result="1-0",
        time_control="600+5",
        date="2024.01.01"
    )
    game.add_move(Move(1, "e4", 600))
    game.add_move(Move(2, "e5", 590))

    output_path = tmp_path / "plot.png"
    plot_time_deltas(game, str(output_path))  # ✅ Fixed this line

    assert os.path.exists(output_path)
