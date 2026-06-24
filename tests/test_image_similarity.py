from ai_models.knn_matcher import rank_image_matches
from database.database_manager import (
    get_reports_by_type,
    initialize_database,
)


def main() -> None:
    initialize_database()

    lost_reports = [
        report
        for report in get_reports_by_type("lost")
        if report.get("image_path")
    ]

    found_reports = [
        report
        for report in get_reports_by_type("found")
        if report.get("image_path")
    ]

    if not lost_reports:
        raise ValueError(
            "No lost reports with images were found."
        )

    if not found_reports:
        raise ValueError(
            "No found reports with images were found."
        )

    source_report = lost_reports[0]

    results = rank_image_matches(
        source_report,
        found_reports,
    )

    print("=" * 60)
    print("MATCHAI SAVED-FEATURE IMAGE SIMILARITY TEST")
    print("=" * 60)

    print(
        f"Source item: {source_report['item_name']}"
    )

    print(
        f"Source feature: "
        f"{source_report.get('feature_path') or 'Not saved'}"
    )

    print("\nRanked found items:")

    for position, result in enumerate(
        results,
        start=1,
    ):
        print(
            f"{position}. "
            f"{result['item_name']} | "
            f"{result['image_similarity']:.2%} | "
            f"Feature: "
            f"{result.get('feature_path') or 'Calculated from image'}"
        )


if __name__ == "__main__":
    main()