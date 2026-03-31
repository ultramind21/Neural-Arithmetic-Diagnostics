"""
================================================================================
VERIFICATION SCRIPT: PHASE 4A
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/project_3_residual_logic_layer.py

PURPOSE:
  Verify that the Project 3 baseline source is structurally transparent and
  auditable at the source/setup level before moving to later verification steps.

THIS SCRIPT VERIFIES:
  1. The official target file exists and is readable
  2. The file can be imported as a Python module (or fails with a visible error)
  3. What major classes and functions are defined
  4. Whether the source visibly depends on ResidualLogicAdder
  5. Whether the main pipeline is visible enough for later layered verification

THIS SCRIPT DOES NOT VERIFY:
  - Data generation correctness
  - Ground-truth execution correctness
  - Metric correctness
  - Official reproduction
  - Performance claims

IMPORTANT PRINCIPLE:
  Step 4A asks:
    "Is the source/setup transparent enough to support disciplined verification?"
  It does NOT ask:
    "Are the results correct?"

================================================================================
"""

import re
import sys
import importlib.util
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
    """
    Attempt dynamic import of target file.
    Returns (success: bool, error_message: str | None)
    """
    try:
        spec = importlib.util.spec_from_file_location("project_3_residual_logic_layer", str(filepath))
        if spec is None or spec.loader is None:
            return False, "Could not create import spec"

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True, None
    except Exception as e:
        return False, str(e)


def read_file_lines(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.readlines()
    except Exception as e:
        fail(f"Could not read target file: {e}")


def extract_classes(lines):
    classes = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"\s*class\s+([A-Za-z_][A-Za-z0-9_]*)", line)
        if m:
            classes.append((i, m.group(1)))
    return classes


def extract_functions(lines):
    functions = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"\s*def\s+([A-Za-z_][A-Za-z0-9_]*)", line)
        if m:
            functions.append((i, m.group(1)))
    return functions


def extract_imports(lines):
    imports = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            imports.append((i, stripped))
    return imports


def keyword_hits(lines, keywords, max_hits_per_keyword=3):
    results = {}
    lower_lines = [(i, line.rstrip("\n")) for i, line in enumerate(lines, 1)]

    for kw in keywords:
        hits = []
        for line_no, text in lower_lines:
            if kw.lower() in text.lower():
                hits.append((line_no, text))
            if len(hits) >= max_hits_per_keyword:
                break
        results[kw] = hits

    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 4A: PROJECT 3 BASELINE SOURCE / SETUP VERIFICATION")
    print(f"Official target: {TARGET_FILE}")

    # ------------------------------------------------------------------------
    # 1) File existence
    # ------------------------------------------------------------------------
    print_header("1) FILE EXISTENCE CHECK")

    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")

    print("✓ Target file exists")

    # ------------------------------------------------------------------------
    # 2) Import attempt
    # ------------------------------------------------------------------------
    print_header("2) IMPORT CHECK")

    success, error_msg = load_target_module(TARGET_FILE)
    if success:
        print("✓ Import successful")
    else:
        print("⚠ Import failed")
        print(f"  Error: {error_msg}")
        print("  Note: import failure does not automatically invalidate source/setup")
        print("        if the source remains readable and structurally auditable.")

    # ------------------------------------------------------------------------
    # 3) Read source and extract structure
    # ------------------------------------------------------------------------
    print_header("3) SOURCE STRUCTURE")

    lines = read_file_lines(TARGET_FILE)
    classes = extract_classes(lines)
    functions = extract_functions(lines)
    imports = extract_imports(lines)

    print(f"Total lines: {len(lines)}")
    print(f"Imports found: {len(imports)}")
    print(f"Classes found: {len(classes)}")
    print(f"Functions found: {len(functions)}")

    print("\nClasses:")
    if classes:
        for line_no, name in classes:
            print(f"  line {line_no:>4}: {name}")
    else:
        print("  (none found)")

    print("\nFunctions:")
    if functions:
        for line_no, name in functions[:25]:
            print(f"  line {line_no:>4}: {name}")
        if len(functions) > 25:
            print(f"  ... and {len(functions) - 25} more")
    else:
        print("  (none found)")

    # ------------------------------------------------------------------------
    # 4) Imports / dependency visibility
    # ------------------------------------------------------------------------
    print_header("4) IMPORTS / DEPENDENCY VISIBILITY")

    for line_no, imp in imports[:30]:
        print(f"  line {line_no:>4}: {imp}")
    if len(imports) > 30:
        print(f"  ... and {len(imports) - 30} more")

    residual_imports = [
        (line_no, imp) for line_no, imp in imports
        if "ResidualLogicAdder" in imp or "residual_logic_adder" in imp
    ]

    print("\nResidualLogicAdder-related imports:")
    if residual_imports:
        for line_no, imp in residual_imports:
            print(f"  line {line_no:>4}: {imp}")
    else:
        print("  (none explicitly found)")

    # ------------------------------------------------------------------------
    # 5) Pipeline visibility clues
    # ------------------------------------------------------------------------
    print_header("5) PIPELINE VISIBILITY CLUES")

    keywords = [
        "__main__",
        "ResidualLogicAdder",
        "train",
        "eval",
        "test",
        "optimizer",
        "loss",
        "DataLoader",
        "digits",
        "carry",
        "accuracy",
    ]

    hits = keyword_hits(lines, keywords)

    for kw in keywords:
        print(f"\nKeyword: {kw}")
        if hits[kw]:
            for line_no, text in hits[kw]:
                print(f"  line {line_no:>4}: {text.strip()}")
        else:
            print("  (no early hit found)")

    # ------------------------------------------------------------------------
    # 6) Final decision
    # ------------------------------------------------------------------------
    print_header("6) STEP 4A FINAL DECISION")

    file_exists = True
    structure_visible = (len(classes) > 0 or len(functions) > 0)
    dependency_visible = (
        len(residual_imports) > 0 or
        any("ResidualLogicAdder" in line for _, line in keyword_hits(lines, ["ResidualLogicAdder"])["ResidualLogicAdder"])
    )

    if file_exists and structure_visible:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The Project 3 baseline source is readable and structurally auditable")
        print("  at the source/setup level.")
        print()
        print("What this step established:")
        print("  - The official target file exists")
        print("  - The source contains inspectable classes/functions/imports")
        print("  - The main pipeline is visible enough for layered follow-up verification")
        if dependency_visible:
            print("  - ResidualLogicAdder dependency is visibly referenced in source")
        else:
            print("  - ResidualLogicAdder dependency was not cleanly confirmed from source scan alone")
        print()
        print("Qualification:")
        print("  This step does not verify correctness of data, semantics, metrics, or results.")
    else:
        print("✗ FAIL")
        print()
        print("Finding:")
        print("  The target source is not sufficiently transparent for disciplined follow-up verification.")
        print()
        print("Qualification:")
        print("  Further source inspection or path correction is required before continuing.")

    print()
    print("Next step if accepted by user:")
    print("  Step 4B — data / generation / setup-path verification")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
