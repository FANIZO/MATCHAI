from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from config import CHART_DIR, MODEL_DIR, TEXT_DATA_DIR


DATASET_PATH = TEXT_DATA_DIR / "item_descriptions.csv"
MODEL_PATH = MODEL_DIR / "text_classifier.joblib"
REPORT_PATH = CHART_DIR / "text_classification_report.txt"
CONFUSION_MATRIX_PATH = CHART_DIR / "text_confusion_matrix.png"


def load_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    dataframe = pd.read_csv(DATASET_PATH)

    required_columns = {"description", "category"}

    if not required_columns.issubset(dataframe.columns):
        raise ValueError(
            "Dataset must contain description and category columns."
        )

    dataframe = dataframe.dropna(
        subset=["description", "category"]
    ).copy()

    dataframe["description"] = (
        dataframe["description"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    dataframe["category"] = (
        dataframe["category"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    dataframe = dataframe[
        dataframe["description"] != ""
    ]

    dataframe = dataframe[
        dataframe["category"] != ""
    ]

    return dataframe


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    ngram_range=(1, 2),
                    min_df=1,
                ),
            ),
            (
                "classifier",
                MultinomialNB(
                    alpha=0.5,
                ),
            ),
        ]
    )


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = load_dataset()

    print("=" * 60)
    print("MATCHAI TEXT CLASSIFIER TRAINING")
    print("=" * 60)

    print(f"Total records: {len(dataframe)}")
    print(f"Categories: {dataframe['category'].nunique()}")

    print("\nCategory distribution:")
    print(dataframe["category"].value_counts().sort_index())

    features = dataframe["description"]
    labels = dataframe["category"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels,
    )

    print(f"\nTraining records: {len(x_train)}")
    print(f"Testing records: {len(x_test)}")

    pipeline = build_pipeline()

    pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    report = classification_report(
        y_test,
        predictions,
        zero_division=0,
    )

    print(f"\nAccuracy: {accuracy:.4f}")
    print("\nClassification report:")
    print(report)

    joblib.dump(
        pipeline,
        MODEL_PATH,
    )

    with REPORT_PATH.open(
        "w",
        encoding="utf-8",
    ) as report_file:
        report_file.write(
            "MATCHAI TEXT CLASSIFIER RESULTS\n"
        )
        report_file.write("=" * 50 + "\n")
        report_file.write(
            f"Total records: {len(dataframe)}\n"
        )
        report_file.write(
            f"Training records: {len(x_train)}\n"
        )
        report_file.write(
            f"Testing records: {len(x_test)}\n"
        )
        report_file.write(
            f"Accuracy: {accuracy:.4f}\n\n"
        )
        report_file.write(report)

    labels_order = sorted(labels.unique())

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=labels_order,
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=labels_order,
    )

    figure, axis = plt.subplots(
        figsize=(12, 10)
    )

    display.plot(
        ax=axis,
        xticks_rotation=45,
        colorbar=False,
    )

    axis.set_title(
        "MatchAI Text Classification Confusion Matrix"
    )

    figure.tight_layout()

    figure.savefig(
        CONFUSION_MATRIX_PATH,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(figure)

    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Report saved to: {REPORT_PATH}")
    print(
        "Confusion matrix saved to: "
        f"{CONFUSION_MATRIX_PATH}"
    )


if __name__ == "__main__":
    main()