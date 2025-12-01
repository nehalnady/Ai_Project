import time
import tkinter as tk
from tkinter import ttk, messagebox
from Board import Board
from OptimizedAI import OptimizedAI
from Evaluator import DIRS


class OptimizedConnect6GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Connect6 - Optimized AI")

        # Game state
        self.size = 19
        self.cell = 30
        self.board_obj = None
        self.ai = None
        self.game_started = False

        # Turn tracking
        self.turn = 1
        self.human_needed = 1
        self.human_placed = 0
        self.ai_needed = 2
        self.game_over = False
        self.last_moves = []
        self.ai_times = []
        self.total_turns = 0
        self.total_stones = 0

        # Performance tracking
        self.total_nodes = 0
        self.total_cache_hits = 0
        self.depths_reached = []

        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self):
        """Create UI with performance monitoring"""
        # Top control panel
        control_frame = tk.LabelFrame(self.window, text="Game Controls",
                                      font=("Arial", 10, "bold"), padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Board size
        # tk.Label(control_frame, text="Board Size:", font=("Arial", 9)).grid(row=0, column=0, padx=5)
        # self.size_var = tk.IntVar(value=19)
        # size_combo = ttk.Combobox(control_frame, textvariable=self.size_var,
        #                           values=[9, 13, 15, 19], state="readonly", width=5)
        # size_combo.grid(row=0, column=1, padx=5)

        # Time limit slider
        tk.Label(control_frame, text="AI Time Limit:", font=("Arial", 9)).grid(row=0, column=2, padx=5)
        self.time_limit_var = tk.DoubleVar(value=5.0)
        time_slider = tk.Scale(control_frame, from_=1, to=10, resolution=0.5,
                               orient=tk.HORIZONTAL, variable=self.time_limit_var,
                               length=150)
        time_slider.grid(row=0, column=3, padx=5)
        self.time_label = tk.Label(control_frame, text="5.0s", font=("Arial", 9))
        self.time_label.grid(row=0, column=4, padx=5)
        time_slider.config(command=lambda v: self.time_label.config(text=f"{float(v):.1f}s"))

        # Buttons
        self.start_btn = tk.Button(control_frame, text="▶ Start Game", command=self.start_game,
                                   bg="#4CAF50", fg="white", font=("Arial", 9, "bold"))
        self.start_btn.grid(row=0, column=5, padx=5)

        self.reset_btn = tk.Button(control_frame, text="↻ Reset", command=self.reset_game,
                                   bg="#FF9800", fg="white", font=("Arial", 9, "bold"), state=tk.DISABLED)
        self.reset_btn.grid(row=0, column=6, padx=5)

        # Canvas
        canvas_frame = tk.Frame(self.window, relief=tk.SUNKEN, borderwidth=2)
        canvas_frame.pack(side=tk.TOP, padx=5, pady=5)
        self.canvas_container = tk.Frame(canvas_frame, bg="#DCB35C")
        self.canvas_container.pack(padx=3, pady=3)
        self.canvas = None

        # Performance metrics panel
        perf_frame = tk.LabelFrame(self.window, text="Performance Metrics",
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        perf_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Metrics grid
        metrics = tk.Frame(perf_frame)
        metrics.pack()

        # Row 1
        tk.Label(metrics, text="Last Move Time:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.last_time_label = tk.Label(metrics, text="--", font=("Arial", 9), fg="#2196F3")
        self.last_time_label.grid(row=0, column=1, sticky=tk.W, padx=5)

        tk.Label(metrics, text="Avg Time:", font=("Arial", 9, "bold")).grid(row=0, column=2, sticky=tk.W, padx=5)
        self.avg_time_label = tk.Label(metrics, text="--", font=("Arial", 9))
        self.avg_time_label.grid(row=0, column=3, sticky=tk.W, padx=5)

        # Row 2
        tk.Label(metrics, text="Depth Reached:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5)
        self.depth_label = tk.Label(metrics, text="--", font=("Arial", 9), fg="#4CAF50")
        self.depth_label.grid(row=1, column=1, sticky=tk.W, padx=5)

        tk.Label(metrics, text="Nodes Explored:", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky=tk.W, padx=5)
        self.nodes_label = tk.Label(metrics, text="--", font=("Arial", 9))
        self.nodes_label.grid(row=1, column=3, sticky=tk.W, padx=5)

        # Row 3
        tk.Label(metrics, text="Cache Hit Rate:", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5)
        self.cache_label = tk.Label(metrics, text="--", font=("Arial", 9), fg="#FF9800")
        self.cache_label.grid(row=2, column=1, sticky=tk.W, padx=5)

        tk.Label(metrics, text="Moves:", font=("Arial", 9, "bold")).grid(row=2, column=2, sticky=tk.W, padx=5)
        self.moves_label = tk.Label(metrics, text="0 turns / 0 stones", font=("Arial", 9))
        self.moves_label.grid(row=2, column=3, sticky=tk.W, padx=5)

        # Status bar
        self.status_label = tk.Label(self.window, text="● Ready - Select board size and click Start",
                                     font=("Arial", 9), fg="#4CAF50", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def start_game(self):
        """Initialize game with optimized AI"""
        try:
            # self.size = self.size_var.get()
            time_limit = self.time_limit_var.get()

            # Calculate cell size
            if self.size == 9:
                self.cell = 45
            elif self.size <= 13:
                self.cell = 38
            else:
                self.cell = 30

            # Initialize game
            self.board_obj = Board(self.size)
            self.ai = OptimizedAI(max_time=time_limit)

            # Reset state
            self.turn = 1
            self.human_needed = 1
            self.human_placed = 0
            self.game_over = False
            self.last_moves = []
            self.ai_times = []
            self.total_turns = 0
            self.total_stones = 0
            self.game_started = True

            self.total_nodes = 0
            self.total_cache_hits = 0
            self.depths_reached = []

            # Update UI
            self.start_btn.config(state=tk.DISABLED)
            self.reset_btn.config(state=tk.NORMAL)
            self.status_label.config(text=f"● Game Active - {self.size}×{self.size} | Time Limit: {time_limit}s",
                                     fg="#4CAF50")

            # Create canvas
            self.create_canvas()
            self.draw_board()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start: {str(e)}")

    def create_canvas(self):
        """Create game canvas"""
        if self.canvas:
            self.canvas.destroy()

        size = self.size * self.cell
        self.canvas = tk.Canvas(self.canvas_container, width=size, height=size,
                                bg="#DCB35C", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        """Draw complete board"""
        if not self.canvas or not self.board_obj:
            return

        self.canvas.delete("all")

        # Grid
        for i in range(self.size):
            offset = self.cell // 2
            self.canvas.create_line(offset, i * self.cell + offset,
                                    self.size * self.cell - offset, i * self.cell + offset)
            self.canvas.create_line(i * self.cell + offset, offset,
                                    i * self.cell + offset, self.size * self.cell - offset)

        # Star points
        if self.size >= 13:
            stars = {
                19: [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)],
                13: [(3, 3), (3, 9), (6, 6), (9, 3), (9, 9)]
            }.get(self.size, [])

            for sx, sy in stars:
                px = sx * self.cell + self.cell // 2
                py = sy * self.cell + self.cell // 2
                self.canvas.create_oval(px - 3, py - 3, px + 3, py + 3, fill="black")

        # Stones
        for x in range(self.size):
            for y in range(self.size):
                if self.board_obj.grid[x][y] != 0:
                    self.draw_stone(x, y, self.board_obj.grid[x][y])

        self.draw_highlights()

    def draw_stone(self, x, y, player):
        """Draw stone"""
        px = x * self.cell + self.cell // 2
        py = y * self.cell + self.cell // 2
        r = max(8, self.cell // 3)

        color = "black" if player == 1 else "white"
        outline = "black" if player == 1 else "gray"

        self.canvas.create_oval(px - r, py - r, px + r, py + r, fill=color, outline=outline, width=2)

    def draw_highlights(self):
        """Highlight last moves"""
        self.canvas.delete("highlight")
        for x, y in self.last_moves:
            px = x * self.cell + self.cell // 2
            py = y * self.cell + self.cell // 2
            r = max(3, self.cell // 10)
            self.canvas.create_oval(px - r, py - r, px + r, py + r, fill="red", tags="highlight")

    def handle_click(self, event):
        """Handle human move"""
        if not self.game_started or self.game_over or self.turn != 1:
            return

        x = event.x // self.cell
        y = event.y // self.cell

        if not (0 <= x < self.size and 0 <= y < self.size) or not self.board_obj.is_empty(x, y):
            return

        # Place stone
        self.board_obj.place_stone(x, y, 1)
        self.draw_stone(x, y, 1)
        self.total_stones += 1
        self.human_placed += 1

        if self.human_placed == 1:
            self.last_moves = [(x, y)]
        else:
            self.last_moves.append((x, y))
        self.draw_highlights()

        if self.check_win(1):
            self.end_game("🎉 Human Wins!")
            return

        if self.human_placed >= self.human_needed:
            self.human_needed = 2
            self.human_placed = 0
            self.turn = -1
            self.total_turns += 1
            self.update_moves()
            self.window.after(100, self.ai_move)

    def ai_move(self):
        """AI makes move with performance tracking"""
        if not self.game_started or self.game_over:
            return

        self.status_label.config(text="● AI Thinking...", fg="#FF9800")
        self.window.update()

        start = time.perf_counter()
        moves = self.ai.find_best_move(self.board_obj, -1, self.ai_needed)
        elapsed = time.perf_counter() - start

        # Update performance metrics
        self.ai_times.append(elapsed)
        self.total_nodes += self.ai.nodes_explored
        self.total_cache_hits += self.ai.cache_hits

        # Update UI metrics
        self.last_time_label.config(text=f"{elapsed:.3f}s")
        avg_time = sum(self.ai_times) / len(self.ai_times)
        self.avg_time_label.config(text=f"{avg_time:.3f}s")
        self.nodes_label.config(text=f"{self.ai.nodes_explored:,}")

        if self.ai.nodes_explored > 0:
            hit_rate = (self.ai.cache_hits / self.ai.nodes_explored) * 100
            self.cache_label.config(text=f"{hit_rate:.1f}%")

        # Place AI stones
        if moves:
            self.last_moves = []
            for mx, my in moves[:2]:
                if 0 <= mx < self.size and 0 <= my < self.size and self.board_obj.is_empty(mx, my):
                    self.board_obj.place_stone(mx, my, -1)
                    self.draw_stone(mx, my, -1)
                    self.total_stones += 1
                    self.last_moves.append((mx, my))

            self.draw_highlights()

            if self.check_win(-1):
                self.end_game("🤖 AI Wins!")
                return

        self.turn = 1
        self.total_turns += 1
        self.update_moves()
        self.status_label.config(text="● Your Turn", fg="#4CAF50")

    def check_win(self, player):
        """Check for win"""
        for x in range(self.size):
            for y in range(self.size):
                if self.board_obj.grid[x][y] != player:
                    continue

                for dx, dy in DIRS:
                    count = 1
                    coords = [(x, y)]

                    nx, ny = x + dx, y + dy
                    while 0 <= nx < self.size and 0 <= ny < self.size and self.board_obj.grid[nx][ny] == player:
                        coords.append((nx, ny))
                        count += 1
                        nx += dx
                        ny += dy

                    nx, ny = x - dx, y - dy
                    while 0 <= nx < self.size and 0 <= ny < self.size and self.board_obj.grid[nx][ny] == player:
                        coords.insert(0, (nx, ny))
                        count += 1
                        nx -= dx
                        ny -= dy

                    if count >= 6:
                        self.highlight_win(coords[:6])
                        return True
        return False

    def highlight_win(self, coords):
        """Highlight winning line"""
        for x, y in coords:
            px = x * self.cell + self.cell // 2
            py = y * self.cell + self.cell // 2
            s = max(10, self.cell // 2.5)
            self.canvas.create_rectangle(px - s, py - s, px + s, py + s, outline="red", width=4)

    def update_moves(self):
        """Update move counter"""
        self.moves_label.config(text=f"{self.total_turns} turns / {self.total_stones} stones")

    def end_game(self, message):
        """End game with statistics"""
        self.game_over = True

        avg = sum(self.ai_times) / len(self.ai_times) if self.ai_times else 0
        total_cache_rate = (self.total_cache_hits / max(self.total_nodes, 1)) * 100

        stats = f"{message}\n\n"
        stats += f"Board: {self.size}×{self.size}\n"
        stats += f"Total Moves: {self.total_turns}\n"
        stats += f"Avg AI Time: {avg:.3f}s\n"
        stats += f"Total Nodes: {self.total_nodes:,}\n"
        stats += f"Cache Hit Rate: {total_cache_rate:.1f}%\n"

        self.status_label.config(text=f"● {message}", fg="red")
        messagebox.showinfo("Game Over", stats)

    def reset_game(self):
        """Reset game"""
        self.game_started = False
        self.start_btn.config(state=tk.NORMAL)
        self.reset_btn.config(state=tk.DISABLED)
        self.status_label.config(text="● Ready - Select settings and click Start", fg="#4CAF50")

        # Clear metrics
        self.last_time_label.config(text="--")
        self.avg_time_label.config(text="--")
        self.depth_label.config(text="--")
        self.nodes_label.config(text="--")
        self.cache_label.config(text="--")
        self.moves_label.config(text="0 turns / 0 stones")

        if self.canvas:
            self.canvas.destroy()
            self.canvas = None


if __name__ == "__main__":
    gui = OptimizedConnect6GUI()