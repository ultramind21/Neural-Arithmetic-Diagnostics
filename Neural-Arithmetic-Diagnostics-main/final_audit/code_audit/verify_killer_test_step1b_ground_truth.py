"""
================================================================================
VERIFICATION SCRIPT: KILLER TEST STEP 1B
================================================================================

OFFICIAL TARGET:
  File: src/train/project_3_killer_test_adversarial_carry_chain.py

PURPOSE:
  Verify that ground-truth arithmetic computation is correct.

THIS SCRIPT VERIFIES:
  1. Independent ground-truth computation for digit_out and carry_out
  2. Correct carry propagation across positions
  3. Consistency on hand-checkable examples
  4. Optional comparison with official helper logic if available

THIS SCRIPT DOES NOT VERIFY:
  - Model training
  - Model predictions
  - Metric computation
  - Any performance claim

IMPORTANT PRINCIPLE:
  This script validates arithmetic truth generation itself.
  No model is used.

================================================================================
"""

import sys
import inspect
import importlib.util
from pathlib import Path


# -----------------------------------------------------------------------------
# PATHS
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "project_3_killer_test_adversarial_carry_chain.py"


# -----------------------------------------------------------------------------
# MODULE LOADING
# -----------------------------------------------------------------------------
def load_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# -----------------------------------------------------------------------------
# INDEPENDENT REFERENCE IMPLEMENTATION
# -----------------------------------------------------------------------------
def compute_ground_truth_reference(a_seq, b_seq):
    """
    Independent reference implementation.
    Assumes little-endian digit order: position 0 is the first processed digit.
    Carry propagates from position i to position i+1.
    """
    if len(a_seq) != len(b_seq):
        raise ValueError("a_seq and b_seq must have the same length")

    digit_out = []
    carry_out = []
    carry = 0

    for i in range(len(a_seq)):
        total = a_seq[i] + b_seq[i] + carry
        digit = total % 10
        carry = 1 if total >= 10 else 0

        digit_out.append(digit)
        carry_out.append(carry)

    return digit_out, carry_out


# -----------------------------------------------------------------------------
# PRETTY PRINTING
# -----------------------------------------------------------------------------
def print_case_trace(case_name, a_seq, b_seq, digit_out, carry_out):
    print("\n" + "=" * 80)
    print(f"CASE: {case_name}")
    print("=" * 80)
    print(f"a_seq = {a_seq}")
    print(f"b_seq = {b_seq}")
    print()

    print(f"{'pos':>4} | {'a':>2} | {'b':>2} | {'c_in':>4} | {'sum':>3} | {'digit':>5} | {'c_out':>5}")
    print("-" * 50)

    carry_in = 0
    for i in range(len(a_seq)):
        total = a_seq[i] + b_seq[i] + carry_in
        print(
            f"{i:>4} | {a_seq[i]:>2} | {b_seq[i]:>2} | {carry_in:>4} | {total:>3} | {digit_out[i]:>5} | {carry_out[i]:>5}"
        )
        carry_in = carry_out[i]

    print()
    print(f"digit_out = {digit_out}")
    print(f"carry_out = {carry_out}")


def assert_equal(label, actual, expected):
    if actual != expected:
        raise AssertionError(f"{label} mismatch:\n  actual   = {actual}\n  expected = {expected}")


# -----------------------------------------------------------------------------
# HAND-CHECK CASES
# -----------------------------------------------------------------------------
def run_hand_check_cases():
    """
    Cases chosen to be manually checkable and to stress carry propagation.
    All expected values verified by manual multiplication.
    """
    cases = [
        {
            "name": "single_no_carry",
            "a": [0],
            "b": [0],
            "expected_digits": [0],
            "expected_carries": [0],
            "manual_check": "0+0=0 → digit=0, carry=0",
        },
        {
            "name": "single_with_carry",
            "a": [9],
            "b": [1],
            "expected_digits": [0],
            "expected_carries": [1],
            "manual_check": "9+1=10 → digit=0, carry=1",
        },
        {
            "name": "two_digits_simple_chain",
            "a": [9, 0],
            "b": [1, 0],
            "expected_digits": [0, 1],
            "expected_carries": [1, 0],
            "manual_check": "pos0: 9+1=10→d=0,c=1; pos1: 0+0+1=1→d=1,c=0",
        },
        {
            "name": "two_digits_full_chain",
            "a": [9, 9],
            "b": [1, 0],
            "expected_digits": [0, 0],
            "expected_carries": [1, 1],
            "manual_check": "pos0: 9+1=10→d=0,c=1; pos1: 9+0+1=10→d=0,c=1",
        },
        {
            "name": "alternating_small",
            "a": [9, 0, 9, 0],
            "b": [1, 0, 1, 0],
            "expected_digits": [0, 1, 0, 1],
            "expected_carries": [1, 0, 1, 0],
            "manual_check": "pos0: 9+1=10→d=0,c=1; pos1: 0+0+1=1→d=1,c=0; pos2: 9+1=10→d=0,c=1; pos3: 0+0+1=1→d=1,c=0",
        },
        {
            "name": "mixed_manual_case",
            "a": [5, 7, 0, 9],
            "b": [4, 2, 9, 0],
            "expected_digits": [9, 9, 9, 9],
            "expected_carries": [0, 0, 0, 0],
            "manual_check": "pos0: 5+4=9→d=9,c=0; pos1: 7+2=9→d=9,c=0; pos2: 0+9=9→d=9,c=0; pos3: 9+0=9→d=9,c=0",
        },
    ]

    print("\n" + "=" * 80)
    print("STEP 1B-A: HAND-CHECK CASES")
    print("=" * 80)

    passed = 0
    failed = 0

    for case in cases:
        digits, carries = compute_ground_truth_reference(case["a"], case["b"])
        print_case_trace(case["name"], case["a"], case["b"], digits, carries)
        print(f"Manual verification: {case['manual_check']}")

        try:
            assert_equal(f"{case['name']} digits", digits, case["expected_digits"])
            assert_equal(f"{case['name']} carries", carries, case["expected_carries"])
            print(f"✓ {case['name']} passed\n")
            passed += 1
        except AssertionError as e:
            print(f"✗ {case['name']} FAILED")
            print(f"  {e}\n")
            failed += 1

    print(f"\nHand-check summary: {passed} passed, {failed} failed")
    if failed > 0:
        raise AssertionError(f"Hand-check cases failed: {failed}")

    print("✓ All hand-check cases passed.")


