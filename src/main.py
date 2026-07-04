from datetime import datetime
from pathlib import Path

from device.adb_client import capture_screenshot
from sudoku.solver import solve_board, validate_board
from vision.board_detector import extract_board
from vision.cell_extractor import save_debug_cells
from vision.ocr_recognizer import recognize_board, save_debug_ocr_cells


def capture_game_screenshot() -> Path:
    game_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = Path(f"tests/test_inputs/game_{game_id}.png")
    print("[1/7] Capturing screenshot from Android device...")
    screenshot.write_bytes(capture_screenshot())
    print(f"[1/7] Screenshot saved to {screenshot}")
    return screenshot


def main() -> None:
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

    print("Validation passed. Board has at least one solution.")
    print(f"Detected board from {screenshot}:")
    for row in numbers:
        print(row)

    print("Solved board:")
    for row in solved:
        print(row)


if __name__ == "__main__":
    main()
