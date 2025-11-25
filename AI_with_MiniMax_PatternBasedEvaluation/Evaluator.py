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

    def count_line_full(self, board, x, y, dx, dy, player):
        """
        Count stones in BOTH directions from a position.
        This gives the full line length.
        """
        count = 1  # Count the starting position

        # Forward direction
        nx, ny = x + dx, y + dy
        while 0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == player:
            count += 1
            nx += dx
            ny += dy

        # Backward direction
        nx, ny = x - dx, y - dy
        while 0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == player:
            count += 1
            nx -= dx
            ny -= dy

        return count

    def check_openness(self, board, x, y, dx, dy, player, line_length):
        """
        Check if a line is open (has empty spaces on both ends).
        Returns: 2 = open both ends, 1 = open one end, 0 = blocked both ends
        """
        openness = 0

        # Check forward end
        nx, ny = x + dx * line_length, y + dy * line_length
        if 0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == 0:
            openness += 1

        # Check backward end
        nx, ny = x - dx, y - dy
        if 0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == 0:
            openness += 1

        return openness

    def evaluate(self, board, player):
        """
        Pattern-Based Heuristic:
        - Scores different patterns (consecutive stones)
        - Distinguishes between open and closed patterns
        - Avoids double-counting by only checking from leftmost/topmost stone
        """
        if self.check_win(board, player):
            return INF
        if self.check_win(board, -player):
            return -INF

        # Score table for different patterns
        score_table = {
            "six": 1000000,  # Winning line
            "five_open": 100000,  # 5 stones, open (guaranteed win next turn)
            "five": 50000,  # 5 stones, closed
            "four_open": 10000,  # 4 stones, open both ends
            "four": 5000,  # 4 stones, open one end
            "three_open": 1000,  # 3 stones, open both ends
            "three": 200,  # 3 stones, open one end
            "two_open": 100,  # 2 stones, open both ends
            "two": 20  # 2 stones, open one end
        }

        my_score = 0
        opp_score = 0

        # Track which lines we've already counted
        counted_lines = set()

        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] == 0:
                    continue

                current_player = board.grid[x][y]

                for dx, dy in DIRS:
                    # Only count from the "start" of each line to avoid duplicates
                    # Check if there's a stone of same color in the opposite direction
                    prev_x, prev_y = x - dx, y - dy
                    if (0 <= prev_x < board.size and
                            0 <= prev_y < board.size and
                            board.grid[prev_x][prev_y] == current_player):
                        # This stone is not the start of the line, skip it
                        continue

                    # Count the full line length
                    count = self.check_line(board, x, y, dx, dy, current_player)

                    if count < 2:
                        # Single stone, not worth scoring
                        continue

                    # Check openness
                    openness = self.check_openness(board, x, y, dx, dy, current_player, count)

                    # Determine pattern score
                    pattern_score = 0

                    if count >= 6:
                        pattern_score = score_table["six"]
                    elif count == 5:
                        if openness >= 1:
                            pattern_score = score_table["five_open"]
                        else:
                            pattern_score = score_table["five"]
                    elif count == 4:
                        if openness == 2:
                            pattern_score = score_table["four_open"]
                        elif openness == 1:
                            pattern_score = score_table["four"]
                        # If blocked both ends (openness=0), worth very little
                    elif count == 3:
                        if openness == 2:
                            pattern_score = score_table["three_open"]
                        elif openness == 1:
                            pattern_score = score_table["three"]
                    elif count == 2:
                        if openness == 2:
                            pattern_score = score_table["two_open"]
                        elif openness == 1:
                            pattern_score = score_table["two"]

                    # Add to appropriate player's score
                    if current_player == player:
                        my_score += pattern_score
                    else:
                        opp_score += pattern_score

        return my_score - opp_score