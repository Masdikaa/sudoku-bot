import cv2


def extract_board(image_path: str, size: int = 450):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot read image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    board_rect = None
    min_area = image.shape[0] * image.shape[1] * 0.10
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        area = width * height
        ratio = width / height
        if area > min_area and 0.85 <= ratio <= 1.15:
            if board_rect is None or area > board_rect[2] * board_rect[3]:
                board_rect = (x, y, width, height)

    if board_rect is None:
        # ponytail: tuned for the current app screenshot; replace with perspective detection when themes vary.
        height, width = image.shape[:2]
        x, y, side = 10, int(height * 0.24), width - 20
        board = image[y:y + side, x:x + side]
    else:
        x, y, width, height = board_rect
        side = min(width, height)
        board = image[y:y + side, x:x + side]

    return cv2.resize(board, (size, size), interpolation=cv2.INTER_AREA)
