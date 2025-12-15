
from Evaluator import Evaluator

class MinimaxAIAlphaBeta:
    def __init__(self):
        self.evaluator = Evaluator()
        self.transposition_table = {}

    def get_candidates(self, board):
        candidates = set()

        if board.is_board_empty():
            c = board.size // 2
            return [(c, c)]

        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != 0:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if board.is_empty(nx, ny):
                                candidates.add((nx, ny))

        return list(candidates)

    def minimax(self, board, depth, player, maximizing, alpha, beta):
        """
        Minimax with Alpha-Beta Pruning and Pattern-Based Evaluation
        """
        if depth == 0 or \
           self.evaluator.check_win(board, 1) or \
           self.evaluator.check_win(board, -1):
            return self.evaluator.evaluate(board, player)

        candidates = self.get_candidates(board)

        if maximizing:
            value = -float("inf")
            for x, y in candidates:
                board.place_stone(x, y, player)

                score = self.minimax(
                    board, depth - 1, player, False, alpha, beta
                )

                board.remove_stone(x, y)

                value = max(value, score)
                alpha = max(alpha, value)

                if beta <= alpha:
                    break  # Beta cutoff - prune
            return value

        else:
            value = float("inf")
            for x, y in candidates:
                board.place_stone(x, y, -player)

                score = self.minimax(
                    board, depth - 1, player, True, alpha, beta
                )

                board.remove_stone(x, y)

                value = min(value, score)
                beta = min(beta, value)

                if beta <= alpha:
                    break  # Alpha cutoff - prune
            return value

    def find_best_move(self, board, player, num_stones):
        print("\nAI thinking (Alpha-Beta + Pattern Recognition)...")

        candidates = self.get_candidates(board)

        if num_stones == 1:
            best_score = -float("inf")
            best_move = None

            for x, y in candidates:
                board.place_stone(x, y, player)

                score = self.minimax(
                    board, 2, player, False,
                    -float("inf"), float("inf")
                )

                board.remove_stone(x, y)

                if score > best_score:
                    best_score = score
                    best_move = (x, y)

            return [best_move]

        else:
            best_score = -float("inf")
            best_pair = None

            for i in range(len(candidates)):
                x1, y1 = candidates[i]

                for j in range(i + 1, len(candidates)):
                    x2, y2 = candidates[j]

                    board.place_stone(x1, y1, player)
                    board.place_stone(x2, y2, player)

                    score = self.minimax(
                        board, 1, player, False,
                        -float("inf"), float("inf")
                    )

                    board.remove_stone(x1, y1)
                    board.remove_stone(x2, y2)

                    if score > best_score:
                        best_score = score
                        best_pair = [(x1, y1), (x2, y2)]

            return best_pair