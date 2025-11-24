DIRS = [(1, 0), (0, 1), (1, 1), (1, -1)]


class Evaluator:
    def check_line(self, board, x, y, dx, dy, player):

        count = 0
        cx, cy = x, y
        while 0 <= cx < board.size and 0 <= cy < board.size and board.grid[cx][cy] == player:
            count += 1
            cx += dx
            cy += dy
        return count

    def is_open_ended(self, board, x, y, dx, dy, length, player):


        bx, by = x - dx, y - dy
        open_before = 0 <= bx < board.size and 0 <= by < board.size and board.grid[bx][by] == 0

        ax, ay = x + dx * length, y + dy * length
        open_after = 0 <= ax < board.size and 0 <= ay < board.size and board.grid[ax][ay] == 0

        if open_before and open_after:
            return "open"
        elif open_before or open_after:
            return "half"
        else:
            return "closed"

    def check_win(self, board, player):

        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] == player:
                    for dx, dy in DIRS:
                        if self.check_line(board, x, y, dx, dy, player) >= 6:
                            return True
        return False

    def evaluate(self, board, player):

        if self.check_win(board, player):
            return 1000000
        if self.check_win(board, -player):
            return -1000000

        score = 0
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] == player:
                    for dx, dy in DIRS:
                        length = self.check_line(board, x, y, dx, dy, player)
                        open_type = self.is_open_ended(board, x, y, dx, dy, length, player)
                        if length >= 4:
                            if open_type == "open":
                                score += length ** 4
                            elif open_type == "half":
                                score += length ** 3
                        elif length == 3:
                            score += 10 if open_type == "open" else 5
                elif board.grid[x][y] == -player:
                    for dx, dy in DIRS:
                        length = self.check_line(board, x, y, dx, dy, -player)
                        open_type = self.is_open_ended(board, x, y, dx, dy, length, -player)
                        if length >= 4:
                            if open_type == "open":
                                score -= length ** 5
                            elif open_type == "half":
                                score -= length ** 4
                        elif length == 3:
                            score -= 20 if open_type == "open" else 10
        return score