import random
from .sudoku_solver import SudokuSolver

class SudokuGenerator:
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty

    def _remove_cells(self, board):
        difficulty_levels = {"easy": 40, "medium": 50, "hard": 60}
        cells_to_remove = difficulty_levels.get(self.difficulty, 50)
        attempts = 0

        while attempts < cells_to_remove:
            r = random.randint(0, 8)
            c = random.randint(0, 8)
            if board[r][c] != 0:
                board[r][c] = 0
                attempts += 1
        return board

    def generate_full_solution(self):
        """Generates a fully solved random Sudoku board."""
        board = [[0 for _ in range(9)] for _ in range(9)]
        solver = SudokuSolver(board)

        # Fill diagonal boxes randomly first (speed up convergence)
        for k in range(0, 9, 3):
            nums = random.sample(range(1, 10), 9)
            idx = 0
            for i in range(k, k + 3):
                for j in range(k, k + 3):
                    board[i][j] = nums[idx]
                    idx += 1

        solver.solve()
        return solver.board

    def generate_puzzle(self):
        """Creates a playable Sudoku puzzle (randomized)."""
        full_board = self.generate_full_solution()
        puzzle = self._remove_cells(full_board)
        return puzzle
