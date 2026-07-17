from dataclasses import dataclass
from typing import Final
from src.interface._constants import WINDOW_HEIGHT, WINDOW_WIDTH, HEADER_HEIGHT


BODY_COLOR_LIGHTEN: Final[int] = 20
STATS_SAFETY_MARGIN: Final[int] = 12

STATS_PANEL_WIDTH_RATIO: Final[float] = 1.05
STATS_PANEL_HEIGHT_RATIO: Final[float] = 1.05
STATS_PANEL_PADDING: Final[int] = 30
STATS_PANEL_SPACE_BETWEEN: Final[int] = 40
STATS_PANEL_CORNERS_RADIUS: Final[int] = 40

PANEL_TITLE_TEXT: Final[str] = "MODEL PERFORMANCE"
PANEL_TITLE_FONT_SIZE: Final[int] = 35

STATS_GRID_COLUMNS: Final[int] = 3
STAT_ROW_SPACE_BETWEEN: Final[int] = 20
STAT_CARD_SPACE_BETWEEN: Final[int] = 24
STAT_CARD_HEIGHT: Final[int] = 150
STAT_CARD_PADDING: Final[int] = 18
STAT_CARD_INNER_SPACE_BETWEEN: Final[int] = 10
STAT_CARD_CORNERS_RADIUS: Final[int] = 30
STAT_CARD_COLOR_LIGHTEN: Final[int] = 100
STAT_CARD_BRIGHTNESS_TOGGLE_INTENSITY: Final[int] = 30

STATS_GRID_HEIGHT: Final[int] = 2 * STAT_CARD_HEIGHT + STAT_ROW_SPACE_BETWEEN

STAT_LABEL_FONT_SIZE: Final[int] = 19
STAT_VALUE_FONT_SIZE: Final[int] = 40
STAT_TEXT_COLOR: Final[tuple[int, int, int]] = (255, 255, 255)

DEFAULT_METRIC_VALUE: Final[str] = "N/A"

ACCENT_GREEN: Final[tuple[int, int, int]] = (120, 208, 98)
ACCENT_BLUE: Final[tuple[int, int, int]] = (33, 158, 188)
ACCENT_ORANGE: Final[tuple[int, int, int]] = (255, 147, 23)
ACCENT_PURPLE: Final[tuple[int, int, int]] = (172, 96, 172)
ACCENT_TEAL: Final[tuple[int, int, int]] = (142, 202, 230)
ACCENT_TERRACOTTA: Final[tuple[int, int, int]] = (224, 122, 95)

TRAINING_ACCURACY_LABEL: Final[str] = "TRAINING ACCURACY"
USER_ACCURACY_LABEL: Final[str] = "USER ACCURACY"
TRAINING_IMAGES_LABEL: Final[str] = "TRAINING IMAGES"
MANUAL_CHECKS_LABEL: Final[str] = "MANUAL CHECKS"
K_VALUE_LABEL: Final[str] = "K VALUE"
RECOGNIZED_CHARACTERS_LABEL: Final[str] = "RECOGNIZED CHARACTERS"

TRAINING_ACCURACY_DESCRIPTION: Final[tuple[str, str]] = (
    "Accuracy the model achieved",
    "on the training dataset.",
)
USER_ACCURACY_DESCRIPTION: Final[tuple[str, str]] = (
    "Accuracy calculated from",
    "your manual verifications.",
)
TRAINING_IMAGES_DESCRIPTION: Final[tuple[str, str]] = (
    "Total number of images",
    "used to train the model.",
)
MANUAL_CHECKS_DESCRIPTION: Final[tuple[str, str]] = (
    "Number of classifications",
    "you have manually verified.",
)
K_VALUE_DESCRIPTION: Final[tuple[str, str]] = (
    "Number of nearest neighbors",
    "used by the KNN algorithm.",
)
RECOGNIZED_CHARACTERS_DESCRIPTION: Final[tuple[str, str]] = (
    "Total distinct character",
    "classes the model can detect.",
)

RETURN_BUTTON_TEXT: Final[str] = "RETURN"
RETURN_BUTTON_COLOR: Final[tuple[int, int, int]] = (227, 8, 66)
RETURN_BUTTON_WIDTH_RATIO: Final[float] = 3
RETURN_BUTTON_HEIGHT: Final[int] = 70
RETURN_BUTTON_CORNERS_RADIUS: Final[int] = 30
RETURN_BUTTON_FONT_SIZE: Final[int] = 28

MODAL_WIDTH: Final[int] = 560
MODAL_HEIGHT: Final[int] = 260
MODAL_HEADER_HEIGHT: Final[int] = 70
MODAL_BODY_HEIGHT: Final[int] = MODAL_HEIGHT - MODAL_HEADER_HEIGHT
MODAL_BODY_PADDING: Final[int] = 30
MODAL_BODY_SPACE_BETWEEN: Final[int] = 20
MODAL_CONTENT_WIDTH: Final[int] = MODAL_WIDTH - 2 * MODAL_BODY_PADDING

MODAL_OVERLAY_COLOR: Final[tuple[int, int, int, int]] = (0, 0, 0, 150)
MODAL_BACKGROUND_COLOR_LIGHTEN: Final[int] = 70
MODAL_HEADER_SPACE_BETWEEN: Final[int] = 70
MODAL_HEADER_COLOR_LIGHTEN: Final[int] = 20
MODAL_TITLE_FONT_SIZE: Final[int] = 26
MODAL_CONTENT_CONTAINER_COLOR_LIGHTEN: Final[int] = 40
MODAL_DESCRIPTION_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    20, 20, 20, 20)

CLOSE_MODAL_BUTTON_WIDTH: Final[int] = 70
CLOSE_MODAL_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    10, 0, 0, 0)
CLOSE_MODAL_BUTTON_TEXT: Final[str] = "X"

MODAL_DESCRIPTION_LINES: Final[int] = 2
MODAL_DESCRIPTION_FONT_SIZE: Final[int] = 24
MODAL_DESCRIPTION_LINE_HEIGHT: Final[int] = 32
MODAL_DESCRIPTION_LINE_SPACE_BETWEEN: Final[int] = 12
MODAL_DESCRIPTION_CONTAINER_HEIGHT: Final[int] = (
    MODAL_DESCRIPTION_LINES * MODAL_DESCRIPTION_LINE_HEIGHT
    + (MODAL_DESCRIPTION_LINES - 1) * MODAL_DESCRIPTION_LINE_SPACE_BETWEEN
)

BODY_HEIGHT: Final[int] = WINDOW_HEIGHT - HEADER_HEIGHT

STATS_PANEL_WIDTH: Final[int] = int(WINDOW_WIDTH / STATS_PANEL_WIDTH_RATIO)
STATS_PANEL_HEIGHT: Final[int] = int(BODY_HEIGHT / STATS_PANEL_HEIGHT_RATIO)

STATS_GRID_WIDTH: Final[int] = STATS_PANEL_WIDTH - \
    2 * STATS_PANEL_PADDING - STATS_SAFETY_MARGIN
STAT_CARD_WIDTH: Final[int] = (
    (STATS_GRID_WIDTH - (STATS_GRID_COLUMNS - 1) *
     STAT_CARD_SPACE_BETWEEN) // STATS_GRID_COLUMNS
)


@dataclass(frozen=True, slots=True)
class StatCardSpec:
    label: str
    value: str
    accent_color: tuple[int, int, int]
    description: tuple[str, str]
