from pathlib import Path

import joblib
import pandas as pd

from config import (
    FINAL_MODEL_METADATA_PATH,
    FINAL_MODEL_PATH,
)
from ai_models.fuzzy_rules import (
    calculate_attribute_similarities,
)
from ai_models.text_similarity import (
    calculate_text_similarity,
    build_report_text,
)
from ai_models.knn_matcher import (
    calculate_report_image_similarity,
)



DEFAULT_WEIGHTS = {
    "image_similarity": 0.30,
    "text_similarity": 0.20,
    "category_similarity": 0.15,
    "colour_similarity": 0.10,
    "brand_similarity": 0.10,
    "location_similarity": 0.075,
    "date_similarity": 0.075,
}


def calculate_weighted_score(
    scores: dict[str, float],
    weights: dict[str, float] | None = None,
) -> float:
    selected_weights = (
        weights
        if weights is not None
        else DEFAULT_WEIGHTS
    )

    total_weight = sum(
        selected_weights.values()
    )

    if total_weight <= 0:
        raise ValueError(
            "The total matching weight must be greater than zero."
        )

    weighted_total = 0.0

    for score_name, weight in selected_weights.items():
        score = scores.get(
            score_name,
            0.0,
        )

        weighted_total += score * weight

    final_score = weighted_total / total_weight

    return max(
        0.0,
        min(1.0, float(final_score)),
    )


def classify_match_strength(
    final_score: float,
) -> str:
    if final_score >= 0.80:
        return "Very Strong Match"

    if final_score >= 0.65:
        return "Strong Match"

    if final_score >= 0.50:
        return "Moderate Match"

    if final_score >= 0.35:
        return "Weak Match"

    return "Very Weak Match"


def create_match_explanation(
    scores: dict[str, float],
) -> list[str]:
    explanations = []
    if scores["image_similarity"] >= 0.80:
        explanations.append(
            "The uploaded item images are highly similar."
        )

    elif scores["image_similarity"] >= 0.60:
        explanations.append(
            "The uploaded images share several visual features."
        )

    else:
        explanations.append(
            "The uploaded images have limited visual similarity."
        )

    if scores["category_similarity"] == 1.0:
        explanations.append(
            "The item categories are identical."
        )
    else:
        explanations.append(
            "The item categories are different."
        )

    if scores["text_similarity"] >= 0.65:
        explanations.append(
            "The report descriptions are highly similar."
        )
    elif scores["text_similarity"] >= 0.40:
        explanations.append(
            "The report descriptions share some matching details."
        )
    else:
        explanations.append(
            "The report descriptions have limited similarity."
        )

    if scores["colour_similarity"] >= 0.80:
        explanations.append(
            "The reported colours are identical or closely related."
        )

    if scores["brand_similarity"] >= 0.80:
        explanations.append(
            "The reported brands match closely."
        )

    if scores["location_similarity"] >= 0.75:
        explanations.append(
            "The reported locations are the same or nearby."
        )

    if scores["date_similarity"] >= 0.90:
        explanations.append(
            "The lost and found dates are the same or one day apart."
        )

    return explanations


def compare_reports(
    source_report: dict,
    candidate_report: dict,
) -> dict:
    source_text = build_report_text(
        source_report
    )

    candidate_text = build_report_text(
        candidate_report
    )

    text_score = calculate_text_similarity(
        source_text,
        candidate_text,
    )

    image_score = 0.0

    try:
        image_score = (
            calculate_report_image_similarity(
                source_report,
                candidate_report,
            )
        )

    except (
        FileNotFoundError,
        ValueError,
        OSError,
    ):
        image_score = 0.0
        
    scores = {
        "image_similarity": image_score,
        "text_similarity": text_score,
        **calculate_attribute_similarities(
            source_report,
            candidate_report,
        ),
    }

    final_score = calculate_weighted_score(
        scores
    )
    
    trained_probability, trained_model_name = (
        predict_trained_match(
            scores
        )
    )

    if trained_probability is not None:
        displayed_score = trained_probability
        score_method = (
            f"Machine Learning: "
            f"{trained_model_name}"
        )
    else:
        displayed_score = final_score
        score_method = (
            "Weighted Fuzzy Baseline"
        )

    return {
        **candidate_report,
        **scores,
        "weighted_score": final_score,
        "trained_probability": trained_probability,
        "final_score": displayed_score,
        "score_method": score_method,
        "match_strength": classify_match_strength(
            final_score
        ),
        "explanations": create_match_explanation(
            scores
        ),
    }

def load_trained_match_model():
    if not FINAL_MODEL_PATH.exists():
        return None, None

    model = joblib.load(
        FINAL_MODEL_PATH
    )

    metadata = None

    if FINAL_MODEL_METADATA_PATH.exists():
        metadata = joblib.load(
            FINAL_MODEL_METADATA_PATH
        )

    return model, metadata


def predict_trained_match(
    scores: dict[str, float],
) -> tuple[float | None, str | None]:
    model, metadata = (
        load_trained_match_model()
    )

    if model is None:
        return None, None

    feature_columns = [
        "image_similarity",
        "text_similarity",
        "category_similarity",
        "colour_similarity",
        "brand_similarity",
        "location_similarity",
        "date_similarity",
    ]

    feature_data = pd.DataFrame(
        [
            {
                feature_name: scores.get(
                    feature_name,
                    0.0,
                )
                for feature_name in feature_columns
            }
        ]
    )

    if hasattr(
        model,
        "predict_proba",
    ):
        probabilities = model.predict_proba(
            feature_data
        )[0]

        class_indexes = list(
            model.classes_
        )

        if 1 in class_indexes:
            match_index = (
                class_indexes.index(1)
            )

            probability = float(
                probabilities[match_index]
            )
        else:
            probability = 0.0

    else:
        prediction = model.predict(
            feature_data
        )[0]

        probability = float(
            prediction
        )

    model_name = (
        metadata.get("model_name")
        if metadata
        else type(model).__name__
    )

    return probability, model_name

def rank_matches(
    source_report: dict,
    candidate_reports: list[dict],
) -> list[dict]:
    results = [
        compare_reports(
            source_report,
            candidate,
        )
        for candidate in candidate_reports
    ]

    results.sort(
        key=lambda result: result["final_score"],
        reverse=True,
    )

    return results