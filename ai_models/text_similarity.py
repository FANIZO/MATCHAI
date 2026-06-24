from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text: str) -> str:
    if text is None:
        return ""

    return " ".join(
        str(text)
        .lower()
        .strip()
        .split()
    )


def calculate_text_similarity(
    text_a: str,
    text_b: str,
) -> float:
    cleaned_a = clean_text(text_a)
    cleaned_b = clean_text(text_b)

    if not cleaned_a or not cleaned_b:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(
            [cleaned_a, cleaned_b]
        )
    except ValueError:
        return 0.0

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2],
    )[0][0]

    return float(similarity)


def rank_text_matches(
    source_report: dict,
    candidate_reports: list[dict],
) -> list[dict]:
    ranked_results = []

    source_text = build_report_text(
        source_report
    )

    for report in candidate_reports:
        candidate_text = build_report_text(
            report
        )

        similarity = calculate_text_similarity(
            source_text,
            candidate_text,
        )

        result = report.copy()
        result["text_similarity"] = similarity

        ranked_results.append(result)

    ranked_results.sort(
        key=lambda item: item["text_similarity"],
        reverse=True,
    )

    return ranked_results
def build_report_text(
    report: dict,
) -> str:
    fields = [
        report.get("item_name", ""),
        report.get("category", ""),
        report.get("description", ""),
        report.get("colour", ""),
        report.get("brand", ""),
        report.get("location", ""),
    ]

    return " ".join(
        str(field).strip()
        for field in fields
        if field
    )