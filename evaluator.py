WIN_SCORE = 10**9

# Directions
DIRS = [(1,0),(0,1),(1,1),(1,-1)]

class Evaluator:

    def analyze_runs_for_color(self, board, color):
        size = board.size
        runs = {2:0, 3:0, 4:0, 5:0}
        open_ends = {2:0, 3:0, 4:0, 5:0}

        for x in range(size):
            for y in range(size):
                if board.grid[x][y] != color:
                    continue

                for dx, dy in DIRS:
                    if not board.inside(x - dx, y - dy):
                        pass
                    else:
                        if board.grid[x - dx][y - dy] == color:
                            continue

                    length = 0
                    cx, cy = x, y
                    while board.inside(cx, cy) and board.grid[cx][cy] == color:
                        length += 1
                        cx += dx
                        cy += dy

                    if length >= 2:
                        if length > 5: length = 5
                        runs[length] += 1

                        open_count = 0
                        bx, by = x - dx, y - dy
                        if board.inside(bx, by) and board.grid[bx][by] == 0:
                            open_count += 1
                        if board.inside(cx, cy) and board.grid[cx][cy] == 0:
                            open_count += 1

                        if open_count > 0:
                            open_ends[length] += 1

        return runs, open_ends


    def evaluate(self, board, color):
        opp = -color

        my_runs, my_open = self.analyze_runs_for_color(board, color)
        op_runs, op_open = self.analyze_runs_for_color(board, opp)

        # Winning detection
        if my_runs[5] > 0: return WIN_SCORE
        if op_runs[5] > 0: return -WIN_SCORE

        score = 0
        threat_multiplier = 5
        weights = {2:10, 3:100, 4:3000, 5:100000}

        for l in range(2, 6):
            score += weights[l] * my_runs[l]
            score += weights[l] * my_open[l] * 2
            score -= threat_multiplier * (weights[l] * op_runs[l])
            score -= threat_multiplier * (weights[l] * op_open[l] * 2)

        return score