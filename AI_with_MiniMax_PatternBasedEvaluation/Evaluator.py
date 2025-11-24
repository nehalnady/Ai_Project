INF = 10**9
DIRS = [(1,0), (0,1), (1,1), (1,-1)]

class Evaluator:
    def check_line(self, board, x, y, dx, dy, player):
        count = 0
        cx, cy = x, y
        while 0 <= cx < board.size and 0 <= cy < board.size and board.grid[cx][cy] == player:
            count += 1
            cx += dx
            cy += dy
        return count

    def check_win(self, board, player):
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] == player:
                    for dx, dy in DIRS:
                        if self.check_line(board, x, y, dx, dy, player) >= 6:
                            return True
        return False

    # =========================
    # Pattern-Based Heuristic
    # =========================
    def evaluate(self, board, player):
        if self.check_win(board, player):
            return INF
        if self.check_win(board, -player):
            return -INF

        score_table = {
            "five": 1000000,
            "open_four": 10000,
            "four": 5000,
            "open_three": 500,
            "three": 50,
            "open_two": 10
        }

        score = 0
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != player:
                    continue
                for dx, dy in DIRS:
                    count = self.check_line(board, x, y, dx, dy, player)
                    if count >= 6:
                        score += score_table["five"]
                    elif count == 5:
                        score += score_table["open_four"]
                    elif count == 4:
                        score += score_table["four"]
                    elif count == 3:
                        score += score_table["open_three"]
                    elif count == 2:
                        score += score_table["open_two"]
        return score
