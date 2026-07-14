from typing import Final
from desklab import Window, Color, Font

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_CAPTION = "knn-character-recognition"

Window.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, caption=WINDOW_CAPTION)

BASE_COLOR: Final[Color] = Color((51, 36, 43))
DEFAULT_FONT: Final[Font] = Font("consolas", 40)
HEADER_HEIGHT: Final[int] = 100

SETUP = True
