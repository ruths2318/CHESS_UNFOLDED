# Author: Ruthura ,Sravanthi
# Date: 05-02-2025
# Description : This code parses the PGN file to create a chess game object.

import re
import io
import chess
import chess.pgn
from game_analyzer.game import ChessGame, Move
from datetime import datetime

class PGNParser:
    """
    A parser class for converting PGN text into a structured ChessGame object.
    """
    @staticmethod
    def parse_clock(comment):
        """
        Parses the clock time from a move comment in PGN (e.g. [%clk 0:09:58.5]).

        Args:
            comment (str): The comment string from the PGN.

        Returns:
            float or None: Time remaining in seconds, or None if not found.
        """
        
        match = re.search(r"\[%clk (\d+):(\d+):(\d+)(\.(\d+))?\]", comment)
    
        if match:
            h = int(match.group(1))
            m = int(match.group(2))
            s = int(match.group(3)) if match.group(3) else 0
            dec = int(match.group(5)) if match.group(5) else 0
            return h * 3600 + m * 60 + s + dec / 10.0
        return None


    def parse_pgn(self, pgn_text):
        """
        Parses a full PGN string and converts it into a ChessGame object.

        Args:
            pgn_text (str): Full PGN text including headers and moves.

        Returns:
            ChessGame: A structured representation of the game with metadata and move details.
        """

        # Read PGN content using chess library
        game = chess.pgn.read_game(io.StringIO(pgn_text))
        headers = game.headers

        # Initialize ChessGame with header metadata
        g = ChessGame(
            date=datetime.strptime(headers["Date"], "%Y.%m.%d").date(),
            white=headers["White"],
            black=headers["Black"],
            result=headers["Termination"],
            time_control=headers["TimeControl"],
            link=headers['Link']
        )
        g.metadata = dict(headers)

        # Set up a board and parse each move
        board = game.board()
        move_number = 1

        for node in game.mainline():
            move = node.move
            san = board.san(move)
            comment = node.comment
            clock = self.parse_clock(comment)
            timestamp = None  

            g.add_move(Move(move_number, san, clock_time=clock, timestamp=timestamp))
            move_number += 1
            board.push(move)

        return g

