from collections import Counter
from pathlib import Path

import cv2
import pytesseract

from sudoku_bot.paths import DEBUG_OCR_DIR
from sudoku_bot.vision.cell_extractor import cell_has_number, extract_cells

OCR_CONFIGS = [
    "--psm 13 --oem 3 -c tessedit_char_whitelist=123456789",
    "--psm 8 --oem 3 -c tessedit_char_whitelist=123456789",
    "--psm 10 --oem 3 -c tessedit_char_whitelist=123456789",
]

DEFAULT_TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if DEFAULT_TESSERACT.exists():
    pytesseract.pytesseract.tesseract_cmd = str(DEFAULT_TESSERACT)


def preprocess_cell_for_ocr(cell):
    images = _preprocess_variants(cell)
    return images[0] if images else None


def _preprocess_variants(cell):
    height, width = cell.shape[:2]
    inner = cell[height // 10:height * 9 // 10, width // 10:width * 9 // 10]
    gray = cv2.cvtColor(inner, cv2.COLOR_BGR2GRAY)
    images = []
    for threshold in (130, 150, 170):
        _, digit_mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
        points = cv2.findNonZero(digit_mask)
        if points is None:
            continue

        x, y, digit_width, digit_height = cv2.boundingRect(points)
        if digit_width < 5 or digit_height < 10:
            continue

        digit = digit_mask[y:y + digit_height, x:x + digit_width]
        canvas = cv2.copyMakeBorder(digit, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=0)
        resized = cv2.resize(cv2.bitwise_not(canvas), (200, 200), interpolation=cv2.INTER_CUBIC)
        images.append(resized)
    return images


def recognize_digit(cell) -> int:
    if not cell_has_number(cell):
        return 0

    images = _preprocess_variants(cell)
    if not images:
        return 0

    votes = []
    for image in images:
        for config in OCR_CONFIGS:
            text = pytesseract.image_to_string(image, config=config).strip()
            votes.extend(char for char in text if char.isdigit())
    if not votes:
        return 0

    digit = int(Counter(votes).most_common(1)[0][0])
    if digit == 3 and _digit_hole_count(cell) > 0:
        return 9
    return digit


def recognize_board(board_image) -> list[list[int]]:
    board = [[recognize_digit(cell) for cell in row] for row in extract_cells(board_image)]
    validate_board(board)
    return board


def _digit_hole_count(cell) -> int:
    height, width = cell.shape[:2]
    inner = cell[height // 10:height * 9 // 10, width // 10:width * 9 // 10]
    gray = cv2.cvtColor(inner, cv2.COLOR_BGR2GRAY)
    _, digit_mask = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    points = cv2.findNonZero(digit_mask)
    if points is None:
        return 0

    x, y, digit_width, digit_height = cv2.boundingRect(points)
    digit = digit_mask[y:y + digit_height, x:x + digit_width]
    _, hierarchy = cv2.findContours(digit, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy is None:
        return 0

    return sum(1 for item in hierarchy[0] if item[3] != -1)


def save_debug_ocr_cells(board_image, output_dir: Path = DEBUG_OCR_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for row_index, row in enumerate(extract_cells(board_image), start=1):
        for col_index, cell in enumerate(row, start=1):
            image = preprocess_cell_for_ocr(cell)
            if image is not None:
                cv2.imwrite(str(output_dir / f"r{row_index}_c{col_index}.png"), image)


def validate_board(board: list[list[int]]) -> None:
    if len(board) != 9 or any(len(row) != 9 for row in board):
        raise ValueError("Board must be 9x9")
    if any(number < 0 or number > 9 for row in board for number in row):
        raise ValueError("Board values must be between 0 and 9")
