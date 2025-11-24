from Connect6Game import Connect6Game
from Connect6GUI import Connect6GUI
import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    gui = Connect6GUI(root)
    root.mainloop()
    # game = Connect6Game()
    # game.play()