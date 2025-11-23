from ZobristHash import ZobristHash

class Board:


    def __init__(self, size=19):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.zobrist = ZobristHash(size)
        self.hash = 0  # Current board hash

    def is_empty(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] == 0

    def place_stone(self, x, y, player):
        self.grid[x][y] = player
        self.hash ^= self.zobrist.get_hash(x, y, player)  # Update hash

    def remove_stone(self, x, y):
        player = self.grid[x][y]
        self.grid[x][y] = 0
        self.hash ^= self.zobrist.get_hash(x, y, player)  # Update hash

    def is_board_empty(self):
        for row in self.grid:
            if any(cell != 0 for cell in row):
                return False
        return True

    def print_board(self):
        print("\n    ", end="")
        for i in range(self.size):
            print(f"{i:2}", end=" ")
        print()

        for y in range(self.size):
            print(f"{y:2}  ", end="")
            for x in range(self.size):
                cell = self.grid[x][y]
                symbol = "X" if cell == 1 else "O" if cell == -1 else "."
                print(f"{symbol}  ", end="")
            print()

