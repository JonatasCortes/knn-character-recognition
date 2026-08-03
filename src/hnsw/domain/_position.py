import numpy as np


class Position(int):

    __SECTIONS = 28  # default dimension size for EMNIST dataset images
    __LUMINANCE_THRESHOLD = 25

    def __new__(cls, image: np.ndarray) -> None:
        super().__new__(cls, cls.__calculate(image))

    @classmethod
    def __calculate(cls, image: np.ndarray) -> int:
        binary = image > cls.__LUMINANCE_THRESHOLD
        rows = np.array_split(binary, cls.__SECTIONS, axis=0)
        position = 1

        for row in rows:
            cells = np.array_split(row, cls.__SECTIONS, axis=1)
            for cell in cells:
                position = (position << 1) | int(cell.mean() >= 0.5)

        return position
