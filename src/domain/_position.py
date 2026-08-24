from typing import Self
import numpy as np


class Position(int):

    __SECTIONS = 28
    __LUMINANCE_THRESHOLD = 100

    def __new__(cls, image: np.ndarray) -> Self:
        return super().__new__(cls, cls.__calculate(image))

    @classmethod
    def __calculate(cls, image: np.ndarray) -> int:
        binary = image > cls.__LUMINANCE_THRESHOLD
        cropped_binary = cls.__crop_to_content(binary)
        normalized_shape = (cls.__SECTIONS, cls.__SECTIONS)
        normalized_binary = cls.__normalize_shape(cropped_binary,
                                                  normalized_shape)
        rows = np.array_split(normalized_binary, cls.__SECTIONS, axis=0)
        position = 1

        for row in rows:
            cells = np.array_split(row, cls.__SECTIONS, axis=1)
            for cell in cells:
                position = (position << 1) | int(cell.mean() >= 0.5)

        return position

    @staticmethod
    def __crop_to_content(binary: np.ndarray) -> np.ndarray:
        rows_with_content = np.any(binary, axis=1)
        cols_with_content = np.any(binary, axis=0)

        if not rows_with_content.any():
            return binary

        top, bottom = np.where(rows_with_content)[0][[0, -1]]
        left, right = np.where(cols_with_content)[0][[0, -1]]

        return binary[top:bottom + 1, left:right + 1]

    @staticmethod
    def __normalize_shape(image: np.ndarray, target_shape: tuple[int, int]) -> np.ndarray:
        target_h, target_w = target_shape
        src_h: int
        src_w: int
        src_h, src_w = image.shape

        row_indices = np.linspace(0, src_h - 1, target_h).astype(int)
        col_indices = np.linspace(0, src_w - 1, target_w).astype(int)

        return image[row_indices[:, None], col_indices]
