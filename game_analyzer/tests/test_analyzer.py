from game_analyzer.analyzer import Analyzer
from  game_analyzer.game import ChessGame


def test_to_cp_cp():
    analyzer = Analyzer()
    eval_dict = {"type": "cp", "value": 50}
    assert analyzer.to_cp(eval_dict) == 50

def test_to_cp_mate():
    analyzer = Analyzer()
    eval_dict = {"type": "mate", "value": -3}
    assert analyzer.to_cp(eval_dict) == -10000

def test_find_blunders_empty_game():
    analyzer = Analyzer()
    game = ChessGame("White", "Black", "1-0", "600+5")
    blunders = analyzer.find_blunders(game)
    assert isinstance(blunders, list)
    assert len(blunders) == 0
