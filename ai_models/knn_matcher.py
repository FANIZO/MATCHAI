from pathlib import Path

import numpy as np
from sklearn.metrics.pairwise import (
    cosine_similarity,
)

from ai_models.cnn_features import (
    extract_image_features,
    load_feature_vector,
)


def calculate_feature_similarity(
    features_a: np.ndarray,
    features_b: np.ndarray,
) -> float:
    vector_a = features_a.reshape(
        1,
        -1,
    )

    vector_b = features_b.reshape(
        1,
        -1,
    )

    similarity = cosine_similarity(
        vector_a,
        vector_b,
    )[0][0]

    return max(
        0.0,
        min(1.0, float(similarity)),
    )


def get_report_features(
    report: dict,
) -> np.ndarray:
    feature_path = report.get(
        "feature_path"
    )

    if feature_path:
        path = Path(feature_path)

        if path.exists():
            return load_feature_vector(
                path
            )

    image_path = report.get(
        "image_path"
    )

    if not image_path:
        raise ValueError(
            "Report has no image or saved feature vector."
        )

    return extract_image_features(
        image_path
    )


def calculate_report_image_similarity(
    report_a: dict,
    report_b: dict,
) -> float:
    features_a = get_report_features(
        report_a
    )

    features_b = get_report_features(
        report_b
    )

    return calculate_feature_similarity(
        features_a,
        features_b,
    )


def rank_image_matches(
    source_report: dict,
    candidate_reports: list[dict],
) -> list[dict]:
    source_features = get_report_features(
        source_report
    )

    ranked_results = []

    for candidate in candidate_reports:
        result = candidate.copy()

        try:
            candidate_features = (
                get_report_features(
                    candidate
                )
            )

            similarity = (
                calculate_feature_similarity(
                    source_features,
                    candidate_features,
                )
            )

        except (
            FileNotFoundError,
            ValueError,
            OSError,
        ):
            similarity = 0.0

        result["image_similarity"] = similarity

        ranked_results.append(
            result
        )

    ranked_results.sort(
        key=lambda item: item[
            "image_similarity"
        ],
        reverse=True,
    )

    return ranked_results