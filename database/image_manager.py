from pathlib import Path
from uuid import uuid4

from PIL import Image

from config import RAW_IMAGE_DIR, SUPPORTED_IMAGE_TYPES


def save_uploaded_image(
    uploaded_file,
    report_type: str,
) -> str:
    if uploaded_file is None:
        raise ValueError("No image was uploaded")

    extension = Path(uploaded_file.name).suffix.lower().replace(".", "")

    if extension not in SUPPORTED_IMAGE_TYPES:
        raise ValueError(
            f"Unsupported image type: {extension}"
        )

    target_folder = RAW_IMAGE_DIR / report_type
    target_folder.mkdir(parents=True, exist_ok=True)

    unique_name = f"{uuid4().hex}.{extension}"
    image_path = target_folder / unique_name

    image = Image.open(uploaded_file).convert("RGB")
    image.save(image_path)

    return str(image_path)