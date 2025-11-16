import tkinter as tk
from src.gui import SudokuGUI

def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()