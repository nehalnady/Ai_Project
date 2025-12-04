import sys
sys.path.append('..')
from UnifiedConnect6GUI import UnifiedConnect6GUI
from Board import Board
from MinimaxAIAlphaBeta import MinimaxAIAlphaBeta
from Evaluator import DIRS

if __name__ == "__main__":
    UnifiedConnect6GUI(
        board_class=Board,
        ai_class=MinimaxAIAlphaBeta,
        ai_name="Level 2: Alpha-Beta Pruning",
        evaluator_dirs=DIRS
    )