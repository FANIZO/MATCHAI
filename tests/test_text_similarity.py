from ai_models.text_similarity import (
    build_report_text,
    calculate_text_similarity,
    rank_text_matches,
)


def main() -> None:
    lost_report = {
        "report_id": 100,
        "item_name": "Black Adidas Backpack",
        "category": "bag",
        "description": (
            "Black backpack with silver zipper "
            "and front pocket"
        ),
        "colour": "black",
        "brand": "Adidas",
        "location": "Library",
    }

    found_reports = [
        {
            "report_id": 1,
            "item_name": "Dark Backpack",
            "category": "bag",
            "description": (
                "Dark backpack with metallic zip "
                "and front compartment"
            ),
            "colour": "black",
            "brand": "Adidas",
            "location": "Library entrance",
        },
        {
            "report_id": 2,
            "item_name": "Blue Bottle",
            "category": "bottle",
            "description": (
                "Blue water bottle with "
                "university sticker"
            ),
            "colour": "blue",
            "brand": "",
            "location": "Cafeteria",
        },
        {
            "report_id": 3,
            "item_name": "Silver Calculator",
            "category": "calculator",
            "description": (
                "Silver scientific calculator "
                "with scratched screen"
            ),
            "colour": "silver",
            "brand": "Casio",
            "location": "Lecture Hall",
        },
    ]

    print("=" * 60)
    print("MATCHAI COMBINED TEXT SIMILARITY TEST")
    print("=" * 60)

    print(
        "\nSource text:",
        build_report_text(lost_report),
    )

    ranked = rank_text_matches(
        lost_report,
        found_reports,
    )

    print("\nRanked matches:")

    for position, report in enumerate(
        ranked,
        start=1,
    ):
        print(
            f"{position}. "
            f"Report {report['report_id']} | "
            f"{report['item_name']} | "
            f"{report['text_similarity']:.2%}"
        )


if __name__ == "__main__":
    main()