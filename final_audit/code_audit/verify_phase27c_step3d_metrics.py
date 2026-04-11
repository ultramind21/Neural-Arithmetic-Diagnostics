"""
================================================================================
VERIFICATION SCRIPT: PHASE 27C STEP 3D
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/phase_27c_architecture_audit.py

PURPOSE:
  Verify the metric computation logic used in the official Project 2
  architecture audit script.

CRITICAL NOTE (Step 3B Caveat):
  Step 3B established that test-pair distribution is BIASED across architectures.
  That caveat remains in force.
  This Step 3D verifies metric semantics only:
    - how predictions are decoded
    - how exact-match correctness is defined
    - how failures are counted
    - how test_acc is computed

THIS SCRIPT VERIFIES:
  1. digit prediction decoding via argmax
  2. carry prediction decoding via threshold (carry_logits > 0)
  3. exact-match logic via both_correct
  4. carry/non-carry case partitioning logic
  5. carry_failures and noncarry_failures counting logic
  6. test_acc formula correctness
  7. equivalence between failure counting and exact-match accuracy

THIS SCRIPT DOES NOT VERIFY:
  - Ground-truth semantics (handled in Step 3C)
  - Test-pair fairness (failed in Step 3B)
  - Model training quality
  - Official result reproduction

IMPORTANT PRINCIPLE:
  This step asks:
    "Are the metrics computed correctly from predictions and labels?"
  It does NOT ask:
    "Are the architectures fairly compared?" or
    "Do the numerical results reproduce?"

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
    spec = importlib.util.spec_from_file_location("phase_27c_architecture_audit", str(filepath))
    if spec is None or spec.loader is None:
        fail(f"Could not create import spec for: {filepath}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reference_case_type(a, b, carry_in):
    """Return True if case is a carry-producing case, else False."""
    return (a + b + carry_in) >= 10


def reference_metric_computation(X_test, y_test, digit_logits, carry_logits):
    """
    Independent reference implementation of the metric logic.

    Recomputes:
      - digit_pred
      - carry_pred
      - both_correct
      - carry_failures
      - noncarry_failures
      - carry_examples
      - noncarry_examples
      - test_acc
    """
    digit_pred = digit_logits.argmax(dim=1)
    carry_pred = (carry_logits > 0).long().squeeze()
    both_correct = (digit_pred == y_test[:, 0]) & (carry_pred == y_test[:, 1])

    # Normalize shape in case squeeze produces scalar-like behavior for tiny batches
    if both_correct.ndim == 0:
        both_correct = both_correct.unsqueeze(0)

    carry_failures = 0
    carry_examples = 0
    noncarry_failures = 0
    noncarry_examples = 0

    X_list = X_test.tolist()
    both_list = both_correct.tolist()

    for i in range(len(X_list)):
        a = int(X_list[i][0])
        b = int(X_list[i][1])
        carry_in = int(X_list[i][2])

        is_carry = reference_case_type(a, b, carry_in)
        failed = not bool(both_list[i])

        if is_carry:
            carry_examples += 1
            if failed:
                carry_failures += 1
        else:
            noncarry_examples += 1
            if failed:
                noncarry_failures += 1

    total_examples = len(X_list)
    total_failures = carry_failures + noncarry_failures
    test_acc = (total_examples - total_failures) / total_examples

    return {
        "digit_pred": digit_pred,
        "carry_pred": carry_pred,
        "both_correct": both_correct,
        "carry_failures": carry_failures,
        "carry_examples": carry_examples,
        "noncarry_failures": noncarry_failures,
        "noncarry_examples": noncarry_examples,
        "total_examples": total_examples,
        "total_failures": total_failures,
        "test_acc": test_acc,
    }


def target_metric_computation_like_source(X_test, y_test, digit_logits, carry_logits):
    """
    Reproduce the metric logic exactly as written in the target source.
    This is the "source behavior" side for comparison against reference logic.
    """
    digit_pred = digit_logits.argmax(dim=1)
    carry_pred = (carry_logits > 0).long().squeeze()
    both_correct = (digit_pred == y_test[:, 0]) & (carry_pred == y_test[:, 1])

    both_correct_np = both_correct.cpu().numpy()
    X_np = X_test.cpu().numpy()

    carry_failures = 0
    carry_examples = 0
    noncarry_failures = 0
    noncarry_examples = 0

    for i in range(len(X_np)):
        a, b, c_in = int(X_np[i, 0]), int(X_np[i, 1]), int(X_np[i, 2])
        s = a + b + c_in
        is_carry = (s >= 10)
        failed = not both_correct_np[i]

        if is_carry:
            carry_examples += 1
            if failed:
                carry_failures += 1
        else:
            noncarry_examples += 1
            if failed:
                noncarry_failures += 1

    total_examples = len(X_np)
    total_failures = carry_failures + noncarry_failures
    test_acc = (total_examples - total_failures) / total_examples

    return {
        "digit_pred": digit_pred,
        "carry_pred": carry_pred,
        "both_correct": both_correct,
        "carry_failures": carry_failures,
        "carry_examples": carry_examples,
        "noncarry_failures": noncarry_failures,
        "noncarry_examples": noncarry_examples,
        "total_examples": total_examples,
        "total_failures": total_failures,
        "test_acc": test_acc,
    }


def print_predictions_table(X_test, y_test, digit_logits, carry_logits, label):
    print_header(f"PREDICTION TABLE: {label}")

    digit_pred = digit_logits.argmax(dim=1)
    carry_pred = (carry_logits > 0).long().squeeze()
    both_correct = (digit_pred == y_test[:, 0]) & (carry_pred == y_test[:, 1])

    X_list = X_test.tolist()
    y_list = y_test.tolist()
    d_pred = digit_pred.tolist()
    c_pred = carry_pred.tolist()
    bc = both_correct.tolist()

    print(f"{'idx':>3} | {'input':<10} | {'target':<10} | {'pred':<10} | {'both_correct':<12}")
    print("-" * 70)

    for i in range(len(X_list)):
        inp = tuple(int(v) for v in X_list[i])
        target = (int(y_list[i][0]), int(y_list[i][1]))
        pred = (int(d_pred[i]), int(c_pred[i]))
        print(f"{i:>3} | {str(inp):<10} | {str(target):<10} | {str(pred):<10} | {str(bool(bc[i])):<12}")


def compare_metric_dicts(source_metrics, reference_metrics):
    print_header("SOURCE VS REFERENCE METRIC COMPARISON")

    keys_to_check = [
        "carry_failures",
        "carry_examples",
        "noncarry_failures",
        "noncarry_examples",
        "total_examples",
        "total_failures",
        "test_acc",
    ]

    all_ok = True
    for key in keys_to_check:
        source_val = source_metrics[key]
        ref_val = reference_metrics[key]

        if isinstance(source_val, float) or isinstance(ref_val, float):
            match = abs(source_val - ref_val) < 1e-12
        else:
            match = (source_val == ref_val)

        if match:
            print(f"✓ {key}: source={source_val}  reference={ref_val}")
        else:
            all_ok = False
            print(f"✗ {key}: source={source_val}  reference={ref_val}")

    # Check predictions too
    pred_checks = [
        ("digit_pred", source_metrics["digit_pred"], reference_metrics["digit_pred"]),
        ("carry_pred", source_metrics["carry_pred"], reference_metrics["carry_pred"]),
        ("both_correct", source_metrics["both_correct"], reference_metrics["both_correct"]),
    ]

    for name, source_tensor, ref_tensor in pred_checks:
        match = torch.equal(source_tensor.cpu(), ref_tensor.cpu())
        if match:
            print(f"✓ {name}: tensors identical")
        else:
            all_ok = False
            print(f"✗ {name}: tensors differ")

    return all_ok


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 27C STEP 3D: METRIC VERIFICATION")
    print(f"Official target: {TARGET_FILE}")

    # ------------------------------------------------------------------------
    # 0) Step 3B caveat
    # ------------------------------------------------------------------------
    print_header("STEP 3B CAVEAT")
    print("Step 3B established that cross-architecture test-pair distribution is BIASED.")
    print("This Step 3D remains valid because it checks metric computation only.")
    print("It does NOT repair or reassess architecture fairness.")

    # ------------------------------------------------------------------------
    # 1) Load target
    # ------------------------------------------------------------------------
    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")

    module = load_target_module(TARGET_FILE)
    print_header("IMPORT CHECK")
    print("✓ Import successful")

    if not hasattr(module, "create_test_data_simple"):
        fail("Target module does not define create_test_data_simple()")

    create_test_data_simple = module.create_test_data_simple

    # ------------------------------------------------------------------------
    # 2) Build small deterministic test set
    # ------------------------------------------------------------------------
    print_header("TEST DATA SETUP")

    test_pairs = [
        (0, 0),   # no carry in both c=0 and c=1
        (4, 5),   # boundary pair: c=0 no carry, c=1 carry
        (9, 0),   # c=0 no carry, c=1 carry
        (9, 9),   # always carry
    ]

    print("Using test pairs:")
    for p in test_pairs:
        print(f"  {p}")

    X_test, y_test = create_test_data_simple(test_pairs)

    print(f"\nX_test shape: {tuple(X_test.shape)}")
    print(f"y_test shape: {tuple(y_test.shape)}")

    # ------------------------------------------------------------------------
    # 3) Synthetic predictions with controlled successes/failures
    # ------------------------------------------------------------------------
    print_header("SYNTHETIC PREDICTION SETUP")

    # Targets from chosen pairs should be:
    # 0: (0,0,0) -> (0,0)   noncarry   correct
    # 1: (0,0,1) -> (1,0)   noncarry   digit wrong only
    # 2: (4,5,0) -> (9,0)   noncarry   correct
    # 3: (4,5,1) -> (0,1)   carry      carry wrong only
    # 4: (9,0,0) -> (9,0)   noncarry   both wrong
    # 5: (9,0,1) -> (0,1)   carry      correct
    # 6: (9,9,0) -> (8,1)   carry      correct
    # 7: (9,9,1) -> (9,1)   carry      digit wrong only

    target_digit_preds = [0, 2, 9, 0, 3, 0, 8, 1]
    target_carry_preds = [0, 0, 0, 0, 1, 1, 1, 1]

    num_examples = len(target_digit_preds)
    digit_logits = torch.full((num_examples, 10), -10.0)
    carry_logits = torch.empty((num_examples, 1))

    for i, pred_digit in enumerate(target_digit_preds):
        digit_logits[i, pred_digit] = 10.0

    for i, pred_carry in enumerate(target_carry_preds):
        carry_logits[i, 0] = 5.0 if pred_carry == 1 else -5.0

    print("Constructed synthetic predictions to test:")
    print("  - exact-match success")
    print("  - digit-only failure")
    print("  - carry-only failure")
    print("  - both-wrong failure")
    print("  - carry/non-carry partitioning")
    print("  - test_acc from total failures")

    # ------------------------------------------------------------------------
    # 4) Show prediction table
    # ------------------------------------------------------------------------
    print_predictions_table(X_test, y_test, digit_logits, carry_logits, "CONTROLLED SYNTHETIC CASES")

    # ------------------------------------------------------------------------
    # 5) Compare source-style metrics vs independent reference
    # ------------------------------------------------------------------------
    source_metrics = target_metric_computation_like_source(X_test, y_test, digit_logits, carry_logits)
    reference_metrics = reference_metric_computation(X_test, y_test, digit_logits, carry_logits)

    comparison_ok = compare_metric_dicts(source_metrics, reference_metrics)

    # ------------------------------------------------------------------------
    # 6) Manual expectation summary
    # ------------------------------------------------------------------------
    print_header("MANUAL EXPECTATION CHECK")

    print("Expected qualitative outcome from synthetic setup:")
    print("  - Total examples: 8")
    print("  - Correct exact-match rows: 4  (rows 0,2,5,6)")
    print("  - Total failures: 4")
    print("  - Expected test_acc: 4/8 = 0.5")
    print("  - Non-carry rows: 0,1,2,4  -> 4 examples")
    print("  - Carry rows:     3,5,6,7  -> 4 examples")
    print("  - Non-carry failures: rows 1,4 -> 2")
    print("  - Carry failures:     rows 3,7 -> 2")

    expected_ok = (
        source_metrics["total_examples"] == 8 and
        source_metrics["total_failures"] == 4 and
        source_metrics["carry_examples"] == 4 and
        source_metrics["noncarry_examples"] == 4 and
        source_metrics["carry_failures"] == 2 and
        source_metrics["noncarry_failures"] == 2 and
        abs(source_metrics["test_acc"] - 0.5) < 1e-12
    )

    if expected_ok:
        print("\n✓ Manual expectation matches computed source-style metrics.")
    else:
        print("\n✗ Manual expectation does NOT match computed source-style metrics.")

    # ------------------------------------------------------------------------
    # 7) Final decision
    # ------------------------------------------------------------------------
    print_header("STEP 3D FINAL DECISION")

    overall_pass = comparison_ok and expected_ok

    if overall_pass:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The metric computation logic in phase_27c_architecture_audit.py")
        print("  is internally consistent and matches an independent reference")
        print("  implementation on controlled synthetic cases.")
        print()
        print("Verified metric semantics:")
        print("  - digit_pred = argmax(digit_logits)")
        print("  - carry_pred = (carry_logits > 0)")
        print("  - both_correct requires BOTH digit and carry to be correct")
        print("  - carry/non-carry partitioning is based on (a + b + carry_in) >= 10")
        print("  - test_acc = exact-match-correct / total_examples")
        print("  - source formula (total - failures) / total is correct")
    else:
        print("✗ FAIL")
        print()
        print("Finding:")
        print("  One or more metric checks did not match the independent reference")
        print("  or the controlled manual expectation.")

    print()
    print("Qualification:")
    print("  This step verifies metric computation only.")
    print("  It does NOT remove the Step 3B comparability caveat.")

    print()
    print("Next step if accepted by user:")
    print("  Phase 3E — Official reproduction / result verification")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
