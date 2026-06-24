from ai_models.text_classifier import TextClassifier


def main() -> None:
    classifier = TextClassifier()

    test_descriptions = [
        "Black Samsung mobile phone with cracked display",
        "Blue backpack with two zipped compartments",
        "Silver Casio scientific calculator",
        "Brown leather wallet with student card",
        "White wireless earbuds in charging case",
        "Large black umbrella with wooden handle",
    ]

    print("=" * 60)
    print("MATCHAI TEXT CLASSIFIER PREDICTION TEST")
    print("=" * 60)

    for description in test_descriptions:
        category, confidence = (
            classifier.predict_category(description)
        )

        print(f"\nDescription: {description}")
        print(f"Predicted category: {category}")
        print(f"Confidence: {confidence:.2%}")


if __name__ == "__main__":
    main()