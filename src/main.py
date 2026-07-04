from datetime import datetime
from pathlib import Path

from device.adb_client import capture_screenshot

def main() -> None:
    game_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = Path(f"tests/test_inputs/game_{game_id}.png")
    output.write_bytes(capture_screenshot())
    print(f"Saved screenshot {game_id} to {output}")

if __name__ == "__main__":
    main()
