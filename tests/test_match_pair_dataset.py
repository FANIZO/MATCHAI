import pandas as pd

from config import PAIR_DATASET_PATH


REQUIRED_COLUMNS = {
    "lost_report_id",
    "found_report_id",
    "image_similarity",
    "text_similarity",
    "category_similarity",
    "colour_similarity",
    "brand_similarity",
    "location_similarity",
    "date_similarity",
    "actual_match",
}


def main() -> None:
    if not PAIR_DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {PAIR_DATASET_PATH}"
        )

    dataframe = pd.read_csv(
        PAIR_DATASET_PATH
    )

    missing_columns = (
        REQUIRED_COLUMNS
        - set(dataframe.columns)
    )

    if missing_columns:
        raise ValueError(
            "Missing columns: "
            + ", ".join(sorted(missing_columns))
        )

    if dataframe["actual_match"].isna().any():
        raise ValueError(
            "Some rows have no actual_match label."
        )

    invalid_labels = set(
        dataframe["actual_match"].unique()
    ) - {0, 1}

    if invalid_labels:
        raise ValueError(
            "actual_match must contain only 0 or 1. "
            f"Invalid values: {invalid_labels}"
        )

    duplicate_pairs = dataframe.duplicated(
        subset=[
            "lost_report_id",
            "found_report_id",
        ]
    ).sum()

    print("=" * 60)
    print("MATCHAI LABELLED PAIR DATASET TEST")
    print("=" * 60)

    print(f"Total pairs: {len(dataframe)}")
    print(
        f"Positive matches: "
        f"{int((dataframe['actual_match'] == 1).sum())}"
    )
    print(
        f"Negative matches: "
        f"{int((dataframe['actual_match'] == 0).sum())}"
    )
    print(f"Duplicate pairs: {duplicate_pairs}")

    print("\nFeature ranges:")

    feature_columns = [
        "image_similarity",
        "text_similarity",
        "category_similarity",
        "colour_similarity",
        "brand_similarity",
        "location_similarity",
        "date_similarity",
    ]

    for column in feature_columns:
        minimum = dataframe[column].min()
        maximum = dataframe[column].max()

        print(
            f"{column}: "
            f"{minimum:.3f} to {maximum:.3f}"
        )

    print("\nDataset validation succeeded.")


if __name__ == "__main__":
    main()