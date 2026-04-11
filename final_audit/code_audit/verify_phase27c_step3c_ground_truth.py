"""
================================================================================
VERIFICATION SCRIPT: PHASE 27C STEP 3C
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/phase_27c_architecture_audit.py

PURPOSE:
  Verify the ground-truth / target semantics used in the official Project 2
  architecture audit script.

CRITICAL NOTE (Step 3B Caveat):
  Step 3B established that test-pair distribution is BIASED across architectures.
  However, the semantics of digit/carry target generation are independent of
  which specific pairs are assigned to each architecture.

  Therefore:
    - Step 3B failure does NOT block semantic verification
    - Step 3C checks only ground-truth correctness and consistency
    - Step 3C does NOT repair or re-evaluate split fairness

THIS SCRIPT VERIFIES:
  1. The official target file can be imported
  2. create_train_data() exists and returns labels consistent with single-digit addition
  3. create_test_data_simple() exists and returns labels consistent with single-digit addition
  4. Train/test target semantics are identical
  5. Label field ordering is consistent: [digit, carry]

THIS SCRIPT DOES NOT VERIFY:
  - Metric computation correctness
  - Model training quality
  - Reproduction of official numerical results
  - Fairness of test-pair distribution (already handled in Step 3B)

IMPORTANT PRINCIPLE:
  This step asks:
    "Is the supervised truth defined correctly?"
  It does NOT ask:
    "Is the architecture comparison fair?" or
    "Do the models learn the task well?"

================================================================================
"""

import importlib.util
import sys
from pathlib import Path

import torch


# ============================================================================
# PATHS
# ============================================================================
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "phase_27c_architecture_audit.py"


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def fail(msg):
    print(f"\nERROR: {msg}")
    sys.exit(1)


