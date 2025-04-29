# game_analyzer/pgn_parser.py

import chess.pgn
import io
from datetime import datetime
from game_analyzer.game import ChessGame, Move

class PGNParser:
    def parse_pgn(self, pgn_text):
        pgn_io = io.StringIO(pgn_text)
        game = chess.pgn.read_game(pgn_io)

        headers = game.headers
        moves = []

        node = game

        while not node.is_end():
            next_node = node.variation(0)
            move_san = node.board().san(next_node.move)
            moves.append(Move(
                move_number=node.board().fullmove_number,
                san=move_san,
                clock_time=600  # default dummy time
            ))
            node = next_node

        # ✅ SAFE date parsing
        raw_date = headers.get("Date", "2024.01.01")
        try:
            parsed_date = datetime.strptime(raw_date, "%Y.%m.%d").date()
        except ValueError:
            parsed_date = datetime(2024, 1, 1).date()

        return ChessGame(
            white=headers.get("White", "?"),
            black=headers.get("Black", "?"),
            result=headers.get("Result", "*"),
            time_control=headers.get("TimeControl", "600+5"),
            date=parsed_date,
            moves=moves
        )
