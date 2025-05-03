import pytest
from unittest import mock
import os

import visualizer



def test_save_board_snapshot_creates_file(tmp_path):
    # Provide a starting FEN
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    filename = tmp_path / "test_board.svg"

    visualizer.save_board_snapshot(fen, filename=str(filename))

    # Check if file was created
    assert filename.exists(), "Board snapshot file was not created"
