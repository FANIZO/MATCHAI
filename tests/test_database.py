from database.database_manager import (
    add_report,
    get_all_reports,
    initialize_database,
)


def main() -> None:
    print("=" * 50)
    print("MATCHAI DATABASE TEST")
    print("=" * 50)

    initialize_database()

    report_id = add_report(
        report_type="lost",
        item_name="Black Backpack",
        category="bag",
        description="Black backpack with a silver zip",
        colour="black",
        brand="Adidas",
        location="Library",
        report_date="2026-06-17",
        contact_name="Test User",
        contact_email="test@example.com",
        contact_phone="0123456789",
        image_path=None,
    )

    print(f"Inserted test report with ID: {report_id}")

    reports = get_all_reports()

    print(f"Total reports found: {len(reports)}")

    for report in reports:
        print(report)

    print("\nDatabase test completed successfully.")


if __name__ == "__main__":
    main()