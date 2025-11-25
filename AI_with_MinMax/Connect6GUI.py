import tkinter as tk
from tkinter import messagebox
from Board import Board
from MInimaxAI import MinimaxAI  # Your AI module

CELL_SIZE = 30
BOARD_SIZE = 19
STONE_COLORS = {1: "black", -1: "white"}
STONE_RADIUS = 12  # radius of stone on intersections

class Connect6GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect-6 19x19 (Intersections)")

        # Game state
        self.board = Board(BOARD_SIZE)
        self.ai = MinimaxAI()
        self.current_player = 1  # 1=Human (black), -1=AI (white)
        self.move_count = 0
        self.pending_moves = []

        # Canvas
        canvas_size = CELL_SIZE * (BOARD_SIZE - 1) + 2*STONE_RADIUS
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="beige")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        # Status and control
        self.status_label = tk.Label(root, text="Your turn! Place 1 stone.", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.move_label = tk.Label(root, text="Total moves: 0", font=("Arial", 12))
        self.move_label.pack(pady=5)

        self.restart_button = tk.Button(root, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=5)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        # Draw grid lines
        for i in range(BOARD_SIZE):
            x = i * CELL_SIZE + STONE_RADIUS
            self.canvas.create_line(x, STONE_RADIUS, x, CELL_SIZE*(BOARD_SIZE-1)+STONE_RADIUS)
        for j in range(BOARD_SIZE):
            y = j * CELL_SIZE + STONE_RADIUS
            self.canvas.create_line(STONE_RADIUS, y, CELL_SIZE*(BOARD_SIZE-1)+STONE_RADIUS, y)
        # Draw stones on intersections
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                stone = self.board.grid[i][j]
                if stone != 0:
                    cx = i * CELL_SIZE + STONE_RADIUS
                    cy = j * CELL_SIZE + STONE_RADIUS
                    self.canvas.create_oval(
                        cx - STONE_RADIUS, cy - STONE_RADIUS,
                        cx + STONE_RADIUS, cy + STONE_RADIUS,
                        fill=STONE_COLORS[stone]
                    )

    def on_click(self, event):
        # Convert click to nearest intersection
        x = round((event.x - STONE_RADIUS) / CELL_SIZE)
        y = round((event.y - STONE_RADIUS) / CELL_SIZE)
        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
            return
        if not self.board.is_empty(x, y):
            return

        # Determine number of stones allowed for human
        human_stones = 1 if self.current_player == 1 and self.move_count == 0 else 2

        # Prevent placing more than allowed stones
        if len(self.pending_moves) >= human_stones:
            return

        # Place human stone
        self.pending_moves.append((x, y))
        self.board.place_stone(x, y, self.current_player)
        self.draw_board()

        # If human hasn't placed all stones yet, wait
        if len(self.pending_moves) < human_stones:
            self.status_label.config(text=f"Place stone {len(self.pending_moves)+1}/{human_stones}")
            return

        # Check human win
        if self.ai.evaluator.check_win(self.board, self.current_player):
            self.highlight_win(self.current_player)
            messagebox.showinfo("Game Over", "You Win!")
            return

        # Reset pending moves before AI turn
        self.pending_moves = []

        # Switch to AI
        self.current_player = -1
        self.status_label.config(text="AI is thinking...")
        self.root.update_idletasks()

        # AI always places 2 stones
        ai_stones = 2
        ai_moves = self.ai.find_best_move(self.board, self.current_player, ai_stones)
        for mx, my in ai_moves:
            self.board.place_stone(mx, my, self.current_player)
        self.draw_board()

        # Check AI win
        if self.ai.evaluator.check_win(self.board, self.current_player):
            self.highlight_win(self.current_player)
            messagebox.showinfo("Game Over", "AI Wins!")
            return

        # Switch back to human
        self.current_player = 1
        self.move_count += 1
        self.update_move_label()
        self.status_label.config(text=f"Your turn! Place {2 if self.move_count > 0 else 1} stone(s).")

    def highlight_win(self, player):
        """Highlights winning line (horizontal/vertical/diagonal)"""
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board.grid[x][y] != player:
                    continue
                for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:
                    win_cells = []
                    cx, cy = x, y
                    while 0 <= cx < BOARD_SIZE and 0 <= cy < BOARD_SIZE and self.board.grid[cx][cy] == player:
                        win_cells.append((cx, cy))
                        cx += dx
                        cy += dy
                    if len(win_cells) >= 6:
                        for wx, wy in win_cells:
                            center_x = wx * CELL_SIZE + STONE_RADIUS
                            center_y = wy * CELL_SIZE + STONE_RADIUS
                            self.canvas.create_oval(
                                center_x - STONE_RADIUS, center_y - STONE_RADIUS,
                                center_x + STONE_RADIUS, center_y + STONE_RADIUS,
                                outline="red", width=3
                            )
                        return

    def restart_game(self):
        """Reset the board and all state"""
        self.board = Board(BOARD_SIZE)
        self.current_player = 1
        self.move_count = 0
        self.pending_moves = []
        self.draw_board()
        self.status_label.config(text="Your turn! Place 1 stone.")
        self.update_move_label()

    def update_move_label(self):
        self.move_label.config(text=f"Total moves: {self.move_count}")
