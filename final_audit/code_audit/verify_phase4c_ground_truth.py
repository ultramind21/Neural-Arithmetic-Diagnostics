"""
================================================================================
VERIFICATION SCRIPT: PHASE 4C
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/project_3_residual_logic_layer.py

PURPOSE:
  Verify the ground-truth / target semantics used in Project 3 baseline data
  generation.

THIS SCRIPT VERIFIES:
  1. The generated target sum sequences are arithmetically correct
  2. For each generated example, sum_seq matches digit-wise addition of a_seq and b_seq
  3. The arithmetic includes carry propagation across positions
  4. The generated targets are consistent across multiple sample lengths

THIS SCRIPT DOES NOT VERIFY:
  - Model metrics
  - Final performance
  - Official full reproduction
  - Any adversarial/killer-test interpretation

IMPORTANT PRINCIPLE:
  Step 4C asks:
    "Are the generated target sequences arithmetically correct?"
  It does NOT ask:
    "Does the model learn them well?"

================================================================================
"""

import importlib.util
import sys
from pathlib import Path


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


def reference_sum_sequence(a_seq, b_seq):
    """
    Reference implementation for Project 3 target semantics.

    The source comments indicate:
      sum_out[i] = a_seq[i] + b_seq[i] + carry_in[i] in [0..19]

    We compute left-to-right over the provided sequence order, carrying forward.
    """
    if len(a_seq) != len(b_seq):
        raise ValueError("a_seq and b_seq must have same length")

    out = []
    carry = 0
    for a, b in zip(a_seq, b_seq):
        s = a + b + carry
        out.append(s)
        carry = 1 if s >= 10 else 0
    return out


def verify_examples(examples):
    """
    Each example expected as:
      (a_seq, b_seq, sum_seq)
    """
    print_header("ROW-BY-ROW SEMANTICS CHECK")

    all_ok = True

    for idx, item in enumerate(examples):
        if not (isinstance(item, tuple) and len(item) == 3):
            all_ok = False
            print(f"✗ row {idx}: invalid example structure: {item}")
            continue

        a_seq, b_seq, sum_seq = item
        expected = reference_sum_sequence(a_seq, b_seq)

        if expected == sum_seq:
            print(f"✓ row {idx:02d}: a={a_seq}  b={b_seq}  sum={sum_seq}")
        else:
            all_ok = False
            print(f"✗ row {idx:02d}: mismatch")
            print(f"  a_seq     = {a_seq}")
            print(f"  b_seq     = {b_seq}")
            print(f"  expected  = {expected}")
            print(f"  actual    = {sum_seq}")

    return all_ok


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 4C: PROJECT 3 GROUND-TRUTH / TARGET SEMANTICS VERIFICATION")
    print(f"Official target: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")

    module = load_target_module(TARGET_FILE)
    print("✓ Import successful")

    if not hasattr(module, "generate_multidigit_sequences"):
        fail("Target module does not define generate_multidigit_sequences()")

    generate_multidigit_sequences = module.generate_multidigit_sequences

    print_header("SAMPLE GENERATION FOR SEMANTICS CHECK")

    try:
        examples = generate_multidigit_sequences(lengths=[2, 3, 4], num_samples_per_length=3, seed=42)
        print(f"✓ Generated {len(examples)} examples for semantics verification")
    except Exception as e:
        fail(f"Could not generate sample examples: {e}")

    if not isinstance(examples, list) or len(examples) == 0:
        fail("Generated examples are empty or not list-like")

    # Check structure quickly
    print_header("STRUCTURE CHECK")
    first = examples[0]
    print(f"First example preview: {first}")

    # Verify semantics
    semantics_ok = verify_examples(examples)

    print_header("STEP 4C FINAL DECISION")

    if semantics_ok:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The generated Project 3 target sequences match independent")
        print("  arithmetic reference computation on sampled examples.")
        print()
        print("Verified semantics:")
        print("  sum_seq[i] = a_seq[i] + b_seq[i] + carry_from_previous_position")
        print("  with carry propagation reflected in later positions.")
    else:
        print("✗ FAIL")
        print()
        print("Finding:")
        print("  One or more generated target sequences did not match")
        print("  independent arithmetic reference computation.")

    print()
    print("Qualification:")
    print("  This step verifies target semantics only.")
    print("  It does NOT verify metrics or reproduction.")

    print()
    print("Next step if accepted by user:")
    print("  Step 4D — metric verification")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
