import subprocess
import sys


TEST_MODULES = [
    "tests.test_database_operations",
    "tests.test_input_validation",
    "tests.test_model_files",
    "tests.test_matching_pipeline",
    "tests.test_performance",
]


def main() -> None:
    print("\nMATCHAI COMPLETE TEST SUITE")
    print("=" * 60)

    passed_tests = []
    failed_tests = []

    for test_module in TEST_MODULES:
        print(
            f"\nRunning: {test_module}"
        )

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                test_module,
            ],
            check=False,
        )

        if result.returncode == 0:
            passed_tests.append(
                test_module
            )

            print(
                f"PASSED: {test_module}"
            )

        else:
            failed_tests.append(
                test_module
            )

            print(
                f"FAILED: {test_module}"
            )

    print("\n" + "=" * 60)

    print(
        f"Tests passed: "
        f"{len(passed_tests)}"
    )

    print(
        f"Tests failed: "
        f"{len(failed_tests)}"
    )

    if failed_tests:
        print(
            "\nFailed modules:"
        )

        for module in failed_tests:
            print(
                f"- {module}"
            )

        raise SystemExit(1)

    print(
        "\nALL MATCHAI TESTS PASSED"
    )


if __name__ == "__main__":
    main()