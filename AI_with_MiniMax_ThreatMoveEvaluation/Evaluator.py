INF = 10 ** 9
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

    def find_threats(self, board, player):
        """
        Find all threat positions for a player.
        A threat is a position where placing a stone would:
        1. Create a winning line (6 in a row) - CRITICAL THREAT
        2. Create 5 in a row - STRONG THREAT
        3. Create 4 in a row with open ends - MEDIUM THREAT
        4. Create 3 in a row with open ends - WEAK THREAT

        Returns: (critical_threats, strong_threats, medium_threats, weak_threats)
        """
        critical = 0  # Win in 1 move (5 stones → 6)
        strong = 0  # 4 stones → 5
        medium = 0  # 3 stones → 4 with openness
        weak = 0  # 2 stones → 3 with openness

        # Check every empty position
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != 0:
                    continue

                # Temporarily place stone to check what it creates
                board.grid[x][y] = player

                # Check all directions from this position
                for dx, dy in DIRS:
                    # Count consecutive stones in both directions
                    count = 1  # The stone we just placed

                    # Forward count
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == player:
                        count += 1
                        nx += dx
                        ny += dy
                    forward_open = (0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == 0)

                    # Backward count
                    nx, ny = x - dx, y - dy
                    while 0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == player:
                        count += 1
                        nx -= dx
                        ny -= dy
                    backward_open = (0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == 0)

                    openness = forward_open + backward_open

                    # Classify threat level
                    if count >= 6:
                        critical += 1
                        break  # Found winning move, no need to check other directions
                    elif count == 5 and openness >= 1:
                        strong += 1
                    elif count == 4 and openness == 2:
                        medium += 1
                    elif count == 3 and openness == 2:
                        weak += 1

                # Remove temporary stone
                board.grid[x][y] = 0

                # If we found a critical threat, we can stop checking this position
                if critical > 0:
                    board.grid[x][y] = 0
                    return (critical, strong, medium, weak)

        return (critical, strong, medium, weak)

    def count_potential_lines(self, board, player):
        """
        Count existing consecutive stones that could become threats.
        This evaluates the "potential" of the board state.
        """
        lines_5 = 0  # 5 consecutive stones (very dangerous)
        lines_4 = 0  # 4 consecutive stones
        lines_3 = 0  # 3 consecutive stones
        lines_2 = 0  # 2 consecutive stones

        counted = set()

        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != player:
                    continue

                for dx, dy in DIRS:
                    # Only count from start of line
                    prev_x, prev_y = x - dx, y - dy
                    if (0 <= prev_x < board.size and
                            0 <= prev_y < board.size and
                            board.grid[prev_x][prev_y] == player):
                        continue

                    count = self.check_line(board, x, y, dx, dy, player)

                    if count >= 5:
                        lines_5 += 1
                    elif count == 4:
                        lines_4 += 1
                    elif count == 3:
                        lines_3 += 1
                    elif count == 2:
                        lines_2 += 1

        return (lines_5, lines_4, lines_3, lines_2)

    def evaluate(self, board, player):
        """
        Threat-Based Evaluation:
        Key principle: BLOCKING opponent threats is more important than creating your own!

        Strategy:
        1. If opponent has winning threat → must block (negative huge score)
        2. If we have winning threat → take it (positive huge score)
        3. Count and compare threat levels
        4. Defensive play is weighted MORE than offensive
        """
        if self.check_win(board, player):
            return INF
        if self.check_win(board, -player):
            return -INF

        # Find immediate threats (moves that would win)
        my_crit, my_strong, my_med, my_weak = self.find_threats(board, player)
        opp_crit, opp_strong, opp_med, opp_weak = self.find_threats(board, -player)

        # Count existing lines (board evaluation)
        my_l5, my_l4, my_l3, my_l2 = self.count_potential_lines(board, player)
        opp_l5, opp_l4, opp_l3, opp_l2 = self.count_potential_lines(board, -player)

        score = 0

        # === THREAT SCORING ===
        # Critical threats (winning moves available)
        score += my_crit * 500000
        score -= opp_crit * 600000  # Blocking opponent win is MOST important!

        # Strong threats (5 in a row possible)
        score += my_strong * 50000
        score -= opp_strong * 60000

        # Medium threats (4 in a row, open)
        score += my_med * 5000
        score -= opp_med * 6000

        # Weak threats (3 in a row, open)
        score += my_weak * 500
        score -= opp_weak * 600

        # === EXISTING LINE SCORING ===
        # Lines already on board
        score += my_l5 * 10000
        score -= opp_l5 * 12000

        score += my_l4 * 1000
        score -= opp_l4 * 1200

        score += my_l3 * 100
        score -= opp_l3 * 120

        score += my_l2 * 10
        score -= opp_l2 * 12

        return score