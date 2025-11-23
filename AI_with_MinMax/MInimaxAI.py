from Evaluator import Evaluator

class MinimaxAI:
    def __init__(self):
        self.evaluator = Evaluator()
        self.nodes_searched = 0
        self.transposition_table = {}  # Zobrist hash -> (depth, score)
        self.tt_hits = 0  # Track cache hits

    def get_candidates(self, board):
        """Get empty cells near existing stones"""
        candidates = set()

        if board.is_board_empty():
            center = board.size // 2
            return [(center, center)]

        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != 0:
                    for dx in [-2, -1, 0, 1, 2]:
                        for dy in [-2, -1, 0, 1, 2]:
                            nx, ny = x + dx, y + dy
                            if board.is_empty(nx, ny):
                                candidates.add((nx, ny))

        return list(candidates) if candidates else [(board.size // 2, board.size // 2)]

    def find_immediate_threat(self, board, player):
        """Find if opponent can win in next move"""
        opponent = -player
        candidates = self.get_candidates(board)

        for x, y in candidates:
            board.place_stone(x, y, opponent)
            if self.evaluator.check_win(board, opponent):
                board.remove_stone(x, y)
                return (x, y)
            board.remove_stone(x, y)
        return None

    def minimax(self, board, depth, player, is_maximizing):
        """Pure Minimax algorithm with Zobrist hashing"""
        self.nodes_searched += 1

        # Check transposition table
        board_hash = board.hash
        if board_hash in self.transposition_table:
            stored_depth, stored_score = self.transposition_table[board_hash]
            if stored_depth >= depth:
                self.tt_hits += 1
                return stored_score

        # Terminal conditions
        if depth == 0 or self.evaluator.check_win(board, 1) or self.evaluator.check_win(board, -1):
            score = self.evaluator.evaluate(board, player)
            self.transposition_table[board_hash] = (depth, score)
            return score

        candidates = self.get_candidates(board)[:15]  # Limit search

        if is_maximizing:
            max_eval = -float('inf')
            for x, y in candidates:
                board.place_stone(x, y, player)
                eval_score = self.minimax(board, depth - 1, player, False)
                board.remove_stone(x, y)
                max_eval = max(max_eval, eval_score)

            # Store in transposition table
            self.transposition_table[board_hash] = (depth, max_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for x, y in candidates:
                board.place_stone(x, y, -player)
                eval_score = self.minimax(board, depth - 1, player, True)
                board.remove_stone(x, y)
                min_eval = min(min_eval, eval_score)

            # Store in transposition table
            self.transposition_table[board_hash] = (depth, min_eval)
            return min_eval

    def find_best_move(self, board, player, num_stones):
        """Find best move using minimax with Zobrist hashing"""
        print(f"\nAI is thinking (searching {num_stones} stone(s))...")
        self.nodes_searched = 0
        self.tt_hits = 0

        # Priority 1: Block immediate threats
        threats_blocked = []
        for _ in range(num_stones):
            threat = self.find_immediate_threat(board, player)
            if threat:
                threats_blocked.append(threat)
                board.place_stone(threat[0], threat[1], player)

        if len(threats_blocked) == num_stones:
            for x, y in threats_blocked:
                board.remove_stone(x, y)
            print(f"AI BLOCKING threats at: {threats_blocked}")
            print(f"Nodes searched: {self.nodes_searched} | TT hits: {self.tt_hits}")
            return threats_blocked

        # Undo temporary placements
        for x, y in threats_blocked:
            board.remove_stone(x, y)

        # Find best moves using minimax
        candidates = self.get_candidates(board)[:20]
        best_moves = []

        if num_stones == 1:
            best_score = -float('inf')
            best_move = None

            for x, y in candidates:
                board.place_stone(x, y, player)
                score = self.minimax(board, 2, player, False)
                board.remove_stone(x, y)

                if score > best_score:
                    best_score = score
                    best_move = (x, y)

            best_moves = [best_move]

        else:  # 2 stones
            best_score = -float('inf')
            best_pair = None

            for i, (x1, y1) in enumerate(candidates):
                for x2, y2 in candidates[i + 1:]:
                    board.place_stone(x1, y1, player)
                    board.place_stone(x2, y2, player)
                    score = self.minimax(board, 1, player, False)
                    board.remove_stone(x1, y1)
                    board.remove_stone(x2, y2)

                    if score > best_score:
                        best_score = score
                        best_pair = [(x1, y1), (x2, y2)]

            best_moves = best_pair if best_pair else [candidates[0], candidates[1]]

        print(f"AI chose: {best_moves} (Score: {best_score if 'best_score' in locals() else 'N/A'})")
        print(
            f"Nodes searched: {self.nodes_searched} | TT hits: {self.tt_hits} | Hit rate: {self.tt_hits / max(1, self.nodes_searched) * 100:.1f}%")
        return best_moves