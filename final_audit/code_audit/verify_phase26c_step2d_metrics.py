"""
================================================================================
VERIFICATION SCRIPT: PHASE 26C STEP 2D
================================================================================

OFFICIAL TARGET:
  File: src/train/phase_26c_failure_audit.py

PURPOSE:
  Verify the metric semantics used in the official Project 1 baseline script.

THIS SCRIPT VERIFIES:
  1. What accuracy means at the sample level
  2. Whether digit accuracy and carry accuracy can diverge legitimately
  3. Whether aggregate accuracy can differ from exact-match accuracy
  4. That controlled synthetic examples produce expected metric values

THIS SCRIPT DOES NOT VERIFY:
  - Model training
  - Actual official result reproduction
  - Data split correctness
  - Mechanistic model interpretation

IMPORTANT PRINCIPLE:
  This script verifies metric semantics independently using synthetic truth/prediction
  pairs. No model is used.

================================================================================
"""

from math import isclose


# -----------------------------------------------------------------------------
# INDEPENDENT METRIC IMPLEMENTATION
# -----------------------------------------------------------------------------
def compute_sample_metrics(digit_true, digit_pred, carry_true, carry_pred):
    """
    Compute metrics for a single sample (one arithmetic case or one sequence).

    Returns:
        digit_accuracy_percent
        carry_accuracy_percent
        exact_match_percent
    """
    if not (len(digit_true) == len(digit_pred) == len(carry_true) == len(carry_pred)):
        raise ValueError("All input lists must have same length")

    n = len(digit_true)

    digit_correct = sum(int(t == p) for t, p in zip(digit_true, digit_pred))
    carry_correct = sum(int(t == p) for t, p in zip(carry_true, carry_pred))

    digit_accuracy = 100.0 * digit_correct / n
    carry_accuracy = 100.0 * carry_correct / n
    exact_match = 100.0 if (
        digit_true == digit_pred and carry_true == carry_pred
    ) else 0.0

    return digit_accuracy, carry_accuracy, exact_match


def compute_dataset_exact_match(samples):
    """
    Compute dataset-level exact match percentage across multiple samples.
    """
    total = len(samples)
    exact = 0

    for s in samples:
        _, _, ex = compute_sample_metrics(
            s["digit_true"], s["digit_pred"],
            s["carry_true"], s["carry_pred"]
        )
        if ex == 100.0:
            exact += 1

    return 100.0 * exact / total


def compute_dataset_mean_metric(samples, metric_index):
    """
    Mean of a per-sample metric across the dataset.
    metric_index:
      0 -> digit_accuracy
      1 -> carry_accuracy
      2 -> exact_match
    """
    vals = []
    for s in samples:
        metrics = compute_sample_metrics(
            s["digit_true"], s["digit_pred"],
            s["carry_true"], s["carry_pred"]
        )
        vals.append(metrics[metric_index])
    return sum(vals) / len(vals)


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def assert_close(label, actual, expected, tol=1e-9):
    if not isclose(actual, expected, rel_tol=tol, abs_tol=tol):
        raise AssertionError(f"{label} mismatch: actual={actual}, expected={expected}")


def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_case_data(d_true, d_pred, c_true, c_pred):
    print(f"digit_true = {d_true}")
    print(f"digit_pred = {d_pred}")
    print(f"carry_true = {c_true}")
    print(f"carry_pred = {c_pred}")
    print()


# -----------------------------------------------------------------------------
# CASES
# -----------------------------------------------------------------------------
def case_1_perfect_prediction():
    print_header("CASE 1: PERFECT PREDICTION")

    d_true = [3]
    d_pred = [3]
    c_true = [0]
    c_pred = [0]

    expected = (100.0, 100.0, 100.0)

    print_case_data(d_true, d_pred, c_true, c_pred)
    actual = compute_sample_metrics(d_true, d_pred, c_true, c_pred)

    print(f"Computed: digit={actual[0]:.2f}, carry={actual[1]:.2f}, exact={actual[2]:.2f}")
    print(f"Expected: digit={expected[0]:.2f}, carry={expected[1]:.2f}, exact={expected[2]:.2f}")

    assert_close("digit_accuracy", actual[0], expected[0])
    assert_close("carry_accuracy", actual[1], expected[1])
    assert_close("exact_match", actual[2], expected[2])

    print("✓ PASS")


def case_2_digit_wrong_carry_correct():
    print_header("CASE 2: DIGIT WRONG, CARRY CORRECT")

    d_true = [0]
    d_pred = [1]
    c_true = [1]
    c_pred = [1]

    expected = (0.0, 100.0, 0.0)

    print_case_data(d_true, d_pred, c_true, c_pred)
    actual = compute_sample_metrics(d_true, d_pred, c_true, c_pred)

    print(f"Computed: digit={actual[0]:.2f}, carry={actual[1]:.2f}, exact={actual[2]:.2f}")
    print(f"Expected: digit={expected[0]:.2f}, carry={expected[1]:.2f}, exact={expected[2]:.2f}")

    assert_close("digit_accuracy", actual[0], expected[0])
    assert_close("carry_accuracy", actual[1], expected[1])
    assert_close("exact_match", actual[2], expected[2])

    print("✓ PASS")
    print("✓ Confirms digit and carry accuracies can diverge legitimately.")


