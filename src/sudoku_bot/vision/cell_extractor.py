from pathlib import Path

import cv2

from sudoku_bot.paths import DEBUG_CELLS_DIR


def extract_cells(board_image):
    height, width = board_image.shape[:2]
    cell_height = height // 9
    cell_width = width // 9

    return [
        [
            board_image[
                row * cell_height:(row + 1) * cell_height,
                col * cell_width:(col + 1) * cell_width,
            ]
            for col in range(9)
        ]
        for row in range(9)
    ]


def cell_has_number(cell) -> bool:
    height, width = cell.shape[:2]
    inner = cell[height // 5:height * 4 // 5, width // 5:width * 4 // 5]
    gray = cv2.cvtColor(inner, cv2.COLOR_BGR2GRAY)
    return int((gray < 100).sum()) > 35


def detect_occupied_cells(board_image) -> list[list[int]]:
    return [
        [1 if cell_has_number(cell) else 0 for cell in row]
        for row in extract_cells(board_image)
    ]


def save_debug_cells(board_image, output_dir: Path = DEBUG_CELLS_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for row_index, row in enumerate(extract_cells(board_image), start=1):
        for col_index, cell in enumerate(row, start=1):
            cv2.imwrite(str(output_dir / f"r{row_index}_c{col_index}.png"), cell)
