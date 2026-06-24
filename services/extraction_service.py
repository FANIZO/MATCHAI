import re

import streamlit as st

from ai_models.text_classifier import TextClassifier
from config import ITEM_CATEGORIES


def load_text_classifier() -> TextClassifier:
    return TextClassifier()

COLOUR_TERMS = [
    "black", "white", "red", "blue", "navy", "green", "yellow",
    "orange", "purple", "pink", "brown", "grey", "gray", "silver",
    "gold", "beige", "maroon", "cream", "transparent", "multicolour",
]

KNOWN_BRANDS = [
    "Adidas", "Nike", "Puma", "Samsung", "Apple", "Huawei", "Xiaomi",
    "Oppo", "Vivo", "Dell", "HP", "Lenovo", "Acer", "Asus", "Casio",
    "Canon", "Sony", "JBL", "Logitech", "Targus", "Fossil", "Rolex", "Naviforce",
    "Seiko", "Citizen", "Uniqlo", "Guess", "Gucci", "Prada",
]

CATEGORY_KEYWORDS = {
    "watch": [
        "watch", "wristwatch", "timepiece",
        "analogue watch", "analog watch", "digital watch",
    ],
    "phone": [
        "phone", "mobile", "smartphone", "iphone", "android",
    ],
    "wallet": [
        "wallet", "purse", "card holder", "cardholder",
    ],
    "bag": [
        "bag", "backpack", "rucksack", "handbag", "school bag",
    ],
    "keys": [
        "key", "keys", "keychain", "key ring",
    ],
    "bottle": [
        "bottle", "flask", "tumbler", "water bottle",
    ],
    "umbrella": ["umbrella"],
    "headphones": [
        "headphone", "headphones", "earphone", "earphones",
        "earbuds", "airpods", "headset",
    ],
    "laptop": [
        "laptop", "notebook computer", "macbook",
    ],
    "document": [
        "document", "file", "folder", "certificate", "paper",
    ],
    "student_card": [
        "student card", "student id", "identity card", "id card",
    ],
    "calculator": ["calculator"],
}

CATEGORY_DISPLAY_NAMES = {
    "phone": "Phone",
    "wallet": "Wallet",
    "bag": "Bag",
    "keys": "Keys",
    "bottle": "Bottle",
    "umbrella": "Umbrella",
    "headphones": "Headphones",
    "laptop": "Laptop",
    "watch": "Watch",
    "document": "Document",
    "student_card": "Student Card",
    "calculator": "Calculator",
}


def extract_category_from_description(
    description: str,
) -> str | None:
    lowered = description.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in sorted(
            keywords,
            key=len,
            reverse=True,
        ):
            if re.search(
                rf"\b{re.escape(keyword)}\b",
                lowered,
            ):
                return category

    return None


def extract_brand_from_description(description: str) -> str:
    lowered = description.lower()

    for brand in KNOWN_BRANDS:
        if re.search(rf"\b{re.escape(brand.lower())}\b", lowered):
            return brand

    patterns = [
        r"\bbrand(?:ed)?\s+(?:is\s+)?([A-Za-z][A-Za-z0-9-]{1,20})",
        r"\bmade\s+by\s+([A-Za-z][A-Za-z0-9-]{1,20})",
        r"\bfrom\s+([A-Z][A-Za-z0-9-]{1,20})",
    ]

    for pattern in patterns:
        match = re.search(pattern, description)
        if match:
            return match.group(1).strip().title()

    return ""


def find_category_keyword_span(
    description: str,
    category: str,
) -> tuple[int, int] | None:
    lowered = description.lower()

    for keyword in sorted(
        CATEGORY_KEYWORDS.get(category, []),
        key=len,
        reverse=True,
    ):
        match = re.search(
            rf"\b{re.escape(keyword)}\b",
            lowered,
        )
        if match:
            return match.start(), match.end()

    return None


