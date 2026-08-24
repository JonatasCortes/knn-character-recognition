from pathlib import Path
from src.domain import Label
from src.hnsw import HnswClassifier
from src.services import extract_balanced_testing_images, extract_balanced_testing_labels
import time
import json


def test_acuracy(max_candidates: int, hnsw_file_path: Path, test_results_file_path: Path):

    start = time.perf_counter()

    images = extract_balanced_testing_images()
    labels = extract_balanced_testing_labels()
    HnswClassifier.download_hnsw(hnsw_file_path)

    correct_count = 0
    incorrect_count = 0
    inconclusive_count = 0

    for image, raw_label in zip(images, labels):

        expected_label = Label(raw_label)
        hnsw_classified_label = HnswClassifier.classify(image, max_candidates)

        if expected_label == hnsw_classified_label:
            correct_count += 1
        else:
            incorrect_count += 1

        if hnsw_classified_label == "n/a":
            inconclusive_count += 1

    elapsed = time.perf_counter() - start

    result: dict[str, int | float] = {
        "max_candidates": max_candidates,
        "total_tests": len(images),
        "total_correct": correct_count,
        "total_incorrect": incorrect_count,
        "total_inconclusive": inconclusive_count,
        "acuracy": correct_count / len(images),
        "execution_time_per_test": elapsed / len(images),
        "total_execution_time": elapsed
    }

    with test_results_file_path.open(mode="w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    return (max_candidates, correct_count / len(images))
