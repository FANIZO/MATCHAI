from pathlib import Path

from ai_models.cnn_features import (
    load_feature_vector,
)
from database.database_manager import (
    get_all_reports,
    initialize_database,
)


def main() -> None:
    initialize_database()

    reports = get_all_reports()

    reports_with_features = [
        report
        for report in reports
        if report.get("feature_path")
    ]

    if not reports_with_features:
        raise ValueError(
            "No reports with saved features were found. "
            "Run build_feature_database first."
        )

    print("=" * 60)
    print("MATCHAI SAVED FEATURE TEST")
    print("=" * 60)

    for report in reports_with_features:
        feature_path = Path(
            report["feature_path"]
        )

        features = load_feature_vector(
            feature_path
        )

        print(
            f"Report {report['report_id']} | "
            f"{report['item_name']} | "
            f"Shape: {features.shape} | "
            f"Exists: {feature_path.exists()}"
        )


if __name__ == "__main__":
    main()