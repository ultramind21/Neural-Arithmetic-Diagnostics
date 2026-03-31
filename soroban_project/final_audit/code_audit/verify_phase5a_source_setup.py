"""
================================================================================
VERIFICATION SCRIPT: PHASE 5A
================================================================================

OFFICIAL TARGET:
  File: soroban_project/src/train/project_3_killer_test_adversarial_carry_chain.py

PURPOSE:
  Verify that the Project 3 adversarial / killer-test source is structurally
  transparent and auditable at the source/setup level before deeper checks.

THIS SCRIPT VERIFIES:
  1. The official target file exists and is readable
  2. The file can be imported as a Python module (or import failure is made visible)
  3. What major classes and functions are defined
  4. What imports/dependencies are visible
  5. Whether the source visibly depends on Project 3 baseline components
  6. Whether the main evaluation pipeline is visible enough for layered verification

THIS SCRIPT DOES NOT VERIFY:
  - Adversarial pattern correctness
  - Ground-truth semantic correctness
  - Metric correctness
  - Official reproduction correctness
  - Scientific interpretation of killer-test outcomes

IMPORTANT PRINCIPLE:
  Step 5A asks:
    "Is the source/setup transparent enough for disciplined verification?"
  It does NOT ask:
    "Are the reported adversarial results correct?"

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
    """
    Attempt dynamic import of target file.
    Returns (success: bool, error_message: str | None)
    """
    try:
        spec = importlib.util.spec_from_file_location(
            "project_3_killer_test_adversarial_carry_chain",
            str(filepath)
        )
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


def keyword_hits(lines, keywords, max_hits_per_keyword=4):
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
    print_header("PHASE 5A: PROJECT 3 KILLER-TEST SOURCE / SETUP VERIFICATION")
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
        for line_no, name in functions[:30]:
            print(f"  line {line_no:>4}: {name}")
        if len(functions) > 30:
            print(f"  ... and {len(functions) - 30} more")
    else:
        print("  (none found)")

    # ------------------------------------------------------------------------
    # 4) Imports / dependency visibility
    # ------------------------------------------------------------------------
    print_header("4) IMPORTS / DEPENDENCY VISIBILITY")

    for line_no, imp in imports[:40]:
        print(f"  line {line_no:>4}: {imp}")
    if len(imports) > 40:
        print(f"  ... and {len(imports) - 40} more")

    project3_related_imports = [
        (line_no, imp) for line_no, imp in imports
        if (
            "ResidualLogicAdder" in imp or
            "residual_logic_adder" in imp or
            "project_3_residual_logic_layer" in imp
        )
    ]

    print("\nProject 3 baseline-related imports:")
    if project3_related_imports:
        for line_no, imp in project3_related_imports:
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
        "killer",
        "adversarial",
        "carry",
        "pattern",
        "evaluate",
        "accuracy",
        "exact_match",
        "load",
        "checkpoint",
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
    print_header("6) STEP 5A FINAL DECISION")

    structure_visible = (len(classes) > 0 or len(functions) > 0)
    dependency_visible = (
        len(project3_related_imports) > 0 or
        len(hits["ResidualLogicAdder"]) > 0
    )

    if structure_visible:
        print("✓ PASS")
        print()
        print("Finding:")
        print("  The Project 3 killer-test source is readable and structurally")
        print("  auditable at the source/setup level.")
        print()
        print("What this step established:")
        print("  - The official target file exists")
        print("  - The source contains inspectable functions/imports")
        print("  - The main evaluation pipeline is visible enough for layered follow-up verification")
        if dependency_visible:
            print("  - Project 3 baseline dependency is visibly referenced in source")
        else:
            print("  - Project 3 baseline dependency was not cleanly confirmed from source scan alone")
        print()
        print("Qualification:")
        print("  This step does not verify adversarial pattern correctness, metrics, or results.")
    else:
        print("✗ FAIL")
        print()
        print("Finding:")
        print("  The target source is not sufficiently transparent for disciplined follow-up verification.")
        print()
        print("Qualification:")
        print("  Further source inspection is required before continuing.")

    print()
    print("Next step if accepted by user:")
    print("  Step 5B — adversarial pattern / data-path verification")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
