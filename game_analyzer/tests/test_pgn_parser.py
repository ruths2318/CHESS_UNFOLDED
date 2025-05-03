import pytest
from unittest.mock import patch, MagicMock
from pgn_parser import PGNParser
from game_analyzer.game import ChessGame, Move

# This is a sample PGN string that represents a short chess game.
# It includes metadata like event name, players, result, time control, and moves.
sample_pgn = """
[Event "Test Event"]
[Site "?"]
[Date "2024.04.29"]
[Round "?"]
[White "WhitePlayer"]
[Black "BlackPlayer"]
[Result "1-0"]
[Termination "1-0"]
[TimeControl "600+5"]
[Link "https://example.com/game"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
"""

def test_parse_clock_with_valid_comment():
    # Test if the parser correctly extracts clock time from a valid comment.
    # Example input: [%clk 0:10:15.2] means 10 minutes, 15.2 seconds left.
    result = PGNParser.parse_clock("[%clk 0:10:15.2]")
    expected_seconds = 10 * 60 + 15 + 0.2  # 10 minutes * 60 + 15 seconds + 0.2
    assert result == expected_seconds

def test_parse_clock_with_invalid_comment():
    # Test that if a comment does not contain clock information, the parser returns None.
    result = PGNParser.parse_clock("No clock info here")
    assert result is None

def test_parse_pgn_returns_chess_game():
    # Create a parser instance
    parser = PGNParser()

    # Parse the sample PGN string into a ChessGame object
    game = parser.parse_pgn(sample_pgn)

    # Check that the parser returns a ChessGame instance
    assert isinstance(game, ChessGame)

    # Verify that key game attributes are correctly extracted from PGN headers
    assert game.white == "WhitePlayer"
    assert game.black == "BlackPlayer"
    assert game.result == "1-0"
    assert game.time_control == "600+5"
    assert game.link == "https://example.com/game"

    # Check that the moves were parsed and added to the game
    assert len(game.moves) == 6  # There should be 6 moves in total

    # Verify details of the first move
    first_move = game.moves[0]
    assert isinstance(first_move, Move)
    assert first_move.move_number == 1
    assert first_move.san == "e4"

def test_parse_pgn_metadata_contains_headers():
    # Create a parser instance
    parser = PGNParser()

    # Parse the sample PGN string
    game = parser.parse_pgn(sample_pgn)

    # Confirm that the metadata dictionary contains PGN headers
    assert "Event" in game.metadata
    assert game.metadata["Event"] == "Test Event"
    assert "White" in game.metadata
    assert game.metadata["White"] == "WhitePlayer"
