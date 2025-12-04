import tkinter as tk
from tkinter import messagebox, font as tkfont
import sys
import os
import subprocess


class GameLauncher:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Connect6 - AI Level Selection")
        self.window.geometry("750x650")
        self.window.configure(bg="#2C3E50")

        # Center window on screen
        self.center_window()

        # Custom fonts
        self.title_font = tkfont.Font(family="Arial", size=28, weight="bold")
        self.subtitle_font = tkfont.Font(family="Arial", size=14)
        self.button_font = tkfont.Font(family="Arial", size=12, weight="bold")

        self.setup_ui()
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
        """Create the main menu UI"""
        # Title frame with gradient effect
        title_frame = tk.Frame(self.window, bg="#34495E", height=120)
        title_frame.pack(fill=tk.X)
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

        # Main content frame
        content_frame = tk.Frame(self.window, bg="#2C3E50")
        content_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=30)

        # AI Level buttons
        levels = [
            {
                "name": "LEVEL 1: BASIC MINIMAX",
                "desc": "Simple evaluation function, no optimizations",
                "difficulty": "Beginner",
                "stars": "⭐",
                "color": "#27AE60",
                "launch_file": "launch_level1.py"
            },
            {
                "name": "LEVEL 2: ALPHA-BETA PRUNING",
                "desc": "Optimized search with pruning techniques",
                "difficulty": "Easy",
                "stars": "⭐⭐",
                "color": "#3498DB",
                "launch_file": "launch_level2.py"
            },
            {
                "name": "LEVEL 3: PATTERN RECOGNITION",
                "desc": "Evaluates stone patterns & formations",
                "difficulty": "Medium",
                "stars": "⭐⭐⭐",
                "color": "#F39C12",
                "launch_file": "launch_level3.py"
            },
            {
                "name": "LEVEL 4: THREAT ANALYSIS",
                "desc": "Advanced threat detection & response",
                "difficulty": "Hard",
                "stars": "⭐⭐⭐⭐",
                "color": "#E74C3C",
                "launch_file": "launch_level4.py"
            },
            {
                "name": "LEVEL 5: OPTIMIZED AI",
                "desc": "Iterative deepening & transposition tables",
                "difficulty": "Expert",
                "stars": "⭐⭐⭐⭐⭐",
                "color": "#8E44AD",
                "launch_file": "launch_level5.py"
            }
        ]

        for i, level in enumerate(levels):
            self.create_level_button(content_frame, level, i)

        # Footer with instructions
        footer_frame = tk.Frame(self.window, bg="#2C3E50", pady=20)
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
        frame.pack(fill=tk.X, pady=6)

        # Left side: Level info
        info_frame = tk.Frame(frame, bg="#34495E")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=12)

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
            self.window.destroy()
            try:
                # Launch the level using the launch file
                subprocess.Popen([sys.executable, level["launch_file"]])
            except Exception as e:
                # Fallback: show error and restart launcher
                messagebox.showerror("Launch Error", f"Could not launch {level['name']}:\n{str(e)}")
                subprocess.Popen([sys.executable, "MainLauncher.py"])

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