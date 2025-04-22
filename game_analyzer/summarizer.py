# from game import Move 
# from game import ChessGame
from pgn_parser import PGNParser
from visualizer import plot_time_deltas
from analyzer import Analyzer

def read_pgn_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def main():

    parser=PGNParser()
    pgn_text = read_pgn_file('./data/sample/data.pgn')
    game=parser.parse_pgn(pgn_text)
    #print(game.moves)
    white,black=game.get_time_deltas()
    print(sum(white)+sum(black))
    plot_time_deltas(game)
    analyzer=Analyzer(r".\engine\stockfish\stockfish-windows-x86-64-avx2.exe")
    analyzer.analyze_game(game)
    blunders=analyzer.find_blunders(game)
    #print("blunders",blunders)
    best_moves=analyzer.find_best_move(game)
    #print("best_moves",best_moves)
    wdl_stats=analyzer.get_wdl_stats(game)
    #print("wdl_stats",wdl_stats)
    mistakes=analyzer.find_mistakes(game)
    #print("mistakes",mistakes)
    highlights=analyzer.find_highlights(game)
    print("highlights",highlights)


main()

