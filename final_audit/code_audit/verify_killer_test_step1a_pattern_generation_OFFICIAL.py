"""
================================================================================
VERIFICATION SCRIPT: KILLER TEST STEP 1A
================================================================================

OFFICIAL TARGET:
  File: src/train/project_3_killer_test_adversarial_carry_chain.py

PURPOSE:
  Verify the ACTUAL pattern generation logic used in the official killer test.

THIS SCRIPT VERIFIES:
  1. Whether the official killer test file can be imported safely
  2. What pattern-generation functions/objects actually exist in that file
  3. The actual generated sequences (a, b) and ground truth outputs
  4. Whether the generated patterns match the documented descriptions

THIS SCRIPT DOES NOT VERIFY:
  - Model training
  - Model predictions
  - Metric computation
  - Any performance claim

IMPORTANT PRINCIPLE:
  This is verification by extraction / inspection of the official source,
  NOT by re-implementing assumed pattern logic from scratch.

OUTPUT:
  - Source inspection summary
  - Candidate generator functions found
  - Extracted/generated pattern traces
  - Manual-verification tables for first positions

================================================================================
"""

import os
import sys
import inspect
import importlib.util
from pathlib import Path


# -----------------------------------------------------------------------------
# PATH SETUP
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "project_3_killer_test_adversarial_carry_chain.py"

