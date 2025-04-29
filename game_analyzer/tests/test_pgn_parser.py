# game_analyzer/tests/test_pgn_parser.py

from game_analyzer.pgn_parser import PGNParser


def test_parse_simple_pgn():
    pgn_text = """[Event "Test Event"]
[Site "?"]
[Date "2024.04.29"]
[Round "?"]
[White "WhitePlayer"]
[Black "BlackPlayer"]
[Result "1-0"]
[TimeControl "600+5"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
"""
    parser = PGNParser()
    game = parser.parse_pgn(pgn_text)

    assert game.white == "WhitePlayer"
    assert game.black == "BlackPlayer"
    assert game.result == "1-0"
    assert len(game.moves) == 6
