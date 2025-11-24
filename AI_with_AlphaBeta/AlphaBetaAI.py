from Evaluator import Evaluator, DIRS

class AlphaBetaAI:
    def __init__(self, mode="B"):

        self.evaluator = Evaluator()
        self.nodes_searched = 0
        self.pruned_branches = 0
        self.transposition_table = {}
        self.tt_hits = 0
        self.mode = mode

    def find_strong_defensive_moves(self, board):

        defend = set()
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] == -1:
                    for dx, dy in DIRS:
                        length = self.evaluator.check_line(board, x, y, dx, dy, -1)
                        open_type = self.evaluator.is_open_ended(board, x, y, dx, dy, length, -1)
                        if length >= 3 and open_type in ("open", "half"):
                            bx = x + dx * length
                            by = y + dy * length
                            if board.is_empty(bx, by):
                                defend.add((bx, by))
        return defend

    def get_candidates(self, board):
        stones = [(x, y) for x in range(board.size) for y in range(board.size) if board.grid[x][y] != 0]
        if not stones:
            c = board.size // 2
            return [(c, c)]

        cand = set()
        for x, y in stones:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if board.is_empty(nx, ny):
                        cand.add((nx, ny))


        cand |= self.find_strong_defensive_moves(board)


        if self.mode == "A":
            return list(cand)[:15]


        scored = []
        for x, y in cand:
            score = sum(1 for dx, dy in DIRS if 0 <= x+dx < board.size and 0 <= y+dy < board.size and board.grid[x+dx][y+dy] != 0)
            scored.append(((x, y), score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [pos for pos, s in scored[:25]]

    def find_immediate_threat(self, board, player):

        opponent = -player
        candidates = self.get_candidates(board)
        for x, y in candidates:
            board.place_stone(x, y, opponent)
            if self.evaluator.check_win(board, opponent):
                board.remove_stone(x, y)
                return (x, y)
            board.remove_stone(x, y)
        return None


    def alpha_beta(self, board, depth, alpha, beta, player, is_maximizing):
        self.nodes_searched += 1
        board_hash = board.hash

        if board_hash in self.transposition_table:
            stored_depth, stored_score, flag = self.transposition_table[board_hash]
            if stored_depth >= depth:
                self.tt_hits += 1
                if flag == 'exact':
                    return stored_score
                elif flag == 'lower':
                    alpha = max(alpha, stored_score)
                elif flag == 'upper':
                    beta = min(beta, stored_score)
                if alpha >= beta:
                    return stored_score

        if depth == 0 or self.evaluator.check_win(board, 1) or self.evaluator.check_win(board, -1):
            score = self.evaluator.evaluate(board, player)
            self.transposition_table[board_hash] = (depth, score, 'exact')
            return score

        candidates = self.get_candidates(board)[:15]

        if is_maximizing:
            max_eval = -float('inf')
            for x, y in candidates:
                board.place_stone(x, y, player)
                eval_score = self.alpha_beta(board, depth - 1, alpha, beta, player, False)
                board.remove_stone(x, y)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    self.pruned_branches += 1
                    break
            flag = 'exact'
            if max_eval <= alpha:
                flag = 'upper'
            elif max_eval >= beta:
                flag = 'lower'
            self.transposition_table[board_hash] = (depth, max_eval, flag)
            return max_eval
        else:
            min_eval = float('inf')
            for x, y in candidates:
                board.place_stone(x, y, -player)
                eval_score = self.alpha_beta(board, depth - 1, alpha, beta, player, True)
                board.remove_stone(x, y)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    self.pruned_branches += 1
                    break
            flag = 'exact'
            if min_eval <= alpha:
                flag = 'upper'
            elif min_eval >= beta:
                flag = 'lower'
            self.transposition_table[board_hash] = (depth, min_eval, flag)
            return min_eval

    def find_best_move(self, board, player, num_stones):

        self.nodes_searched = 0
        self.tt_hits = 0
        self.pruned_branches = 0


        threats = list(self.find_strong_defensive_moves(board))
        threats = sorted(threats, key=lambda t: -self.evaluator.evaluate(board, -player))

        move_list = []
        for t in threats[:num_stones]:
            move_list.append(t)
            board.place_stone(t[0], t[1], player)

        if len(move_list) == num_stones:
            for x, y in move_list:
                board.remove_stone(x, y)
            return move_list


        for x, y in move_list:
            board.remove_stone(x, y)


        candidates = self.get_candidates(board)[:25]
        remaining = num_stones - len(move_list)
        best_moves = []

        for _ in range(remaining):
            best_score = -float('inf')
            best_move = None
            for x, y in candidates:
                if (x, y) in move_list or board.grid[x][y] != 0:
                    continue
                board.place_stone(x, y, player)
                score = self.alpha_beta(board, 3, -float('inf'), float('inf'), player, False)
                board.remove_stone(x, y)
                if score > best_score:
                    best_score = score
                    best_move = (x, y)
            if best_move:
                best_moves.append(best_move)
                board.place_stone(best_move[0], best_move[1], player)


        for x, y in move_list + best_moves:
            board.remove_stone(x, y)

        return move_list + best_moves


