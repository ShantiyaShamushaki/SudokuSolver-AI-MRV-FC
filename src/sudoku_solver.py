import copy

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.domains = self._init_domains()

    def _init_domains(self):
        """Initialize possible values (domain) for each cell."""
        domains = {}
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    domains[(r, c)] = self._get_possible_values(r, c)
        return domains

    def _get_possible_values(self, row, col):
        """Return a set of valid values for a given empty cell."""
        used = set()

        # Row + Column
        used.update(self.board[row])
        used.update(self.board[i][col] for i in range(9))

        # Box
        box_x, box_y = (col // 3) * 3, (row // 3) * 3
        for i in range(box_y, box_y + 3):
            for j in range(box_x, box_x + 3):
                used.add(self.board[i][j])

        return {n for n in range(1, 10) if n not in used}

    def _select_unassigned_variable(self):
        """Select the unfilled cell with the smallest domain (MRV heuristic)."""
        if not self.domains:
            return None
        return min(self.domains, key=lambda cell: len(self.domains[cell]))

    def _forward_check(self, row, col, val, domains):
        """Propagate constraints after assigning a value."""
        for i in range(9):
            # Row
            if (row, i) in domains and val in domains[(row, i)]:
                domains[(row, i)] = domains[(row, i)] - {val}
                if not domains[(row, i)]:
                    return False
            # Column
            if (i, col) in domains and val in domains[(i, col)]:
                domains[(i, col)] = domains[(i, col)] - {val}
                if not domains[(i, col)]:
                    return False

        # Box
        box_x, box_y = (col // 3) * 3, (row // 3) * 3
        for i in range(box_y, box_y + 3):
            for j in range(box_x, box_x + 3):
                if (i, j) in domains and val in domains[(i, j)]:
                    domains[(i, j)] = domains[(i, j)] - {val}
                    if not domains[(i, j)]:
                        return False
        return True
    
    def _find_mrv_cell(self):
        """Selects the cell with the minimum domain size (MRV heuristic)."""
        board = self.board
        min_domain = 10
        best = None
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    values = self._get_possible_values(i, j)
                    if len(values) < min_domain:
                        min_domain = len(values)
                        best = (i, j)
                        if min_domain == 1:
                            return best
        return best

    def solve(self, step_callback=None):
        if not self.domains:
            return True

        cell = self._find_mrv_cell()
        if not cell:
            return True

        row, col = cell
        for val in sorted(self.domains[cell]):
            if val in self._get_possible_values(row, col):
                self.board[row][col] = val

                # گزارش پیشرفت
                if step_callback:
                    step_callback(row, col, val, is_backtrack=False)

                new_domains = copy.deepcopy(self.domains)
                del new_domains[cell]
                if self._forward_check(row, col, val, new_domains):
                    sub_solver = SudokuSolver(copy.deepcopy(self.board))
                    sub_solver.domains = new_domains
                    if sub_solver.solve(step_callback=step_callback):
                        self.board = sub_solver.board
                        return True

                # Backtrack
                self.board[row][col] = 0
                if step_callback:
                    step_callback(row, col, val, is_backtrack=True)
        return False
    
    def print_board(self):
        board = self.board
        for i in range(len(board)):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(len(board[0])):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                if j == 8:
                    print(board[i][j])
                else:
                    print(str(board[i][j]) + " ", end="")