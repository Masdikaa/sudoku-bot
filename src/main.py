from datetime import datetime
from pathlib import Path

from device.adb_client import capture_screenshot
from vision.board_detector import extract_board
from vision.cell_extractor import save_debug_cells
from vision.ocr_recognizer import recognize_board, save_debug_ocr_cells


def capture_game_screenshot() -> Path:
    game_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = Path(f"tests/test_inputs/game_{game_id}.png")
    screenshot.write_bytes(capture_screenshot())
    return screenshot


def main() -> None:
    screenshot = capture_game_screenshot()
    board = extract_board(str(screenshot))
    save_debug_cells(board)
    save_debug_ocr_cells(board)
    numbers = recognize_board(board)

    print(f"Detected board from {screenshot}:")
    for row in numbers:
        print(row)


if __name__ == "__main__":
    main()
