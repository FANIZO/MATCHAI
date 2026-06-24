from database.database_manager import (
    get_all_reports,
    get_dashboard_statistics,
    get_match_history,
)


def main() -> None:
    print("\nDATABASE OPERATIONS TEST")
    print("-" * 50)

    reports = get_all_reports()

    print(
        f"Total reports retrieved: {len(reports)}"
    )

    if reports:
        required_report_fields = {
            "report_id",
            "report_type",
            "item_name",
            "category",
            "description",
            "location",
            "report_date",
            "status",
        }

        for report in reports:
            missing_fields = (
                required_report_fields
                - set(report.keys())
            )

            if missing_fields:
                raise AssertionError(
                    "Report is missing fields: "
                    f"{missing_fields}"
                )

        print(
            "Report field validation: PASSED"
        )

    statistics = get_dashboard_statistics()

    required_statistics = {
        "total_reports",
        "total_lost",
        "total_found",
        "active_reports",
        "matched_reports",
        "confirmed_matches",
        "rejected_matches",
        "pending_matches",
        "confirmation_rate",
        "average_probability",
    }

    missing_statistics = (
        required_statistics
        - set(statistics.keys())
    )

    if missing_statistics:
        raise AssertionError(
            "Dashboard statistics are missing: "
            f"{missing_statistics}"
        )

    if (
        statistics["total_lost"]
        + statistics["total_found"]
        != statistics["total_reports"]
    ):
        raise AssertionError(
            "Lost and found totals do not match "
            "the total number of reports."
        )

    print(
        "Dashboard statistics validation: PASSED"
    )

    match_history = get_match_history()

    print(
        f"Match history records: "
        f"{len(match_history)}"
    )

    for match in match_history:
        if match["match_status"] not in {
            "pending",
            "confirmed",
            "rejected",
        }:
            raise AssertionError(
                "Invalid match status found: "
                f"{match['match_status']}"
            )

    print(
        "Match history validation: PASSED"
    )

    print(
        "\nDATABASE OPERATIONS TEST PASSED"
    )


if __name__ == "__main__":
    main()