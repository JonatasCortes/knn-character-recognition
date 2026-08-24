from src.services import extract_balanced_training_images, extract_balanced_training_labels
from src.domain import HNSW
from src.services import NodeManager
from pathlib import Path
import json
import logging
import time


class HnswBuilder:

    __PROGRESS_LOG_INTERVAL = 28

    def __init__(self, file_path: Path, max_neighbors: int, max_candidates: int) -> None:
        self.__file_path = file_path
        self.__hnsw = HNSW()
        self.__node_inserter = NodeManager(
            self.__hnsw, max_neighbors, max_candidates)

    def build(self) -> None:
        images = extract_balanced_training_images()
        labels = extract_balanced_training_labels()
        total_nodes = len(images)

        logging.info(f"Starting HNSW build with {total_nodes} nodes")
        started_at = time.perf_counter()
        checkpoint_at = started_at
        checkpoint_processed = 0

        for target_id, (image, label) in enumerate(zip(images, labels)):
            self.__node_inserter.insert(target_id, image, label)
            checkpoint_at, checkpoint_processed = self.__log_progress(
                target_id, total_nodes, checkpoint_at, checkpoint_processed)

        elapsed = time.perf_counter() - started_at
        logging.info(
            f"Finished inserting {total_nodes} nodes in {elapsed:.1f}s")

        with self.__file_path.open(mode="w", encoding="utf-8") as file:
            json.dump(self.__hnsw, file, indent=4, ensure_ascii=False)

        logging.info(f"HNSW written to {self.__file_path}")

    def __log_progress(self, target_id: int, total_nodes: int,
                       checkpoint_at: float, checkpoint_processed: int) -> tuple[float, int]:
        processed = target_id + 1
        is_checkpoint = processed % self.__PROGRESS_LOG_INTERVAL == 0
        is_last = processed == total_nodes

        if not is_checkpoint and not is_last:
            return checkpoint_at, checkpoint_processed

        now = time.perf_counter()
        window_elapsed = now - checkpoint_at
        window_processed = processed - checkpoint_processed
        rate = window_processed / window_elapsed if window_elapsed > 0 else 0
        remaining_seconds = (total_nodes - processed) / rate if rate > 0 else 0
        percentage = processed / total_nodes * 100

        logging.info(
            f"[{processed}/{total_nodes}] {percentage:.1f}% "
            f"- {rate:.1f} nodes/s - ETA {remaining_seconds:.0f}s"
        )

        return now, processed
