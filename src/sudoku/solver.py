def validate_board(board: list[list[int]]) -> None:
    _validate_shape(board)
    _validate_units(board)
    if not _solve([row[:] for row in board]):
        raise ValueError("Board has no solution")


def solve_board(board: list[list[int]]) -> list[list[int]]:
    validate_board(board)
    solved = [row[:] for row in board]
    if not _solve(solved):
        raise ValueError("Board has no solution")
    return solved


def _validate_shape(board: list[list[int]]) -> None:
    if len(board) != 9 or any(len(row) != 9 for row in board):
        raise ValueError("Board must be 9x9")
    if any(not isinstance(number, int) or number < 0 or number > 9 for row in board for number in row):
        raise ValueError("Board values must be integers between 0 and 9")


def _validate_units(board: list[list[int]]) -> None:
    for index, row in enumerate(board, start=1):
        _validate_no_duplicates(row, f"row {index}")

    for col in range(9):
        _validate_no_duplicates([board[row][col] for row in range(9)], f"column {col + 1}")

    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            values = [
                board[row][col]
                for row in range(box_row, box_row + 3)
                for col in range(box_col, box_col + 3)
            ]
            _validate_no_duplicates(values, f"box {box_row // 3 + 1},{box_col // 3 + 1}")


def _validate_no_duplicates(values: list[int], label: str) -> None:
    filled = [value for value in values if value != 0]
    if len(filled) != len(set(filled)):
        raise ValueError(f"Duplicate number in {label}")


def _solve(board: list[list[int]]) -> bool:
    empty = _find_best_empty_cell(board)
    if empty is None:
        return True

    row, col, candidates = empty
    if not candidates:
        return False

    for number in candidates:
        board[row][col] = number
        if _solve(board):
            return True
        board[row][col] = 0

    return False


def _find_best_empty_cell(board: list[list[int]]) -> tuple[int, int, list[int]] | None:
    best = None
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                candidates = _candidates_for(board, row, col)
                if best is None or len(candidates) < len(best[2]):
                    best = (row, col, candidates)
                if not candidates:
                    return best
    return best


def _candidates_for(board: list[list[int]], row: int, col: int) -> list[int]:
    used = set(board[row])
    used.update(board[r][col] for r in range(9))

    box_row = row // 3 * 3
    box_col = col // 3 * 3
    used.update(
        board[r][c]
        for r in range(box_row, box_row + 3)
        for c in range(box_col, box_col + 3)
    )
    return [number for number in range(1, 10) if number not in used]
