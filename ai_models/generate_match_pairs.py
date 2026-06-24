import csv

from ai_models.final_matcher import compare_reports
from config import MATCH_PAIR_DIR, UNLABELLED_PAIR_PATH
from database.database_manager import (
    get_reports_by_type,
    initialize_database,
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


def generate_pairs() -> list[dict]:
    lost_reports = get_reports_by_type("lost")
    found_reports = get_reports_by_type("found")

    pairs = []

    for lost_report in lost_reports:
        for found_report in found_reports:
            comparison = compare_reports(
                lost_report,
                found_report,
            )

            pair = {
                "lost_report_id": lost_report["report_id"],
                "found_report_id": found_report["report_id"],
                "lost_item_name": lost_report["item_name"],
                "found_item_name": found_report["item_name"],
            }

            for feature_name in FEATURE_COLUMNS:
                pair[feature_name] = round(
                    comparison[feature_name],
                    6,
                )

            # This must be filled manually:
            # 1 = same physical item
            # 0 = different physical item
            pair["actual_match"] = ""

            pairs.append(pair)

    return pairs


def save_pairs(pairs: list[dict]) -> None:
    MATCH_PAIR_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "lost_report_id",
        "found_report_id",
        "lost_item_name",
        "found_item_name",
        *FEATURE_COLUMNS,
        "actual_match",
    ]

    with UNLABELLED_PAIR_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(pairs)


def main() -> None:
    initialize_database()

    pairs = generate_pairs()

    if not pairs:
        print(
            "No pairs were generated. "
            "Add at least one lost report and "
            "one found report."
        )
        return

    save_pairs(pairs)

    print("=" * 60)
    print("MATCHAI MATCH-PAIR GENERATOR")
    print("=" * 60)
    print(f"Pairs generated: {len(pairs)}")
    print(f"Saved to: {UNLABELLED_PAIR_PATH}")
    print(
        "\nOpen the CSV and fill actual_match "
        "with either 1 or 0."
    )


if __name__ == "__main__":
    main()