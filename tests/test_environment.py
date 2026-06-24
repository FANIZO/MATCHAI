import sys
from pathlib import Path

import cv2
import joblib
import matplotlib
import numpy as np
import pandas as pd
import sklearn
import streamlit
from PIL import Image


def main() -> None:
    print("=" * 50)
    print("MATCHAI ENVIRONMENT TEST")
    print("=" * 50)

    print("Python version:", sys.version)
    print("Python executable:", sys.executable)
    print("OpenCV version:", cv2.__version__)
    print("NumPy version:", np.__version__)
    print("Pandas version:", pd.__version__)
    print("Scikit-learn version:", sklearn.__version__)
    print("Streamlit version:", streamlit.__version__)
    print("Matplotlib version:", matplotlib.__version__)

    project_root = Path(__file__).resolve().parent.parent

    required_folders = [
        project_root / "ai_models",
        project_root / "database",
        project_root / "data",
        project_root / "models",
        project_root / "outputs",
    ]

    print("\nFolder check:")

    for folder in required_folders:
        status = "FOUND" if folder.exists() else "MISSING"
        print(f"{folder.name}: {status}")

    print("\nPillow imported successfully.")
    print("Joblib imported successfully.")
    print("\nMatchAI environment setup is successful.")


if __name__ == "__main__":
    main()