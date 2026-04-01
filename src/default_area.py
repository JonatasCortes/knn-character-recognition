from src.rgb_color import RgbColor
from src.default_entity import DefaultEntity


class DefaultArea(DefaultEntity):
    def __init__(self, x: int, y: int, width: int, height: int, color: RgbColor = RgbColor(255, 255, 255)):
        self.__set_width(width)
        self.__set_height(height)
        super().__init__(x, y, color)

    def __validate_dimension(self, dim: int):
        if dim < 0:
            error = "ERROR: dimension value can't be lower than 0."
            raise ValueError(error)

    def __set_width(self, width: int):
        self.__validate_dimension(width)
        self.__width = width

    def __set_height(self, height: int):
        self.__validate_dimension(height)
        self.__height = height

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height
