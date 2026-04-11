"""
================================================================================
VERIFICATION SCRIPT: PHASE 6C
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/phase_30_multidigit_learning.py

PURPOSE:
  Verify the data / target semantics used in the Phase 30 multidigit learning file.

THIS SCRIPT VERIFIES:
  1. The data-generation path can be called directly
  2. Generated examples are structurally coherent
  3. Digit targets match independent arithmetic reference computation
  4. Carry targets match independent arithmetic reference computation
  5. Target semantics are coherent across sampled sequence lengths

THIS SCRIPT DOES NOT VERIFY:
  - Metric correctness
  - Official reproduction
  - Broader claims about model capability
  - Historical interpretation of Phase 30 results

IMPORTANT PRINCIPLE:
  Step 6C asks:
    "Are the generated digit/carry targets arithmetically correct?"
  It does NOT ask:
    "Does the model learn them well?"

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
TARGET_FILE = ROOT / "src" / "train" / "phase_30_multidigit_learning.py"


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
    spec = importlib.util.spec_from_file_location("phase_30_multidigit_learning", str(filepath))
    if spec is None or spec.loader is None:
        fail(f"Could not create import spec for: {filepath}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reference_digit_carry(a_seq, b_seq):
    """
    Independent left-to-right local-sum reference.

    Returns:
      digit_targets, carry_targets
    where
      total = a_i + b_i + carry_prev
      digit_i = total % 10
      carry_i = 1 if total >= 10 else 0
    """
    if len(a_seq) != len(b_seq):
        raise ValueError("a_seq and b_seq must have equal length")

    digit_targets = []
    carry_targets = []
    carry = 0

    for a, b in zip(a_seq, b_seq):
        total = int(a) + int(b) + carry
        digit_targets.append(total % 10)
        carry = 1 if total >= 10 else 0
        carry_targets.append(carry)

    return digit_targets, carry_targets


def preview(obj, max_chars=300):
    r = repr(obj)
    if len(r) > max_chars:
        return r[:max_chars] + " ..."
    return r


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 6C: PHASE-30 DATA / TARGET SEMANTICS VERIFICATION")
    print(f"Official target: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")

    # ------------------------------------------------------------------------
    # 1) Import
    # ------------------------------------------------------------------------
    print_header("1) IMPORT CHECK")
    module = load_target_module(TARGET_FILE)
    print("✓ Import successful")

    if not hasattr(module, "generate_multidigit_sequences"):
        fail("Target module does not define generate_multidigit_sequences()")

    if not hasattr(module, "sequences_to_tensors"):
        fail("Target module does not define sequences_to_tensors()")

    generate_multidigit_sequences = module.generate_multidigit_sequences
    sequences_to_tensors = module.sequences_to_tensors

    # ------------------------------------------------------------------------
    # 2) Generate examples
    # ------------------------------------------------------------------------
    print_header("2) SAMPLE GENERATION")

    try:
        examples = generate_multidigit_sequences(lengths=[2, 3, 4], num_samples_per_length=3, seed=42)
        print(f"✓ Generated {len(examples)} examples")
    except Exception as e:
        fail(f"Could not generate sampled examples: {e}")

    if not isinstance(examples, list) or len(examples) == 0:
        fail("Generated examples are empty or not list-like")

    print(f"First example preview: {preview(examples[0])}")

    # ------------------------------------------------------------------------
    # 3) Structural check
    # ------------------------------------------------------------------------
    print_header("3) STRUCTURE CHECK")

    structure_ok = True
    for i, ex in enumerate(examples[:5]):
        if not isinstance(ex, tuple):
            structure_ok = False
            print(f"✗ row {i}: example is not tuple-like")
            continue

        print(f"row {i}: tuple len={len(ex)} preview={preview(ex, 200)}")

    if not structure_ok:
        fail("Generated example structure is not suitable for semantics verification")

    # ------------------------------------------------------------------------
    # 4) Tensor conversion path
    # ------------------------------------------------------------------------
    print_header("4) TENSOR CONVERSION PATH")

    try:
        converted = sequences_to_tensors(examples)
        print("✓ sequences_to_tensors() succeeded")
        print(f"Converted object type: {type(converted)}")
        print(f"Preview: {preview(converted, 500)}")
    except Exception as e:
        print(f"⚠ sequences_to_tensors() call failed: {e}")
        print("  Continuing with direct example-level semantic verification")

    # ------------------------------------------------------------------------
    # 5) Example-level semantics check
    # ------------------------------------------------------------------------
    print_header("5) ROW-BY-ROW TARGET SEMANTICS CHECK")

    all_ok = True

    for idx, ex in enumerate(examples):
        if len(ex) < 4:
            all_ok = False
            print(f"✗ row {idx}: expected at least 4 tuple elements, got {len(ex)}")
            continue

        a_seq = ex[0]
        b_seq = ex[1]
        digit_true = ex[2]
        carry_true = ex[3]

        expected_digit, expected_carry = reference_digit_carry(a_seq, b_seq)

        digit_match = list(digit_true) == list(expected_digit)
        carry_match = list(carry_true) == list(expected_carry)

        if digit_match and carry_match:
            print(f"✓ row {idx:02d}: semantics match")
            print(f"  a={a_seq}")
            print(f"  b={b_seq}")
            print(f"  digit={list(digit_true)}")
            print(f"  carry={list(carry_true)}")
        else:
            all_ok = False
            print(f"✗ row {idx:02d}: mismatch")
            print(f"  a={a_seq}")
            print(f"  b={b_seq}")
            print(f"  expected_digit={expected_digit}")
            print(f"  actual_digit={list(digit_true)}")
            print(f"  expected_carry={expected_carry}")
            print(f"  actual_carry={list(carry_true)}")

    # ------------------------------------------------------------------------
    # 6) Final decision
    # ------------------------------------------------------------------------
    print_header("6) STEP 6C FINAL DECISION")

    if all_ok:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The generated Phase 30 digit/carry targets match independent")
        print("  arithmetic reference computation on sampled examples.")
        print()
        print("Verified semantics:")
        print("  total_i = a_i + b_i + carry_from_previous_position")
        print("  digit_i = total_i % 10")
        print("  carry_i = 1 if total_i >= 10 else 0")
    else:
        print("✗ FAIL")
        print()
        print("Finding:")
        print("  One or more generated digit/carry targets did not match")
        print("  the independent arithmetic reference computation.")

    print()
    print("Qualification:")
    print("  This step verifies target semantics only.")
    print("  It does NOT verify metrics or reproduction.")

    print()
    print("Next step if accepted by user:")
    print("  Step 6D — metric verification")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
