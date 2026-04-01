import logging


class RgbColor:
    def __init__(self, r: int, g: int, b: int) -> None:
        self.__R = r
        self.__G = g
        self.__B = b

    def get_R(self) -> int:
        return self.__R

    def get_G(self) -> int:
        return self.__G

    def get_B(self) -> int:
        return self.__B


class RgbColorMap:

    __color_map: dict[str, RgbColor] = {
        "WHITE": RgbColor(255, 255, 255),
        "NOT_TOO_WHITE": RgbColor(220, 220, 220),
        "DRAWING_COLOR": RgbColor(250, 250, 250),
        "BLACK": RgbColor(0, 0, 0),
        "RED": RgbColor(255, 0, 0),
        "GREEN": RgbColor(0, 255, 0),
        "BLUE": RgbColor(0, 0, 255),
        "YELLOW": RgbColor(255, 255, 0),
        "CYAN": RgbColor(0, 255, 255),
        "MAGENTA": RgbColor(200, 0, 100),
        "GRAY": RgbColor(128, 128, 128),
        "DARK_GRAY": RgbColor(64, 64, 64),
        "LIGHT_GRAY": RgbColor(192, 192, 192),
        "ORANGE": RgbColor(255, 165, 0),
        "PINK": RgbColor(255, 192, 203),
        "PURPLE": RgbColor(128, 0, 128),
        "BROWN": RgbColor(165, 42, 42),
        "GOLD": RgbColor(255, 215, 0),
        "SILVER": RgbColor(192, 192, 192),
        "NAVY": RgbColor(0, 0, 128),
        "LIME": RgbColor(0, 255, 0),
        "OLIVE": RgbColor(128, 128, 0),
        "MAROON": RgbColor(128, 0, 0),
        "TEAL": RgbColor(0, 128, 128),
        "INDIGO": RgbColor(75, 0, 130),
        "VIOLET": RgbColor(238, 130, 238),
        "TURQUOISE": RgbColor(64, 224, 208)
    }

    __default_color = "WHITE"

    @classmethod
    def get_color_map(cls) -> dict[str, RgbColor]:
        return cls.__color_map

    @classmethod
    def get_color(cls, color: str) -> RgbColor:
        try:
            return cls.__color_map[color]
        except KeyError:
            warning = (f"\nWARNING: Invalid color value will be defaulted to {cls.__default_color}."
                       f"\n         Please replace the given value with a valid one, acording to the availuable color map.\n")
            logging.warning(warning)
            return cls.__color_map["WHITE"]
