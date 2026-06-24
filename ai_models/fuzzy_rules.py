from datetime import datetime
from difflib import SequenceMatcher


COLOUR_GROUPS = {
    "black": {
        "black",
        "dark black",
        "charcoal",
        "dark grey",
        "dark gray",
    },
    "blue": {
        "blue",
        "dark blue",
        "light blue",
        "navy",
        "navy blue",
        "sky blue",
    },
    "red": {
        "red",
        "dark red",
        "light red",
        "maroon",
        "burgundy",
    },
    "green": {
        "green",
        "dark green",
        "light green",
        "olive",
    },
    "grey": {
        "grey",
        "gray",
        "silver",
        "dark grey",
        "dark gray",
        "light grey",
        "light gray",
    },
    "white": {
        "white",
        "cream",
        "off white",
    },
    "brown": {
        "brown",
        "dark brown",
        "light brown",
        "tan",
        "beige",
    },
    "purple": {
        "purple",
        "violet",
        "lavender",
    },
    "yellow": {
        "yellow",
        "gold",
        "golden",
    },
    "orange": {
        "orange",
    },
    "pink": {
        "pink",
        "rose",
        "rose gold",
    },
}


def normalise_text(value: str | None) -> str:
    if value is None:
        return ""

    return " ".join(
        str(value)
        .lower()
        .strip()
        .replace("-", " ")
        .replace("_", " ")
        .split()
    )


def string_similarity(
    value_a: str | None,
    value_b: str | None,
) -> float:
    cleaned_a = normalise_text(value_a)
    cleaned_b = normalise_text(value_b)

    if not cleaned_a or not cleaned_b:
        return 0.0

    if cleaned_a == cleaned_b:
        return 1.0

    return float(
        SequenceMatcher(
            None,
            cleaned_a,
            cleaned_b,
        ).ratio()
    )


def category_similarity(
    category_a: str | None,
    category_b: str | None,
) -> float:
    cleaned_a = normalise_text(category_a)
    cleaned_b = normalise_text(category_b)

    if not cleaned_a or not cleaned_b:
        return 0.0

    return 1.0 if cleaned_a == cleaned_b else 0.0


def find_colour_group(
    colour: str | None,
) -> str | None:
    cleaned_colour = normalise_text(colour)

    if not cleaned_colour:
        return None

    for group_name, colour_names in COLOUR_GROUPS.items():
        if cleaned_colour in colour_names:
            return group_name

    return None


def colour_similarity(
    colour_a: str | None,
    colour_b: str | None,
) -> float:
    cleaned_a = normalise_text(colour_a)
    cleaned_b = normalise_text(colour_b)

    if not cleaned_a or not cleaned_b:
        return 0.0

    if cleaned_a == cleaned_b:
        return 1.0

    group_a = find_colour_group(cleaned_a)
    group_b = find_colour_group(cleaned_b)

    if group_a is not None and group_a == group_b:
        return 0.8

    lexical_score = string_similarity(
        cleaned_a,
        cleaned_b,
    )

    if lexical_score >= 0.75:
        return 0.6

    return 0.0


def brand_similarity(
    brand_a: str | None,
    brand_b: str | None,
) -> float:
    cleaned_a = normalise_text(brand_a)
    cleaned_b = normalise_text(brand_b)

    if not cleaned_a and not cleaned_b:
        return 0.5

    if not cleaned_a or not cleaned_b:
        return 0.0

    return string_similarity(
        cleaned_a,
        cleaned_b,
    )


def location_similarity(
    location_a: str | None,
    location_b: str | None,
) -> float:
    cleaned_a = normalise_text(location_a)
    cleaned_b = normalise_text(location_b)

    if not cleaned_a or not cleaned_b:
        return 0.0

    if cleaned_a == cleaned_b:
        return 1.0

    if (
        cleaned_a in cleaned_b
        or cleaned_b in cleaned_a
    ):
        return 0.85

    similarity = string_similarity(
        cleaned_a,
        cleaned_b,
    )

    if similarity >= 0.75:
        return 0.75

    if similarity >= 0.50:
        return 0.50

    return 0.0


def date_similarity(
    date_a: str | None,
    date_b: str | None,
) -> float:
    if not date_a or not date_b:
        return 0.0

    try:
        parsed_a = datetime.strptime(
            str(date_a),
            "%Y-%m-%d",
        ).date()

        parsed_b = datetime.strptime(
            str(date_b),
            "%Y-%m-%d",
        ).date()

    except ValueError:
        return 0.0

    day_difference = abs(
        (parsed_a - parsed_b).days
    )

    if day_difference == 0:
        return 1.0

    if day_difference == 1:
        return 0.9

    if day_difference <= 3:
        return 0.7

    if day_difference <= 7:
        return 0.4

    return 0.0


def calculate_attribute_similarities(
    source_report: dict,
    candidate_report: dict,
) -> dict[str, float]:
    return {
        "category_similarity": category_similarity(
            source_report.get("category"),
            candidate_report.get("category"),
        ),
        "colour_similarity": colour_similarity(
            source_report.get("colour"),
            candidate_report.get("colour"),
        ),
        "brand_similarity": brand_similarity(
            source_report.get("brand"),
            candidate_report.get("brand"),
        ),
        "location_similarity": location_similarity(
            source_report.get("location"),
            candidate_report.get("location"),
        ),
        "date_similarity": date_similarity(
            source_report.get("report_date"),
            candidate_report.get("report_date"),
        ),
    }