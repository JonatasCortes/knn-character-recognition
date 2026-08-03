from src.hnsw.domain._label import Label
from src.hnsw.domain._position import Position


class Node:

    __global_id = 0

    def __init__(self, position: Position, label: Label) -> None:
        self.__position = position
        self.__label = label
        self.__id = self.__global_id
        self.__global_id += 1
        self.neighbors: list[Node] = []

    def get_position(self) -> Position:
        return self.__position

    def get_label(self) -> Label:
        return self.__label

    def get_id(self) -> int:
        return self.__id
