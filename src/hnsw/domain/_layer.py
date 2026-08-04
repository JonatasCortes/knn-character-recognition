from src.hnsw.domain._node import Node


class Layer:

    top_id = -1

    def __init__(self, starting_node: Node, degree: int) -> None:
        self.__id = self.top_id + 1
        self.top_id += 1
        self.__nodes: dict[int, Node] = {starting_node.get_id(): starting_node}
        self.__degree = degree

    def get_id(self) -> int:
        return self.__id

    def get_node_by_id(self, node_id: int) -> Node:
        return self.__nodes[node_id]

    def get_nodes(self) -> dict[int, Node]:
        return self.__nodes

    def get_degree(self) -> int:
        return self.__degree
