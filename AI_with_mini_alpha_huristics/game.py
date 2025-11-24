from AI_with_mini_alpha_huristics.board import Board
from searcher import Searcher

class Game:
    def __init__(self):
        self.board = Board()
        self.searcher = Searcher()
        self.turn = 1  # 1 = black (AI or human), -1 = white

    def print_board(self):
        size = self.board.size

        # Print column numbers
        print("   ", end="")
        for x in range(size):
            print(f"{x:2}", end=" ")
        print()

        # Print rows
        for y in range(size):
            print(f"{y:2} ", end="")
            for x in range(size):
                v = self.board.grid[x][y]
                if v == 1:
                    print("X ", end=" ")
                elif v == -1:
                    print("O ", end=" ")
                else:
                    print(". ", end=" ")
            print()

    def player_move(self):
        print(f"You are {'Black (X)' if self.turn == 1 else 'White (O)'}")

        first_move = self.board.is_board_empty()
        if first_move:
            print("FIRST MOVE RULE: Place ONE stone only.")
        else:
            print("Enter TWO stones (row col):")

        valid = False
        while not valid:
            try:
                if first_move:
                    row, col = map(int, input("Stone (row col): ").split())
                    if not self.board.inside(col, row):
                        print(" Out of bounds. Try again.")
                        continue
                    if not self.board.is_empty(col, row):
                        print(" That position is occupied. Try again.")
                        continue
                    move = [(col, row)]  # Swap here
                    valid = True
                else:
                    print("Stone 1:")
                    row1, col1 = map(int, input().split())
                    print("Stone 2:")
                    row2, col2 = map(int, input().split())

                    if (not self.board.inside(col1, row1)) or (not self.board.inside(col2, row2)):
                        print(" One stone is out of bounds. Try again.")
                        continue
                    if not self.board.is_empty(col1, row1):
                        print(" Stone 1 position is occupied.")
                        continue
                    if not self.board.is_empty(col2, row2):
                        print(" Stone 2 position is occupied.")
                        continue

                    move = [(col1, row1), (col2, row2)]  # Swap here
                    valid = True
            except ValueError:
                print(" Invalid input. Use: row col")
                continue

        self.board.apply_move(move, self.turn)

    def ai_move(self):
        print("AI thinking...")
        first_move = self.board.is_board_empty()

        # Check for immediate threats (opponent about to win)
        block_move = self.searcher.find_immediate_block(self.board, self.turn)
        if block_move:
            move = block_move
            print("AI blocks opponent:", move)
        else:
            move = self.searcher.iterative_deepening(self.board, self.turn, max_depth=3)

        # First move: only one stone
        if first_move and len(move) == 2:
            move = [move[0]]

        print("AI chose:", move)
        self.board.apply_move(move, self.turn)

    def loop(self):
        while True:
            self.print_board()

            if self.turn == 1:
                self.player_move()
            else:
                self.ai_move()

            # Check win after the move
            if self.check_win():
                self.print_board()  # show final board
                print("GAME OVER!")
                print(f"{'Black (X)' if self.turn == 1 else 'White (O)'} wins!")
                break

            self.turn *= -1

    def check_win(self):
        return self.has_six_in_a_row(self.turn)

    def has_six_in_a_row(self, player):
        size = self.board.size
        directions = [(1,0), (0,1), (1,1), (1,-1)]  # horizontal, vertical, diagonal down-right, diagonal up-right

        for y in range(size):
            for x in range(size):
                if self.board.grid[x][y] != player:
                    continue
                for dx, dy in directions:
                    count = 1
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < size and 0 <= ny < size and self.board.grid[nx][ny] == player:
                        count += 1
                        nx += dx
                        ny += dy
                    if count >= 6:
                        return True
        return False
