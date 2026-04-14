"""
================================================================================
VERIFICATION SCRIPT: PHASE 27C STEP 3A
================================================================================

OFFICIAL TARGET:
  File: src/train/phase_27c_architecture_audit.py

PURPOSE:
  Verify Project 2 (Phase 27c) source file and setup structure.

THIS SCRIPT VERIFIES:
  1. The official Phase 27c script exists and can be imported
  2. What architectural models are defined or compared
  3. What data generation/split logic is present
  4. What baseline or reference is being used
  5. What metrics or evaluation structure is defined
  6. Whether setup section is transparent enough to understand the comparison intent

THIS SCRIPT DOES NOT VERIFY:
  - Whether results are correct
  - Whether metrics are computed correctly
  - Whether the comparison is mechanistically valid
  - Full reproduction (that comes later)

IMPORTANT PRINCIPLE:
  This is source-level structural inspection only.
  No execution, no results collection
  = we're just checking if the script is understandable at source level

================================================================================
"""

import re
import sys
from pathlib import Path


# ============================================================================
# PATHS
# ============================================================================
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "phase_27c_architecture_audit.py"


# ============================================================================
# HELPERS
# ============================================================================
def fail(msg):
    print(f"\nERROR: {msg}")
    sys.exit(1)


def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def attempt_import(filepath):
    """
    Try to import the target file as a Python module.
    Returns (success: bool, error_msg: str or None)
    """
    try:
        spec = __import__('importlib.util').util.spec_from_file_location(
            "phase_27c", str(filepath)
        )
        module = __import__('importlib.util').util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True, None
    except Exception as e:
        return False, str(e)


def read_file_with_line_numbers(filepath):
    """Read file and return list of (line_number, content) tuples."""
    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                lines.append((i, line.rstrip('\n')))
    except Exception as e:
        fail(f"Cannot read file: {e}")
    return lines


def find_keyword_contexts(lines, keywords, context_lines=5):
    """
    Find all lines containing keywords and return with surrounding context.
    Returns dict: keyword -> list of (line_number, context_block) tuples
    """
    results = {}
    for kw in keywords:
        results[kw] = []
    
    for i, (line_num, content) in enumerate(lines):
        for kw in keywords:
            if kw in content.lower():
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                context_block = '\n'.join(
                    f"{lines[j][0]:05d}: {lines[j][1]}"
                    for j in range(start, end)
                )
                results[kw].append((line_num, context_block))
    
    return results


def extract_class_definitions(lines):
    """Extract all class definitions."""
    classes = []
    for line_num, content in lines:
        if content.strip().startswith('class '):
            match = re.match(r'class\s+(\w+)', content)
            if match:
                classes.append((line_num, match.group(1)))
    return classes


def extract_function_definitions(lines):
    """Extract all function definitions."""
    functions = []
    for line_num, content in lines:
        if content.strip().startswith('def '):
            match = re.match(r'def\s+(\w+)', content)
            if match:
                functions.append((line_num, match.group(1)))
    return functions


# ============================================================================
# MAIN
# ============================================================================
def main():
    print_header("PHASE 27C STEP 3A: SOURCE / SETUP VERIFICATION")
    print(f"Official target: {TARGET_FILE}")
    print()

    # Check file existence
    if not TARGET_FILE.exists():
        fail(f"Official target file not found: {TARGET_FILE}")
    
    print("✓ Official target file exists.")
    print()

    # Try import
    print("Attempting import...")
    success, error = attempt_import(TARGET_FILE)
    if success:
        print("✓ Official target imported successfully (no syntax errors).")
    else:
        print(f"⚠️ Import failed: {error}")
        print("(This may be expected if script has external dependencies.)")
    print()

    # Read file
    print("Reading file structure...")
    lines = read_file_with_line_numbers(TARGET_FILE)
    total_lines = len(lines)
    print(f"✓ File has {total_lines} lines.")
    print()

    # Extract classes and functions
    print_header("MODULE STRUCTURE")
    classes = extract_class_definitions(lines)
    functions = extract_function_definitions(lines)
    
    print("Classes defined in module:")
    if classes:
        for line_num, class_name in classes:
            print(f"  {class_name:30} (line {line_num})")
    else:
        print("  (none found)")
    
    print()
    print("Functions defined in module:")
    if functions:
        # Show first 20
        for line_num, func_name in functions[:20]:
            print(f"  {func_name:30} (line {line_num})")
        if len(functions) > 20:
            print(f"  ... and {len(functions) - 20} more")
    else:
        print("  (none found)")
    
    print()

    # Search for key structural elements
    print_header("KEY STRUCTURAL ELEMENTS")
    
    keywords = [
        'seed', 'random', 'model', 'train', 'test', 'accuracy', 
        'metric', 'loss', 'evaluate', 'baseline', 'architecture',
        'dataloader', 'pair', 'digit', 'carry', 'import torch'
    ]
    
    contexts = find_keyword_contexts(lines, keywords, context_lines=2)
    
    for kw, occurrences in contexts.items():
        if occurrences:
            print(f"\nKeyword: '{kw}'")
            print("-" * 80)
            for line_num, context in occurrences[:1]:  # Show first occurrence only
                print(f"Line {line_num}:")
                print(context)
            if len(occurrences) > 1:
                print(f"  ... and {len(occurrences) - 1} more occurrence(s)")

    print()

    # Summary
    print_header("STEP 3A INITIAL ASSESSMENT")
    print("What this step establishes:")
    print("  ✓ Whether the official Phase 27c script exists and can be accessed")
    print("  ✓ What core classes/functions are defined")
    print("  ✓ Whether key structural elements (seeds, models, data, metrics) are visible")
    print("  ✓ Whether setup is transparent enough for further inspection")
    print()
    print("What remains open after this step:")
    print("  - Whether imported modules execute successfully")
    print("  - Whether data split is actually executed correctly")
    print("  - Whether results are correct")
    print("  - Full architectural comparison details")
    print()
    print("Next recommended step:")
    print("  Step 3B — Data generation / split verification")
    print("=" * 80)


if __name__ == "__main__":
    main()
