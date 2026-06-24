from ai_models.cnn_features import extract_and_save_features
from database.database_manager import (
    add_report,
    update_report_feature_path,
)
from database.image_manager import save_uploaded_image


def save_report_with_features(
    *,
    report_type: str,
    item_name: str,
    category: str,
    description: str,
    colour: str,
    brand: str,
    location: str,
    report_date: str,
    contact_name: str,
    contact_email: str,
    contact_phone: str,
    uploaded_image,
) -> tuple[int, str, str | None]:
    """Save a report, its image, and its CNN feature path.

    Returns:
        (report_id, image_path, feature_warning)
    """
    image_path = save_uploaded_image(
        uploaded_file=uploaded_image,
        report_type=report_type,
    )

    report_id = add_report(
        report_type=report_type,
        item_name=item_name,
        category=category,
        description=description,
        colour=colour,
        brand=brand,
        location=location,
        report_date=report_date,
        contact_name=contact_name,
        contact_email=contact_email,
        contact_phone=contact_phone,
        image_path=image_path,
    )

    feature_warning = None

    try:
        feature_path = extract_and_save_features(
            image_path=image_path,
            report_id=report_id,
            report_type=report_type,
        )

        update_report_feature_path(
            report_id=report_id,
            feature_path=feature_path,
        )

    except Exception as error:
        feature_warning = str(error)

    return report_id, image_path, feature_warning
