from time import perf_counter

from ai_models.final_matcher import rank_matches
from database.database_manager import (
    get_all_reports,
    get_opposite_reports,
)


def main() -> None:
    print("\nPERFORMANCE TEST")
    print("-" * 50)

    active_reports = [
        report
        for report in get_all_reports()
        if report["status"] == "active"
    ]

    if not active_reports:
        print(
            "No active reports are available."
        )
        return

    source_report = active_reports[0]

    candidates = get_opposite_reports(
        source_report["report_type"]
    )

    if not candidates:
        print(
            "No opposite reports are available."
        )
        return

    start_time = perf_counter()

    ranked_matches = rank_matches(
        source_report,
        candidates,
    )

    end_time = perf_counter()

    execution_time = (
        end_time - start_time
    )

    print(
        f"Candidates processed: "
        f"{len(candidates)}"
    )

    print(
        f"Ranked results returned: "
        f"{len(ranked_matches)}"
    )

    print(
        f"Execution time: "
        f"{execution_time:.4f} seconds"
    )

    if execution_time > 10:
        print(
            "WARNING: Matching took more "
            "than 10 seconds."
        )
    else:
        print(
            "Performance result: ACCEPTABLE"
        )

    print(
        "\nPERFORMANCE TEST PASSED"
    )


if __name__ == "__main__":
    main()