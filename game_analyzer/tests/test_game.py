# test_game.py

import pytest
from game import ChessGame, Move


def test_chess_game_creation():



    game = ChessGame(
        white="Magnus Carlsen",
        black="Hikaru Nakamura",
        result="1-0",
        time_control="600+5",
        date="2024-05-01",
        link="https://example.com/game"  # we add a fake link here
    )

    # we check if the game saved all the info we gave it
    assert game.white == "Magnus Carlsen"
    assert game.black == "Hikaru Nakamura"
    assert game.result == "1-0"
    assert game.time_control == "600+5"
    assert game.date == "2024-05-01"
    assert game.link == "https://example.com/game"

    # Since it’s a new game, it shouldn’t have any moves yet
    assert game.moves == []

def test_add_move():
    # We want to make sure adding a move actually works

    # First, create a new game with dummy link
    game = ChessGame("White", "Black", "1-0", "600+5", "2024-05-01", "https://example.com/game")

    # Then make a move (move number 1, played e4, 600 seconds left)
    move = Move(1, "e4", 600)

    # Add the move to the game
    game.add_move(move)

    # Now the game should have exactly one move in its list
    assert len(game.moves) == 1

    # And that move should match what we added
    assert game.moves[0].san == "e4"


def test_move_with_evaluation():
    # We want to check if moves can store evaluation data (like Stockfish eval)

    # Pretend this was the evaluation before the move
    eval_before = {"type": "cp", "value": 50}

    # And this was the evaluation after the move
    eval_after = {"type": "cp", "value": 100}

    # Now we make a move normally
    move = Move(1, "e4", 600)

    # We assign eval_before and eval_after after creation
    move.eval_before = eval_before
    move.eval_after = eval_after

    # Check if the move saved the evaluations correctly
    assert move.eval_before["type"] == "cp"
    assert move.eval_before["value"] == 50
    assert move.eval_after["type"] == "cp"
    assert move.eval_after["value"] == 100
