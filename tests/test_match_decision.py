from database.database_manager import (
    add_match,
    get_match_by_id,
    get_reports_by_type,
    initialize_database,
    process_match_decision,
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
            "At least one lost report and "
            "one found report are required."
        )

    lost_report = lost_reports[0]
    found_report = found_reports[0]

    match_id = add_match(
        lost_report_id=lost_report[
            "report_id"
        ],
        found_report_id=found_report[
            "report_id"
        ],
        image_similarity=0.80,
        text_similarity=0.70,
        category_similarity=1.0,
        colour_similarity=1.0,
        brand_similarity=0.90,
        location_similarity=0.85,
        date_similarity=0.90,
        final_probability=0.88,
    )

    print(
        f"Created test match ID: {match_id}"
    )

    process_match_decision(
        match_id=match_id,
        decision="rejected",
        notes="Test rejection",
    )

    updated_match = get_match_by_id(
        match_id
    )

    print(
        f"Updated status: "
        f"{updated_match['match_status']}"
    )

    print(
        "\nMatch decision test completed."
    )


if __name__ == "__main__":
    main()