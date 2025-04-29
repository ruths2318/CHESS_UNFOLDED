# game_analyzer/tests/test_analyzer.py

from unittest.mock import patch, MagicMock
from game_analyzer.analyzer import Analyzer
from game_analyzer.game import ChessGame, Move

@patch('game_analyzer.analyzer.Stockfish')
def test_to_cp_cp(mock_stockfish_class):
    mock_stockfish = MagicMock()
    mock_stockfish_class.return_value = mock_stockfish
    analyzer = Analyzer()
    eval_dict = {"type": "cp", "value": 50}
    assert analyzer.to_cp(eval_dict) == 50

@patch('game_analyzer.analyzer.Stockfish')
def test_to_cp_mate(mock_stockfish_class):
    mock_stockfish = MagicMock()
    mock_stockfish_class.return_value = mock_stockfish
    analyzer = Analyzer()
    eval_dict = {"type": "mate", "value": -3}
    assert analyzer.to_cp(eval_dict) == -10000

@patch('game_analyzer.analyzer.Stockfish')
def test_find_blunders_empty_game(mock_stockfish_class):
    mock_stockfish = MagicMock()
    mock_stockfish_class.return_value = mock_stockfish
    analyzer = Analyzer()
    game = ChessGame(
        white="White",
        black="Black",
        result="1-0",
        time_control="600+5",
        date="2024.01.01"   # ✅ Added date here
    )
    blunders = analyzer.find_blunders(game)
    assert isinstance(blunders, list)
    assert len(blunders) == 0
