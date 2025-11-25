import time
import tkinter as tk
from Board import Board
from MinimaxAI import MinimaxAI
from Evaluator import DIRS

class Connect6GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Connect6")

        self.size = 19
        self.cell = 30

        # Game objects
        self.board_obj = Board(self.size)
        self.ai = MinimaxAI()

        # Turn & stones tracking
        self.turn = 1  # human = 1 (black), AI = -1 (white)
        self.human_needed = 1    # first human turn -> 1 stone
        self.human_placed = 0    # stones placed this human turn
        self.ai_needed = 2       # AI always places 2 stones

        self.game_over = False
        self.last_moves = []     # highlight last move(s)
        self.ai_times = []       # AI response times

        # Move counters
        self.total_turns = 0
        self.total_stones = 0

        # Canvas and UI
        self.canvas = tk.Canvas(self.window,
                                width=self.size*self.cell,
                                height=self.size*self.cell,
                                bg="#EECFA1")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.restart_btn = tk.Button(self.window, text="Restart", command=self.restart_game)
        self.restart_btn.pack(pady=5)

        self.time_label = tk.Label(self.window, text="AI Time: 0.000s")
        self.time_label.pack()

        self.moves_label = tk.Label(self.window, text="Total Turns: 0 | Total Stones: 0")
        self.moves_label.pack()

        self.draw_grid()
        self.window.mainloop()

    # ---------- drawing ----------
    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.size):
            self.canvas.create_line(
                self.cell//2, i*self.cell + self.cell//2,
                self.size*self.cell - self.cell//2, i*self.cell + self.cell//2
            )
            self.canvas.create_line(
                i*self.cell + self.cell//2, self.cell//2,
                i*self.cell + self.cell//2, self.size*self.cell - self.cell//2
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
        px = x*self.cell + self.cell//2
        py = y*self.cell + self.cell//2
        color = "black" if player == 1 else "white"
        self.canvas.create_oval(px-12, py-12, px+12, py+12, fill=color, outline="black")

    def highlight_last_moves(self):
        for (x, y) in self.last_moves:
            px = x*self.cell + self.cell//2
            py = y*self.cell + self.cell//2
            self.canvas.create_oval(px-4, py-4, px+4, py+4, fill="yellow", tags="highlight")

    # ---------- move tracking ----------
    def place_stone(self, x, y, player):
        self.board_obj.place_stone(x, y, player)
        self.draw_stone(x, y, player)
        self.total_stones += 1
        self.update_moves_label()

    def update_moves_label(self):
        self.moves_label.config(text=f"Total Turns: {self.total_turns} | Total Stones: {self.total_stones}")

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
            self.end_game("Human wins!")
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
        self.time_label.config(text=f"AI Time: {end-start:.3f}s")

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
                self.end_game("AI wins!")
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
                for dx, dy in DIRS:
                    count = 1
                    coords = [(x, y)]
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < self.size and 0 <= ny < self.size and grid[nx][ny] == player:
                        coords.append((nx, ny))
                        count += 1
                        nx += dx; ny += dy
                    nx, ny = x - dx, y - dy
                    while 0 <= nx < self.size and 0 <= ny < self.size and grid[nx][ny] == player:
                        coords.insert(0, (nx, ny))
                        count += 1
                        nx -= dx; ny -= dy
                    if count >= 6:
                        self.highlight_win_line(coords[:6])
                        return True
        return False

    def highlight_win_line(self, stones):
        for (x, y) in stones:
            px = x*self.cell + self.cell//2
            py = y*self.cell + self.cell//2
            self.canvas.create_rectangle(px-14, py-14, px+14, py+14, outline="red", width=3)

    # ---------- end & restart ----------
    def end_game(self, message):
        self.game_over = True
        avg = sum(self.ai_times)/len(self.ai_times) if self.ai_times else 0.0
        print(f"\n{message}")
        print(f"Average AI response time: {avg:.3f} seconds")
        self.time_label.config(text=f"{message} | Avg AI Time: {avg:.3f}s")

    def restart_game(self):
        self.board_obj = Board(self.size)
        self.turn = 1
        self.human_needed = 1
        self.human_placed = 0
        self.ai_times = []
        self.game_over = False
        self.last_moves = []
        self.total_turns = 0
        self.total_stones = 0
        self.time_label.config(text="AI Time: 0.000s")
        self.update_moves_label()
        self.draw_grid()
