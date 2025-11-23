from Board import Board
from MInimaxAI import MinimaxAI

class Connect6Game:
    def __init__(self):
        self.board = Board(19)
        self.ai = MinimaxAI()
        self.current_player = 1  # 1 = Human (X), -1 = AI (O)
        self.move_count = 0

    def get_human_move(self, num_stones):
        """Get move from human player"""
        moves = []
        print(f"\nYour turn! Place {num_stones} stone(s)")

        for i in range(num_stones):
            while True:
                try:
                    coords = input(f"Stone {i + 1} (x y): ").strip().split()
                    x, y = int(coords[0]), int(coords[1])

                    if self.board.is_empty(x, y):
                        moves.append((x, y))
                        self.board.place_stone(x, y, self.current_player)
                        break
                    else:
                        print("Cell occupied! Try again.")
                except:
                    print("Invalid input! Use format: x y")

        return moves

    def play(self):
        """Main game loop"""
        print("=== CONNECT-6 GAME ===")
        print("You are X (Black), AI is O (White)")
        print("First move: 1 stone, then 2 stones per turn")
        print("Win by getting 6 in a row!\n")

        while True:
            self.board.print_board()

            # Check win condition
            if self.ai.evaluator.check_win(self.board, 1):
                print("\n🎉 YOU WIN! Congratulations!")
                break
            if self.ai.evaluator.check_win(self.board, -1):
                print("\n😔 AI WINS! Better luck next time!")
                break

            # Determine number of stones
            num_stones = 1 if self.move_count == 0 else 2

            # Make move
            if self.current_player == 1:  # Human
                self.get_human_move(num_stones)
            else:  # AI
                moves = self.ai.find_best_move(self.board, self.current_player, num_stones)
                for x, y in moves:
                    self.board.place_stone(x, y, self.current_player)

            # Switch players
            self.current_player *= -1
            self.move_count += 1
