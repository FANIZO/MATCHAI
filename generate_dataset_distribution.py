from pathlib import Path
import sqlite3

import pandas as pd

from config import DATABASE_PATH, ITEM_CATEGORIES


PROJECT_DIR = Path(__file__).resolve().parents[1]

OUTPUT_PATH = (
    PROJECT_DIR
    / "outputs"
    / "dataset_category_distribution.csv"
)


def normalise_category(value: str) -> str:
    """Convert category names to one consistent format."""
    return (
        str(value)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def find_text_training_csv() -> Path | None:
    """
    Find a CSV containing category labels and text descriptions.
    """
    possible_folders = [
        PROJECT_DIR / "data",
        PROJECT_DIR / "data" / "text_data",
        PROJECT_DIR / "datasets",
        PROJECT_DIR / "training_data",
    ]

    category_columns = {
        "category",
        "label",
        "class",
        "target",
    }

    text_columns = {
        "description",
        "text",
        "sentence",
        "item_description",
    }

    for folder in possible_folders:
        if not folder.exists():
            continue

        for csv_path in folder.rglob("*.csv"):
            try:
                dataframe = pd.read_csv(csv_path)

                columns = {
                    str(column).strip().lower()
                    for column in dataframe.columns
                }

                has_category = bool(
                    columns.intersection(category_columns)
                )

                has_text = bool(
                    columns.intersection(text_columns)
                )

                if has_category and has_text:
                    print(
                        "Text-classifier dataset found:",
                        csv_path,
                    )
                    return csv_path

            except Exception:
                continue

    return None


def get_text_sample_counts() -> dict[str, int]:
    """Count text-classifier samples per category."""
    csv_path = Path(
        r"C:\Users\irfom\Downloads\AI_PROJECT\data\text_data\item_descriptions.csv"
    )

    if csv_path is None:
        print(
            "No text-classifier CSV was found. "
            "Text sample values will be zero."
        )
        return {}

    dataframe = pd.read_csv(csv_path)

    category_column = next(
        column
        for column in dataframe.columns
        if str(column).strip().lower()
        in {
            "category",
            "label",
            "class",
            "target",
        }
    )

    dataframe["normalised_category"] = (
        dataframe[category_column]
        .astype(str)
        .apply(normalise_category)
    )

    counts = (
        dataframe["normalised_category"]
        .value_counts()
        .to_dict()
    )

    return {
        str(category): int(count)
        for category, count in counts.items()
    }


def get_report_counts() -> dict[str, dict[str, int]]:
    """Count report images, lost reports and found reports."""
    connection = sqlite3.connect(DATABASE_PATH)

    query = """
        SELECT
            category,

            SUM(
                CASE
                    WHEN report_type = 'lost'
                    THEN 1
                    ELSE 0
                END
            ) AS lost_reports,

            SUM(
                CASE
                    WHEN report_type = 'found'
                    THEN 1
                    ELSE 0
                END
            ) AS found_reports,

            SUM(
                CASE
                    WHEN image_path IS NOT NULL
                        AND TRIM(image_path) <> ''
                    THEN 1
                    ELSE 0
                END
            ) AS report_images

        FROM reports

        GROUP BY category
    """

    dataframe = pd.read_sql_query(
        query,
        connection,
    )

    connection.close()

    if dataframe.empty:
        return {}

    dataframe["normalised_category"] = (
        dataframe["category"]
        .astype(str)
        .apply(normalise_category)
    )

    grouped = (
        dataframe.groupby(
            "normalised_category",
            as_index=False,
        )[
            [
                "report_images",
                "lost_reports",
                "found_reports",
            ]
        ]
        .sum()
    )

    results = {}

    for _, row in grouped.iterrows():
        category = row["normalised_category"]

        results[category] = {
            "report_images": int(
                row["report_images"]
            ),
            "lost_reports": int(
                row["lost_reports"]
            ),
            "found_reports": int(
                row["found_reports"]
            ),
        }

    return results


def main() -> None:
    text_counts = get_text_sample_counts()
    report_counts = get_report_counts()

    rows = []

    for category in ITEM_CATEGORIES:
        normalised = normalise_category(category)

        category_reports = report_counts.get(
            normalised,
            {},
        )

        rows.append(
            {
                "Category": (
                    normalised
                    .replace("_", " ")
                    .title()
                ),
                "Text-classifier samples": (
                    text_counts.get(
                        normalised,
                        0,
                    )
                ),
                "Report images": (
                    category_reports.get(
                        "report_images",
                        0,
                    )
                ),
                "Lost reports": (
                    category_reports.get(
                        "lost_reports",
                        0,
                    )
                ),
                "Found reports": (
                    category_reports.get(
                        "found_reports",
                        0,
                    )
                ),
            }
        )

    result = pd.DataFrame(rows)

    total_row = {
        "Category": "Total",
        "Text-classifier samples": int(
            result[
                "Text-classifier samples"
            ].sum()
        ),
        "Report images": int(
            result["Report images"].sum()
        ),
        "Lost reports": int(
            result["Lost reports"].sum()
        ),
        "Found reports": int(
            result["Found reports"].sum()
        ),
    }

    result = pd.concat(
        [
            result,
            pd.DataFrame([total_row]),
        ],
        ignore_index=True,
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print()
    print("Dataset Category Distribution")
    print("=" * 75)
    print(result.to_string(index=False))
    print()
    print(
        "Saved to:",
        OUTPUT_PATH,
    )


if __name__ == "__main__":
    main()