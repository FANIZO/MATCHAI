from ai_models.fuzzy_rules import (
    brand_similarity,
    calculate_attribute_similarities,
    category_similarity,
    colour_similarity,
    date_similarity,
    location_similarity,
)


def main() -> None:
    print("=" * 60)
    print("MATCHAI FUZZY ATTRIBUTE TEST")
    print("=" * 60)

    print(
        "Category:",
        category_similarity("bag", "bag"),
    )

    print(
        "Colour exact:",
        colour_similarity("black", "black"),
    )

    print(
        "Colour related:",
        colour_similarity("black", "dark grey"),
    )

    print(
        "Brand:",
        brand_similarity("Adidas", "adidas"),
    )

    print(
        "Location:",
        location_similarity(
            "Library",
            "Library Entrance",
        ),
    )

    print(
        "Date same:",
        date_similarity(
            "2026-06-17",
            "2026-06-17",
        ),
    )

    print(
        "Date one day:",
        date_similarity(
            "2026-06-17",
            "2026-06-18",
        ),
    )

    lost_report = {
        "category": "bag",
        "colour": "black",
        "brand": "Adidas",
        "location": "Library",
        "report_date": "2026-06-17",
    }

    found_report = {
        "category": "bag",
        "colour": "dark grey",
        "brand": "Adidas",
        "location": "Library Entrance",
        "report_date": "2026-06-18",
    }

    scores = calculate_attribute_similarities(
        lost_report,
        found_report,
    )

    print("\nCombined attribute scores:")

    for name, score in scores.items():
        print(
            f"{name}: {score:.2%}"
        )


if __name__ == "__main__":
    main()