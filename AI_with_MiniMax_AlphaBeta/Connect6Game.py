from Board import Board
from MinimaxAIAlphaBeta import MinimaxAIAlphaBeta

class Connect6Game:
    def __init__(self):
        self.board = Board(19)
        self.ai = MinimaxAIAlphaBeta()
        self.current_player = 1
        self.move_count = 0

    def get_human_move(self, num_stones):
        moves = []
        print(f"\nYour turn! Place {num_stones} stone(s)")

        for i in range(num_stones):
            while True:
                try:
                    coords = input(f"Stone {i+1} (x y): ").strip().split()
                    x, y = int(coords[0]), int(coords[1])

                    if self.board.is_empty(x, y):
                        moves.append((x, y))
                        self.board.place_stone(x, y, self.current_player)
                        break
                    else:
                        print("Cell occupied! Try again.")
                except:
                    print("Invalid input!")

        return moves

    def play(self):
        print("=== CONNECT-6 ===")
        print("You are X (Black). AI is O (White).")
        print("First move = 1 stone. Others = 2 stones.\n")

        while True:
            self.board.print_board()

            if self.ai.evaluator.check_win(self.board, 1):
                print("\nYOU WIN!")
                break
            if self.ai.evaluator.check_win(self.board, -1):
                print("\nAI WINS!")
                break

            num_stones = 1 if self.move_count == 0 else 2

            if self.current_player == 1:
                self.get_human_move(num_stones)
            else:
                moves = self.ai.find_best_move(self.board, self.current_player, num_stones)
                for x, y in moves:
                    self.board.place_stone(x, y, self.current_player)

            self.current_player *= -1
            self.move_count += 1
