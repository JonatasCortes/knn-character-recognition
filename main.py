from tests.test_acuracy import test_acuracy
from src.hnsw import HnswBuilder
from pathlib import Path
import matplotlib.pyplot as plt
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] ===> %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# builder = HnswBuilder(Path("hnsw.json"), 32, 200)
# builder.build()

precision_per_max_candidates: list[tuple[int, float]] = []