def case_3_digit_correct_carry_wrong():
    print_header("CASE 3: DIGIT CORRECT, CARRY WRONG")

    d_true = [9]
    d_pred = [9]
    c_true = [0]
    c_pred = [1]

    expected = (100.0, 0.0, 0.0)

    print_case_data(d_true, d_pred, c_true, c_pred)
    actual = compute_sample_metrics(d_true, d_pred, c_true, c_pred)

    print(f"Computed: digit={actual[0]:.2f}, carry={actual[1]:.2f}, exact={actual[2]:.2f}")
    print(f"Expected: digit={expected[0]:.2f}, carry={expected[1]:.2f}, exact={expected[2]:.2f}")

    assert_close("digit_accuracy", actual[0], expected[0])
    assert_close("carry_accuracy", actual[1], expected[1])
    assert_close("exact_match", actual[2], expected[2])

    print("✓ PASS")


def case_4_sequence_partial_correct():
    print_header("CASE 4: PARTIALLY CORRECT SEQUENCE")

    d_true = [0, 1, 0, 1]
    d_pred = [0, 0, 0, 0]  # 2/4 correct
    c_true = [1, 0, 1, 0]
    c_pred = [1, 0, 1, 0]  # 4/4 correct

    expected = (50.0, 100.0, 0.0)

    print_case_data(d_true, d_pred, c_true, c_pred)
    actual = compute_sample_metrics(d_true, d_pred, c_true, c_pred)

    print(f"Computed: digit={actual[0]:.2f}, carry={actual[1]:.2f}, exact={actual[2]:.2f}")
    print(f"Expected: digit={expected[0]:.2f}, carry={expected[1]:.2f}, exact={expected[2]:.2f}")

    assert_close("digit_accuracy", actual[0], expected[0])
    assert_close("carry_accuracy", actual[1], expected[1])
    assert_close("exact_match", actual[2], expected[2])

    print("✓ PASS")
    print("✓ Confirms 50% digit and 100% carry is metric-legitimate.")


def case_5_dataset_level_exact_match():
    print_header("CASE 5: DATASET-LEVEL EXACT MATCH")

    samples = [
        {
            "digit_true": [0],
            "digit_pred": [0],
            "carry_true": [0],
            "carry_pred": [0],
        },
        {
            "digit_true": [1],
            "digit_pred": [0],  # digit wrong
            "carry_true": [0],
            "carry_pred": [0],
        },
        {
            "digit_true": [9],
            "digit_pred": [9],
            "carry_true": [1],
            "carry_pred": [1],
        },
    ]

    expected_dataset_exact = 100.0 * 2 / 3
    expected_mean_digit = (100.0 + 0.0 + 100.0) / 3
    expected_mean_carry = (100.0 + 100.0 + 100.0) / 3

    actual_dataset_exact = compute_dataset_exact_match(samples)
    actual_mean_digit = compute_dataset_mean_metric(samples, 0)
    actual_mean_carry = compute_dataset_mean_metric(samples, 1)

    print(f"Expected dataset exact match: {expected_dataset_exact:.2f}%")
    print(f"Computed dataset exact match: {actual_dataset_exact:.2f}%")
    print()
    print(f"Expected mean digit accuracy: {expected_mean_digit:.2f}%")
    print(f"Computed mean digit accuracy: {actual_mean_digit:.2f}%")
    print()
    print(f"Expected mean carry accuracy: {expected_mean_carry:.2f}%")
    print(f"Computed mean carry accuracy: {actual_mean_carry:.2f}%")

    assert_close("dataset_exact_match", actual_dataset_exact, expected_dataset_exact)
    assert_close("dataset_mean_digit", actual_mean_digit, expected_mean_digit)
    assert_close("dataset_mean_carry", actual_mean_carry, expected_mean_carry)

    print("✓ PASS")
    print("✓ Confirms exact match and averaged component accuracies are distinct.")


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    print_header("PHASE 26C STEP 2D: METRIC VERIFICATION")
    print("No model is used. All cases are synthetic and fully controlled.")
    print()

    case_1_perfect_prediction()
    case_2_digit_wrong_carry_correct()
    case_3_digit_correct_carry_wrong()
    case_4_sequence_partial_correct()
    case_5_dataset_level_exact_match()

    print_header("STEP 2D FINAL STATUS")
    print("✓ Sample-level metric semantics verified")
    print("✓ Digit and carry accuracies can diverge legitimately")
    print("✓ Exact match semantics verified")
    print("✓ Dataset-level averaging semantics verified")
    print()
    print("Next recommended step:")
    print("  Step 2E — Official baseline reproduction")
    print("=" * 80)


if __name__ == "__main__":
    main()
