"""
================================================================================
VERIFICATION SCRIPT: PHASE 26C STEP 2A
================================================================================

OFFICIAL TARGET:
  File: src/train/phase_26c_failure_audit.py

PURPOSE:
  Verify the source/setup structure of the official Project 1 baseline script.

THIS SCRIPT VERIFIES:
  1. The official target file exists
  2. The file can be imported safely (if possible)
  3. What model classes / helper functions are defined or referenced
  4. Whether seed handling appears in the source
  5. Whether data-generation, split, and metric-related code sections exist
  6. Whether the script structure matches its intended baseline role

THIS SCRIPT DOES NOT VERIFY:
  - Correctness of data split
  - Ground-truth correctness
  - Metric correctness
  - Actual reproduction of results

IMPORTANT PRINCIPLE:
  This is source/setup inspection only.
  It establishes what the script is structurally doing before any deeper audit.

================================================================================
"""

import inspect
import importlib.util
from pathlib import Path


# -----------------------------------------------------------------------------
# PATHS
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "phase_26c_failure_audit.py"


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def load_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def print_source_excerpt(file_path: Path, keywords, context=6):
    print("\n" + "=" * 80)
    print(f"SOURCE EXCERPTS: {file_path.name}")
    print("=" * 80)

    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()

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
        print("No keyword matches found.")


def summarize_functions_and_classes(module):
    print("\n" + "=" * 80)
    print("MODULE STRUCTURE SUMMARY")
    print("=" * 80)

    classes_found = []
    functions_found = []

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            # Only list classes that come from this module
            if getattr(obj, "__module__", None) == module.__name__:
                classes_found.append(name)
        elif inspect.isfunction(obj):
            if getattr(obj, "__module__", None) == module.__name__:
                functions_found.append(name)

    print("\nClasses defined in module:")
    if classes_found:
        for c in classes_found:
            print(f"  - {c}")
    else:
        print("  (none found)")

    print("\nFunctions defined in module:")
    if functions_found:
        for f in functions_found:
            print(f"  - {f}")
    else:
        print("  (none found)")


def summarize_candidate_methods(module):
    print("\n" + "=" * 80)
    print("CANDIDATE STRUCTURAL ELEMENTS")
    print("=" * 80)

    candidate_keywords = [
        "seed", "random", "split", "train", "test", "pair",
        "carry", "digit", "accuracy", "eval", "dataset"
    ]

    found = []

    for name, obj in inspect.getmembers(module):
        lower_name = name.lower()
        if any(k in lower_name for k in candidate_keywords):
            found.append(name)

    if found:
        for item in sorted(set(found)):
            print(f"  - {item}")
    else:
        print("  No obvious candidate names found by keyword scan.")


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    print("\n" + "=" * 80)
    print("PHASE 26C STEP 2A: SOURCE / SETUP VERIFICATION")
    print("=" * 80)
    print(f"Official target: {TARGET_FILE}")
    print()

    # Step A1: file existence
    if not TARGET_FILE.exists():
        print("ERROR: Official target file does not exist.")
        return

    print("✓ Official target file exists.")

    # Step A2: import module
    try:
        module = load_module_from_path("phase26c_module", TARGET_FILE)
        print("✓ Official target imported successfully.")
        imported = True
    except Exception as e:
        print(f"⚠ Import failed: {e}")
        print("Proceeding with source inspection only.")
        module = None
        imported = False

    # Step A3: source-level excerpts
    print_source_excerpt(
        TARGET_FILE,
        keywords=[
            "seed",
            "random",
            "pair",
            "train",
            "test",
            "split",
            "carry",
            "digit",
            "accuracy",
            "evaluate",
            "mlp",
            "transformer",
            "lstm",
        ],
        context=6
    )

    # Step A4: module summary if import worked
    if imported:
        summarize_functions_and_classes(module)
        summarize_candidate_methods(module)

    # Step A5: final setup assessment
    print("\n" + "=" * 80)
    print("STEP 2A FINAL STATUS")
    print("=" * 80)
    print("This step verifies only the source/setup layer.")
    print()

    print("What this step should let us answer:")
    print("  ✓ Does the official baseline file exist?")
    print("  ✓ Can it be imported safely?")
    print("  ✓ What structural elements does it contain?")
    print("  ✓ Are data/split/metric/seed sections visibly present in source?")
    print()

    print("What still remains open:")
    print("  - actual data split correctness")
    print("  - actual ground-truth correctness")
    print("  - actual metric correctness")
    print("  - reproduction of reported results")
    print()

    print("Next recommended step:")
    print("  Step 2B — Data generation and split verification")
    print("=" * 80)


if __name__ == "__main__":
    main()
