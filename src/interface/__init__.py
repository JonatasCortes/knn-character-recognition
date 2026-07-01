from ._main_menu import main_menu_setup
from desklab import Window

Window.setup(width=1000, height=700, caption="knn-character-recognition")
MAIN_MENU = main_menu_setup()

__all__ = [
    "MAIN_MENU"
]
