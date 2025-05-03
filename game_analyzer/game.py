# Author: Ruthura ,Sravanthi
# Date: 05-02-2025
# Description : This code defines a Move class,Chess Game Class to store information about each move and each individual game.

class Move:
    """
    Represents a single move in a chess game.

    Attributes:
        move_number (int): The move number in the game.
        san (str): Standard Algebraic Notation (SAN) for the move.
        clock_time (float): Remaining time after the move in seconds.
        timestamp (float): Optional timestamp for when the move was played.
        eval_before (dict): Stockfish evaluation before the move.
        eval_after (dict): Stockfish evaluation after the move.
    """

    def __init__(self, move_number, san, clock_time=None, timestamp=None):
        self.move_number = move_number
        self.san = san
        self.clock_time = clock_time  
        self.timestamp = timestamp
        self.eval_before = None
        self.eval_after = None

class ChessGame:
    """
    Represents a full chess game with metadata and list of moves.

    Attributes:
        date (datetime.date): Date of the game.
        white (str): Name of the white player.
        black (str): Name of the black player.
        result (str): Game result (e.g., "1-0", "0-1", "draw").
        time_control (str): Format of time control (e.g., "600").
        link (str): External link to the game (e.g., chess.com link).
        moves (list): List of Move objects.
        metadata (dict): Additional PGN header information.
    """
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
        """
        Adds a Move object to the game's move list.

        Args:
            move (Move): The move to be added.
        """
        self.moves.append(move)

    def get_time_deltas(game):
        """
        Computes time taken per move by each player based on clock times.

        Returns:
            tuple: Two lists containing time spent on each move by white and black.
        """
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
