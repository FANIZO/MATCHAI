from ai_models.final_matcher import (
    rank_matches,
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
        "report_date": "2026-06-17",
    }

    found_reports = [
        {
            "report_id": 1,
            "item_name": "Dark Adidas Backpack",
            "category": "bag",
            "description": (
                "Dark school backpack with metallic zip "
                "and front compartment"
            ),
            "colour": "dark grey",
            "brand": "Adidas",
            "location": "Library Entrance",
            "report_date": "2026-06-18",
        },
        {
            "report_id": 2,
            "item_name": "Blue Water Bottle",
            "category": "bottle",
            "description": (
                "Blue drinking bottle with black cap"
            ),
            "colour": "blue",
            "brand": "",
            "location": "Cafeteria",
            "report_date": "2026-06-17",
        },
        {
            "report_id": 3,
            "item_name": "Black Laptop Bag",
            "category": "bag",
            "description": (
                "Black laptop carrying bag "
                "with shoulder strap"
            ),
            "colour": "black",
            "brand": "HP",
            "location": "Lecture Hall",
            "report_date": "2026-06-20",
        },
    ]

    results = rank_matches(
        lost_report,
        found_reports,
    )

    print("=" * 60)
    print("MATCHAI FINAL MATCHING TEST")
    print("=" * 60)

    for position, result in enumerate(
        results,
        start=1,
    ):
        print(
            f"\n{position}. {result['item_name']}"
        )

        print(
            f"Final score: "
            f"{result['final_score']:.2%}"
        )

        print(
            f"Strength: "
            f"{result['match_strength']}"
        )

        print(
            f"Text: "
            f"{result['text_similarity']:.2%}"
        )

        print(
            f"Category: "
            f"{result['category_similarity']:.2%}"
        )

        print(
            f"Colour: "
            f"{result['colour_similarity']:.2%}"
        )

        print(
            f"Brand: "
            f"{result['brand_similarity']:.2%}"
        )

        print(
            f"Location: "
            f"{result['location_similarity']:.2%}"
        )

        print(
            f"Date: "
            f"{result['date_similarity']:.2%}"
        )

        print("Reasons:")

        for reason in result["explanations"]:
            print(
                f"- {reason}"
            )


if __name__ == "__main__":
    main()