print("\n" + "=" * 80)
print("KILLER TEST STEP 1A: OFFICIAL PATTERN GENERATION VERIFICATION")
print("=" * 80)
print(f"Repository root: {ROOT}")
print(f"Official target: {TARGET_FILE}")
print()


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def load_module_from_path(module_name: str, file_path: Path):
    """Dynamically load a Python module from a path."""
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for: {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compute_ground_truth(a_seq, b_seq):
    """
    Compute digit_out and carry_out from raw digit sequences.
    Assumes least-significant-digit-first order, position by position.
    """
    digit_out = []
    carry_out = []
    carry = 0

    for i in range(len(a_seq)):
        total = a_seq[i] + b_seq[i] + carry
        digit = total % 10
        carry = 1 if total >= 10 else 0

        digit_out.append(digit)
        carry_out.append(carry)

    return digit_out, carry_out


def print_pattern_table(name, a_seq, b_seq, digit_out, carry_out, show_n=20):
    """Pretty-print first positions of a pattern."""
    print("\n" + "=" * 80)
    print(f"PATTERN TRACE: {name}")
    print("=" * 80)
    print(f"Length: {len(a_seq)}")
    print(f"First {min(show_n, len(a_seq))} positions:")
    print()

    print(f"{'pos':>4} | {'a':>2} | {'b':>2} | {'c_in':>4} | {'sum':>3} | {'digit':>5} | {'c_out':>5}")
    print("-" * 50)

    carry_in = 0
    for i in range(min(show_n, len(a_seq))):
        total = a_seq[i] + b_seq[i] + carry_in
        print(
            f"{i:>4} | {a_seq[i]:>2} | {b_seq[i]:>2} | {carry_in:>4} | {total:>3} | {digit_out[i]:>5} | {carry_out[i]:>5}"
        )
        carry_in = carry_out[i]

    print()
    print(f"a[:{show_n}]      = {a_seq[:show_n]}")
    print(f"b[:{show_n}]      = {b_seq[:show_n]}")
    print(f"digit_out[:{show_n}] = {digit_out[:show_n]}")
    print(f"carry_out[:{show_n}] = {carry_out[:show_n]}")
    print(f"carry count      = {sum(carry_out)}")
    carry_positions = [i for i, c in enumerate(carry_out) if c == 1]
    print(f"carry positions (first 30) = {carry_positions[:30]}")
    print()


def looks_like_sequence_pair(obj):
    """
    Check whether obj might be a tuple/list containing two sequences (a, b),
    or more sequences (a, b, digit_out, carry_out).
    """
    if not isinstance(obj, (tuple, list)):
        return False
    if len(obj) < 2:
        return False
    if not isinstance(obj[0], (list, tuple)):
        return False
    if not isinstance(obj[1], (list, tuple)):
        return False
    return True


def try_extract_pattern_from_return(name, returned_obj):
    """
    Attempt to normalize returned pattern object into:
      a_seq, b_seq, digit_out, carry_out
    """
    if not looks_like_sequence_pair(returned_obj):
        return None

    # Case 1: returned (a_seq, b_seq, digit_out, carry_out)
    if len(returned_obj) >= 4:
        a_seq = list(returned_obj[0])
        b_seq = list(returned_obj[1])
        digit_out = list(returned_obj[2])
        carry_out = list(returned_obj[3])
        return a_seq, b_seq, digit_out, carry_out

    # Case 2: returned only (a_seq, b_seq)
    if len(returned_obj) == 2:
        a_seq = list(returned_obj[0])
        b_seq = list(returned_obj[1])
        digit_out, carry_out = compute_ground_truth(a_seq, b_seq)
        return a_seq, b_seq, digit_out, carry_out

    return None


def print_source_excerpt(file_path: Path, keywords, context=8):
    """Print source lines around keyword hits for manual inspection."""
    print("\n" + "=" * 80)
    print("SOURCE EXCERPTS FOR MANUAL INSPECTION")
    print("=" * 80)

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
        print("No keyword matches found.")
    print()


# -----------------------------------------------------------------------------
# STEP 1: VERIFY TARGET FILE EXISTS
# -----------------------------------------------------------------------------
if not TARGET_FILE.exists():
    print("ERROR: Official target file does not exist.")
    sys.exit(1)

print("✓ Official target file exists.\n")


# -----------------------------------------------------------------------------
# STEP 2: LOAD MODULE
# -----------------------------------------------------------------------------
try:
    killer_module = load_module_from_path("killer_test_module", TARGET_FILE)
    print("✓ Official killer test module imported successfully.\n")
except Exception as e:
    print("ERROR: Could not import official killer test module.")
    print(f"Import error: {e}")
    print("\nProceeding to source-level inspection only.")
    killer_module = None


# -----------------------------------------------------------------------------
# STEP 3: INSPECT AVAILABLE FUNCTIONS / OBJECTS
# -----------------------------------------------------------------------------
candidate_functions = []
candidate_names = [
    "alternating",
    "pattern",
    "chain",
    "block",
    "generate",
    "killer",
]

if killer_module is not None:
    print("=" * 80)
    print("AVAILABLE FUNCTIONS / OBJECTS IN OFFICIAL MODULE")
    print("=" * 80)

    for name, obj in inspect.getmembers(killer_module):
        if inspect.isfunction(obj):
            lower_name = name.lower()
            if any(token in lower_name for token in candidate_names):
                candidate_functions.append((name, obj))
                print(f"Function candidate: {name}{inspect.signature(obj)}")

    if not candidate_functions:
        print("No obvious pattern-generation functions found by name search.")

    print()


# -----------------------------------------------------------------------------
# STEP 4: TRY TO EXECUTE CANDIDATE PATTERN FUNCTIONS
# -----------------------------------------------------------------------------
extracted_patterns = []

if killer_module is not None and candidate_functions:
    print("=" * 80)
    print("ATTEMPTING TO EXTRACT PATTERNS FROM OFFICIAL FUNCTIONS")
    print("=" * 80)

    for func_name, func in candidate_functions:
        sig = inspect.signature(func)
        params = sig.parameters

        print(f"\nTrying function: {func_name}{sig}")

        # Try a few common invocation patterns
        trial_calls = []

        if len(params) == 0:
            trial_calls.append(())
        elif len(params) == 1:
            trial_calls.append((20,))
            trial_calls.append((100,))
        elif len(params) == 2:
            # common guesses: (length, seed) or (length, block_size)
            trial_calls.append((20, 42))
            trial_calls.append((100, 42))
            trial_calls.append((20, 10))
            trial_calls.append((100, 10))
        elif len(params) == 3:
            trial_calls.append((20, 10, 42))
            trial_calls.append((100, 10, 42))

        success = False
        for args in trial_calls:
            try:
                result = func(*args)
                normalized = try_extract_pattern_from_return(func_name, result)
                if normalized is not None:
                    a_seq, b_seq, digit_out, carry_out = normalized
                    extracted_patterns.append((func_name, a_seq, b_seq, digit_out, carry_out))
                    print(f"  ✓ Success with args={args}")
                    success = True
                    break
                else:
                    print(f"  Returned object from args={args}, but format not recognized.")
            except Exception as e:
                print(f"  Failed with args={args}: {e}")

        if not success:
            print(f"  Could not extract usable pattern from function: {func_name}")

    print()


# -----------------------------------------------------------------------------
# STEP 5: PRINT EXTRACTED PATTERNS
# -----------------------------------------------------------------------------
if extracted_patterns:
    print("=" * 80)
    print("EXTRACTED PATTERN TRACES")
    print("=" * 80)

    for func_name, a_seq, b_seq, digit_out, carry_out in extracted_patterns:
        print_pattern_table(func_name, a_seq, b_seq, digit_out, carry_out, show_n=20)
else:
    print("=" * 80)
    print("NO PATTERNS AUTOMATICALLY EXTRACTED")
    print("=" * 80)
    print("This does NOT mean the official file is wrong.")
    print("It means automatic extraction was insufficient.")
    print("Proceeding to source-level keyword inspection.\n")


# -----------------------------------------------------------------------------
# STEP 6: SOURCE-LEVEL MANUAL INSPECTION
# -----------------------------------------------------------------------------
print_source_excerpt(
    TARGET_FILE,
    keywords=[
        "alternating",
        "block",
        "chain",
        "pattern",
        "generate",
        "999",
        "9090",
        "1010",
    ],
    context=6,
)


# -----------------------------------------------------------------------------
# STEP 7: FINAL STATUS
# -----------------------------------------------------------------------------
print("=" * 80)
print("STEP 1A STATUS")
print("=" * 80)

if extracted_patterns:
    print("Result: PARTIAL/AUTOMATED EXTRACTION SUCCESS")
    print("You now have direct traces from functions found in the official file.")
    print("Next action: compare these traces to documented pattern descriptions manually.")
else:
    print("Result: MANUAL SOURCE INSPECTION REQUIRED")
    print("Automatic extraction did not conclusively recover pattern generators.")
    print("Next action: inspect source excerpts and identify exact official pattern definitions.")
    print("Then build a second script that mirrors those definitions exactly.")
print()

print("IMPORTANT:")
print("- Do NOT infer model behavior from this script.")
print("- Do NOT infer metric correctness from this script.")
print("- This script only verifies official pattern-generation definitions/traces.")
print()
print("=" * 80)
print("END OF STEP 1A")
print("=" * 80)
