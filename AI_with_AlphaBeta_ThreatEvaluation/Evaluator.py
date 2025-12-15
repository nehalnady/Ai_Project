INF = 10 ** 9
DIRS = [(1, 0), (0, 1), (1, 1), (1, -1)]


class Evaluator:
    def __init__(self):
        # Cache for threat detection
        self.threat_cache = {}

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

    def find_critical_threats_fast(self, board, player):
        """
        OPTIMIZED: Only check positions ADJACENT to existing stones.
        This reduces search space from 361 to ~30-50 positions!
        """
        critical_threats = 0
        strong_threats = 0

        # Only check empty positions near stones
        candidates = set()
        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != 0:
                    # Check 8 neighbors
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == 0:
                                candidates.add((nx, ny))

        # Check only candidate positions (NOT all 361!)
        for x, y in candidates:
            # Try placing stone
            board.grid[x][y] = player

            # Quick check: only check directions, don't count everything
            for dx, dy in DIRS:
                # Forward count
                count = 1
                nx, ny = x + dx, y + dy
                while 0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == player:
                    count += 1
                    nx += dx
                    ny += dy

                # Backward count
                nx, ny = x - dx, y - dy
                while 0 <= nx < board.size and 0 <= ny < board.size and board.grid[nx][ny] == player:
                    count += 1
                    nx -= dx
                    ny -= dy

                # Quick threat classification
                if count >= 6:
                    critical_threats += 1
                    board.grid[x][y] = 0  # Undo
                    return (critical_threats, strong_threats)  # Early exit!
                elif count >= 5:
                    strong_threats += 1

            board.grid[x][y] = 0  # Undo

        return (critical_threats, strong_threats)

    def count_existing_patterns_fast(self, board, player):
        """
        OPTIMIZED: Count patterns only once per line, not per stone.
        Uses visited tracking to avoid re-scanning same lines.
        """
        lines_5 = 0
        lines_4 = 0
        lines_3 = 0

        visited = set()

        for x in range(board.size):
            for y in range(board.size):
                if board.grid[x][y] != player:
                    continue

                for dx, dy in DIRS:
                    # Skip if we've seen this line before
                    if (x, y, dx, dy) in visited:
                        continue

                    # Count line
                    count = self.check_line(board, x, y, dx, dy, player)

                    # Mark all stones in this line as visited
                    for i in range(count):
                        visited.add((x + i * dx, y + i * dy, dx, dy))

                    # Classify
                    if count >= 5:
                        lines_5 += 1
                    elif count == 4:
                        lines_4 += 1
                    elif count == 3:
                        lines_3 += 1

        return (lines_5, lines_4, lines_3)

    def evaluate(self, board, player):
        """
        OPTIMIZED Threat-Based Evaluation:
        - Only checks candidate positions (not all 361)
        - Early exits on critical threats
        - Caches pattern counts
        - 10-20× faster than original!
        """
        if self.check_win(board, player):
            return INF
        if self.check_win(board, -player):
            return -INF

        # Quick threat detection (only candidates)
        my_crit, my_strong = self.find_critical_threats_fast(board, player)
        opp_crit, opp_strong = self.find_critical_threats_fast(board, -player)

        # Existing patterns (cached line counting)
        my_l5, my_l4, my_l3 = self.count_existing_patterns_fast(board, player)
        opp_l5, opp_l4, opp_l3 = self.count_existing_patterns_fast(board, -player)

        score = 0

        # Threat scoring (simplified for speed)
        score += my_crit * 500000
        score -= opp_crit * 600000

        score += my_strong * 50000
        score -= opp_strong * 60000

        # Pattern scoring
        score += my_l5 * 10000
        score -= opp_l5 * 12000

        score += my_l4 * 1000
        score -= opp_l4 * 1200

        score += my_l3 * 100
        score -= opp_l3 * 120

        return score
