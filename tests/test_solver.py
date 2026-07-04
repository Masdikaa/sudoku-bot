from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sudoku.solver import solve_board, validate_board


BOARD = [
    [5, 9, 0, 8, 0, 4, 6, 0, 7],
    [6, 0, 0, 0, 1, 0, 8, 0, 9],
    [7, 8, 2, 6, 9, 5, 0, 0, 0],
    [0, 0, 9, 7, 0, 0, 2, 8, 5],
    [0, 0, 0, 0, 8, 3, 9, 0, 0],
    [4, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 3, 5, 0, 6, 2, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 6],
    [1, 0, 6, 9, 0, 8, 4, 0, 0],
]


def _assert_solved(board):
    expected = set(range(1, 10))
    assert all(set(row) == expected for row in board)
    assert all({board[row][col] for row in range(9)} == expected for col in range(9))
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            assert {
                board[row][col]
                for row in range(box_row, box_row + 3)
                for col in range(box_col, box_col + 3)
            } == expected


validate_board(BOARD)
_assert_solved(solve_board(BOARD))

invalid = [row[:] for row in BOARD]
invalid[0][2] = 5
try:
    validate_board(invalid)
    raise AssertionError("invalid board passed validation")
except ValueError:
    pass

print("solver self-check passed")
