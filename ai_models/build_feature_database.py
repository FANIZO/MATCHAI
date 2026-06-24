from ai_models.cnn_features import (
    extract_and_save_features,
)
from database.database_manager import (
    get_all_reports,
    initialize_database,
    update_report_feature_path,
)


def main() -> None:
    initialize_database()

    reports = get_all_reports()

    if not reports:
        print("No reports were found.")
        return

    print("=" * 60)
    print("MATCHAI FEATURE DATABASE BUILDER")
    print("=" * 60)

    successful = 0
    failed = 0
    skipped = 0

    for report in reports:
        report_id = report["report_id"]
        report_type = report["report_type"]
        image_path = report.get("image_path")
        existing_feature_path = report.get(
            "feature_path"
        )

        if existing_feature_path:
            print(
                f"Report {report_id}: "
                "feature already exists."
            )

            skipped += 1
            continue

        if not image_path:
            print(
                f"Report {report_id}: "
                "no image available."
            )

            failed += 1
            continue

        try:
            feature_path = (
                extract_and_save_features(
                    image_path=image_path,
                    report_id=report_id,
                    report_type=report_type,
                )
            )

            update_report_feature_path(
                report_id=report_id,
                feature_path=feature_path,
            )

            print(
                f"Report {report_id}: "
                f"saved {feature_path}"
            )

            successful += 1

        except Exception as error:
            print(
                f"Report {report_id}: "
                f"failed — {error}"
            )

            failed += 1

    print("\nSummary")
    print(f"Created: {successful}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()