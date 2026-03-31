"""
================================================================================
VERIFICATION SCRIPT: PHASE 26C STEP 2C
================================================================================

OFFICIAL TARGET:
  File: src/train/phase_26c_failure_audit.py

PURPOSE:
  Verify the ground-truth / target semantics used in the official Project 1
  baseline script.

THIS SCRIPT VERIFIES:
  1. What the model is actually being asked to predict
  2. Whether digit and carry targets are defined clearly in the source
  3. Whether arithmetic target computation is consistent with single-digit addition
     with carry-in / carry-out
  4. Whether target semantics match the Project 1 interpretation

THIS SCRIPT DOES NOT VERIFY:
  - Model training quality
  - Final accuracy reproduction
  - Metric correctness
  - Deep internal model mechanism

IMPORTANT PRINCIPLE:
  This step focuses on the semantics of the labels/targets.
  It is about "what truth is being supervised?" not "how well is it learned?"

================================================================================
"""

import ast
from pathlib import Path


# -----------------------------------------------------------------------------
# PATHS
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = ROOT / "src" / "train" / "phase_26c_failure_audit.py"


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_source_excerpt(file_path: Path, keywords, context=6):
    print_header(f"SOURCE EXCERPTS: {file_path.name}")

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


def reference_single_digit_addition(a, b, carry_in):
    """
    Independent reference implementation for single-digit addition with carry.
    Returns:
        total_sum
        digit_out
        carry_out
    """
    total = a + b + carry_in
    digit_out = total % 10
    carry_out = 1 if total >= 10 else 0
    return total, digit_out, carry_out


def run_hand_check_cases():
    """
    Hand-check a few representative cases to anchor the intended semantics.
    """
    print_header("INDEPENDENT REFERENCE: HAND-CHECK CASES")

    test_cases = [
        (0, 0, 0),
        (0, 0, 1),
        (4, 5, 0),
        (4, 5, 1),
        (9, 0, 0),
        (9, 0, 1),
        (9, 9, 0),
        (9, 9, 1),
    ]

    print(f"{'a':>2} | {'b':>2} | {'c_in':>4} | {'sum':>3} | {'digit':>5} | {'c_out':>5}")
    print("-" * 40)

    for a, b, c_in in test_cases:
        total, digit_out, carry_out = reference_single_digit_addition(a, b, c_in)
        print(f"{a:>2} | {b:>2} | {c_in:>4} | {total:>3} | {digit_out:>5} | {carry_out:>5}")

    print()
    print("Interpretation:")
    print("  - digit_out = (a + b + carry_in) % 10")
    print("  - carry_out = 1 if (a + b + carry_in) >= 10 else 0")


def inspect_target_semantics(file_text):
    """
    Search for target-related semantics in the source.
    """
    lower = file_text.lower()

    findings = {
        "digit_keyword_present": ("digit" in lower),
        "carry_keyword_present": ("carry" in lower),
        "sum_keyword_present": ("sum" in lower),
        "mod10_present": ("% 10" in file_text or "%10" in file_text),
        "carry_threshold_present": (">= 10" in file_text or ">=10" in file_text),
        "target_word_present": ("target" in lower),
        "label_word_present": ("label" in lower),
    }

    return findings


def print_findings(findings):
    print_header("TARGET SEMANTICS INDICATORS")
    for k, v in findings.items():
        print(f"{k:<28}: {'✓ FOUND' if v else '✗ NOT FOUND'}")


def parse_literal_assignments(file_text):
    """
    Best-effort extraction of simple literal assignments.
    """
    results = {}
    try:
        tree = ast.parse(file_text)
    except Exception:
        return results

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id
                    try:
                        value = ast.literal_eval(node.value)
                        results[name] = value
                    except Exception:
                        pass
    return results


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    print_header("PHASE 26C STEP 2C: GROUND-TRUTH / TARGET SEMANTICS VERIFICATION")
    print(f"Official target: {TARGET_FILE}")
    print()

    if not TARGET_FILE.exists():
        print("ERROR: Official target file does not exist.")
        return

    file_text = TARGET_FILE.read_text(encoding="utf-8")

    # 1) Source excerpts related to target semantics
    print_source_excerpt(
        TARGET_FILE,
        keywords=[
            "digit",
            "carry",
            "sum",
            "target",
            "label",
            "% 10",
            ">= 10",
            "carry_in",
            "carry_out",
        ],
        context=6
    )

    # 2) Best-effort literal recovery
    literals = parse_literal_assignments(file_text)
    print_header("RECOVERED SIMPLE LITERAL ASSIGNMENTS (BEST EFFORT)")
    if literals:
        for k, v in sorted(literals.items()):
            print(f"{k} = {v}")
    else:
        print("No simple literal assignments recovered.")

    # 3) Independent arithmetic reference
    run_hand_check_cases()

    # 4) Semantic indicators
    findings = inspect_target_semantics(file_text)
    print_findings(findings)

    # 5) Final assessment
    print_header("STEP 2C FINAL STATUS")
    print("This step verifies target semantics at the source/meaning level.")
    print()

    print("Questions this step should help answer:")
    print("  ✓ Is the task framed in terms of digit/carry or total sum?")
    print("  ✓ Is carry explicitly represented in the supervision logic?")
    print("  ✓ Does the script appear consistent with single-digit addition semantics?")
    print()

    print("What remains open after this step:")
    print("  - whether these targets are used correctly during training")
    print("  - whether metrics evaluate these targets correctly")
    print("  - whether the reported baseline reproduces")
    print()

    print("Next recommended step:")
    print("  Step 2D — Metric verification")
    print("=" * 80)


if __name__ == "__main__":
    main()
