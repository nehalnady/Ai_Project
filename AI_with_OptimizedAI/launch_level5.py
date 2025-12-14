import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "AI_with_OptimizedAI"))
from OptimizedConnect6GUI import OptimizedConnect6GUI

if __name__ == "__main__":
    # Get board size from command line argument, default to 19
    board_size = 19
    if len(sys.argv) > 1:
        try:
            board_size = int(sys.argv[1])
            # Validate board size
            if board_size not in [9, 13, 15, 19]:
                print(f"Invalid board size: {board_size}. Using default: 19")
                board_size = 19
        except ValueError:
            print(f"Invalid board size argument. Using default: 19")
            board_size = 19

    OptimizedConnect6GUI(board_size=board_size)