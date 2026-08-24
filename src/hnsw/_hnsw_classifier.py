from typing import Any

from src.domain import HNSW, Candidate, Position, Label
from src.services import SearchEngine, hamming_distance
from pathlib import Path
from collections import Counter
import numpy as np
import json


class HnswClassifier:

    @classmethod
    def download_hnsw(cls, file_path: Path):
        with file_path.open(mode="r", encoding="utf-8") as file:
            cls.__hnsw = HNSW(
                json.load(file, object_hook=cls.__restore_integer_keys))
            cls.__search_engine = SearchEngine(cls.__hnsw, hamming_distance)

    @classmethod
    def classify(cls, image: np.ndarray, max_candidates: int) -> str:
        target_position = Position(image)
        engine = cls.__search_engine

        top_layer_id = next(reversed(cls.__hnsw))
        pointer = next(iter(cls.__hnsw[top_layer_id]))

        for layer_id in reversed(cls.__hnsw):
            engine.explore_layer(target_position, layer_id,
                                 max_candidates, pointer)
            pointer = engine.get_nearest_neighbor()

        return cls.__extract_most_common_label(engine.get_candidates())

    @classmethod
    def __extract_most_common_label(cls, candidates: list[Candidate]) -> str:
        bottom_layer = cls.__hnsw[0]
        frequency_map = Counter(Label(bottom_layer[c.id]["label"])
                                for c in candidates)

        if not frequency_map:
            return "n/a"

        most_common = frequency_map.most_common(2)

        if len(most_common) == 1:
            return most_common[0][0]

        top1, top2 = most_common

        if top1[1] == top2[1]:
            return "n/a"

        return top1[0]

    @staticmethod
    def __restore_integer_keys(obj: dict[Any, Any]) -> dict[int, Any]:
        if obj and all(key.isdigit() for key in obj):
            return {int(key): value for key, value in obj.items()}
        return obj
