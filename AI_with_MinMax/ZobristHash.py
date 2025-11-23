import random


class ZobristHash:
    def __init__(self, board_size=19):
        random.seed(12345)  # Fixed seed for consistency
        self.table = {}

        # Generate random hash values for each position and player
        for x in range(board_size):
            for y in range(board_size):
                self.table[(x, y, 1)] = random.getrandbits(64)  # Player 1 (X)
                self.table[(x, y, -1)] = random.getrandbits(64)  # Player -1 (O)

    def get_hash(self, x, y, player):
        return self.table.get((x, y, player), 0)