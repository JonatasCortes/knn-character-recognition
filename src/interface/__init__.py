from ._constants import SETUP
from ._classify_menu import classify_menu_setup
from ._main_menu import main_menu_setup
from ._metrics_menu import metrics_menu_setup

assert SETUP
CLASSIFY_MENU = classify_menu_setup()
METRICS_MENU = metrics_menu_setup()
MAIN_MENU = main_menu_setup(CLASSIFY_MENU, METRICS_MENU)
__all__ = [
    "MAIN_MENU"
]
