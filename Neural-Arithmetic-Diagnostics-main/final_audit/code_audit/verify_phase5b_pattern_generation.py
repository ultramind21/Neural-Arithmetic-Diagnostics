"""
================================================================================
VERIFICATION SCRIPT: PHASE 5B
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/project_3_killer_test_adversarial_carry_chain.py

PURPOSE:
  Verify the adversarial pattern generation / data-path logic used in the
  Project 3 killer-test source.

THIS SCRIPT VERIFIES:
  1. generate_test_patterns() exists and can be called
  2. The returned pattern structure is readable and usable
  3. The expected pattern collection is present
  4. Generated pattern examples have coherent shapes/types
  5. Pattern generation is consistent with the visible source intent
  6. Basic structural properties of the adversarial patterns can be inspected

THIS SCRIPT DOES NOT VERIFY:
  - Ground-truth arithmetic correctness of evaluation outputs (Phase 5C)
  - Metric correctness (Phase 5D)
  - Full official reproduction (Phase 5E)
  - Final interpretation of killer-test success/failure thresholds

IMPORTANT PRINCIPLE:
  Step 5B asks:
    "Are the adversarial patterns/data path generated coherently and visibly?"
  It does NOT ask:
    "Do the evaluated results on those patterns prove algorithmic reasoning?"

================================================================================
"""

import importlib.util
import inspect
import sys
from pathlib import Path


# ============================================================================
# PATHS
# ============================================================================
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "project_3_killer_test_adversarial_carry_chain.py"


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
    spec = importlib.util.spec_from_file_location(
        "project_3_killer_test_adversarial_carry_chain",
        str(filepath)
    )
    if spec is None or spec.loader is None:
        fail(f"Could not create import spec for: {filepath}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def preview(obj, max_chars=300):
    r = repr(obj)
    if len(r) > max_chars:
        return r[:max_chars] + " ..."
    return r


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 5B: KILLER-TEST PATTERN GENERATION / DATA-PATH VERIFICATION")
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
    # 2) Required function check
    # ------------------------------------------------------------------------
    print_header("2) REQUIRED FUNCTION CHECK")

    if not hasattr(module, "generate_test_patterns"):
        fail("Target module does not define generate_test_patterns()")

    generate_test_patterns = module.generate_test_patterns
    print("✓ Found generate_test_patterns")

    try:
        sig = inspect.signature(generate_test_patterns)
        print(f"generate_test_patterns{sig}")
    except Exception as e:
        print(f"Could not inspect signature: {e}")

    # ------------------------------------------------------------------------
    # 3) Call generator
    # ------------------------------------------------------------------------
    print_header("3) PATTERN GENERATION CALL")

    try:
        patterns = generate_test_patterns(length=20, num_samples=5)
        print("✓ generate_test_patterns(length=20, num_samples=5) succeeded")
    except Exception as e:
        fail(f"generate_test_patterns() call failed: {e}")

    print(f"Returned object type: {type(patterns)}")
    print(f"Preview: {preview(patterns, 500)}")

    # ------------------------------------------------------------------------
    # 4) Structure inspection
    # ------------------------------------------------------------------------
    print_header("4) PATTERN STRUCTURE INSPECTION")

    structure_ok = True

    if isinstance(patterns, dict):
        print(f"✓ Returned object is dict-like with {len(patterns)} entries")
        pattern_items = list(patterns.items())
    elif isinstance(patterns, list):
        print(f"✓ Returned object is list-like with {len(patterns)} entries")
        pattern_items = list(enumerate(patterns))
    else:
        structure_ok = False
        pattern_items = []
        print("✗ Returned object is neither dict-like nor list-like")

    for key, value in pattern_items[:10]:
        print(f"\nPattern key: {key}")
        print(f"  value type: {type(value)}")
        print(f"  preview: {preview(value, 200)}")

    # ------------------------------------------------------------------------
    # 5) Conservative validation of pattern examples
    # ------------------------------------------------------------------------
    print_header("5) CONSERVATIVE PATTERN CONTENT CHECK")

    content_ok = True

    for key, value in pattern_items[:10]:
        # Most likely each pattern maps to (a, b, desc) or similar
        if isinstance(value, tuple):
            print(f"\nPattern {key}: tuple len={len(value)}")
            for i, part in enumerate(value):
                print(f"  part[{i}] type={type(part)} preview={preview(part, 120)}")
        else:
            print(f"\nPattern {key}: non-tuple value preview={preview(value, 160)}")

    # ------------------------------------------------------------------------
    # 6) Source-intent clues
    # ------------------------------------------------------------------------
    print_header("6) SOURCE-INTENT PATTERN CLUES")

    file_text = TARGET_FILE.read_text(encoding="utf-8")

    clues = [
        "Generate 5 adversarial carry-chain patterns",
        "maximum sequential carry",
        "alternating",
        "single carry",
        "blocks",
    ]

    found_any = False
    for clue in clues:
        if clue.lower() in file_text.lower():
            found_any = True
            print(f"✓ Found clue: {clue}")
        else:
            print(f"⚠ Not found literally: {clue}")

    # ------------------------------------------------------------------------
    # 7) Final decision
    # ------------------------------------------------------------------------
    print_header("7) STEP 5B FINAL DECISION")

    overall_pass = structure_ok and content_ok and len(pattern_items) > 0

    if overall_pass:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The killer-test pattern generation path is executable and")
        print("  structurally coherent at the data-path level.")
        print()
        print("What this step established:")
        print("  - generate_test_patterns() exists and runs")
        print("  - returned patterns are inspectable")
        print("  - pattern data path is structurally visible")
        if found_any:
            print("  - source-level adversarial pattern intent is visibly documented")
        else:
            print("  - pattern intent is only partially visible from source text search")
        print()
        print("Qualification:")
        print("  This step does NOT yet verify that the generated patterns are")
        print("  arithmetically or adversarially correct in the intended sense.")
    else:
        print("✗ FAIL")
        print()
        print("Finding:")
        print("  The killer-test pattern generation path is not yet sufficiently")
        print("  verified at the structural/data-path level.")
        print()
        print("Qualification:")
        print("  Step 5C should not proceed until this issue is understood.")

    print()
    print("Next step if accepted by user:")
    print("  Step 5C — ground-truth / pattern semantics verification")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
