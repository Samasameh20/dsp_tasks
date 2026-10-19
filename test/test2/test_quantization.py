
"""Automatic tests for DSP quantization: Test Case 1 and Test Case 2."""

import sys
from pathlib import Path

# Allow importing signal_operations.py from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from signal_operations import quantize_signal


TEST_DIR = Path(__file__).resolve().parent

# Change these names only if your actual filenames differ.
CASE1_INPUT = TEST_DIR / "Quan1_input.txt"
CASE1_OUTPUT = TEST_DIR / "Quan1_out.txt"

CASE2_INPUT = TEST_DIR / "Quan2_input.txt"
CASE2_OUTPUT = TEST_DIR / "Quan2_Out.txt"

TOLERANCE = 0.01


def read_data_file(file_path, columns):
    """Read a supplied test file, skipping its three header lines."""
    if not file_path.exists():
        raise FileNotFoundError(f"Test file not found: {file_path}")

    rows = []

    with file_path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    # The supplied files have three header lines.
    for line_number, line in enumerate(lines[3:], start=4):
        parts = line.split()

        if not parts:
            continue

        if len(parts) != columns:
            # Ignore non-data lines, but reject malformed data rows.
            continue

        try:
            rows.append(parts)
        except ValueError as error:
            raise ValueError(
                f"Invalid data in {file_path.name}, line {line_number}"
            ) from error

    if not rows:
        raise ValueError(f"No data rows found in {file_path}")

    return rows


def load_signal(file_path):
    """Load the instructor's input file into our signal dictionary."""
    rows = read_data_file(file_path, columns=2)

    indices = []
    samples = []

    for row in rows:
        indices.append(int(row[0]))
        samples.append(float(row[1]))

    return {
        "indices": indices,
        "samples": samples,
        "name": file_path.name,
    }


def check_close(actual, expected, label, failures):
    """Compare numeric lists using the instructor's tolerance."""
    if len(actual) != len(expected):
        failures.append(
            f"{label}: length mismatch "
            f"(actual {len(actual)}, expected {len(expected)})"
        )
        return

    for i, (got, wanted) in enumerate(zip(actual, expected)):
        if abs(float(got) - float(wanted)) >= TOLERANCE:
            failures.append(
                f"{label}[{i}]: got {got}, expected {wanted}"
            )


def check_encoded(actual, expected, failures):
    """Compare binary codes exactly."""
    if len(actual) != len(expected):
        failures.append(
            "Encoded values: length mismatch "
            f"(actual {len(actual)}, expected {len(expected)})"
        )
        return

    for i, (got, wanted) in enumerate(zip(actual, expected)):
        if str(got) != str(wanted):
            failures.append(
                f"Encoded values[{i}]: got {got!r}, "
                f"expected {wanted!r}"
            )


def test_case_1():
    """Test 1: 3 bits, hence 8 levels."""
    print("\n--- Quantization Test Case 1: 3 bits ---")

    signal = load_signal(CASE1_INPUT)
    expected_rows = read_data_file(CASE1_OUTPUT, columns=2)

    result = quantize_signal(signal, levels=2 ** 3)

    expected_encoded = [row[0] for row in expected_rows]
    expected_quantized = [float(row[1]) for row in expected_rows]

    failures = []

    check_encoded(
        result["encoded_signal"],
        expected_encoded,
        failures,
    )
    check_close(
        result["quantized_samples"],
        expected_quantized,
        "Quantized values",
        failures,
    )

    report_result("Test Case 1", failures)


def test_case_2():
    """Test 2: 4 levels; check interval, code, value, and error."""
    print("\n--- Quantization Test Case 2: 4 levels ---")

    signal = load_signal(CASE2_INPUT)
    expected_rows = read_data_file(CASE2_OUTPUT, columns=4)

    result = quantize_signal(signal, levels=4)

    expected_intervals = [int(row[0]) for row in expected_rows]
    expected_encoded = [row[1] for row in expected_rows]
    expected_quantized = [float(row[2]) for row in expected_rows]
    expected_errors = [float(row[3]) for row in expected_rows]

    # The implementation returns one-based interval numbers separately
    # from the zero-based indices used to generate binary codes.
    actual_intervals = result.get(
        "interval_indices",
        result.get("intervals", []),
    )

    failures = []

    if len(actual_intervals) != len(expected_intervals):
        failures.append(
            "Interval indices: length mismatch "
            f"(actual {len(actual_intervals)}, "
            f"expected {len(expected_intervals)})"
        )
    else:
        for i, (got, wanted) in enumerate(
            zip(actual_intervals, expected_intervals)
        ):
            if int(got) != wanted:
                failures.append(
                    f"Interval indices[{i}]: got {got}, "
                    f"expected {wanted}"
                )

    check_encoded(
        result["encoded_signal"],
        expected_encoded,
        failures,
    )
    check_close(
        result["quantized_samples"],
        expected_quantized,
        "Quantized values",
        failures,
    )
    check_close(
        result["errors"],
        expected_errors,
        "Sampled errors",
        failures,
    )

    report_result("Test Case 2", failures)


def report_result(test_name, failures):
    if failures:
        print(f"❌ {test_name} FAILED")

        for failure in failures:
            print(f"  - {failure}")
    else:
        print(f"✅ {test_name} PASSED")


def main():
    failures = 0

    for test_function in (test_case_1, test_case_2):
        try:
            test_function()
        except Exception as error:
            failures += 1
            print(f"❌ Test could not run: {error}")

    if failures:
        print("\nSome tests could not run. Check the file paths above.")
        return

    print("\nFinished running quantization tests.")
    print("Review the individual test results above.")


if __name__ == "__main__":
    main()
