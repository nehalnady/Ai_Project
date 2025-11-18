import time
from movegen import generate_move_pairs
from evaluator import Evaluator, WIN_SCORE

class Searcher:
    def __init__(self):
        self.tt = {}        # transposition table
        self.evaluator = Evaluator()
        self.nodes = 0

    def negamax(self, board, depth, alpha, beta, color):
        self.nodes += 1

        # Transposition Table lookup
        old = self.tt.get(board.hash)
        if old is not None and old["depth"] >= depth:
            return old["score"]

        # Terminal or depth reached
        if depth == 0:
            score = self.evaluator.evaluate(board, color)
            return score

        best_score = -10**15

        moves = generate_move_pairs(board, is_first_move=False)

        for move in moves:
            board.apply_move(move, color)

            score = -self.negamax(board, depth - 1, -beta, -alpha, -color)

            board.undo_move(move, color)

            if score > best_score:
                best_score = score

            if best_score > alpha:
                alpha = best_score

            if alpha >= beta:
                break  # alpha-beta cutoff

        # Save to TT
        self.tt[board.hash] = {"depth": depth, "score": best_score}

        return best_score


    def iterative_deepening(self, board, color, max_depth=3, time_limit=5):
        start = time.time()
        best_move = None

        moves = generate_move_pairs(board, is_first_move=False)

        for depth in range(1, max_depth + 1):
            best_score = -10**15

            for move in moves:
                if time.time() - start > time_limit:
                    return best_move

                board.apply_move(move, color)
                score = -self.negamax(board, depth - 1, -WIN_SCORE, WIN_SCORE, -color)
                board.undo_move(move, color)

                if score > best_score:
                    best_move = move
                    best_score = score

        return best_move

    def find_immediate_block(self, board, color):
        """
        Check if the opponent has a 5-in-a-row next turn.
        If yes, return a move that blocks it immediately.
        """
        opp = -color
        moves = generate_move_pairs(board, is_first_move=False)  # <-- pass is_first_move

        for move in moves:
            board.apply_move(move, opp)  # simulate opponent move
            score = self.evaluator.evaluate(board, opp)
            board.undo_move(move, opp)
            if score >= WIN_SCORE:  # opponent can win
                return move  # block this move
        return None
