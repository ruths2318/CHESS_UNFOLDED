# analysis/visualizer.py
import matplotlib.pyplot as plt
import chess
import chess.svg
import os
from django.conf import settings

def plot_time_deltas(game, filename="time_plot.png"):

    folder = os.path.join(settings.BASE_DIR, "game_analyzer", "static", "plots")
    os.makedirs(folder, exist_ok=True)

    full_path = os.path.join(folder, filename)
   
    white_deltas, black_deltas = game.get_time_deltas()

    plt.figure(figsize=(10, 4))
    
    # Plot white and black time per move
    plt.plot(range(1, len(white_deltas)+1), white_deltas, marker='o', label='White')
    plt.plot(range(1, len(black_deltas)+1), black_deltas, marker='s', label='Black')
    
    plt.title("Time Spent per Move")
    plt.xlabel("Move Number (half-moves)")
    plt.ylabel("Seconds Spent")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(full_path)
    plt.close()


def plot_wdl_over_moves(wdl_by_move, moves=None, filename='wdl_plot.png'):


    folder = os.path.join(settings.BASE_DIR, "game_analyzer", "static", "plots")
    os.makedirs(folder, exist_ok=True)

    full_path = os.path.join(folder, filename)

    white_probs = [wdl['white'] for wdl in wdl_by_move]
    draw_probs = [wdl['draw'] for wdl in wdl_by_move]
    black_probs = [wdl['black'] for wdl in wdl_by_move]

    x = list(range(1, len(wdl_by_move) + 1))

    plt.figure(figsize=(12, 6))
    plt.stackplot(x, white_probs, draw_probs, black_probs, labels=['White', 'Draw', 'Black'], alpha=0.85)
    plt.legend(loc='upper right')
    plt.title('WDL Probabilities Over Game Moves')
    plt.xlabel('Move Number')
    plt.ylabel('Probability (%)')

    # if moves:
    #     plt.xticks(x, moves, rotation=90)

    plt.tight_layout()
    plt.savefig(full_path)
    plt.close()



def save_board_snapshot(fen, filename="board.svg"):
    board = chess.Board(fen)
    svg = chess.svg.board(board)
    with open(filename, "w") as f:
        f.write(svg)
