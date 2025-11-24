from zobrist import Zobrist

class Board:
    def __init__(self, size=19):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.zobrist = Zobrist(size)
        self.hash = self.zobrist.hash_board(self)

    def inside(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def is_empty(self, x, y):
        return self.inside(x, y) and self.grid[x][y] == 0

    def place(self, x, y, color):
        """Places a stone and updates hash."""
        self.grid[x][y] = color
        self.hash = self.zobrist.update_hash(self.hash, x, y, color)

    def remove(self, x, y, color):
        """Removes a stone and updates hash (used by minimax undo)."""
        self.grid[x][y] = 0
        self.hash = self.zobrist.update_hash(self.hash, x, y, color)

    def apply_move(self, move, color):
        """Move = (cell1, cell2) or (cell,) for first move."""
        for (x, y) in move:
            self.place(x, y, color)

    def undo_move(self, move, color):
        for (x, y) in move:
            self.remove(x, y, color)

    def is_board_empty(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] != 0:
                    return False
        return True