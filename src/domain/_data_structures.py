from functools import total_ordering
from typing import Any


class Node(dict[str, Any]):
    pass


class Layer(dict[int, Node]):
    pass


class HNSW(dict[int, Layer]):
    pass


@total_ordering
class Candidate:

    def __init__(self, node_id: int, node_position: int, distance_to_target: int) -> None:
        self.id = node_id
        self.position = node_position
        self.distance_to_target = distance_to_target

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Candidate):
            return self.distance_to_target == other.distance_to_target
        return False

    def __lt__(self, other: object):
        if isinstance(other, Candidate):
            return self.distance_to_target < other.distance_to_target
        return False
