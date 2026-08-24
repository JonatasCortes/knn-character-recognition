from typing import Callable
from src.domain import HNSW, Candidate, Layer
import heapq


class SearchEngine:

    def __init__(self, hnsw: HNSW, distance_metric: Callable[[int, int], int]) -> None:
        self.__hnsw = hnsw
        self.__distance_metric = distance_metric
        self.__nearest_neighbor: int | None = None
        self.__candidates: list[Candidate] = []

    def get_candidates(self) -> list[Candidate]:
        return self.__candidates

    def get_nearest_neighbor(self) -> int:
        if self.__nearest_neighbor is None:
            raise RuntimeError("No layer was explored yet.")
        return self.__nearest_neighbor

    def explore_layer(self, target_position: int, layer_id: int, max_candidates: int, entry_node_id: int = 0) -> None:
        layer = self.__hnsw[layer_id]
        entry = self.__build_candidate(entry_node_id, layer, target_position)

        self.__candidates = []
        self.__update_candidates(entry, max_candidates)

        frontier: list[Candidate] = [entry]
        visited: set[int] = {entry_node_id}

        while frontier:
            nearest_unexpanded = heapq.heappop(frontier)

            if self.__cannot_improve(nearest_unexpanded, max_candidates):
                break

            for neighbor_id in layer[nearest_unexpanded.id]["neighbors"]:
                if neighbor_id in visited:
                    continue
                visited.add(neighbor_id)

                neighbor = self.__build_candidate(neighbor_id, layer,
                                                  target_position)
                heapq.heappush(frontier, neighbor)
                self.__update_candidates(neighbor, max_candidates)

        self.__nearest_neighbor = min(self.__candidates).id

    def __build_candidate(self, node_id: int, layer: Layer, target_position: int) -> Candidate:
        position = layer[node_id]["position"]
        distance = self.__distance_metric(position, target_position)
        return Candidate(node_id, position, distance)

    def __update_candidates(self, candidate: Candidate, max_candidates: int) -> None:
        heapq.heappush_max(self.__candidates, candidate)
        if len(self.__candidates) > max_candidates:
            heapq.heappop_max(self.__candidates)

    def __cannot_improve(self, candidate: Candidate, max_candidates: int) -> bool:
        if len(self.__candidates) < max_candidates:
            return False
        worst_kept = self.__candidates[0]
        return candidate.distance_to_target > worst_kept.distance_to_target
