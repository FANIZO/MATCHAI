import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = Path(
    os.getenv(
        "MATCHAI_DB_PATH",
        str(BASE_DIR / "database" / "matchai.db"),
    )
)


BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = Path(
    os.getenv(
        "MATCHAI_STORAGE_DIR",
        str(BASE_DIR),
    )
)

DATABASE_DIR = STORAGE_DIR / "database"
DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
DATABASE_PATH = DATABASE_DIR / "matchai.db"

DATA_DIR = BASE_DIR / "data"
RAW_IMAGE_DIR = DATA_DIR / "raw_images"
PROCESSED_IMAGE_DIR = DATA_DIR / "processed_images"
FEATURE_DIR = DATA_DIR / "image_features"
TEXT_DATA_DIR = DATA_DIR / "text_data"
MATCH_PAIR_DIR = DATA_DIR / "match_pairs"

MODEL_DIR = BASE_DIR / "models"

OUTPUT_DIR = BASE_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
REPORT_DIR = OUTPUT_DIR / "reports"
TEST_RESULT_DIR = OUTPUT_DIR / "test_results"

DATABASE_DIR = BASE_DIR / "database"


PAIR_DATASET_PATH = (
    MATCH_PAIR_DIR / "labelled_match_pairs.csv"
)

UNLABELLED_PAIR_PATH = (
    MATCH_PAIR_DIR / "unlabelled_match_pairs.csv"
)

FINAL_MODEL_PATH = (
    MODEL_DIR / "final_match_classifier.joblib"
)

FINAL_MODEL_METADATA_PATH = (
    MODEL_DIR / "final_match_metadata.joblib"
)

ITEM_CATEGORIES = [
    "phone",
    "wallet",
    "bag",
    "keys",
    "bottle",
    "umbrella",
    "headphones",
    "laptop",
    "watch",
    "document",
    "student_card",
    "calculator",
    "other",
]

REPORT_TYPES = [
    "lost",
    "found",
]

SUPPORTED_IMAGE_TYPES = [
    "jpg",
    "jpeg",
    "png",
]

MAX_IMAGE_SIZE_MB = 10