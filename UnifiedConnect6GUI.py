import time
import tkinter as tk
from tkinter import messagebox
import sys
import os

class UnifiedConnect6GUI:
    """
    Enhanced Connect6 GUI with game statistics and menu navigation
    Works with any AI implementation
    """

    def __init__(self, board_class, ai_class, ai_name="AI", evaluator_dirs=None):
        self.window = tk.Tk()
        self.window.title(f"Connect6 vs {ai_name}")

        # Store classes
        self.board_class = board_class
        self.ai_class = ai_class
        self.ai_name = ai_name
        self.DIRS = evaluator_dirs or [(1, 0), (0, 1), (1, 1), (1, -1)]

        # Game settings
        self.size = 19
        self.cell = 30

        # Game objects
        self.board_obj = board_class(self.size)
        self.ai = ai_class()

        # Turn & stones tracking
        self.turn = 1  # human = 1 (black), AI = -1 (white)
        self.human_needed = 1  # first human turn -> 1 stone
        self.human_placed = 0  # stones placed this human turn
        self.ai_needed = 2  # AI always places 2 stones

        self.game_over = False
        self.last_moves = []  # highlight last move(s)
        self.ai_times = []  # AI response times

        # Move counters
        self.total_turns = 0
        self.total_stones = 0
        self.game_start_time = time.time()

        # Canvas and UI
        self.canvas = tk.Canvas(
            self.window,
            width=self.size * self.cell,
            height=self.size * self.cell,
            bg="#EECFA1"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        # Buttons frame
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=5)

        self.restart_btn = tk.Button(
            btn_frame,
            text="🔄 Restart",
            command=self.restart_game,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            padx=10
        )
        self.restart_btn.pack(side=tk.LEFT, padx=5)

        self.menu_btn = tk.Button(
            btn_frame,
            text="🏠 Main Menu",
            command=self.return_to_menu,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            padx=10
        )
        self.menu_btn.pack(side=tk.LEFT, padx=5)

        # Info labels
        info_frame = tk.Frame(self.window)
        info_frame.pack(pady=5)

        tk.Label(info_frame, text="Opponent:", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5)
        tk.Label(info_frame, text=ai_name, font=("Arial", 9), fg="#2196F3").grid(row=0, column=1, padx=5)

        tk.Label(info_frame, text="Last AI Time:", font=("Arial", 9, "bold")).grid(row=1, column=0, padx=5)
        self.time_label = tk.Label(info_frame, text="0.000s", font=("Arial", 9))
        self.time_label.grid(row=1, column=1, padx=5)

        tk.Label(info_frame, text="Moves:", font=("Arial", 9, "bold")).grid(row=2, column=0, padx=5)
        self.moves_label = tk.Label(info_frame, text="Turns: 0 | Stones: 0", font=("Arial", 9))
        self.moves_label.grid(row=2, column=1, padx=5)

        self.draw_grid()
        self.window.mainloop()

    # ---------- drawing ----------
    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.size):
            self.canvas.create_line(
                self.cell // 2, i * self.cell + self.cell // 2,
                self.size * self.cell - self.cell // 2, i * self.cell + self.cell // 2
            )
            self.canvas.create_line(
                i * self.cell + self.cell // 2, self.cell // 2,
                i * self.cell + self.cell // 2, self.size * self.cell - self.cell // 2
            )
        # draw existing stones
        for x in range(self.size):
            for y in range(self.size):
                v = self.board_obj.grid[x][y]
                if v != 0:
                    self.draw_stone(x, y, v)
        # highlight last moves
        self.highlight_last_moves()

    def draw_stone(self, x, y, player):
        px = x * self.cell + self.cell // 2
        py = y * self.cell + self.cell // 2
        color = "black" if player == 1 else "white"
        self.canvas.create_oval(px - 12, py - 12, px + 12, py + 12, fill=color, outline="black")

    def highlight_last_moves(self):
        for (x, y) in self.last_moves:
            px = x * self.cell + self.cell // 2
            py = y * self.cell + self.cell // 2
            self.canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="yellow", tags="highlight")

    # ---------- move tracking ----------
    def place_stone(self, x, y, player):
        self.board_obj.place_stone(x, y, player)
        self.draw_stone(x, y, player)
        self.total_stones += 1
        self.update_moves_label()

    def update_moves_label(self):
        self.moves_label.config(text=f"Turns: {self.total_turns} | Stones: {self.total_stones}")

    # ---------- draw check ----------
    def is_draw(self):
        return all(self.board_obj.grid[x][y] != 0 for x in range(self.size) for y in range(self.size))

    # ---------- human click ----------
    def handle_click(self, event):
        if self.game_over or self.turn != 1:
            return

        x = event.x // self.cell
        y = event.y // self.cell
        if not (0 <= x < self.size and 0 <= y < self.size):
            return
        if not self.board_obj.is_empty(x, y):
            return

        self.place_stone(x, y, 1)
        self.human_placed += 1
        # highlight last moves
        if self.human_placed == 1:
            self.last_moves = [(x, y)]
        else:
            self.last_moves.append((x, y))
        self.canvas.delete("highlight")
        self.highlight_last_moves()

        if self.check_win(1):
            self.end_game("Human")
            return
        elif self.is_draw():
            self.end_game("Draw")
            return

        # finish human turn if placed required stones
        if self.human_placed >= self.human_needed:
            self.human_needed = 2  # future human turns = 2 stones
            self.human_placed = 0
            self.turn = -1
            self.total_turns += 1
            self.update_moves_label()
            self.window.after(80, self.ai_move)

    # ---------- AI move ----------
    def ai_move(self):
        if self.game_over:
            return

        start = time.perf_counter()
        moves = self.ai.find_best_move(self.board_obj, -1, self.ai_needed)
        end = time.perf_counter()

        self.ai_times.append(end - start)
        self.time_label.config(text=f"{end - start:.3f}s")

        valid_moves = []
        if moves:
            for m in moves[:2]:
                x, y = m
                if 0 <= x < self.size and 0 <= y < self.size and self.board_obj.is_empty(x, y):
                    self.place_stone(x, y, -1)
                    valid_moves.append((x, y))

        self.last_moves = valid_moves
        self.canvas.delete("highlight")
        self.highlight_last_moves()

        for x, y in valid_moves:
            if self.check_win(-1):
                self.end_game("AI")
                return

        if self.is_draw():
            self.end_game("Draw")
            return

        self.turn = 1
        self.total_turns += 1
        self.update_moves_label()

    # ---------- win detection ----------
    def check_win(self, player):
        grid = self.board_obj.grid
        for x in range(self.size):
            for y in range(self.size):
                if grid[x][y] != player:
                    continue
                for dx, dy in self.DIRS:
                    count = 1
                    coords = [(x, y)]
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < self.size and 0 <= ny < self.size and grid[nx][ny] == player:
                        coords.append((nx, ny))
                        count += 1
                        nx += dx;
                        ny += dy
                    nx, ny = x - dx, y - dy
                    while 0 <= nx < self.size and 0 <= ny < self.size and grid[nx][ny] == player:
                        coords.insert(0, (nx, ny))
                        count += 1
                        nx -= dx;
                        ny -= dy
                    if count >= 6:
                        self.highlight_win_line(coords[:6])
                        return True
        return False

    def highlight_win_line(self, stones):
        for (x, y) in stones:
            px = x * self.cell + self.cell // 2
            py = y * self.cell + self.cell // 2
            self.canvas.create_rectangle(px - 14, py - 14, px + 14, py + 14, outline="red", width=3)

    # ---------- end & restart ----------
    def end_game(self, winner):
        self.game_over = True
        game_duration = time.time() - self.game_start_time
        avg = sum(self.ai_times) / len(self.ai_times) if self.ai_times else 0.0
        min_time = min(self.ai_times) if self.ai_times else 0.0
        max_time = max(self.ai_times) if self.ai_times else 0.0

        # Create detailed statistics message
        stats = "=" * 50 + "\n"
        if winner == "Draw":
            stats += f"🎮 GAME OVER - DRAW!\n"
        else:
            stats += f"🎮 GAME OVER - {winner.upper()} WINS!\n"
        stats += "=" * 50 + "\n\n"

        stats += f"👤 Opponent: {self.ai_name}\n"
        stats += f"🏆 Result: {winner}\n\n"

        stats += "📊 Game Statistics:\n"
        stats += f"  • Total Turns: {self.total_turns}\n"
        stats += f"  • Total Stones: {self.total_stones}\n"
        stats += f"  • Game Duration: {game_duration:.1f}s\n\n"

        stats += "🤖 AI Performance:\n"
        stats += f"  • Avg Response Time: {avg:.3f}s\n"
        stats += f"  • Min Response Time: {min_time:.3f}s\n"
        stats += f"  • Max Response Time: {max_time:.3f}s\n"
        stats += f"  • Total AI Moves: {len(self.ai_times)}\n\n"

        stats += "=" * 50

        print("\n" + stats)

        # Show custom dialog with three options
        self.show_game_over_dialog(winner, avg, game_duration)

    def show_game_over_dialog(self, winner, avg_time, game_duration):
        """Show custom dialog with three options after game ends"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Game Over")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.configure(bg="#2C3E50")

        # Make dialog modal
        dialog.transient(self.window)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"+{x}+{y}")

        # Header
        header_frame = tk.Frame(dialog, bg="#34495E", pady=15)
        header_frame.pack(fill=tk.X)

        if winner == "Draw":
            msg = "🤝 GAME DRAWN! 🤝"
            color = "#F1C40F"
        elif winner == "Human":
            msg = "🎉 HUMAN WINS! 🎉"
            color = "#F1C40F"
        else:
            msg = f"🤖 {winner.upper()} WINS! 🤖"
            color = "#3498DB"

        tk.Label(
            header_frame,
            text=msg,
            font=("Arial", 18, "bold"),
            bg="#34495E",
            fg=color
        ).pack()

        # Stats frame
        stats_frame = tk.Frame(dialog, bg="#2C3E50", pady=20)
        stats_frame.pack(fill=tk.BOTH, expand=True)

        stats_data = [
            ("Opponent:", self.ai_name),
            ("Total Turns:", str(self.total_turns)),
            ("Total Stones:", str(self.total_stones)),
            ("Game Duration:", f"{game_duration:.1f}s"),
            ("Avg AI Time:", f"{avg_time:.3f}s")
        ]

        for i, (label, value) in enumerate(stats_data):
            row_frame = tk.Frame(stats_frame, bg="#2C3E50")
            row_frame.pack(fill=tk.X, padx=30, pady=3)

            tk.Label(
                row_frame,
                text=label,
                font=("Arial", 10, "bold"),
                bg="#2C3E50",
                fg="#BDC3C7",
                anchor=tk.W,
                width=15
            ).pack(side=tk.LEFT)

            tk.Label(
                row_frame,
                text=value,
                font=("Arial", 10),
                bg="#2C3E50",
                fg="white",
                anchor=tk.W
            ).pack(side=tk.LEFT)

        # Buttons frame
        btn_frame = tk.Frame(dialog, bg="#2C3E50", pady=15)
        btn_frame.pack(fill=tk.X)

        def play_again():
            dialog.destroy()
            self.restart_game()

        def choose_level():
            dialog.destroy()
            self.window.destroy()
            # Do NOT launch MainLauncher.py here; main process will handle menu.

        def quit_game():
            dialog.destroy()
            self.window.destroy()

        # Play Again button
        tk.Button(
            btn_frame,
            text="🔄 Play Again",
            font=("Arial", 11, "bold"),
            bg="#27AE60",
            fg="white",
            width=18,
            height=2,
            command=play_again,
            cursor="hand2"
        ).pack(pady=5)

        # Choose Another Level button
        tk.Button(
            btn_frame,
            text="🎮 Choose Another Level",
            font=("Arial", 11, "bold"),
            bg="#3498DB",
            fg="white",
            width=18,
            height=2,
            command=choose_level,
            cursor="hand2"
        ).pack(pady=5)

        # Quit button
        tk.Button(
            btn_frame,
            text="❌ Quit",
            font=("Arial", 11, "bold"),
            bg="#E74C3C",
            fg="white",
            width=18,
            height=2,
            command=quit_game,
            cursor="hand2"
        ).pack(pady=5)

        # Wait for dialog to close
        dialog.wait_window()

    def restart_game(self):
        self.board_obj = self.board_class(self.size)
        self.turn = 1
        self.human_needed = 1
        self.human_placed = 0
        self.ai_times = []
        self.game_over = False
        self.last_moves = []
        self.total_turns = 0
        self.total_stones = 0
        self.game_start_time = time.time()
        self.time_label.config(text="0.000s")
        self.update_moves_label()
        self.draw_grid()

    def return_to_menu(self):
        """Return to main menu"""
        if not self.game_over:
            result = messagebox.askyesno(
                "Confirm",
                "Game in progress. Return to main menu?",
                icon='warning'
            )
            if not result:
                return
        self.window.destroy()
        # Do NOT launch MainLauncher.py here; main process will handle menu.