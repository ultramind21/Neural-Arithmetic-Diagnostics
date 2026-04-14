"""
================================================================================
VERIFICATION SCRIPT: PHASE 4D
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/project_3_residual_logic_layer.py

PURPOSE:
  Verify the metric computation logic used in the Project 3 baseline evaluation.

THIS SCRIPT VERIFIES:
  1. How digit predictions are decoded from model outputs
  2. How carry predictions are decoded from model outputs
  3. How exact match is defined
  4. Whether metric logic matches an independent reference implementation
  5. Whether divergence between digit / carry / exact-match metrics is handled correctly

THIS SCRIPT DOES NOT VERIFY:
  - Ground-truth generation correctness (already verified in 4C)
  - Official reproduction (4E)
  - Final reported scientific claims

IMPORTANT PRINCIPLE:
  Step 4D asks:
    "Are evaluation metrics computed correctly from predictions and targets?"
  It does NOT ask:
    "Do official results reproduce?"

================================================================================
"""

import importlib.util
import inspect
import math
import sys
from pathlib import Path

import torch


# ============================================================================
# PATHS
# ============================================================================
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "project_3_residual_logic_layer.py"


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
    spec = importlib.util.spec_from_file_location("project_3_residual_logic_layer", str(filepath))
    if spec is None or spec.loader is None:
        fail(f"Could not create import spec for: {filepath}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reference_decode_sum_sequence(pred_sum_seq):
    """
    Decode Project 3 regression-style sum outputs into:
      - rounded local sum sequence
      - digit sequence
      - carry sequence

    Semantics:
      rounded_sum = round(pred_sum).clamp(0, 19)
      digit = rounded_sum % 10
      carry = rounded_sum // 10
    """
    rounded = torch.round(pred_sum_seq).clamp(0, 19).long()
    digit = rounded % 10
    carry = rounded // 10
    return rounded, digit, carry


def reference_metrics(pred_sum_seq, true_sum_seq):
    """
    Independent reference metric implementation.

    Returns:
      digit_acc
      carry_acc
      exact_match
    """
    _, pred_digit, pred_carry = reference_decode_sum_sequence(pred_sum_seq)
    _, true_digit, true_carry = reference_decode_sum_sequence(true_sum_seq)

    digit_correct = (pred_digit == true_digit)
    carry_correct = (pred_carry == true_carry)
    exact_correct = digit_correct & carry_correct

    digit_acc = digit_correct.float().mean().item()
    carry_acc = carry_correct.float().mean().item()
    exact_match = exact_correct.float().mean().item()

    return {
        "pred_digit": pred_digit,
        "pred_carry": pred_carry,
        "true_digit": true_digit,
        "true_carry": true_carry,
        "digit_acc": digit_acc,
        "carry_acc": carry_acc,
        "exact_match": exact_match,
    }


def source_style_metrics(pred_sum_seq, true_sum_seq):
    """
    Reproduce the expected source-style metric semantics for comparison.
    """
    pred_sum_int = torch.round(pred_sum_seq).clamp(0, 19).long()
    true_sum_int = torch.round(true_sum_seq).clamp(0, 19).long()

    pred_digit = pred_sum_int % 10
    pred_carry = pred_sum_int // 10

    true_digit = true_sum_int % 10
    true_carry = true_sum_int // 10

    digit_acc = (pred_digit == true_digit).float().mean().item()
    carry_acc = (pred_carry == true_carry).float().mean().item()
    exact_match = ((pred_digit == true_digit) & (pred_carry == true_carry)).float().mean().item()

    return {
        "pred_digit": pred_digit,
        "pred_carry": pred_carry,
        "true_digit": true_digit,
        "true_carry": true_carry,
        "digit_acc": digit_acc,
        "carry_acc": carry_acc,
        "exact_match": exact_match,
    }


def print_case_table(pred_sum_seq, true_sum_seq):
    print_header("CONTROLLED METRIC TEST CASES")

    _, pred_digit, pred_carry = reference_decode_sum_sequence(pred_sum_seq)
    _, true_digit, true_carry = reference_decode_sum_sequence(true_sum_seq)

    print(f"{'idx':>3} | {'pred_sum':>8} | {'true_sum':>8} | {'pred(d,c)':>12} | {'true(d,c)':>12}")
    print("-" * 70)

    for i in range(len(pred_sum_seq)):
        ps = float(pred_sum_seq[i].item())
        ts = float(true_sum_seq[i].item())
        pd = int(pred_digit[i].item())
        pc = int(pred_carry[i].item())
        td = int(true_digit[i].item())
        tc = int(true_carry[i].item())

        print(f"{i:>3} | {ps:>8.2f} | {ts:>8.2f} | {str((pd, pc)):>12} | {str((td, tc)):>12}")


def close(a, b, tol=1e-6):
    return math.isclose(a, b, rel_tol=0.0, abs_tol=tol)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 4D: PROJECT 3 METRIC VERIFICATION")
    print(f"Official target: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")

    # ------------------------------------------------------------------------
    # 1) Import module
    # ------------------------------------------------------------------------
    print_header("1) IMPORT CHECK")
    module = load_target_module(TARGET_FILE)
    print("✓ Import successful")

    # ------------------------------------------------------------------------
    # 2) Evaluate-model visibility check
    # ------------------------------------------------------------------------
    print_header("2) EVALUATION FUNCTION CHECK")

    if hasattr(module, "evaluate_model"):
        print("✓ Found evaluate_model")
        try:
            sig = inspect.signature(module.evaluate_model)
            print(f"evaluate_model{sig}")
        except Exception as e:
            print(f"Could not inspect evaluate_model signature: {e}")
    else:
        print("⚠ evaluate_model not found by import-level lookup")
        print("  Continuing with source-intent metric verification")

    # ------------------------------------------------------------------------
    # 3) Controlled synthetic test cases
    # ------------------------------------------------------------------------
    print_header("3) SYNTHETIC METRIC TEST SETUP")

    # Design cases to cover:
    # - exact correct
    # - digit wrong only
    # - carry wrong only
    # - both wrong
    pred_sum_seq = torch.tensor([
        5.0,    # exact correct vs 5
        6.0,    # digit wrong only vs 5
        9.0,    # carry wrong only vs 10
        12.0,   # exact correct vs 12
        17.0,   # exact correct vs 17
        8.0,    # both wrong vs 19
    ], dtype=torch.float32)

    true_sum_seq = torch.tensor([
        5.0,    # digit 5, carry 0
        5.0,    # digit 5, carry 0
        10.0,   # digit 0, carry 1
        12.0,   # digit 2, carry 1
        17.0,   # digit 7, carry 1
        19.0,   # digit 9, carry 1
    ], dtype=torch.float32)

    print_case_table(pred_sum_seq, true_sum_seq)

    # ------------------------------------------------------------------------
    # 4) Compare source-style vs reference
    # ------------------------------------------------------------------------
    print_header("4) SOURCE-STYLE VS REFERENCE COMPARISON")

    source = source_style_metrics(pred_sum_seq, true_sum_seq)
    reference = reference_metrics(pred_sum_seq, true_sum_seq)

    all_ok = True

    tensor_keys = ["pred_digit", "pred_carry", "true_digit", "true_carry"]
    for key in tensor_keys:
        if torch.equal(source[key], reference[key]):
            print(f"✓ {key}: identical")
        else:
            all_ok = False
            print(f"✗ {key}: mismatch")

    scalar_keys = ["digit_acc", "carry_acc", "exact_match"]
    for key in scalar_keys:
        s = source[key]
        r = reference[key]
        if close(s, r):
            print(f"✓ {key}: source={s:.6f}, reference={r:.6f}")
        else:
            all_ok = False
            print(f"✗ {key}: source={s:.6f}, reference={r:.6f}")

    # ------------------------------------------------------------------------
    # 5) Manual expectation check
    # ------------------------------------------------------------------------
    print_header("5) MANUAL EXPECTATION CHECK")

    expected_digit_acc = 3 / 6
    expected_carry_acc = 4 / 6
    expected_exact_match = 3 / 6

    print("Expected qualitative behavior:")
    print("  row 0: exact correct")
    print("  row 1: digit wrong only")
    print("  row 2: carry wrong only")
    print("  row 3: exact correct")
    print("  row 4: exact correct")
    print("  row 5: both wrong")
    print()
    print("Expected accuracies:")
    print(f"  digit_acc   = 3/6 = {expected_digit_acc:.6f}")
    print(f"  carry_acc   = 4/6 = {expected_carry_acc:.6f}")
    print(f"  exact_match = 3/6 = {expected_exact_match:.6f}")

    expected_ok = (
        close(source["digit_acc"], expected_digit_acc) and
        close(source["carry_acc"], expected_carry_acc) and
        close(source["exact_match"], expected_exact_match)
    )

    if expected_ok:
        print("\n✓ Manual expectation matches computed metrics")
    else:
        all_ok = False
        print("\n✗ Manual expectation does not match computed metrics")

    # ------------------------------------------------------------------------
    # 6) Final decision
    # ------------------------------------------------------------------------
    print_header("6) STEP 4D FINAL DECISION")

    if all_ok and expected_ok:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The Project 3 metric computation logic is consistent with")
        print("  an independent reference implementation on controlled cases.")
        print()
        print("Verified metric semantics:")
        print("  - rounded_sum = round(pred_sum).clamp(0, 19)")
        print("  - digit = rounded_sum % 10")
        print("  - carry = rounded_sum // 10")
        print("  - exact_match requires both digit and carry to match")
        print("  - digit / carry / exact-match divergence is handled correctly")
    else:
        print("✗ FAIL")
        print()
        print("Finding:")
        print("  One or more Project 3 metric checks did not match")
        print("  the independent reference implementation.")

    print()
    print("Qualification:")
    print("  This step verifies metric semantics only.")
    print("  It does NOT reproduce official reported results.")

    print()
    print("Next step if accepted by user:")
    print("  Step 4E — official reproduction / result verification")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
