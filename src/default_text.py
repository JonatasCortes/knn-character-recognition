from src.rgb_color import RgbColor
from src.default_entity import DefaultEntity


class DefaultText(DefaultEntity):

    def __init__(self, text: str, x: int, y: int, size: int = 50, color: RgbColor = RgbColor(255, 255, 255)):

        self.__text = text
        self.set_size(size)
        super().__init__(x, y, color)

    def get_text(self) -> str:
        return self.__text

    def get_size(self) -> int:
        return self.__size

    def set_size(self, size: int) -> None:
        if size < 0:
            error = f"ERROR: size {size} is invalid."
            raise ValueError(error)
        self.__size = size
