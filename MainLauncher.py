import tkinter as tk
from tkinter import messagebox, font as tkfont
import sys
import os

# Import all AI implementations
sys.path.append('AI_with_MiniMax_only')
sys.path.append('AI_with_MiniMax_AlphaBeta')
sys.path.append('AI_with_MiniMax_PatternBasedEvaluation')
sys.path.append('AI_with_MiniMax_ThreatMoveEvaluation')
sys.path.append('AI_with_OptimizedAI')


class GameLauncher:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Connect6 - AI Level Selection")
        self.window.geometry("700x600")
        self.window.configure(bg="#2C3E50")

        # Custom fonts
        self.title_font = tkfont.Font(family="Arial", size=24, weight="bold")
        self.subtitle_font = tkfont.Font(family="Arial", size=12)
        self.button_font = tkfont.Font(family="Arial", size=11, weight="bold")

        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self):
        """Create the main menu UI"""
        # Title
        title_frame = tk.Frame(self.window, bg="#34495E", pady=20)
        title_frame.pack(fill=tk.X)

        title = tk.Label(
            title_frame,
            text="🎮 CONNECT-6 GAME",
            font=self.title_font,
            bg="#34495E",
            fg="white"
        )
        title.pack()

        subtitle = tk.Label(
            title_frame,
            text="Select Your AI Opponent Level",
            font=self.subtitle_font,
            bg="#34495E",
            fg="#BDC3C7"
        )
        subtitle.pack(pady=5)

        # Main content frame
        content_frame = tk.Frame(self.window, bg="#2C3E50")
        content_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)

        # AI Level buttons
        levels = [
            {
                "name": "Level 1: Basic Minimax",
                "desc": "Simple stone counting evaluation",
                "difficulty": "⭐ Beginner",
                "color": "#27AE60",
                "command": self.launch_basic
            },
            {
                "name": "Level 2: Alpha-Beta Pruning",
                "desc": "Optimized search with pruning",
                "difficulty": "⭐⭐ Easy",
                "color": "#3498DB",
                "command": self.launch_alphabeta
            },
            {
                "name": "Level 3: Pattern Recognition",
                "desc": "Evaluates stone patterns & formations",
                "difficulty": "⭐⭐⭐ Medium",
                "color": "#F39C12",
                "command": self.launch_pattern
            },
            {
                "name": "Level 4: Threat Analysis",
                "desc": "Advanced threat detection & response",
                "difficulty": "⭐⭐⭐⭐ Hard",
                "color": "#E74C3C",
                "command": self.launch_threat
            },
            {
                "name": "Level 5: Optimized AI",
                "desc": "Iterative deepening & transposition tables",
                "difficulty": "⭐⭐⭐⭐⭐ Expert",
                "color": "#8E44AD",
                "command": self.launch_optimized
            }
        ]

        for i, level in enumerate(levels):
            self.create_level_button(content_frame, level, i)

        # Footer
        footer = tk.Label(
            self.window,
            text="First player places 1 stone, then everyone places 2 stones per turn\nConnect 6 in a row to win!",
            font=("Arial", 9),
            bg="#2C3E50",
            fg="#95A5A6",
            justify=tk.CENTER
        )
        footer.pack(pady=10)

    def create_level_button(self, parent, level, index):
        """Create a styled level selection button"""
        frame = tk.Frame(parent, bg="#34495E", relief=tk.RAISED, borderwidth=2)
        frame.pack(fill=tk.X, pady=8)

        # Level info
        info_frame = tk.Frame(frame, bg="#34495E")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)

        name_label = tk.Label(
            info_frame,
            text=level["name"],
            font=self.button_font,
            bg="#34495E",
            fg="white",
            anchor=tk.W
        )
        name_label.pack(anchor=tk.W)

        desc_label = tk.Label(
            info_frame,
            text=level["desc"],
            font=("Arial", 9),
            bg="#34495E",
            fg="#BDC3C7",
            anchor=tk.W
        )
        desc_label.pack(anchor=tk.W, pady=2)

        diff_label = tk.Label(
            info_frame,
            text=level["difficulty"],
            font=("Arial", 9, "bold"),
            bg="#34495E",
            fg="#F1C40F",
            anchor=tk.W
        )
        diff_label.pack(anchor=tk.W)

        # Play button
        play_btn = tk.Button(
            frame,
            text="▶ PLAY",
            font=self.button_font,
            bg=level["color"],
            fg="white",
            activebackground=level["color"],
            activeforeground="white",
            cursor="hand2",
            width=10,
            command=level["command"],
            relief=tk.FLAT
        )
        play_btn.pack(side=tk.RIGHT, padx=15)

        # Hover effects
        def on_enter(e):
            frame.config(bg="#3E5060", relief=tk.RAISED, borderwidth=3)
            info_frame.config(bg="#3E5060")
            name_label.config(bg="#3E5060")
            desc_label.config(bg="#3E5060")
            diff_label.config(bg="#3E5060")

        def on_leave(e):
            frame.config(bg="#34495E", relief=tk.RAISED, borderwidth=2)
            info_frame.config(bg="#34495E")
            name_label.config(bg="#34495E")
            desc_label.config(bg="#34495E")
            diff_label.config(bg="#34495E")

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        info_frame.bind("<Enter>", on_enter)
        info_frame.bind("<Leave>", on_leave)

    def launch_basic(self):
        """Launch Basic Minimax AI"""
        self.window.destroy()
        from AI_with_MiniMax_only.Connect6GUI import Connect6GUI
        Connect6GUI()

    def launch_alphabeta(self):
        """Launch Alpha-Beta Pruning AI"""
        self.window.destroy()
        from AI_with_MiniMax_AlphaBeta.Connect6GUI import Connect6GUI
        Connect6GUI()

    def launch_pattern(self):
        """Launch Pattern-Based AI"""
        self.window.destroy()
        from AI_with_MiniMax_PatternBasedEvaluation.Connect6GUI import Connect6GUI
        Connect6GUI()

    def launch_threat(self):
        """Launch Threat Analysis AI"""
        self.window.destroy()
        from AI_with_MiniMax_ThreatMoveEvaluation.Connect6GUI import Connect6GUI
        Connect6GUI()

    def launch_optimized(self):
        """Launch Optimized AI"""
        self.window.destroy()
        from AI_with_OptimizedAI.OptimizedConnect6GUI import OptimizedConnect6GUI
        OptimizedConnect6GUI()


if __name__ == "__main__":
    launcher = GameLauncher()