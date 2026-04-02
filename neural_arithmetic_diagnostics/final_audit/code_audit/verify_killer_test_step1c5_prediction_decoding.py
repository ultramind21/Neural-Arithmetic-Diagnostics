"""
================================================================================
VERIFICATION SCRIPT: KILLER TEST STEP 1C.5
================================================================================

OFFICIAL TARGETS:
  - src/train/project_3_killer_test_adversarial_carry_chain.py
  - src/models/residual_logic_adder.py

PURPOSE:
  Verify how raw model outputs are decoded into:
    - integer sum
    - predicted digit
    - predicted carry

THIS SCRIPT VERIFIES:
  1. Where decoding logic lives in the official code
  2. Whether decoding uses round / clamp / integer cast
  3. Whether digit_pred and carry_pred are derived from decoded sum
  4. What happens on boundary and near-boundary raw values

THIS SCRIPT DOES NOT VERIFY:
  - Model training
  - Model accuracy
  - Pattern generation
  - Ground-truth generation

IMPORTANT PRINCIPLE:
  We do not assume decoding semantics.
  We inspect official source and test decoding behavior on synthetic values.

================================================================================
"""

import inspect
import importlib.util
from pathlib import Path


# -----------------------------------------------------------------------------
# PATHS
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
KILLER_FILE = ROOT / "src" / "train" / "project_3_killer_test_adversarial_carry_chain.py"
MODEL_FILE = ROOT / "src" / "models" / "residual_logic_adder.py"


# -----------------------------------------------------------------------------
# MODULE LOADER
# -----------------------------------------------------------------------------
def load_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# -----------------------------------------------------------------------------
# SOURCE INSPECTION
# -----------------------------------------------------------------------------
def print_source_excerpt(file_path: Path, keywords, context=6):
    """Print source code excerpts around keywords for manual inspection."""
    print("\n" + "=" * 80)
    print(f"SOURCE EXCERPTS: {file_path.name}")
    print("=" * 80)

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    lines = file_path.read_text(encoding="utf-8").splitlines()
    found_any = False

    for kw in keywords:
        hits = [i for i, line in enumerate(lines) if kw.lower() in line.lower()]
        if hits:
            found_any = True
            print(f"\nKeyword: {kw!r}")
            for hit in hits[:5]:
                start = max(0, hit - context)
                end = min(len(lines), hit + context + 1)
                print("-" * 80)
                for idx in range(start, end):
                    marker = ">>" if idx == hit else "  "
                    print(f"{marker} {idx+1:04d}: {lines[idx]}")
                print("-" * 80)

    if not found_any:
        print("No matching keywords found.")
    print()


# -----------------------------------------------------------------------------
# SYNTHETIC DECODING LOGIC
# -----------------------------------------------------------------------------
def decode_reference(sum_pred):
    """
    Reference decoding logic expected from prior project scripts:
      1. round to nearest integer
      2. clamp to [0, 19]
      3. digit = sum_int % 10
      4. carry = sum_int // 10

    NOTE:
      This is a reference hypothesis to test against source excerpts,
      not a claim unless confirmed by source inspection.
    """
    sum_int = round(sum_pred)

    if sum_int < 0:
        sum_int = 0
    if sum_int > 19:
        sum_int = 19

    digit_pred = sum_int % 10
    carry_pred = sum_int // 10

    return sum_int, digit_pred, carry_pred


def run_synthetic_cases():
    """Test decoding on synthetic raw values."""
    print("\n" + "=" * 80)
    print("SYNTHETIC DECODING CASES")
    print("=" * 80)
    print("Testing reference decoding logic on boundary and near-boundary values.")
    print()

    test_values = [
        -0.4, 0.0, 0.49, 0.51,
        1.0, 1.49, 1.51,
        8.49, 8.51,
        9.49, 9.51,
        10.0, 10.49, 10.51,
        11.49, 11.51,
        18.9, 19.2, 20.0
    ]

    print(f"{'sum_pred':>10} | {'sum_int':>7} | {'digit':>5} | {'carry':>5}")
    print("-" * 40)

    for x in test_values:
        s_int, digit, carry = decode_reference(x)
        print(f"{x:>10.2f} | {s_int:>7} | {digit:>5} | {carry:>5}")

    print()
    print("Interpretation notes:")
    print("- Values near 0.5 change after rounding (affects digit/carry)")
    print("- Negative values clamp to 0 (sum_int=0 -> digit=0, carry=0)")
    print("- Values above 19 clamp to 19 (sum_int=19 -> digit=9, carry=1)")
    print("- Digit and carry are linked through decoded integer sum")
    print()


# -----------------------------------------------------------------------------
# OPTIONAL MODEL METHOD INSPECTION
# -----------------------------------------------------------------------------
def inspect_model_methods():
    """Scan model module for decoding-related methods."""
    print("\n" + "=" * 80)
    print("MODEL METHOD INSPECTION")
    print("=" * 80)

    if not MODEL_FILE.exists():
        print("Model file missing. Skipping method inspection.")
        return

    try:
        model_module = load_module_from_path("residual_logic_model_step1c5", MODEL_FILE)
        print("✓ Model module imported")
    except Exception as e:
        print(f"Could not import model module: {e}")
        print("Proceeding to source inspection only.")
        return

    found_any = False
    for name, obj in inspect.getmembers(model_module):
        if inspect.isclass(obj):
            if "ResidualLogicAdder" in name or "Adder" in name:
                print(f"\nFound class: {name}")
                for meth_name, meth in inspect.getmembers(obj):
                    if inspect.isfunction(meth):
                        if any(k in meth_name.lower() for k in ["logic", "forward", "carry", "digit", "decode"]):
                            found_any = True
                            try:
                                sig = inspect.signature(meth)
                                print(f"  Method candidate: {meth_name}{sig}")
                            except Exception:
                                print(f"  Method candidate: {meth_name}(signature unavailable)")

    if not found_any:
        print("No obvious decoding-related methods found by name scan.")
    print()


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    print("\n" + "=" * 80)
    print("KILLER TEST STEP 1C.5: PREDICTION DECODING VERIFICATION")
    print("=" * 80)
    print("Goal: verify how raw model outputs become digit/carry predictions.")
    print()

    if not KILLER_FILE.exists():
        print(f"ERROR: killer test file not found: {KILLER_FILE}")
        return False

    if not MODEL_FILE.exists():
        print(f"ERROR: model file not found: {MODEL_FILE}")
        return False

    # Source inspection: look for decoding logic
    print_source_excerpt(
        KILLER_FILE,
        keywords=[
            "forward_with_logic", "digit", "carry", "sum",
            "round", "clamp", "//", "%", "int", "floor"
        ],
        context=6
    )

    print_source_excerpt(
        MODEL_FILE,
        keywords=[
            "forward_with_logic", "digit", "carry", "sum",
            "round", "clamp", "//", "%", "int", "floor"
        ],
        context=6
    )

    # Model method discovery
    inspect_model_methods()

    # Synthetic decoding behavior
    run_synthetic_cases()

    print("=" * 80)
    print("STEP 1C.5 FINAL STATUS")
    print("=" * 80)
    print("This step provides:")
    print("✓ source-level evidence about decoding logic")
    print("✓ synthetic examples showing decoding consequences")
    print()
    print("Recommendations:")
    print("- Review source excerpts carefully for actual decoding implementation")
    print("- If decoding differs from reference, update reference before Step 1D")
    print("- If no decoding found, check model.forward() vs evaluation code")
    print()
    print("Next: Step 1D (official killer test reproduction)")
    print("=" * 80)
    print()

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
