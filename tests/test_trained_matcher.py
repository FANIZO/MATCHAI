from ai_models.final_matcher import (
    rank_matches,
)
from database.database_manager import (
    get_reports_by_type,
    initialize_database,
)


def main() -> None:
    initialize_database()

    lost_reports = get_reports_by_type(
        "lost"
    )

    found_reports = get_reports_by_type(
        "found"
    )

    if not lost_reports or not found_reports:
        raise ValueError(
            "Lost and found reports are required."
        )

    source_report = lost_reports[0]

    results = rank_matches(
        source_report,
        found_reports,
    )

    print("=" * 60)
    print("MATCHAI TRAINED MATCHER TEST")
    print("=" * 60)

    print(
        f"Source: {source_report['item_name']}"
    )

    for position, result in enumerate(
        results,
        start=1,
    ):
        print(
            f"\n{position}. "
            f"{result['item_name']}"
        )
        print(
            f"Final score: "
            f"{result['final_score']:.2%}"
        )
        print(
            f"Weighted baseline: "
            f"{result['weighted_score']:.2%}"
        )
        print(
            f"Method: "
            f"{result['score_method']}"
        )


if __name__ == "__main__":
    main()