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

    def check_win(self, board, player):

        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] == player:
                    for dx, dy in DIRS:
                        if self.check_line(board, x, y, dx, dy, player) >= 6:
                            return True
        return False

    def count_consecutive(self, board, x, y, dx, dy, player):

        left = 0
        cx, cy = x - dx, y - dy
        while 0 <= cx < board.size and 0 <= cy < board.size and board.grid[cx][cy] == player:
            left += 1
            cx -= dx
            cy -= dy


        right = 0
        cx, cy = x + dx, y + dy
        while 0 <= cx < board.size and 0 <= cy < board.size and board.grid[cx][cy] == player:
            right += 1
            cx += dx
            cy += dy

        total = left + 1 + right


        open_ends = 0

        lx = x - (left + 1) * dx
        ly = y - (left + 1) * dy
        if 0 <= lx < board.size and 0 <= ly < board.size and board.grid[lx][ly] == 0:
            open_ends += 1


        rx = x + (right + 1) * dx
        ry = y + (right + 1) * dy
        if 0 <= rx < board.size and 0 <= ry < board.size and board.grid[rx][ry] == 0:
            open_ends += 1

        return total, open_ends

    def has_threat(self, board, player, length=4):

        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != player:
                    continue
                for dx, dy in DIRS:
                    total, open_ends = self.count_consecutive(board, x, y, dx, dy, player)
                    if total >= length and open_ends >= 1:
                        return True
        return False

    def count_threats(self, board, player):

        threats = 0
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != player:
                    continue
                for dx, dy in DIRS:
                    total, open_ends = self.count_consecutive(board, x, y, dx, dy, player)
                    if total >= 4 and open_ends >= 1:
                        threats += (total - 3) ** 2
        return threats

    def evaluate(self, board, player):

        if self.check_win(board, player):
            return 1000000
        if self.check_win(board, -player):
            return -1000000

        my_threats = self.count_threats(board, player)
        opp_threats = self.count_threats(board, -player)


        return (my_threats * 80) - (opp_threats * 300)
