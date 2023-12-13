"""
ISTA450 Final Project
Tyler Kimball
Fall 2023
Sudoku CSP with backtracking and forward checking
"""
import time

class SudokuSolver:
    def __init__(self, board, algorithm='backtracking'):
        self.board = board
        self.size = len(board)
        self.square_size = int(self.size**0.5)
        self.algorithm = algorithm

    def is_safe(self, row, col, num):
        if num not in self.board[row] and num not in [self.board[i][col] for i in range(self.size)]:
            start_row = self.square_size * (row // self.square_size)
            start_col = self.square_size * (col // self.square_size)
            for i in range(self.square_size):
                for j in range(self.square_size):
                    if self.board[start_row + i][start_col + j] == num:
                        return False
            return True
        return False

    def forward_check(self, row, col, num):
        for i in range(self.size):
            if i != col and num in self.board[row]:
                return False
            if i != row and num in [self.board[i][col] for i in range(self.size)]:
                return False
            
        start_row = self.square_size * (row // self.square_size)
        start_col = self.square_size * (col // self.square_size)
        for i in range(self.square_size):
            for j in range(self.square_size):
                if (start_row + i != row or start_col + j != col) and self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True 
        
        row, col = empty_cell
        for num in range(1, self.size + 1):
            if self.is_safe(row, col, num):
                self.board[row][col] = num

                if self.algorithm == 'forwardchecking' and not self.forward_check(row, col, num):
                    continue
                if self.solve_sudoku():
                    return True
            
                # Backtrack
                self.board[row][col] = 0
        return False

    def find_empty_cell(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j
        return None

def measure_time(problem):
    start_time = time.time()
    problem.solve_sudoku()
    end_time = time.time()
    return end_time - start_time

def main():
    board = input("Please type 1 or 2 to select board: \n")
    if board == '2':
        sudoku_board = [
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [2, 0, 0, 8, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 0, 0],
            [0, 0, 3, 0, 0, 9, 0, 0, 0],
            [0, 6, 0, 7, 0, 0, 0, 9, 0],
            [7, 0, 0, 0, 6, 0, 0, 0, 2],
            [0, 0, 4, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0, 0, 6],
            [0, 9, 0, 0, 0, 0, 2, 0, 0],
        ]
    else:
        sudoku_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]

    backtracking = SudokuSolver(sudoku_board, algorithm='backtracking')
    forwardchecking = SudokuSolver(sudoku_board, algorithm='forwardchecking')

    backtracking_time = measure_time(backtracking)
    forwardchecking_time = measure_time(forwardchecking)

    print("Backtracking - Solved Sudoku:\n")
    for row in backtracking.board:
        print(row)

    print("Backtracking:")
    print(f"Time: {backtracking_time:.6f} seconds")
    print("\n--------------------------------\n")

    print("Forward Checking - Solved Sudoku:\n")
    for row in forwardchecking.board:
        print(row)

    print("Forward Checking:")
    print(f"Time: {forwardchecking_time:.6f} seconds")
    print("\n--------------------------------\n")

    if backtracking_time < forwardchecking_time:
        print("Backtracking is faster")
    elif backtracking_time > forwardchecking_time:
        print("Forward Checking is faster")
    else:
        print("Both algorithms have similar performance")

if __name__ == "__main__":
    main()