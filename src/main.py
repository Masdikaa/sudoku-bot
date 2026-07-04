from datetime import datetime
from pathlib import Path

from device.adb_client import capture_screenshot
from vision.board_detector import extract_board
from vision.cell_extractor import detect_occupied_cells


def capture_game_screenshot() -> Path:
    game_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = Path(f"tests/test_inputs/game_{game_id}.png")
    screenshot.write_bytes(capture_screenshot())
    return screenshot


def main() -> None:
    screenshot = capture_game_screenshot()
    board = extract_board(str(screenshot))
    occupied_cells = detect_occupied_cells(board)

    print(f"Detected occupied cells from {screenshot}:")
    for row in occupied_cells:
        print(row)


if __name__ == "__main__":
    main()
