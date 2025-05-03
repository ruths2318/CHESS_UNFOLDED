import pytest
from unittest.mock import MagicMock, patch
from analyzer import Analyzer

@pytest.fixture
def mock_game():
    # Create a fake move with basic evaluation values
    mock_move = MagicMock()
    mock_move.san = "e4"  # The move in standard algebraic notation
    mock_move.eval_before = {"type": "cp", "value": 20}  # Evaluation before the move
    mock_move.eval_after = {"type": "cp", "value": -300}  # Evaluation after the move

    # Create a fake game with a list of moves (only one here for simplicity)
    game = MagicMock()
    game.moves = [mock_move]
    return game


@pytest.fixture
def analyzer():
    # We "patch" Stockfish inside the analyzer module so no real Stockfish engine is needed
    with patch("analyzer.Stockfish") as MockStockfish:
        mock_sf = MockStockfish.return_value
        mock_sf.get_evaluation.return_value = {"type": "cp", "value": 0}
        mock_sf.get_best_move.return_value = "e2e4"
        mock_sf.get_wdl_stats.return_value = [40, 20, 40]
        yield Analyzer()

# This tests the to_cp() function when input is already centipawn (cp)
def test_to_cp_cp(analyzer):
    result = analyzer.to_cp({"type": "cp", "value": 150})
    assert result == 150  # should return the same cp value

# This tests to_cp() when evaluation is checkmate in a few moves (positive)
def test_to_cp_mate_positive(analyzer):
    result = analyzer.to_cp({"type": "mate", "value": 1})
    assert result == 10000  # we treat mate in X as a large number

# This tests to_cp() for checkmate in negative value (i.e. opponent mating)
def test_to_cp_mate_negative(analyzer):
    result = analyzer.to_cp({"type": "mate", "value": -3})
    assert result == -10000  # large negative number for mate against us

# This tests that analyze_game updates move evaluations
def test_analyze_game_calls_stockfish(analyzer, mock_game):
    analyzer.analyze_game(mock_game)
    # Check if evaluations are still there after analysis
    assert mock_game.moves[0].eval_before is not None
    assert mock_game.moves[0].eval_after is not None

# This checks if find_blunders correctly identifies a blunder
def test_find_blunders(analyzer, mock_game):
    blunders = analyzer.find_blunders(mock_game)
    assert len(blunders) >= 1  # expect at least one blunder detected
    assert blunders[0]["move"] == "e4"  # it should be our fake move

# This tests finding the best moves
def test_find_best_moves(analyzer, mock_game):
    best_moves = analyzer.find_best_moves(mock_game)
    assert isinstance(best_moves, list)  # should return a list

# This tests identifying mistakes or inaccuracies
def test_find_mistakes(analyzer, mock_game):
    from unittest.mock import MagicMock

    move1 = MagicMock()
    move1.eval_before = {"type": "cp", "value": 100}
    move1.eval_after = {"type": "cp", "value": 200}

    move2 = MagicMock()
    move2.eval_before = {"type": "cp", "value": 150}
    move2.eval_after = {"type": "cp", "value": 400}

    mock_game.moves = [move1, move2]

    mistakes = analyzer.find_mistakes(mock_game)
    assert any(item["type"] in ["Mistake", "Inaccuracy"] for item in mistakes)


# This tests finding the single best move in the whole game
def test_find_overall_best_move(analyzer, mock_game):
    best_move = analyzer.find_overall_best_move(mock_game)
    assert best_move is not None
    assert best_move["move"] == "e4"

# This tests finding the biggest blunder
def test_find_biggest_blunder(analyzer, mock_game):
    blunder = analyzer.find_biggest_blunder(mock_game)
    assert blunder is not None
    assert blunder["move"] == "e4"

# This tests finding the first blunder in the game
def test_find_first_blunder(analyzer, mock_game):
    first_blunder = analyzer.find_first_blunder(mock_game)
    assert first_blunder is not None
    assert first_blunder["move"] == "e4"

# This tests identifying turning points in the game
def test_find_turning_points(analyzer, mock_game):
    turning_points = analyzer.find_turning_points(mock_game)
    assert isinstance(turning_points, list)  # should return a list

# This tests finding all highlights (best move, blunders, turning point)
def test_find_highlights(analyzer, mock_game):
    highlights = analyzer.find_highlights(mock_game)
    assert "best_move" in highlights
    assert "biggest_blunder" in highlights
    assert "first_blunder" in highlights
    assert "turning_point" in highlights

# This tests normalizing WDL (win/draw/loss) stats to percentages
def test_normalize_wdl(analyzer):
    wdl = analyzer.normalize_wdl([40, 20, 40])
    assert wdl == {"white": 40.0, "draw": 20.0, "black": 40.0}