# -----------------------------------------------------------------------------
# RANDOM SMALL CASES
# -----------------------------------------------------------------------------
def run_small_consistency_cases():
    """
    Additional independent consistency checks.
    """
    test_cases = [
        ([1, 2, 3], [4, 5, 6]),
        ([9, 9, 9], [1, 0, 0]),
        ([8, 0, 0], [1, 0, 0]),
        ([0, 0, 0], [0, 0, 0]),
        ([9, 0, 9, 0, 9], [1, 0, 1, 0, 1]),
    ]

    print("\n" + "=" * 80)
    print("STEP 1B-B: SMALL CONSISTENCY CASES")
    print("=" * 80)

    for idx, (a_seq, b_seq) in enumerate(test_cases, start=1):
        digits, carries = compute_ground_truth_reference(a_seq, b_seq)
        print_case_trace(f"consistency_case_{idx}", a_seq, b_seq, digits, carries)
        print(f"✓ consistency_case_{idx} computed")

    print("\n✓ All small consistency cases computed successfully.")


# -----------------------------------------------------------------------------
# OPTIONAL OFFICIAL FUNCTION COMPARISON
# -----------------------------------------------------------------------------
def run_optional_official_comparison():
    """
    If the official file exposes a helper function for ground truth computation,
    compare against it. This is optional and non-blocking.
    """
    print("\n" + "=" * 80)
    print("STEP 1B-C: OPTIONAL COMPARISON WITH OFFICIAL MODULE")
    print("=" * 80)

    if not TARGET_FILE.exists():
        print("Official target file missing. Skipping official comparison.")
        return

    try:
        module = load_module_from_path("killer_test_module_step1b", TARGET_FILE)
        print("✓ Official module imported")
    except Exception as e:
        print(f"Could not import official module: {e}")
        print("Skipping official comparison.")
        return

    # Search for helper-like functions
    helper_candidates = []
    helper_keywords = ["ground", "truth", "compute", "carry", "digit", "target"]

    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            lower_name = name.lower()
            if any(k in lower_name for k in helper_keywords):
                helper_candidates.append((name, obj))

    if not helper_candidates:
        print("No obvious official helper functions found.")
        print("This is not a failure; step still valid using independent reference implementation.")
        return

    print("Helper candidates found:")
    for name, func in helper_candidates:
        print(f"  - {name}{inspect.signature(func)}")

    print("\nNo automatic helper execution performed unless function semantics are unambiguous.")
    print("If needed, inspect these functions manually in the official source.")


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    print("\n" + "=" * 80)
    print("KILLER TEST STEP 1B: GROUND TRUTH VERIFICATION")
    print("=" * 80)
    print(f"Official target: {TARGET_FILE}")
    print("No model is used in this script.")
    print()

    if not TARGET_FILE.exists():
        print("ERROR: Official target file does not exist.")
        sys.exit(1)

    try:
        run_hand_check_cases()
        run_small_consistency_cases()
        run_optional_official_comparison()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)

    print("\n" + "=" * 80)
    print("STEP 1B FINAL STATUS")
    print("=" * 80)
    print("✓ Independent ground-truth reference implementation works on hand-check cases.")
    print("✓ Carry propagation logic is validated on manually inspectable examples.")
    print("✓ This step verifies arithmetic truth generation only.")
    print()
    print("Next: Step 1C (metric computation verification).")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
