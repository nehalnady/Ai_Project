from Evaluator import Evaluator


class MinimaxAIAlphaBeta:
    def __init__(self):
        self.evaluator = Evaluator()

    def get_candidates(self, board):
        """Get candidate moves near existing stones to reduce search space."""
        candidates = set()

        # If board is empty, return center position
        if board.is_board_empty():
            c = board.size // 2
            return [(c, c)]

        # Otherwise, get positions adjacent to existing stones
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != 0:  # If there's a stone here
                    # Check all 8 directions around it
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue  # Skip the stone itself
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < board.size and 0 <= ny < board.size:
                                if board.is_empty(nx, ny):
                                    candidates.add((nx, ny))
        return list(candidates)

    def minimax(self, board, depth, player, maximizing, alpha, beta):
        """Minimax algorithm with alpha-beta pruning."""
        # Check terminal conditions
        eval_score = self.evaluator.evaluate(board, player)

        # If we've reached depth limit or game is over, return evaluation
        if depth == 0 or abs(eval_score) >= self.evaluator.INF // 2:
            return eval_score

        candidates = self.get_candidates(board)

        if maximizing:
            # Maximizing player's turn
            value = -float("inf")
            for x, y in candidates:
                # Try placing player's stone
                board.place_stone(x, y, player)

                # Recursively evaluate with opponent's turn next (maximizing=False)
                score = self.minimax(board, depth - 1, player, False, alpha, beta)

                board.remove_stone(x, y)

                # Update value and alpha
                value = max(value, score)
                alpha = max(alpha, value)

                # Alpha-beta pruning condition
                if beta <= alpha:
                    break  # Beta cutoff
            return value

        else:
            # Minimizing player's turn (opponent)
            value = float("inf")
            for x, y in candidates:
                # Opponent places their stone (-player)
                board.place_stone(x, y, -player)

                # Recursively evaluate with player's turn next (maximizing=True)
                score = self.minimax(board, depth - 1, player, True, alpha, beta)

                board.remove_stone(x, y)

                # Update value and beta
                value = min(value, score)
                beta = min(beta, value)

                # Alpha-beta pruning condition
                if beta <= alpha:
                    break  # Alpha cutoff
            return value

    def find_best_move(self, board, player, num_stones):
        """Find the best move(s) for the given number of stones to place."""
        print("\nAI thinking (alpha-beta)...")

        candidates = self.get_candidates(board)

        if num_stones == 1:
            # For single stone, find the best position
            best_score = -float("inf")
            best_move = None

            for x, y in candidates:
                board.place_stone(x, y, player)

                # Search with depth 2 for single stone
                score = self.minimax(board, 2, player, False, -float("inf"), float("inf"))

                board.remove_stone(x, y)

                if score > best_score:
                    best_score = score
                    best_move = (x, y)

            return [best_move]

        else:
            # For two stones, find the best pair
            best_score = -float("inf")
            best_pair = None

            # Try all pairs of candidate positions
            for i in range(len(candidates)):
                x1, y1 = candidates[i]

                for j in range(i + 1, len(candidates)):
                    x2, y2 = candidates[j]

                    # Place both stones
                    board.place_stone(x1, y1, player)
                    board.place_stone(x2, y2, player)

                    # Search with depth 1 for two stones (shallower due to more branching)
                    score = self.minimax(board, 1, player, False, -float("inf"), float("inf"))

                    board.remove_stone(x1, y1)
                    board.remove_stone(x2, y2)

                    if score > best_score:
                        best_score = score
                        best_pair = [(x1, y1), (x2, y2)]

            return best_pair