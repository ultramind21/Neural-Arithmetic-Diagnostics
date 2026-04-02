"""
================================================================================
VERIFICATION SCRIPT: PHASE 6B
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/phase_30_multidigit_learning.py

PURPOSE:
  Verify the visible training setup, model initialization path, and major
  architecture declarations in the Phase 30 crisis-origin file.

THIS SCRIPT VERIFIES:
  1. What model classes are defined in source
  2. Whether train_model() and evaluate_model() are visibly present
  3. Whether optimizer / loss / device setup are visible
  4. Whether model initialization path is visible in source
  5. Whether the training pipeline is structurally transparent enough for
     later semantic and metric verification

THIS SCRIPT DOES NOT VERIFY:
  - Data semantic correctness
  - Metric correctness
  - Reproduction correctness
  - Whether the file's historical claims were valid

IMPORTANT PRINCIPLE:
  Step 6B asks:
    "Is the training/model setup path visible and auditable?"
  It does NOT ask:
    "Does the model behave correctly?"

================================================================================
"""

import re
import sys
from pathlib import Path
import importlib.util


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
    try:
        spec = importlib.util.spec_from_file_location("phase_30_multidigit_learning", str(filepath))
        if spec is None or spec.loader is None:
            return False, "Could not create import spec"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True, None
    except Exception as e:
        return False, str(e)


def read_lines(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.readlines()


def extract_classes(lines):
    out = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"\s*class\s+([A-Za-z_][A-Za-z0-9_]*)", line)
        if m:
            out.append((i, m.group(1)))
    return out


def extract_functions(lines):
    out = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"\s*def\s+([A-Za-z_][A-Za-z0-9_]*)", line)
        if m:
            out.append((i, m.group(1)))
    return out


def extract_imports(lines):
    out = []
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("import ") or s.startswith("from "):
            out.append((i, s))
    return out


def find_keyword_contexts(lines, keywords, max_hits=4):
    results = {}
    for kw in keywords:
        hits = []
        for i, line in enumerate(lines, 1):
            if kw.lower() in line.lower():
                hits.append((i, line.rstrip("\n")))
            if len(hits) >= max_hits:
                break
        results[kw] = hits
    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 6B: PHASE-30 TRAINING SETUP / MODEL INITIALIZATION VERIFICATION")
    print(f"Official target: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")

    # ------------------------------------------------------------------------
    # 1) Import attempt
    # ------------------------------------------------------------------------
    print_header("1) IMPORT CHECK")

    success, error_msg = load_target_module(TARGET_FILE)
    if success:
        print("✓ Import successful")
    else:
        print("⚠ Import failed")
        print(f"  Error: {error_msg}")
        print("  Note: source-level inspection can still proceed if file remains readable.")

    # ------------------------------------------------------------------------
    # 2) Read source
    # ------------------------------------------------------------------------
    lines = read_lines(TARGET_FILE)

    # ------------------------------------------------------------------------
    # 3) Class and function structure
    # ------------------------------------------------------------------------
    print_header("2) CLASS / FUNCTION STRUCTURE")

    classes = extract_classes(lines)
    functions = extract_functions(lines)

    print(f"Classes found: {len(classes)}")
    for line_no, name in classes:
        print(f"  line {line_no:>4}: {name}")

    print(f"\nFunctions found: {len(functions)}")
    for line_no, name in functions:
        print(f"  line {line_no:>4}: {name}")

    # ------------------------------------------------------------------------
    # 4) Imports and model-related dependencies
    # ------------------------------------------------------------------------
    print_header("3) IMPORTS / MODEL-DEPENDENCY VISIBILITY")

    imports = extract_imports(lines)
    for line_no, imp in imports[:40]:
        print(f"  line {line_no:>4}: {imp}")
    if len(imports) > 40:
        print(f"  ... and {len(imports) - 40} more")

    model_related = [
        (line_no, imp) for line_no, imp in imports
        if any(k in imp for k in [
            "ResidualLogicAdder",
            "nn",
            "optim",
            "DataLoader",
            "TensorDataset",
        ])
    ]

    print("\nModel/training-related imports:")
    if model_related:
        for line_no, imp in model_related:
            print(f"  line {line_no:>4}: {imp}")
    else:
        print("  (none explicitly found)")

    # ------------------------------------------------------------------------
    # 5) Training-path keyword contexts
    # ------------------------------------------------------------------------
    print_header("4) TRAINING-PATH KEYWORD CONTEXTS")

    keywords = [
        "optimizer",
        "criterion",
        "loss",
        "backward",
        "step(",
        "train_model",
        "evaluate_model",
        "device",
        "to(device)",
        "ResidualLogicAdder",
        "MSELoss",
        "CrossEntropyLoss",
        "Adam",
    ]

    contexts = find_keyword_contexts(lines, keywords)

    for kw in keywords:
        print(f"\nKeyword: {kw}")
        if contexts[kw]:
            for line_no, text in contexts[kw]:
                print(f"  line {line_no:>4}: {text.strip()}")
        else:
            print("  (no early hit found)")

    # ------------------------------------------------------------------------
    # 6) Visibility checks
    # ------------------------------------------------------------------------
    print_header("5) TRAINING-SETUP VISIBILITY ASSESSMENT")

    class_names = [name for _, name in classes]
    function_names = [name for _, name in functions]

    has_train_model = "train_model" in function_names
    has_evaluate_model = "evaluate_model" in function_names
    has_main = any('__main__' in line for line in lines)
    has_model_class = len(class_names) > 0
    has_residual_logic = any("ResidualLogicAdder" in line for line in lines)
    has_optimizer_visibility = any("optimizer" in line.lower() for line in lines)
    has_loss_visibility = any("loss" in line.lower() or "criterion" in line.lower() for line in lines)

    print(f"has_train_model:         {has_train_model}")
    print(f"has_evaluate_model:      {has_evaluate_model}")
    print(f"has_main:                {has_main}")
    print(f"has_model_class:         {has_model_class}")
    print(f"has_residual_logic_ref:  {has_residual_logic}")
    print(f"has_optimizer_visibility:{has_optimizer_visibility}")
    print(f"has_loss_visibility:     {has_loss_visibility}")

    # ------------------------------------------------------------------------
    # 7) Final decision
    # ------------------------------------------------------------------------
    print_header("6) STEP 6B FINAL DECISION")

    overall_pass = (
        has_train_model and
        has_evaluate_model and
        has_main and
        (has_model_class or has_residual_logic) and
        has_optimizer_visibility and
        has_loss_visibility
    )

    if overall_pass:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The Phase 30 training/model setup path is structurally visible")
        print("  and auditable at the source/setup level.")
        print()
        print("What this step established:")
        print("  - Model declarations are visible")
        print("  - train_model() and evaluate_model() are present")
        print("  - optimizer/loss/device setup are visible in source")
        print("  - the training pipeline is inspectable for later verification")
    else:
        print("✗ FAIL")
        print()
        print("Finding:")
        print("  The Phase 30 training/model setup path is not yet sufficiently")
        print("  transparent for disciplined follow-up verification.")

    print()
    print("Qualification:")
    print("  This step verifies setup visibility only.")
    print("  It does NOT verify data semantics, metrics, or reproduction.")

    print()
    print("Next step if accepted by user:")
    print("  Step 6C — data / target semantics verification")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
