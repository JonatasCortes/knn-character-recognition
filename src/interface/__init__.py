from ._classify_menu import classify_menu_setup
from ._main_menu import main_menu_setup
from desklab import Window

Window.setup(width=1000, height=700, caption="knn-character-recognition")
CLASSIFY_MENU = classify_menu_setup()
MAIN_MENU = main_menu_setup(CLASSIFY_MENU)

__all__ = [
    "MAIN_MENU"
]
