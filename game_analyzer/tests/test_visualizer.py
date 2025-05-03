import pytest
from unittest import mock
import os

import visualizer

def test_plot_time_deltas_creates_file(tmp_path):
    # Create a dummy game object with get_time_deltas method
    mock_game = mock.Mock()
    mock_game.get_time_deltas.return_value = ([10, 20, 30], [15, 25, 35])

    # Mock Django settings to use tmp_path as BASE_DIR
    with mock.patch("visualizer.settings") as mock_settings:
        mock_settings.BASE_DIR = tmp_path


        visualizer.plot_time_deltas(mock_game, filename="test_time_plot.png")

        # The file should now exist in the mocked folder
        expected_file = tmp_path / "game_analyzer" / "static" / "plots" / "test_time_plot.png"
        assert expected_file.exists(), "Time plot file was not created"



def test_save_board_snapshot_creates_file(tmp_path):
    # Provide a starting FEN
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    filename = tmp_path / "test_board.svg"

    visualizer.save_board_snapshot(fen, filename=str(filename))

    # Check if file was created
    assert filename.exists(), "Board snapshot file was not created"
