import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "AI_with_MiniMax_ThreatMoveEvaluation"))
from UnifiedConnect6GUI import UnifiedConnect6GUI
from Board import Board
from MinimaxAI import MinimaxAI
from Evaluator import DIRS

if __name__ == "__main__":
    UnifiedConnect6GUI(
        board_class=Board,
        ai_class=MinimaxAI,
        ai_name="Level 4: Threat Analysis",
        evaluator_dirs=DIRS
    )