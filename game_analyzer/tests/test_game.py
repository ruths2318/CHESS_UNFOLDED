

from game_analyzer.game import ChessGame, Move

def test_move_creation():
    move = Move(1, "e4", 600)
    assert move.move_number == 1
    assert move.san == "e4"
    assert move.clock_time == 600
    assert move.eval_before is None
    assert move.eval_after is None

def test_chess_game_add_move():
    game = ChessGame("White", "Black", "1-0", "600+5")
    move = Move(1, "e4")
    game.add_move(move)
    assert len(game.moves) == 1
    assert game.moves[0].san == "e4"

def test_chess_game_time_deltas():
    game = ChessGame("White", "Black", "1-0", "600+5")
    game.add_move(Move(1, "e4", 600))
    game.add_move(Move(2, "e5", 590))
    white_deltas, black_deltas = game.get_time_deltas()
    assert white_deltas[0] == 0
    assert black_deltas[0] == 0
