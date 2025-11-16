import tkinter as tk
from time import sleep
from .sudoku_solver import SudokuSolver
from .sudoku_generator import SudokuGenerator


class SudokuGUI:
    """Final stable Sudoku GUI with proper 3×3 borders and live animation"""
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver (MRV + Forward Checking)")

        self.mode = tk.StringVar(value="manual")
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.board = [[0 for _ in range(9)] for _ in range(9)]

        # ساخت رابط اصلی
        self._build_controls()
        self._build_main_grid()

    # ======================================================
    # کنترل‌های بالایی
    # ======================================================
    def _build_controls(self):
        frame = tk.Frame(self.master)
        frame.pack(side="top", pady=10)

        tk.Radiobutton(frame, text="Manual Input",
                       variable=self.mode, value="manual").grid(row=0, column=0, padx=5)
        tk.Radiobutton(frame, text="Random Puzzle",
                       variable=self.mode, value="random").grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Generate / Start",
                  command=self._initialize_board,
                  bg="#2666CF", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=10)

        tk.Button(frame, text="Solve",
                  command=self._start_solve,
                  bg="#003366", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=3, padx=10)

    # ======================================================
    # شبکه ۹×۹ با فریم‌بندی دقیق بلوک‌های ۳×۳
    # ======================================================
    def _build_main_grid(self):
        """Each 3x3 block enclosed in a thick black frame."""
        outer = tk.Frame(self.master, bg="black")
        outer.pack(side="top", padx=10, pady=10)

        for br in range(3):
            for bc in range(3):
                block = tk.Frame(outer, bg="black", bd=2, relief="solid")
                block.grid(row=br, column=bc, padx=2, pady=2)
                # سلول‌های داخل بلوک
                for i in range(3):
                    for j in range(3):
                        r = br * 3 + i
                        c = bc * 3 + j
                        e = tk.Entry(block, width=3, justify="center",
                                     font=("Arial", 16), bd=1, relief="solid")
                        e.grid(row=i, column=j, padx=1, pady=1)
                        self.cells[r][c] = e

    # ======================================================
    # مقداردهی اولیه (ورودی یا تصادفی)
    # ======================================================
    def _initialize_board(self):
        mode = self.mode.get()
        if mode == "random":
            generator = SudokuGenerator("medium")
            self.board = generator.generate_puzzle()
            self._update_display(editable=False)
        else:
            self.board = [[0 for _ in range(9)] for _ in range(9)]
            self._update_display(editable=True)

    def _update_display(self, editable=True):
        """بازتاب ماتریس board در سلول‌های GUI"""
        for r in range(9):
            for c in range(9):
                cell = self.cells[r][c]
                val = self.board[r][c]
                cell.config(state="normal")
                cell.delete(0, tk.END)
                if val != 0:
                    cell.insert(0, str(val))
                    if not editable:
                        cell.config(state="disabled", disabledforeground="black")
                elif not editable:
                    cell.config(state="disabled")

    # ======================================================
    # حل سودوکو با انیمیشن زنده
    # ======================================================
    def _start_solve(self):
        """خواندن ورودی GUI، اجرای solver، و نمایش انیمیشن"""
        # خواندن اعداد موجود
        for r in range(9):
            for c in range(9):
                v = self.cells[r][c].get()
                self.board[r][c] = int(v) if v.isdigit() else 0

        solver = SudokuSolver(self.board)
        solved = solver.solve(step_callback=self._animate_step)
        if solved:
            print("✅ Sudoku solved successfully!")
        else:
            print("❌ No solution found.")

    def _animate_step(self, r, c, val, is_backtrack):
        """به‌روزرسانی زنده برای هر گام از الگوریتم"""
        cell = self.cells[r][c]
        cell.config(state="normal")
        cell.delete(0, tk.END)

        if not is_backtrack:
            cell.insert(0, str(val))
            cell.config(fg="blue")
        else:
            cell.config(fg="red")

        self.master.update_idletasks()  # فورس رفرش GUI
        sleep(0.05)
