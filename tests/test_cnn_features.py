from pathlib import Path

from ai_models.cnn_features import (
    extract_image_features,
)
from config import RAW_IMAGE_DIR


def find_first_image() -> Path:
    supported_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
    }

    image_files = [
        path
        for path in RAW_IMAGE_DIR.rglob("*")
        if (
            path.is_file()
            and path.suffix.lower()
            in supported_extensions
        )
    ]

    if not image_files:
        raise FileNotFoundError(
            "No uploaded report images were found."
        )

    return image_files[0]


def main() -> None:
    image_path = find_first_image()

    print("=" * 60)
    print("MATCHAI CNN FEATURE TEST")
    print("=" * 60)

    print(f"Image: {image_path}")

    features = extract_image_features(
        image_path
    )

    print(
        f"Feature vector shape: {features.shape}"
    )

    print(
        f"Data type: {features.dtype}"
    )

    print(
        f"Vector norm: "
        f"{float((features ** 2).sum() ** 0.5):.6f}"
    )

    print(
        "\nCNN feature extraction succeeded."
    )


if __name__ == "__main__":
    main()