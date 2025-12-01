from Evaluator import Evaluator
import time


class OptimizedAI:
    """
    Hybrid AI that balances strategic depth with real-time responsiveness.

    Optimizations:
    1. Time-limited iterative deepening
    2. Smart candidate pruning
    3. Move ordering for better alpha-beta
    4. Transposition table (position caching)
    5. Adaptive depth based on position complexity
    """

    def __init__(self, max_time=5.0):
        self.evaluator = Evaluator()
        self.max_time = max_time  # Maximum time per move (seconds)
        self.transposition_table = {}
        self.nodes_explored = 0
        self.cache_hits = 0

    def clear_cache(self):
        """Clear transposition table between games"""
        self.transposition_table = {}

    def get_position_hash(self, board):
        """Use Zobrist hash for position identification"""
        return board.hash

    def count_stones(self, board):
        """Efficiently count stones on board"""
        return sum(1 for row in board.grid for cell in row if cell != 0)

    def evaluate_candidate_quality(self, board, x, y, player):
        """
        Quick heuristic to score candidate move quality.
        Used for move ordering to improve alpha-beta pruning.
        """
        score = 0

        # Check how many stones are nearby (within distance 2)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.size and 0 <= ny < board.size:
                    if board.grid[nx][ny] == player:
                        distance = abs(dx) + abs(dy)
                        score += (5 - distance)  # Closer = better
                    elif board.grid[nx][ny] == -player:
                        distance = abs(dx) + abs(dy)
                        score += (3 - distance)  # Near opponent also good

        # Bonus for center positions
        center = board.size // 2
        dist_to_center = abs(x - center) + abs(y - center)
        score += max(0, 10 - dist_to_center)

        return score

    def get_ordered_candidates(self, board, player):
        """
        Generate candidates sorted by likely quality.
        Better move ordering = more alpha-beta pruning.
        """
        candidates = set()

        # Empty board - return center
        if board.is_board_empty():
            center = board.size // 2
            return [(center, center)]

        # Collect all candidates near stones
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != 0:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if board.is_empty(nx, ny):
                                candidates.add((nx, ny))

        # Score each candidate
        scored_candidates = []
        for x, y in candidates:
            score = self.evaluate_candidate_quality(board, x, y, player)
            scored_candidates.append((score, x, y))

        # Sort by score (descending)
        scored_candidates.sort(reverse=True, key=lambda item: item[0])

        # Return positions only (without scores)
        return [(x, y) for _, x, y in scored_candidates]

    def minimax_alphabeta(self, board, depth, player, maximizing, alpha, beta, start_time):
        """
        Minimax with alpha-beta pruning, transposition table, and time limit.
        """
        self.nodes_explored += 1

        # Time limit check
        if time.perf_counter() - start_time > self.max_time:
            return self.evaluator.evaluate(board, player)

        # Check transposition table
        pos_hash = self.get_position_hash(board)
        if pos_hash in self.transposition_table:
            cached_depth, cached_score = self.transposition_table[pos_hash]
            if cached_depth >= depth:
                self.cache_hits += 1
                return cached_score

        # Terminal conditions
        if depth == 0:
            score = self.evaluator.evaluate(board, player)
            self.transposition_table[pos_hash] = (depth, score)
            return score

        if self.evaluator.check_win(board, 1):
            return 10 ** 9 if player == 1 else -10 ** 9

        if self.evaluator.check_win(board, -1):
            return 10 ** 9 if player == -1 else -10 ** 9

        # Get ordered candidates (better ordering = more pruning)
        candidates = self.get_ordered_candidates(board, player if maximizing else -player)

        if maximizing:
            value = -float('inf')
            for x, y in candidates:
                board.place_stone(x, y, player)
                score = self.minimax_alphabeta(board, depth - 1, player, False, alpha, beta, start_time)
                board.remove_stone(x, y)

                value = max(value, score)
                alpha = max(alpha, value)

                if beta <= alpha:
                    break  # Beta cutoff

            self.transposition_table[pos_hash] = (depth, value)
            return value
        else:
            value = float('inf')
            for x, y in candidates:
                board.place_stone(x, y, -player)
                score = self.minimax_alphabeta(board, depth - 1, player, True, alpha, beta, start_time)
                board.remove_stone(x, y)

                value = min(value, score)
                beta = min(beta, value)

                if beta <= alpha:
                    break  # Alpha cutoff

            self.transposition_table[pos_hash] = (depth, value)
            return value

    def iterative_deepening(self, board, player, start_time):
        """
        Iteratively search deeper until time runs out.
        Returns best move found so far.
        """
        candidates = self.get_ordered_candidates(board, player)
        best_move = candidates[0] if candidates else (board.size // 2, board.size // 2)
        best_score = -float('inf')

        # Start with depth 1, increase until time limit
        depth = 1
        max_depth_reached = 0

        while time.perf_counter() - start_time < self.max_time * 0.9:  # Leave 10% buffer
            current_best_move = None
            current_best_score = -float('inf')

            for x, y in candidates:
                # Time check
                if time.perf_counter() - start_time > self.max_time * 0.9:
                    break

                board.place_stone(x, y, player)
                score = self.minimax_alphabeta(
                    board, depth, player, False,
                    -float('inf'), float('inf'), start_time
                )
                board.remove_stone(x, y)

                if score > current_best_score:
                    current_best_score = score
                    current_best_move = (x, y)

            # If we completed this depth, update best move
            if current_best_move:
                best_move = current_best_move
                best_score = current_best_score
                max_depth_reached = depth

            depth += 1

            # Practical depth limit
            if depth > 6:
                break

        return best_move, best_score, max_depth_reached

    def find_best_move(self, board, player, num_stones):
        """
        Main entry point: Find best move(s) with time limit.
        Balances strategic depth with responsiveness.
        """
        start_time = time.perf_counter()
        self.nodes_explored = 0
        self.cache_hits = 0

        stone_count = self.count_stones(board)

        print(f"\n{'=' * 60}")
        print(f"OPTIMIZED AI ANALYSIS")
        print(f"{'=' * 60}")
        print(f"Board Size: {board.size}×{board.size}")
        print(f"Stones on Board: {stone_count}")
        print(f"Time Limit: {self.max_time}s")
        print(f"Stones to Place: {num_stones}")

        if num_stones == 1:
            # Single stone - use iterative deepening
            best_move, best_score, depth_reached = self.iterative_deepening(
                board, player, start_time
            )

            elapsed = time.perf_counter() - start_time

            print(f"Max Depth Reached: {depth_reached}")
            print(f"Nodes Explored: {self.nodes_explored}")
            print(f"Cache Hits: {self.cache_hits}")
            print(f"Cache Hit Rate: {self.cache_hits / max(self.nodes_explored, 1) * 100:.1f}%")
            print(f"Best Move: {best_move}")
            print(f"Score: {best_score}")
            print(f"Time Used: {elapsed:.3f}s / {self.max_time}s")
            print(f"{'=' * 60}\n")

            return [best_move]

        else:  # num_stones == 2
            # Two stones - limited search due to combinatorial explosion
            candidates = self.get_ordered_candidates(board, player)

            # Limit candidate pairs based on time budget
            max_pairs = min(300, len(candidates) * (len(candidates) - 1) // 4)

            best_pair = None
            best_score = -float('inf')
            pairs_checked = 0

            # Adaptive depth based on candidate count
            if len(candidates) < 20:
                search_depth = 2
            elif len(candidates) < 40:
                search_depth = 1
            else:
                search_depth = 1

            for i in range(len(candidates)):
                for j in range(i + 1, len(candidates)):
                    # Time check
                    if time.perf_counter() - start_time > self.max_time * 0.9:
                        print(f"Time limit reached, stopping search...")
                        break

                    x1, y1 = candidates[i]
                    x2, y2 = candidates[j]

                    board.place_stone(x1, y1, player)
                    board.place_stone(x2, y2, player)

                    score = self.minimax_alphabeta(
                        board, search_depth, player, False,
                        -float('inf'), float('inf'), start_time
                    )

                    board.remove_stone(x1, y1)
                    board.remove_stone(x2, y2)

                    if score > best_score:
                        best_score = score
                        best_pair = [(x1, y1), (x2, y2)]

                    pairs_checked += 1
                    if pairs_checked >= max_pairs:
                        break

                if pairs_checked >= max_pairs or time.perf_counter() - start_time > self.max_time * 0.9:
                    break

            elapsed = time.perf_counter() - start_time

            print(f"Search Depth: {search_depth}")
            print(f"Candidates: {len(candidates)}")
            print(f"Pairs Checked: {pairs_checked}")
            print(f"Nodes Explored: {self.nodes_explored}")
            print(f"Cache Hits: {self.cache_hits}")
            print(f"Cache Hit Rate: {self.cache_hits / max(self.nodes_explored, 1) * 100:.1f}%")
            print(f"Best Pair: {best_pair}")
            print(f"Score: {best_score}")
            print(f"Time Used: {elapsed:.3f}s / {self.max_time}s")
            print(f"{'=' * 60}\n")

            if best_pair:
                return best_pair
            else:
                center = board.size // 2
                return [(center, center), (center + 1, center)]