def extract_colour_details(
    description: str,
    category: str,
) -> dict[str, str]:
    lowered = description.lower()
    matches = []

    for colour in sorted(COLOUR_TERMS, key=len, reverse=True):
        for match in re.finditer(
            rf"\b{re.escape(colour)}\b",
            lowered,
        ):
            matches.append(
                {
                    "colour": "grey" if colour == "gray" else colour,
                    "start": match.start(),
                    "end": match.end(),
                }
            )

    if not matches:
        return {"primary": "", "secondary": "", "display": ""}

    item_span = find_category_keyword_span(description, category)

    accessory_terms = [
        "zip", "zipper", "strap", "logo", "lining",
        "keychain", "key chain", "pocket", "case",
        "cover", "screen", "button", "buckle",
        "clasp", "mark", "scratch", "stitch",
        "trim", "edge", "handle", "frame",
    ]

    scored = []

    for match in matches:
        score = 0.0
        start = match["start"]
        end = match["end"]

        if item_span is not None:
            item_start, item_end = item_span

            if end <= item_start:
                distance = item_start - end
                if distance <= 5:
                    score += 12
                elif distance <= 15:
                    score += 9
                elif distance <= 30:
                    score += 6
                elif distance <= 50:
                    score += 3
            elif start >= item_end:
                distance = start - item_end
                if distance <= 8:
                    score += 5
                elif distance <= 20:
                    score += 2

        score += max(
            0.0,
            4.0 - (start / max(len(lowered), 1)) * 4.0,
        )

        context = lowered[
            max(0, start - 22):
            min(len(lowered), end + 30)
        ]

        if any(
            re.search(rf"\b{re.escape(term)}\b", context)
            for term in accessory_terms
        ):
            score -= 7

        before = lowered[max(0, start - 18):start]
        if re.search(r"\bwith\s+(?:a|an|the)?\s*$", before):
            score -= 5

        scored.append((score, match))

    scored.sort(
        key=lambda item: (
            item[0],
            -item[1]["start"],
        ),
        reverse=True,
    )

    primary = scored[0][1]["colour"]
    secondary = []

    for _, match in scored[1:]:
        colour = match["colour"]
        if colour != primary and colour not in secondary:
            secondary.append(colour)

    primary_title = primary.title()
    secondary_title = ", ".join(
        colour.title()
        for colour in secondary
    )

    display = (
        f"{primary_title} with {secondary_title} accents"
        if secondary_title
        else primary_title
    )

    return {
        "primary": primary_title,
        "secondary": secondary_title,
        "display": display,
    }


def extract_colour_from_description(
    description: str,
    category: str,
) -> str:
    return extract_colour_details(
        description,
        category,
    )["display"]


def build_item_name(
    category: str,
    colour: str,
    brand: str,
) -> str:
    default_category_name = (
        str(category)
        .replace("_", " ")
        .strip()
        .title()
    )

    category_name = CATEGORY_DISPLAY_NAMES.get(
        category,
        default_category_name,
    )

    parts = [
        value
        for value in (
            colour,
            brand,
            category_name,
        )
        if value
    ]

    return " ".join(parts)

def extract_smart_report_fields(
    description: str,
) -> dict[str, str | float]:
    keyword_category = extract_category_from_description(
        description
    )

    if keyword_category in ITEM_CATEGORIES:
        final_category = keyword_category
        confidence = 1.0
    else:
        classifier = load_text_classifier()
        predicted_category, confidence = (
            classifier.predict_category(description)
        )
        final_category = (
            predicted_category
            if predicted_category in ITEM_CATEGORIES
            else ITEM_CATEGORIES[0]
        )

    colour_details = extract_colour_details(
        description,
        final_category,
    )
    brand = extract_brand_from_description(description)

    item_name = build_item_name(
        final_category,
        colour_details["primary"],
        brand,
    )

    return {
        "item_name": item_name,
        "category": final_category,
        "colour": colour_details["display"],
        "primary_colour": colour_details["primary"],
        "secondary_colours": colour_details["secondary"],
        "brand": brand,
        "confidence": float(confidence),
    }


def reset_smart_report_state(prefix: str) -> None:
    for key in [
        f"{prefix}_analysis",
        f"{prefix}_item_name",
        f"{prefix}_category",
        f"{prefix}_category_select",
        f"{prefix}_colour",
        f"{prefix}_brand",
        f"{prefix}_description",
        f"{prefix}_location",
        f"{prefix}_contact_name",
        f"{prefix}_contact_email",
        f"{prefix}_contact_phone",
        f"{prefix}_last_description",
        f"{prefix}_analysis_error",
    ]:
        st.session_state.pop(key, None)
