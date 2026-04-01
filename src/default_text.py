from src.rgb_color import RgbColor


class DefaultText:

    def __init__(self, text: str, x: int, y: int, size: int = 50, color: RgbColor = RgbColor(255, 255, 255)):

        self.__text = text
        self.set_y(y)
        self.set_x(x)
        self.__size = size
        self.__color = color

    def set_color(self, color: RgbColor):
        self.__color = color

    def get_color(self) -> RgbColor:
        return self.__color

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

    def get_text(self) -> str:
        return self.__text

    def get_size(self) -> int:
        return self.__size
