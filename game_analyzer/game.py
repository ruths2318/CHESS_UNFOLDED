# Author: Ruthura ,Sravanthi
# Date: 05-02-2025
# Description : This code defines a Move class,Chess Game Class to store information about each move and each individual game.

class Move:
    def __init__(self, move_number, san, clock_time=None, timestamp=None):
        self.move_number = move_number
        self.san = san
        self.clock_time = clock_time  
        self.timestamp = timestamp
        self.eval_before = None
        self.eval_after = None

class ChessGame:
    def __init__(self, date,white, black, result, time_control, link,moves=None):
        self.date=date
        self.white = white
        self.black = black
        self.result = result
        self.time_control = time_control
        self.link=link
        self.moves = moves if moves else []
        self.metadata = {}

    def add_move(self, move):
        self.moves.append(move)

    def get_time_deltas(game):
        white_deltas = []
        black_deltas = []

        prev_white_time = None
        prev_black_time = None

        for idx, move in enumerate(game.moves):
            if idx % 2 == 0:  # White's move
                if prev_white_time is not None and move.clock_time is not None:
                    white_deltas.append(prev_white_time - move.clock_time)
                else:
                    white_deltas.append(0)
                prev_white_time = move.clock_time
            else:  # Black's move
                if prev_black_time is not None and move.clock_time is not None:
                    black_deltas.append(prev_black_time - move.clock_time)
                else:
                    black_deltas.append(0)
                prev_black_time = move.clock_time

        return white_deltas, black_deltas
