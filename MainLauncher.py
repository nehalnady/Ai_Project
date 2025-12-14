import tkinter as tk
from tkinter import messagebox, font as tkfont
import sys
import os
import subprocess


class GameLauncher:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Connect6 - AI Level Selection")
        self.window.geometry("750x700")
        self.window.configure(bg="#2C3E50")

        # Custom fonts
        self.title_font = tkfont.Font(family="Arial", size=28, weight="bold")
        self.subtitle_font = tkfont.Font(family="Arial", size=14)
        self.button_font = tkfont.Font(family="Arial", size=12, weight="bold")

        # Board size selection
        self.selected_board_size = tk.IntVar(value=19)

        self.setup_ui()
        self.center_window()
        self.window.mainloop()

    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Create the main menu UI with scrollbar"""
        # Title frame (fixed at top)
        title_frame = tk.Frame(self.window, bg="#34495E", height=120)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)

        title = tk.Label(
            title_frame,
            text="🎮 CONNECT-6 AI CHALLENGE",
            font=self.title_font,
            bg="#34495E",
            fg="white",
            pady=20
        )
        title.pack()

        subtitle = tk.Label(
            title_frame,
            text="Challenge 5 Different AI Algorithms • First Move: 1 Stone • Then: 2 Stones per Turn",
            font=self.subtitle_font,
            bg="#34495E",
            fg="#BDC3C7",
            pady=5
        )
        subtitle.pack()

        # Create main scrollable container
        main_container = tk.Frame(self.window, bg="#2C3E50")
        main_container.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # Create canvas for scrolling
        canvas = tk.Canvas(main_container, bg="#2C3E50", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)

        # Create scrollable frame
        scrollable_frame = tk.Frame(canvas, bg="#2C3E50")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Board size selection frame (inside scrollable area)
        board_size_frame = tk.LabelFrame(
            scrollable_frame,
            text="Select Board Size",
            font=("Arial", 12, "bold"),
            bg="#2C3E50",
            fg="white",
            padx=20,
            pady=15
        )
        board_size_frame.pack(fill=tk.X, padx=40, pady=(20, 10))

        # Board size options
        sizes_container = tk.Frame(board_size_frame, bg="#2C3E50")
        sizes_container.pack()

        board_sizes = [
            (9, "9×9", "Quick Game"),
            (13, "13×13", "Medium Game"),
            (15, "15×15", "Standard"),
            (19, "19×19", "Classic")
        ]

        for size, label, desc in board_sizes:
            size_frame = tk.Frame(sizes_container, bg="#34495E", relief=tk.RAISED, borderwidth=1)
            size_frame.pack(side=tk.LEFT, padx=5)

            radio = tk.Radiobutton(
                size_frame,
                text=label,
                variable=self.selected_board_size,
                value=size,
                font=("Arial", 11, "bold"),
                bg="#34495E",
                fg="white",
                selectcolor="#3498DB",
                activebackground="#34495E",
                activeforeground="white",
                indicatoron=True,
                padx=10,
                pady=5
            )
            radio.pack()

            desc_label = tk.Label(
                size_frame,
                text=desc,
                font=("Arial", 8),
                bg="#34495E",
                fg="#BDC3C7"
            )
            desc_label.pack(pady=(0, 5))

        # AI Levels section
        levels_label = tk.Label(
            scrollable_frame,
            text="Choose AI Difficulty Level",
            font=("Arial", 14, "bold"),
            bg="#2C3E50",
            fg="white",
            pady=10
        )
        levels_label.pack(padx=40)

        # Main content frame for levels
        content_frame = tk.Frame(scrollable_frame, bg="#2C3E50")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 10))

        # AI Level buttons
        levels = [
            {
                "name": "LEVEL 1: BASIC MINIMAX",
                "desc": "Simple evaluation function, no optimizations",
                "difficulty": "Beginner",
                "stars": "⭐",
                "color": "#27AE60",
                "launch_file": "AI_with_MiniMax_only/launch_level1.py"
            },
            {
                "name": "LEVEL 2: ALPHA-BETA PRUNING",
                "desc": "Optimized search with pruning techniques",
                "difficulty": "Easy",
                "stars": "⭐⭐",
                "color": "#3498DB",
                "launch_file": "AI_with_MiniMax_AlphaBeta/launch_level2.py"
            },
            {
                "name": "LEVEL 3: PATTERN RECOGNITION",
                "desc": "Evaluates stone patterns & formations",
                "difficulty": "Medium",
                "stars": "⭐⭐⭐",
                "color": "#F39C12",
                "launch_file": "AI_with_MiniMax_PatternBasedEvaluation/launch_level3.py"
            },
            {
                "name": "LEVEL 4: THREAT ANALYSIS",
                "desc": "Advanced threat detection & response",
                "difficulty": "Hard",
                "stars": "⭐⭐⭐⭐",
                "color": "#E74C3C",
                "launch_file": "AI_with_MiniMax_ThreatMoveEvaluation/launch_level4.py"
            },
            {
                "name": "LEVEL 5: OPTIMIZED AI",
                "desc": "Iterative deepening & transposition tables",
                "difficulty": "Expert",
                "stars": "⭐⭐⭐⭐⭐",
                "color": "#8E44AD",
                "launch_file": "AI_with_OptimizedAI/launch_level5.py"
            }
        ]

        for i, level in enumerate(levels):
            self.create_level_button(content_frame, level, i)

        # Footer with instructions (inside scrollable area)
        footer_frame = tk.Frame(scrollable_frame, bg="#2C3E50", pady=10)
        footer_frame.pack(fill=tk.X)

        instructions = [
            "HOW TO PLAY:",
            "• Human plays Black (●), AI plays White (○)",
            "• First move: Place 1 stone",
            "• Subsequent moves: Place 2 stones per turn",
            "• Win by connecting 6 stones in any direction"
        ]

        for instruction in instructions:
            label = tk.Label(
                footer_frame,
                text=instruction,
                font=("Arial", 9),
                bg="#2C3E50",
                fg="#95A5A6",
                justify=tk.LEFT
            )
            label.pack(anchor=tk.W, padx=50)

    def create_level_button(self, parent, level, index):
        """Create a styled level selection button"""
        frame = tk.Frame(parent, bg="#34495E", relief=tk.RAISED, borderwidth=2)
        frame.pack(fill=tk.X, pady=5)

        # Left side: Level info
        info_frame = tk.Frame(frame, bg="#34495E")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Stars and name
        stars_name_frame = tk.Frame(info_frame, bg="#34495E")
        stars_name_frame.pack(anchor=tk.W)

        stars_label = tk.Label(
            stars_name_frame,
            text=level["stars"],
            font=("Arial", 14),
            bg="#34495E",
            fg="#F1C40F"
        )
        stars_label.pack(side=tk.LEFT, padx=(0, 10))

        name_label = tk.Label(
            stars_name_frame,
            text=level["name"],
            font=self.button_font,
            bg="#34495E",
            fg="white",
            anchor=tk.W
        )
        name_label.pack(side=tk.LEFT)

        # Description
        desc_label = tk.Label(
            info_frame,
            text=level["desc"],
            font=("Arial", 10),
            bg="#34495E",
            fg="#BDC3C7",
            anchor=tk.W
        )
        desc_label.pack(anchor=tk.W, pady=(5, 0))

        # Difficulty
        diff_frame = tk.Frame(info_frame, bg="#34495E")
        diff_frame.pack(anchor=tk.W, pady=(5, 0))

        diff_tag = tk.Label(
            diff_frame,
            text="DIFFICULTY:",
            font=("Arial", 8, "bold"),
            bg="#34495E",
            fg="#7F8C8D"
        )
        diff_tag.pack(side=tk.LEFT)

        diff_label = tk.Label(
            diff_frame,
            text=level["difficulty"],
            font=("Arial", 9, "bold"),
            bg="#34495E",
            fg="#F1C40F"
        )
        diff_label.pack(side=tk.LEFT, padx=5)

        # Right side: Play button
        def launch_level():
            board_size = self.selected_board_size.get()
            self.window.withdraw()  # Hide the main menu window
            try:
                # Launch the level with board size argument
                process = subprocess.Popen([
                    sys.executable,
                    level["launch_file"],
                    str(board_size)
                ])
                process.wait()  # Wait until the game window is closed
            except Exception as e:
                messagebox.showerror("Launch Error", f"Could not launch {level['name']}:\n{str(e)}")
            self.window.deiconify()  # Show the main menu window again

        play_btn = tk.Button(
            frame,
            text="▶ PLAY",
            font=self.button_font,
            bg=level["color"],
            fg="white",
            activebackground=level["color"],
            activeforeground="white",
            cursor="hand2",
            width=12,
            command=launch_level,
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        play_btn.pack(side=tk.RIGHT, padx=20)

        # Hover effects
        def on_enter(e):
            frame.config(bg="#3E5060", relief=tk.SUNKEN, borderwidth=2)
            info_frame.config(bg="#3E5060")
            stars_name_frame.config(bg="#3E5060")
            diff_frame.config(bg="#3E5060")
            name_label.config(bg="#3E5060")
            desc_label.config(bg="#3E5060")
            diff_tag.config(bg="#3E5060")
            diff_label.config(bg="#3E5060")
            stars_label.config(bg="#3E5060")

        def on_leave(e):
            frame.config(bg="#34495E", relief=tk.RAISED, borderwidth=2)
            info_frame.config(bg="#34495E")
            stars_name_frame.config(bg="#34495E")
            diff_frame.config(bg="#34495E")
            name_label.config(bg="#34495E")
            desc_label.config(bg="#34495E")
            diff_tag.config(bg="#34495E")
            diff_label.config(bg="#34495E")
            stars_label.config(bg="#34495E")

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        info_frame.bind("<Enter>", on_enter)
        info_frame.bind("<Leave>", on_leave)
        play_btn.bind("<Enter>", on_enter)
        play_btn.bind("<Leave>", on_leave)


if __name__ == "__main__":
    launcher = GameLauncher()