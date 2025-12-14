import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "AI_with_MiniMax_AlphaBeta"))
from UnifiedConnect6GUI import UnifiedConnect6GUI
from Board import Board
from MinimaxAIAlphaBeta import MinimaxAIAlphaBeta
from Evaluator import DIRS

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

    UnifiedConnect6GUI(
        board_class=Board,
        ai_class=MinimaxAIAlphaBeta,
        ai_name="Level 2: Alpha-Beta Pruning",
        evaluator_dirs=DIRS,
        board_size=board_size
    )