
import re
import io
import chess
import chess.pgn
from .game import ChessGame, Move
from datetime import datetime

class PGNParser:
    @staticmethod
    def parse_clock(comment):
        
        match = re.search(r"\[%clk (\d+):(\d+):(\d+)(\.(\d+))?\]", comment)
    
        if match:
            h = int(match.group(1))
            m = int(match.group(2))
            s = int(match.group(3)) if match.group(3) else 0
            dec = int(match.group(5)) if match.group(5) else 0
            return h * 3600 + m * 60 + s + dec / 10.0
        return None

    def parse_pgn(self, pgn_text):
        game = chess.pgn.read_game(io.StringIO(pgn_text))
        headers = game.headers

        g = ChessGame(
            date=datetime.strptime(headers["Date"], "%Y.%m.%d").date(),
            white=headers["White"],
            black=headers["Black"],
            result=headers["Result"],
            time_control=headers["TimeControl"]
        )
        g.metadata = dict(headers)

        board = game.board()
        move_number = 1

        for node in game.mainline():
            move = node.move
            san = board.san(move)
            comment = node.comment
            clock = self.parse_clock(comment)
            timestamp = None  # Extend if needed

            g.add_move(Move(move_number, san, clock_time=clock, timestamp=timestamp))
            move_number += 1
            board.push(move)

        return g

