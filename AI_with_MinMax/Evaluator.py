DIRS = [(1, 0), (0, 1), (1, 1), (1, -1)]


class Evaluator:
    def check_line(self, board, x, y, dx, dy, player):
        """Count consecutive stones in a direction"""
        count = 0
        cx, cy = x, y
        while (0 <= cx < board.size and 0 <= cy < board.size and
               board.grid[cx][cy] == player):
            count += 1
            cx += dx
            cy += dy
        return count

    def check_win(self, board, player):
        """Check if player has 6 in a row"""
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] == player:
                    for dx, dy in DIRS:
                        if self.check_line(board, x, y, dx, dy, player) >= 6:
                            return True
        return False

    def count_threats(self, board, player):
        """Count potential winning sequences"""
        threats = 0
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] == player:
                    for dx, dy in DIRS:
                        length = self.check_line(board, x, y, dx, dy, player)
                        if length >= 4:
                            threats += (length - 3) ** 2
        return threats

    def evaluate(self, board, player):
        """Evaluate board position for given player"""
        if self.check_win(board, player):
            return 1000000
        if self.check_win(board, -player):
            return -1000000

        my_threats = self.count_threats(board, player)
        opp_threats = self.count_threats(board, -player)

        return (my_threats * 100) - (opp_threats * 150)

