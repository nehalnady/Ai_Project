INF = 10**9
DIRS = [(1,0), (0,1), (1,1), (1,-1)]

class Evaluator:
    def check_line(self, board, x, y, dx, dy, player):
        count = 0
        cx, cy = x, y
        while (
            0 <= cx < board.size and
            0 <= cy < board.size and
            board.grid[cx][cy] == player
        ):
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

    def evaluate(self, board, player):
        if self.check_win(board, player):
            return INF
        if self.check_win(board, -player):
            return -INF

        my_stones = 0
        op_stones = 0

        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] == player:
                    my_stones += 1
                elif board.grid[x][y] == -player:
                    op_stones += 1

        return my_stones - op_stones
