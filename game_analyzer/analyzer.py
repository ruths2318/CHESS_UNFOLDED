# Author: Ruthura ,Sravanthi
# Date: 05-02-2025
# Description : This code finds mistakes,game highlights,blunders,turning points,best moves,etc with the help of stockfish integeration.

from stockfish import Stockfish
import chess
import chess.pgn
from game_analyzer.game import ChessGame

class Analyzer:
    """
    Analyzer class integrates with Stockfish to analyze a chess game.
    """

    def __init__(self, stockfish_path="stockfish"):
        """
        Initialize the Analyzer with Stockfish engine.
        
        Args:
            stockfish_path (str): Path to the Stockfish binary.
        """
        self.sf = Stockfish(path=stockfish_path)
    

    def analyze_game(self, game: ChessGame):
        """
        Analyzes the evaluation before and after each move in the game.

        Args:
            game (ChessGame): Parsed chess game object.
        """

        board = chess.Board()
        for i, move in enumerate(game.moves):
            self.sf.set_fen_position(board.fen())
            move.eval_before = self.sf.get_evaluation()
            board.push_san(move.san)
            self.sf.set_fen_position(board.fen())
            move.eval_after = self.sf.get_evaluation()
            

    def to_cp(self,eval_dict):
        """
        Converts Stockfish evaluation to centipawns.

        Args:
            eval_dict (dict): Stockfish evaluation.

        Returns:
            int: Evaluation in centipawns.
        """

        if eval_dict["type"] == "cp":
            return eval_dict["value"]
        elif eval_dict["type"] == "mate":
            
            return 10000 if eval_dict["value"] > 0 else -10000


    def find_blunders(self,game, threshold=300):
        """
        Identifies blunders based on a centipawn drop threshold.

        Args:
            game (ChessGame): Game to analyze.
            threshold (int): Minimum drop to consider as a blunder.

        Returns:
            list: Blunders in the game.
        """

        blunders = []
        for i, move in enumerate(game.moves):
            before = move.eval_before
            after = move.eval_after
            if before and after:
                eval_before = self.to_cp(before)
                eval_after = self.to_cp(after)
                diff = eval_after - eval_before
                if abs(diff) >= threshold:
                    blunders.append({
                        "move_number": i + 1,
                        "player": "White" if i % 2 == 0 else "Black",
                        "move": move.san,
                        "eval_before": eval_before,
                        "eval_after": eval_after,
                        "drop": diff,
                        "drop_type": "mate" if before["type"] == "mate" or after["type"] == "mate" else "cp"
                    })
        return blunders
    

    def find_best_moves(self, game):
        """
        Identifies moves that match Stockfish's best suggested move.

        Args:
            game (ChessGame): Game to analyze.

        Returns:
            list: Best moves played in the game.
        """
        best_moves = []
        board = chess.Board()

        for move in game.moves:
            # Set position BEFORE move
            self.sf.set_fen_position(board.fen())

            # Get best move from Stockfish at this point
            best_move_uci = self.sf.get_best_move()

            # Convert actual move from SAN to UCI
            try:
                actual_move = board.parse_san(move.san)
            except ValueError:
                continue  

            if best_move_uci == actual_move.uci():
                best_moves.append({
                    'move_number': board.fullmove_number,
                    'player': 'White' if board.turn else 'Black',
                    'move': move.san,
                    'uci': actual_move.uci()
                })

            # make the move on the board
            board.push(actual_move)

        return best_moves

    def normalize_wdl(self,wdl_raw):
        """
        Normalizes WDL counts to percentage.

        Args:
            wdl_raw (list): Raw WDL list from Stockfish.

        Returns:
            dict: Normalized percentages.
        """

        total = sum(wdl_raw)
        return {
            'white': round(100 * wdl_raw[0] / total, 1),
            'draw': round(100 * wdl_raw[1] / total, 1),
            'black': round(100 * wdl_raw[2] / total, 1)
        }


    def get_wdl_stats(self, game):
        """
        Collects WDL stats at each move of the game.

        Args:
            game (ChessGame): Game to analyze.

        Returns:
            list: Normalized WDL statistics over the course of the game.
        """

        wdl_stats = []
        board = chess.Board()

        for move in game.moves:
            # Get WDL before move
            self.sf.set_fen_position(board.fen())
            wdl = self.sf.get_wdl_stats()  
            normalized_wdl=self.normalize_wdl(wdl) # Returns {'white': int, 'draw': int, 'black': int}
            wdl_stats.append(normalized_wdl)

            # Play the move
            try:
                board.push_san(move.san)
            except ValueError:
                break  # Stop if move is invalid 

        return wdl_stats


    def find_mistakes(self,game, thresholds=(50, 100, 300)):
        """
        Identifies inaccuracies and mistakes based on centipawn drops.

        Args:
            game (ChessGame): Game to analyze.
            thresholds (tuple): Thresholds for inaccuracy, mistake, blunder.

        Returns:
            list: List of inaccuracies and mistakes.
        """

        inaccuracies = []
        mistakes = []

        for i, move in enumerate(game.moves):
            before = move.eval_before
            after = move.eval_after
            if before and after:
                eval_before = self.to_cp(before)
                eval_after = self.to_cp(after)
                diff = eval_after - eval_before
                abs_diff = abs(diff)

                entry = {
                    "move_number": i + 1,
                    "player": "White" if i % 2 == 0 else "Black",
                    "move": move.san,
                    "eval_before": eval_before,
                    "eval_after": eval_after,
                    "drop": diff,
                    "drop_type": "mate" if before["type"] == "mate" or after["type"] == "mate" else "cp"
                }

                if thresholds[1] <= abs_diff < thresholds[2]:
                    mistakes.append({**entry, "type": "Mistake"})
                elif thresholds[0] <= abs_diff < thresholds[1]:
                    inaccuracies.append({**entry, "type": "Inaccuracy"})

        return inaccuracies + mistakes
    
    def find_overall_best_move(self,game):
        """
        Finds the move that had the most positive evaluation change.

        Args:
            game (ChessGame): Game to analyze.

        Returns:
            dict: Details of the best move.
        """

        best_move = None
        max_gain = float('-inf')

        for i, move in enumerate(game.moves):
            before = move.eval_before
            after = move.eval_after
            if before and after:
                gain = self.to_cp(after) - self.to_cp(before)
                if gain > max_gain:
                    max_gain = gain
                    best_move = {
                        "move_number": i + 1,
                        "player": "White" if i % 2 == 0 else "Black",
                        "move": move.san,
                        "gain": gain,
                        "eval_before": self.to_cp(before),
                        "eval_after": self.to_cp(after)
                    }
        return best_move

    def find_biggest_blunder(self,game):
        """
        Finds the move that caused the largest evaluation drop.

        Args:
            game (ChessGame): Game to analyze.

        Returns:
            dict: Details of the biggest blunder.
        """

        biggest_blunder = None
        max_drop = float('-inf')

        for i, move in enumerate(game.moves):
            before = move.eval_before
            after = move.eval_after
            if before and after:
                drop = self.to_cp(before) - self.to_cp(after)
                if drop > max_drop:
                    max_drop = drop
                    biggest_blunder = {
                        "move_number": i + 1,
                        "player": "White" if i % 2 == 0 else "Black",
                        "move": move.san,
                        "drop": drop,
                        "eval_before": self.to_cp(before),
                        "eval_after": self.to_cp(after)
                    }
        return biggest_blunder

    def find_first_blunder(self,game, threshold=300):
        """
        Finds the first blunder in the game based on threshold.

        Args:
            game (ChessGame): Game to analyze.
            threshold (int): Drop to be considered a blunder.

        Returns:
            dict or None: First blunder if any, else None.
        """

        for i, move in enumerate(game.moves):
            before = move.eval_before
            after = move.eval_after
            if before and after:
                drop = self.to_cp(before) - self.to_cp(after)
                if drop >= threshold:
                    return {
                        "move_number": i + 1,
                        "player": "White" if i % 2 == 0 else "Black",
                        "move": move.san,
                        "drop": drop,
                        "eval_before": self.to_cp(before),
                        "eval_after": self.to_cp(after)
                    }
        return None

    def find_turning_points(self,game):
        """
        Identifies turning points in the game where evaluation flipped.

        Args:
            game (ChessGame): Game to analyze.

        Returns:
            list: List of turning point moves.
        """

        turning_points=[]
        for i, move in enumerate(game.moves):
            before = move.eval_before
            after = move.eval_after
            if before and after:
                val_before = self.to_cp(before)
                val_after = self.to_cp(after)
                if (val_before > 0 and val_after < 0) or (val_before < 0 and val_after > 0):
                    turning_points.append({
                        "move_number": i + 1,
                        "player": "White" if i % 2 == 0 else "Black",
                        "move": move.san,
                        "eval_before": val_before,
                        "eval_after": val_after
                    })
                
        return turning_points


    def find_highlights(self,game, swing_threshold=250):
        """
        Summarizes key game moments including best move, biggest blunder,
        first blunder, and turning points.

        Args:
            game (ChessGame): Game to analyze.
            swing_threshold (int): Not used currently but reserved for future use.

        Returns:
            dict: Highlighted game events.
        """

        best_move=self.find_overall_best_move(game)
        biggest_blunder=self.find_biggest_blunder(game)
        first_blunder=self.find_first_blunder(game)
        turning_points=self.find_turning_points(game)

        return {
        "best_move": best_move,
        "biggest_blunder": biggest_blunder,
        "first_blunder": first_blunder,
        "turning_point": turning_points
        }

   
        