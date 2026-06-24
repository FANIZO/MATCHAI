def validate_report_input(
    item_name: str,
    description: str,
    location: str,
    contact_name: str,
    contact_email: str,
    image_provided: bool,
) -> list[str]:
    errors = []

    if not item_name.strip():
        errors.append(
            "Item name is required."
        )

    if not description.strip():
        errors.append(
            "Description is required."
        )

    if not location.strip():
        errors.append(
            "Location is required."
        )

    if not contact_name.strip():
        errors.append(
            "Contact name is required."
        )

    if not contact_email.strip():
        errors.append(
            "Contact email is required."
        )

    if image_provided is False:
        errors.append(
            "An item image is required."
        )

    return errors


def main() -> None:
    print("\nINPUT VALIDATION TEST")
    print("-" * 50)

    valid_errors = validate_report_input(
        item_name="Black Backpack",
        description=(
            "Black backpack with silver zip."
        ),
        location="Library",
        contact_name="Test User",
        contact_email="test@example.com",
        image_provided=True,
    )

    assert len(valid_errors) == 0

    print(
        "Valid report input: PASSED"
    )

    empty_errors = validate_report_input(
        item_name="",
        description="",
        location="",
        contact_name="",
        contact_email="",
        image_provided=False,
    )

    assert len(empty_errors) == 6

    print(
        "Empty required fields: PASSED"
    )

    partial_errors = validate_report_input(
        item_name="Phone",
        description="Black phone",
        location="",
        contact_name="Test User",
        contact_email="test@example.com",
        image_provided=True,
    )

    assert (
        "Location is required."
        in partial_errors
    )

    print(
        "Missing location detection: PASSED"
    )

    print(
        "\nINPUT VALIDATION TEST PASSED"
    )


if __name__ == "__main__":
    main()