from src.rgb_color import RgbColor
from abc import ABC


class DefaultEntity(ABC):

    def __init__(self, x: int, y: int, color: RgbColor) -> None:
        self.set_y(y)
        self.set_x(x)
        self.__color = color

    def __set_pos(self, pos: int):
        return pos if pos >= 0 else 0

    def set_x(self, x: int):
        self.__x = self.__set_pos(x)

    def get_x(self) -> int:
        return self.__x

    def set_y(self, y: int):
        self.__y = self.__set_pos(y)

    def get_y(self) -> int:
        return self.__y

    def set_color(self, color: RgbColor):
        self.__color = color

    def get_color(self) -> RgbColor:
        return self.__color
