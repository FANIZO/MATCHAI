from functools import lru_cache
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
)
from tensorflow.keras.preprocessing import image


IMAGE_SIZE = (224, 224)


@lru_cache(maxsize=1)
def load_feature_extractor() -> tf.keras.Model:
    """
    Load MobileNetV2 without its final classification layer.

    Global average pooling produces one feature vector
    for each input image.
    """
    model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=(224, 224, 3),
    )

    model.trainable = False

    return model


def validate_image_path(
    image_path: str | Path,
) -> Path:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image was not found: {path}"
        )

    supported_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
    }

    if path.suffix.lower() not in supported_extensions:
        raise ValueError(
            f"Unsupported image type: {path.suffix}"
        )

    return path


def extract_image_features(
    image_path: str | Path,
) -> np.ndarray:
    """
    Convert an image into a normalised CNN feature vector.
    """
    path = validate_image_path(image_path)

    loaded_image = image.load_img(
        path,
        target_size=IMAGE_SIZE,
        color_mode="rgb",
    )

    image_array = image.img_to_array(
        loaded_image
    )

    image_batch = np.expand_dims(
        image_array,
        axis=0,
    )

    processed_batch = preprocess_input(
        image_batch
    )

    model = load_feature_extractor()

    features = model.predict(
        processed_batch,
        verbose=0,
    )[0]

    feature_norm = np.linalg.norm(features)

    if feature_norm > 0:
        features = features / feature_norm

    return features.astype(np.float32)


def save_feature_vector(
    features: np.ndarray,
    output_path: str | Path,
) -> None:
    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    np.save(
        path,
        features,
    )


def load_feature_vector(
    feature_path: str | Path,
) -> np.ndarray:
    path = Path(feature_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Feature file was not found: {path}"
        )

    return np.load(path)

def save_feature_vector(
    features: np.ndarray,
    output_path: str | Path,
) -> str:
    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    np.save(
        path,
        features,
        allow_pickle=False,
    )

    return str(path)


def load_feature_vector(
    feature_path: str | Path,
) -> np.ndarray:
    path = Path(feature_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Feature vector not found: {path}"
        )

    features = np.load(
        path,
        allow_pickle=False,
    )

    return features.astype(
        np.float32
    )


def create_feature_path(
    report_id: int,
    report_type: str,
) -> Path:
    from config import FEATURE_DIR

    target_folder = (
        FEATURE_DIR / report_type
    )

    target_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    return (
        target_folder
        / f"report_{report_id}.npy"
    )


def extract_and_save_features(
    image_path: str | Path,
    report_id: int,
    report_type: str,
) -> str:
    features = extract_image_features(
        image_path
    )

    feature_path = create_feature_path(
        report_id=report_id,
        report_type=report_type,
    )

    return save_feature_vector(
        features,
        feature_path,
    )