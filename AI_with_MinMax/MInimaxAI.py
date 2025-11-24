from Evaluator import Evaluator, DIRS


class MinimaxAI:
    def __init__(self):
        self.evaluator = Evaluator()
        self.nodes_searched = 0
        self.transposition_table = {}
        self.tt_hits = 0


    def local_heuristic(self, board, x, y):

        score = 0
        for dx, dy in DIRS:
            cx, cy = x + dx, y + dy
            if 0 <= cx < board.size and 0 <= cy < board.size and board.grid[cx][cy] != 0:
                score += 5
        return score

    def get_candidates(self, board):

        candidates = set()
        if board.is_board_empty():
            c = board.size // 2
            return [(c, c)]

        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != 0:
                    for dx in [-2, -1, 0, 1, 2]:
                        for dy in [-2, -1, 0, 1, 2]:
                            nx, ny = x + dx, y + dy
                            if board.is_empty(nx, ny):
                                candidates.add((nx, ny))

        cand_list = list(candidates)
        cand_list.sort(key=lambda mv: -self.local_heuristic(board, mv[0], mv[1]))
        return cand_list if cand_list else [(board.size // 2, board.size // 2)]


    def find_forced_blocks(self, board, player):

        opponent = -player
        blocks = []
        added = set()


        for x in range(board.size):
            for y in range(board.size):
                if not board.is_empty(x, y):
                    continue

                board.place_stone(x, y, opponent)

                if self.evaluator.check_win(board, opponent):
                    if (x, y) not in added:
                        blocks.append((x, y))
                        added.add((x, y))
                    board.remove_stone(x, y)
                    continue

                if self.evaluator.has_threat(board, opponent, 5):
                    if (x, y) not in added:
                        blocks.append((x, y))
                        added.add((x, y))
                    board.remove_stone(x, y)
                    continue

                if self.evaluator.has_threat(board, opponent, 4):
                    if (x, y) not in added:
                        blocks.append((x, y))
                        added.add((x, y))
                    board.remove_stone(x, y)
                    continue

                board.remove_stone(x, y)

        return blocks


    def find_immediate_threat(self, board, player):

        opponent = -player
        for x, y in self.get_candidates(board)[:30]:
            board.place_stone(x, y, opponent)
            if self.evaluator.check_win(board, opponent):
                board.remove_stone(x, y)
                return (x, y)
            board.remove_stone(x, y)


        forced = self.find_forced_blocks(board, player)
        return forced[0] if forced else None


    def minimax(self, board, depth, player, is_maximizing):
        self.nodes_searched += 1

        h = board.hash
        if h in self.transposition_table:
            saved_depth, saved_score = self.transposition_table[h]
            if saved_depth >= depth:
                self.tt_hits += 1
                return saved_score


        if is_maximizing:

            opp_forced = self.find_forced_blocks(board, -player)
            if opp_forced:
                return -999999
        else:

            self_forced = self.find_forced_blocks(board, player)
            if self_forced:
                return 999999


        if depth == 0 or self.evaluator.check_win(board, 1) or self.evaluator.check_win(board, -1):
            score = self.evaluator.evaluate(board, player)
            self.transposition_table[h] = (depth, score)
            return score

        candidates = self.get_candidates(board)[:15]

        if is_maximizing:
            best_val = -float("inf")
            for x, y in candidates:
                board.place_stone(x, y, player)
                val = self.minimax(board, depth - 1, player, False)
                board.remove_stone(x, y)
                best_val = max(best_val, val)
            self.transposition_table[h] = (depth, best_val)
            return best_val
        else:
            best_val = float("inf")
            for x, y in candidates:
                board.place_stone(x, y, -player)
                val = self.minimax(board, depth - 1, player, True)
                board.remove_stone(x, y)
                best_val = min(best_val, val)
            self.transposition_table[h] = (depth, best_val)
            return best_val


    def find_best_move(self, board, player, num_stones):
        print(f"\nAI is thinking (search depth: 2)...")
        self.nodes_searched = 0
        self.tt_hits = 0


        forced = self.find_forced_blocks(board, player)
        if forced:

            take = forced[:num_stones]
            print("AI MUST BLOCK (forced):", take)
            return take


        blocked = []
        for _ in range(num_stones):
            threat = self.find_immediate_threat(board, player)
            if threat:
                blocked.append(threat)
                board.place_stone(threat[0], threat[1], player)

        if len(blocked) == num_stones:
            for x, y in blocked:
                board.remove_stone(x, y)
            print("AI BLOCKS (immediate):", blocked)
            return blocked


        for x, y in blocked:
            board.remove_stone(x, y)


        candidates = self.get_candidates(board)[:20]

        if num_stones == 1:
            best_score = -float("inf")
            best_move = None
            for x, y in candidates:
                board.place_stone(x, y, player)
                score = self.minimax(board, 2, player, False)
                board.remove_stone(x, y)
                if score > best_score:
                    best_score = score
                    best_move = (x, y)
            print("AI chose:", best_move, "score:", best_score)
            return [best_move]
        else:
            best_score = -float("inf")
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
            print("AI chose pair:", best_pair, "score:", best_score)
            return best_pair
