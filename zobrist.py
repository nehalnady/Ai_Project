import random

class Zobrist:
    def __init__(self, size=19):
        self.size = size
        self.table = [[[random.getrandbits(64) for _ in range(2)]
                       for _ in range(size)] for _ in range(size)]

    def hash_board(self, board):
        """Computes a unique hash based on board stones."""
        h = 0
        for x in range(self.size):
            for y in range(self.size):
                stone = board.grid[x][y]
                if stone != 0:  # 1 = black, -1 = white
                    color_index = 0 if stone == 1 else 1
                    h ^= self.table[x][y][color_index]
        return h

    def update_hash(self, h, x, y, color):
        """Updates hash when adding/removing a stone."""
        index = 0 if color == 1 else 1
        return h ^ self.table[x][y][index]