def load_target_module(filepath):
    """Dynamically import target file as module."""
    spec = importlib.util.spec_from_file_location("phase_27c_architecture_audit", str(filepath))
    if spec is None or spec.loader is None:
        fail(f"Could not create import spec for: {filepath}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reference_semantics(a, b, carry_in):
    """
    Independent reference implementation for single-digit addition with carry.
    Returns (digit_out, carry_out).
    """
    total = a + b + carry_in
    digit_out = total % 10
    carry_out = 1 if total >= 10 else 0
    return digit_out, carry_out


def expected_rows_for_pairs(pairs):
    """
    Expected rows in the exact order used by target functions:
      for a,b in pairs:
          for carry_in in range(2):
              ...
    Returns list of tuples:
      (input_triplet, expected_label)
    """
    rows = []
    for a, b in pairs:
        for carry_in in range(2):
            digit_out, carry_out = reference_semantics(a, b, carry_in)
            rows.append(((a, b, carry_in), (digit_out, carry_out)))
    return rows


def tensor_to_rows(X, y):
    """
    Convert tensors returned by target functions into row-wise python tuples.
    Returns list of:
      ((a,b,carry_in), (digit,carry))
    """
    X_list = X.tolist()
    y_list = y.tolist()

    rows = []
    for x_row, y_row in zip(X_list, y_list):
        a, b, carry_in = int(x_row[0]), int(x_row[1]), int(x_row[2])
        digit = int(y_row[0])
        carry = int(y_row[1])
        rows.append(((a, b, carry_in), (digit, carry)))
    return rows


def compare_rows(actual_rows, expected_rows, label):
    """
    Compare actual target rows to expected reference rows.
    """
    print_header(f"ROW-BY-ROW COMPARISON: {label}")

    if len(actual_rows) != len(expected_rows):
        print(f"✗ Row count mismatch: actual={len(actual_rows)} expected={len(expected_rows)}")
        return False

    all_ok = True
    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        if actual != expected:
            all_ok = False
            print(f"✗ MISMATCH at row {i}")
            print(f"  actual:   input={actual[0]}  label={actual[1]}")
            print(f"  expected: input={expected[0]}  label={expected[1]}")
        else:
            print(f"✓ row {i:02d}: input={actual[0]} -> label={actual[1]}")

    if all_ok:
        print("\n✓ All rows match expected single-digit addition semantics.")
    else:
        print("\n✗ One or more rows do not match expected semantics.")

    return all_ok


def summarize_tensor_shapes(X, y, label):
    print_header(f"TENSOR SHAPE CHECK: {label}")
    print(f"X shape: {tuple(X.shape)}")
    print(f"y shape: {tuple(y.shape)}")
    print(f"X dtype: {X.dtype}")
    print(f"y dtype: {y.dtype}")


def validate_label_ranges(rows, label):
    """
    Check digit in [0..9], carry in {0,1}
    """
    print_header(f"LABEL RANGE CHECK: {label}")

    ok = True
    for i, (_, (digit, carry)) in enumerate(rows):
        digit_ok = (0 <= digit <= 9)
        carry_ok = (carry in (0, 1))

        if digit_ok and carry_ok:
            print(f"✓ row {i:02d}: digit={digit}, carry={carry}")
        else:
            ok = False
            print(f"✗ row {i:02d}: digit={digit}, carry={carry}")

    if ok:
        print("\n✓ All labels are in valid ranges: digit∈[0,9], carry∈{0,1}")
    else:
        print("\n✗ Invalid label values detected.")

    return ok


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 27C STEP 3C: GROUND-TRUTH / TARGET SEMANTICS VERIFICATION")
    print(f"Official target: {TARGET_FILE}")

    # ------------------------------------------------------------------------
    # 0) Step 3B caveat
    # ------------------------------------------------------------------------
    print_header("STEP 3B CAVEAT")
    print("Step 3B established that cross-architecture test-pair distribution is BIASED.")
    print("This Step 3C check is still valid because it verifies target semantics only.")
    print("It does NOT assess split fairness, architecture comparability, or model quality.")

    # ------------------------------------------------------------------------
    # 1) Existence + import
    # ------------------------------------------------------------------------
    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")

    print_header("IMPORT CHECK")
    print("Attempting to import official target module...")
    module = load_target_module(TARGET_FILE)
    print("✓ Import successful")

    # ------------------------------------------------------------------------
    # 2) Function existence
    # ------------------------------------------------------------------------
    print_header("FUNCTION EXISTENCE CHECK")

    required_functions = ["create_train_data", "create_test_data_simple"]
    missing = []

    for fn_name in required_functions:
        if hasattr(module, fn_name):
            print(f"✓ Found function: {fn_name}")
        else:
            print(f"✗ Missing function: {fn_name}")
            missing.append(fn_name)

    if missing:
        fail(f"Required function(s) missing: {missing}")

    create_train_data = module.create_train_data
    create_test_data_simple = module.create_test_data_simple

    # ------------------------------------------------------------------------
    # 3) Hand-check pairs
    # ------------------------------------------------------------------------
    print_header("HAND-CHECK TEST SETUP")

    test_pairs = [
        (0, 0),   # minimal no carry
        (4, 5),   # boundary around carry with carry_in
        (9, 0),   # max digit + no carry
        (9, 9),   # maximum carry cases
    ]

    print("Selected test pairs:")
    for p in test_pairs:
        print(f"  {p}")

    expected = expected_rows_for_pairs(test_pairs)

    print("\nExpected rows (reference semantics):")
    for i, (inp, out) in enumerate(expected):
        print(f"  row {i:02d}: input={inp} -> expected_label={out}")

    # ------------------------------------------------------------------------
    # 4) Verify create_train_data semantics
    # ------------------------------------------------------------------------
    print_header("VERIFY create_train_data()")

    X_train, y_train = create_train_data(test_pairs)
    summarize_tensor_shapes(X_train, y_train, "create_train_data")

    # The training function expands/repeats rows to reach 50k samples.
    # For semantic verification, only the first len(expected) rows matter,
    # because they correspond to the first pass through the provided pairs.
    expected_len = len(expected)

    train_rows_full = tensor_to_rows(X_train, y_train)
    train_rows_prefix = train_rows_full[:expected_len]

    train_ranges_ok = validate_label_ranges(train_rows_prefix, "create_train_data (prefix)")
    train_semantics_ok = compare_rows(train_rows_prefix, expected, "create_train_data (prefix)")

    # ------------------------------------------------------------------------
    # 5) Verify create_test_data_simple semantics
    # ------------------------------------------------------------------------
    print_header("VERIFY create_test_data_simple()")

    X_test, y_test = create_test_data_simple(test_pairs)
    summarize_tensor_shapes(X_test, y_test, "create_test_data_simple")

    test_rows = tensor_to_rows(X_test, y_test)

    test_ranges_ok = validate_label_ranges(test_rows, "create_test_data_simple")
    test_semantics_ok = compare_rows(test_rows, expected, "create_test_data_simple")

    # ------------------------------------------------------------------------
    # 6) Train/Test consistency
    # ------------------------------------------------------------------------
    print_header("TRAIN / TEST CONSISTENCY CHECK")

    train_test_same = (train_rows_prefix == test_rows)

    if train_test_same:
        print("✓ PASS: Training and test target generation are identical on matched inputs.")
    else:
        print("✗ FAIL: Training and test target generation differ on matched inputs.")
        print("\nFirst few differences:")
        for i, (tr, te) in enumerate(zip(train_rows_prefix, test_rows)):
            if tr != te:
                print(f"  row {i}: train={tr}  test={te}")

    # ------------------------------------------------------------------------
    # 7) Final decision
    # ------------------------------------------------------------------------
    print_header("STEP 3C FINAL DECISION")

    overall_pass = (
        train_ranges_ok and
        train_semantics_ok and
        test_ranges_ok and
        test_semantics_ok and
        train_test_same
    )

    if overall_pass:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The official Phase 27c source uses correct single-digit addition")
        print("  semantics for target generation in both training and test data.")
        print()
        print("Verified semantics:")
        print("  digit_out = (a + b + carry_in) % 10")
        print("  carry_out = 1 if (a + b + carry_in) >= 10 else 0")
        print()
        print("Additional confirmation:")
        print("  - Label ordering is consistent as [digit, carry]")
        print("  - Train/test target generation is semantically identical")
    else:
        print("✗ FAIL")
        print()
        print("Finding:")
        print("  One or more checks failed in target generation semantics.")
        print("  Phase 27c ground-truth definition cannot yet be considered verified.")

    print()
    print("Qualification:")
    print("  This step verifies target semantics only.")
    print("  It does NOT overturn the Step 3B finding that architecture comparison")
    print("  is biased at the test-pair distribution level.")

    print()
    print("Next step if accepted by user:")
    print("  Phase 3D — Metric verification")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
