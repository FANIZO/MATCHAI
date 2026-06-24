from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from config import (
    CHART_DIR,
    FINAL_MODEL_METADATA_PATH,
    FINAL_MODEL_PATH,
    PAIR_DATASET_PATH,
)


FEATURE_COLUMNS = [
    "image_similarity",
    "text_similarity",
    "category_similarity",
    "colour_similarity",
    "brand_similarity",
    "location_similarity",
    "date_similarity",
]


def load_dataset() -> pd.DataFrame:
    if not PAIR_DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {PAIR_DATASET_PATH}"
        )

    dataframe = pd.read_csv(
        PAIR_DATASET_PATH
    )

    dataframe = dataframe.dropna(
        subset=[
            *FEATURE_COLUMNS,
            "actual_match",
        ]
    ).copy()

    dataframe["actual_match"] = (
        dataframe["actual_match"].astype(int)
    )

    if set(
        dataframe["actual_match"].unique()
    ) != {0, 1}:
        raise ValueError(
            "The dataset must contain both "
            "positive and negative examples."
        )

    return dataframe


def build_models(
    training_size: int,
) -> dict:
    # K must be smaller than the number
    # of available training records.
    selected_k = min(
        5,
        max(1, training_size - 1),
    )

    return {
        "KNN": Pipeline(
            steps=[
                (
                    "scaler",
                    StandardScaler(),
                ),
                (
                    "classifier",
                    KNeighborsClassifier(
                        n_neighbors=selected_k,
                        weights="distance",
                    ),
                ),
            ]
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=5,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
            class_weight="balanced",
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
        ),
    }


def calculate_metrics(
    actual,
    predicted,
) -> dict[str, float]:
    return {
        "accuracy": accuracy_score(
            actual,
            predicted,
        ),
        "precision": precision_score(
            actual,
            predicted,
            zero_division=0,
        ),
        "recall": recall_score(
            actual,
            predicted,
            zero_division=0,
        ),
        "f1_score": f1_score(
            actual,
            predicted,
            zero_division=0,
        ),
    }


def save_confusion_matrix(
    actual,
    predicted,
    model_name: str,
) -> None:
    matrix = confusion_matrix(
        actual,
        predicted,
        labels=[0, 1],
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=[
            "Not Match",
            "Match",
        ],
    )

    figure, axis = plt.subplots(
        figsize=(6, 5)
    )

    display.plot(
        ax=axis,
        colorbar=False,
    )

    axis.set_title(
        f"{model_name} Confusion Matrix"
    )

    figure.tight_layout()

    safe_name = (
        model_name.lower()
        .replace(" ", "_")
    )

    output_path = (
        CHART_DIR
        / f"{safe_name}_confusion_matrix.png"
    )

    figure.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(figure)


def save_comparison_chart(
    results: pd.DataFrame,
) -> None:
    chart_data = results.set_index(
        "model"
    )[
        [
            "accuracy",
            "precision",
            "recall",
            "f1_score",
        ]
    ]

    axis = chart_data.plot(
        kind="bar",
        figsize=(10, 6),
    )

    axis.set_ylim(0, 1.05)
    axis.set_ylabel("Score")
    axis.set_title(
        "Final Match Classifier Comparison"
    )
    axis.tick_params(
        axis="x",
        rotation=0,
    )

    figure = axis.get_figure()
    figure.tight_layout()

    figure.savefig(
        CHART_DIR
        / "final_model_comparison.png",
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(figure)


def main() -> None:
    CHART_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    FINAL_MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe = load_dataset()

    print("=" * 65)
    print("MATCHAI FINAL CLASSIFIER TRAINING")
    print("=" * 65)

    print(f"Total pairs: {len(dataframe)}")
    print(
        "Positive pairs:",
        int(
            (
                dataframe["actual_match"]
                == 1
            ).sum()
        ),
    )
    print(
        "Negative pairs:",
        int(
            (
                dataframe["actual_match"]
                == 0
            ).sum()
        ),
    )

    features = dataframe[
        FEATURE_COLUMNS
    ]

    labels = dataframe[
        "actual_match"
    ]

    x_train, x_test, y_train, y_test = (
        train_test_split(
            features,
            labels,
            test_size=0.25,
            random_state=42,
            stratify=labels,
        )
    )

    models = build_models(
        training_size=len(x_train)
    )

    results = []
    trained_models = {}

    for model_name, model in models.items():
        print("\n" + "-" * 65)
        print(f"Training: {model_name}")
        print("-" * 65)

        model.fit(
            x_train,
            y_train,
        )

        predictions = model.predict(
            x_test
        )

        metrics = calculate_metrics(
            y_test,
            predictions,
        )

        print(
            classification_report(
                y_test,
                predictions,
                target_names=[
                    "Not Match",
                    "Match",
                ],
                zero_division=0,
            )
        )

        print(
            f"Accuracy: "
            f"{metrics['accuracy']:.4f}"
        )
        print(
            f"Precision: "
            f"{metrics['precision']:.4f}"
        )
        print(
            f"Recall: "
            f"{metrics['recall']:.4f}"
        )
        print(
            f"F1-score: "
            f"{metrics['f1_score']:.4f}"
        )

        results.append(
            {
                "model": model_name,
                **metrics,
            }
        )

        trained_models[
            model_name
        ] = model

        save_confusion_matrix(
            y_test,
            predictions,
            model_name,
        )

    results_dataframe = pd.DataFrame(
        results
    )

    results_dataframe = (
        results_dataframe.sort_values(
            by=[
                "f1_score",
                "accuracy",
            ],
            ascending=False,
        )
    )

    best_model_name = (
        results_dataframe.iloc[0]["model"]
    )

    best_model = trained_models[
        best_model_name
    ]

    joblib.dump(
        best_model,
        FINAL_MODEL_PATH,
    )

    metadata = {
        "model_name": best_model_name,
        "feature_columns": FEATURE_COLUMNS,
        "training_records": len(x_train),
        "testing_records": len(x_test),
        "positive_pairs": int(
            (labels == 1).sum()
        ),
        "negative_pairs": int(
            (labels == 0).sum()
        ),
        "results": (
            results_dataframe.to_dict(
                orient="records"
            )
        ),
    }

    joblib.dump(
        metadata,
        FINAL_MODEL_METADATA_PATH,
    )

    results_path = (
        CHART_DIR
        / "final_model_results.csv"
    )

    results_dataframe.to_csv(
        results_path,
        index=False,
    )

    save_comparison_chart(
        results_dataframe
    )

    print("\n" + "=" * 65)
    print("MODEL COMPARISON")
    print("=" * 65)
    print(
        results_dataframe.to_string(
            index=False
        )
    )

    print(
        f"\nBest model: {best_model_name}"
    )
    print(
        f"Saved model: {FINAL_MODEL_PATH}"
    )
    print(
        f"Saved metadata: "
        f"{FINAL_MODEL_METADATA_PATH}"
    )
    print(
        f"Saved results: {results_path}"
    )


if __name__ == "__main__":
    main()