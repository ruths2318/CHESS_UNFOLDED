# game_analyzer/tests/test_game.py

from game_analyzer.game import Move, ChessGame

def test_move_creation():
    move = Move(1, "e4", 600)
    assert move.move_number == 1
    assert move.san == "e4"
    assert move.clock_time == 600
    assert move.eval_before is None
    assert move.eval_after is None

def test_chess_game_add_move():
    game = ChessGame(
        white="White",
        black="Black",
        result="1-0",
        time_control="600+5",
        date="2024.01.01"    # ✅ Added date here
    )
    move = Move(1, "e4")
    game.add_move(move)
    assert len(game.moves) == 1
    assert game.moves[0].san == "e4"

def test_chess_game_time_deltas():
    game = ChessGame(
        white="White",
        black="Black",
        result="1-0",
        time_control="600+5",
        date="2024.01.01"    # ✅ Added date here
    )
    game.add_move(Move(1, "e4", 600))
    game.add_move(Move(2, "e5", 590))
    white_deltas, black_deltas = game.get_time_deltas()
    assert white_deltas[0] == 0
    assert black_deltas[0] == 0
