from ai_models.final_matcher import rank_matches
from database.database_manager import (
    get_all_reports,
    get_opposite_reports,
)


def main() -> None:
    print("\nMATCHING PIPELINE TEST")
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
            "No opposite report candidates "
            "are available."
        )
        return

    ranked_matches = rank_matches(
        source_report,
        candidates,
    )

    if not ranked_matches:
        raise AssertionError(
            "The matching pipeline returned "
            "no ranked results."
        )

    required_fields = {
        "report_id",
        "item_name",
        "image_similarity",
        "text_similarity",
        "category_similarity",
        "colour_similarity",
        "brand_similarity",
        "location_similarity",
        "date_similarity",
        "weighted_score",
        "final_score",
        "match_strength",
        "score_method",
        "explanations",
    }

    for candidate in ranked_matches:
        missing_fields = (
            required_fields
            - set(candidate.keys())
        )

        if missing_fields:
            raise AssertionError(
                "Candidate is missing fields: "
                f"{missing_fields}"
            )

        similarity_fields = [
            "image_similarity",
            "text_similarity",
            "category_similarity",
            "colour_similarity",
            "brand_similarity",
            "location_similarity",
            "date_similarity",
            "weighted_score",
            "final_score",
        ]

        for field in similarity_fields:
            value = candidate[field]

            if not 0.0 <= value <= 1.0:
                raise AssertionError(
                    f"{field} is outside 0 to 1: "
                    f"{value}"
                )

    final_scores = [
        candidate["final_score"]
        for candidate in ranked_matches
    ]

    if final_scores != sorted(
        final_scores,
        reverse=True,
    ):
        raise AssertionError(
            "Ranked results are not sorted "
            "from highest to lowest."
        )

    print(
        f"Source report ID: "
        f"{source_report['report_id']}"
    )

    print(
        f"Candidates tested: "
        f"{len(ranked_matches)}"
    )

    print(
        f"Top candidate: "
        f"{ranked_matches[0]['item_name']}"
    )

    print(
        f"Top score: "
        f"{ranked_matches[0]['final_score']:.2%}"
    )

    print(
        "Field validation: PASSED"
    )

    print(
        "Score range validation: PASSED"
    )

    print(
        "Ranking order validation: PASSED"
    )

    print(
        "\nMATCHING PIPELINE TEST PASSED"
    )


if __name__ == "__main__":
    main()