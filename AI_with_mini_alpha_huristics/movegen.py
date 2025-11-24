NEIGHBOR_RADIUS = 2
MAX_CANDIDATES = 12
MAX_MOVE_PAIRS = 40

def candidate_cells(board):
    size = board.size
    candidates = set()

    # First move: return center
    stones = [(x, y) for x in range(size) for y in range(size)
              if board.grid[x][y] != 0]

    if not stones:
        mid = size // 2
        return [(mid, mid)]

    # Otherwise only nearby empty cells
    for (sx, sy) in stones:
        for dx in range(-NEIGHBOR_RADIUS, NEIGHBOR_RADIUS + 1):
            for dy in range(-NEIGHBOR_RADIUS, NEIGHBOR_RADIUS + 1):
                x, y = sx + dx, sy + dy
                if board.inside(x, y) and board.is_empty(x, y):
                    candidates.add((x, y))

    return list(candidates)


def score_cell(board, x, y):
    """Simple scoring: center-based + adjacency-based."""
    size = board.size
    center = size // 2
    score = -abs(x - center) - abs(y - center)

    # adjacency bonus
    adj = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
    for dx, dy in adj:
        nx, ny = x + dx, y + dy
        if board.inside(nx, ny) and board.grid[nx][ny] != 0:
            score += 5

    return score


def generate_move_pairs(board, is_first_move):
    cand = candidate_cells(board)

    # First move: single stone
    if is_first_move:
        return [(cand[0], )]

    # Score and take top N
    scored = sorted(cand, key=lambda c: score_cell(board, c[0], c[1]), reverse=True)
    best = scored[:MAX_CANDIDATES]

    # Generate pairs
    pairs = []
    for i in range(len(best)):
        for j in range(i + 1, len(best)):
            pairs.append((best[i], best[j]))

    return pairs[:MAX_MOVE_PAIRS]