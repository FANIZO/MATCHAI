from pathlib import Path

from config import (
    FINAL_MODEL_METADATA_PATH,
    FINAL_MODEL_PATH,
    MODEL_DIR,
)


def main() -> None:
    print("\nMODEL FILES TEST")
    print("-" * 50)

    model_files = {
        "Final match classifier": (
            FINAL_MODEL_PATH
        ),
        "Final model metadata": (
            FINAL_MODEL_METADATA_PATH
        ),
        "Text classifier": (
            MODEL_DIR
            / "text_classifier.joblib"
        ),
    }

    missing_files = []

    for model_name, model_path in (
        model_files.items()
    ):
        path = Path(model_path)

        if path.exists():
            print(
                f"{model_name}: FOUND"
            )

            print(
                f"  Path: {path}"
            )

            print(
                f"  Size: "
                f"{path.stat().st_size} bytes"
            )

        else:
            print(
                f"{model_name}: MISSING"
            )

            missing_files.append(
                model_name
            )

    if missing_files:
        raise FileNotFoundError(
            "Missing model files: "
            + ", ".join(missing_files)
        )

    print(
        "\nMODEL FILES TEST PASSED"
    )


if __name__ == "__main__":
    main()