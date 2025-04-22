# analysis/visualizer.py
import matplotlib.pyplot as plt
import chess
import chess.svg
import os

def plot_time_deltas(game, save_path="time_plot.png"):
   
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
    plt.savefig(save_path)
    plt.close()

def save_board_snapshot(fen, filename="board.svg"):
    board = chess.Board(fen)
    svg = chess.svg.board(board)
    with open(filename, "w") as f:
        f.write(svg)
