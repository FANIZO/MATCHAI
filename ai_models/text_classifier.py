from pathlib import Path

import joblib

from config import MODEL_DIR


MODEL_PATH = MODEL_DIR / "text_classifier.joblib"


class TextClassifier:
    def __init__(
        self,
        model_path: Path = MODEL_PATH,
    ) -> None:
        if not model_path.exists():
            raise FileNotFoundError(
                "Text classifier model was not found. "
                "Run the training script first."
            )

        self.pipeline = joblib.load(model_path)

    def predict_category(
        self,
        description: str,
    ) -> tuple[str, float]:
        cleaned_description = description.strip()

        if not cleaned_description:
            raise ValueError(
                "Description cannot be empty."
            )

        predicted_category = self.pipeline.predict(
            [cleaned_description]
        )[0]

        probabilities = self.pipeline.predict_proba(
            [cleaned_description]
        )[0]

        highest_probability = float(
            probabilities.max()
        )

        return (
            str(predicted_category),
            highest_probability,
        )