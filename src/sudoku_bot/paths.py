from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
DEBUG_DIR = DATA_DIR / "debug"
DEBUG_CELLS_DIR = DEBUG_DIR / "cells"
DEBUG_OCR_DIR = DEBUG_DIR / "ocr"
