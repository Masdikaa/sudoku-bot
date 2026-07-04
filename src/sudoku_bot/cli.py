from datetime import datetime
from pathlib import Path
from time import perf_counter

from sudoku_bot.device.adb_client import capture_screenshot
from sudoku_bot.paths import SCREENSHOTS_DIR
from sudoku_bot.sudoku.solver import solve_board, validate_board
from sudoku_bot.vision.board_detector import extract_board
from sudoku_bot.vision.cell_extractor import save_debug_cells
from sudoku_bot.vision.ocr_recognizer import recognize_board, save_debug_ocr_cells


def capture_game_screenshot() -> Path:
    game_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = SCREENSHOTS_DIR / f"game_{game_id}.png"
    screenshot.parent.mkdir(parents=True, exist_ok=True)
    print("[1/7] Capturing screenshot from Android device...")
    screenshot.write_bytes(capture_screenshot())
    print(f"[1/7] Screenshot saved to {screenshot}")
    return screenshot


def format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.2f}s"

    total_seconds = round(seconds)
    minutes, remaining_seconds = divmod(total_seconds, 60)
    return f"{minutes}.{remaining_seconds:02d}m"


def main() -> None:
    started_at = perf_counter()
    screenshot = capture_game_screenshot()

    print("[2/7] Extracting Sudoku board from screenshot...")
    board = extract_board(str(screenshot))

    print("[3/7] Saving debug cell images...")
    save_debug_cells(board)

    print("[4/7] Saving OCR debug images...")
    save_debug_ocr_cells(board)

    print("[5/7] Recognizing board numbers with OCR...")
    numbers = recognize_board(board)

    print("[6/7] Validating detected board...")
    validate_board(numbers)

    print("[7/7] Solving Sudoku board...")
    solved = solve_board(numbers)
    duration = perf_counter() - started_at

    print("Validation passed. Board has at least one solution.")
    print()

    print(f"Detected board from {screenshot}:")
    for row in numbers:
        print(row)

    print()
    print("Solved board:")
    for row in solved:
        print(row)

    print()
    print(f"Solved in {format_duration(duration)}")
