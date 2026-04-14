"""
================================================================================
VERIFICATION SCRIPT: PHASE 26C STEP 2F
================================================================================

OFFICIAL TARGET:
  File: src/train/phase_26c_failure_audit.py

PURPOSE:
  Describe the behavioral error structure of the Project 1 baseline result,
  after reproduction has been attempted.

THIS SCRIPT VERIFIES / EXPLORES:
  1. Whether errors appear concentrated in specific arithmetic subcases
  2. Whether carry-related cases appear harder than non-carry cases
  3. Whether failures seem localized or broadly distributed
  4. Whether the observed baseline behavior is best described as:
     - broad competence with narrow weak spots
     - or broad weakness with scattered successes

THIS SCRIPT DOES NOT VERIFY:
  - Deep internal mechanism
  - Full causal explanation of failure
  - Whether architecture-level interpretation is final
  - Any claim stronger than behavioral characterization

IMPORTANT PRINCIPLE:
  This is a behavioral characterization step.
  It should remain modest: describe error structure, not overclaim mechanism.

ASSUMPTION:
  This script is most useful AFTER Step 2E reproduction is successful or partially
  understood, and can be adapted once the exact official output format is known.

================================================================================
"""

from collections import defaultdict


# -----------------------------------------------------------------------------
# INDEPENDENT REFERENCE ARITHMETIC
# -----------------------------------------------------------------------------
def single_digit_addition(a, b, carry_in):
    total = a + b + carry_in
    digit_out = total % 10
    carry_out = 1 if total >= 10 else 0
    return total, digit_out, carry_out


# -----------------------------------------------------------------------------
# SYNTHETIC PLACEHOLDER ANALYSIS FRAME
# -----------------------------------------------------------------------------
# NOTE:
# This script does not assume access to official model predictions yet.
# It provides the exact analysis structure needed once prediction pairs
# (truth vs predicted outputs) are available from reproduction logs or direct export.
#
# You can later connect this to:
#   - parsed output dumps
#   - manually exported prediction tables
#   - or a dedicated local-evaluation extraction script


def analyze_cases(case_records):
    """
    case_records: list of dicts, each with keys:
      - a
      - b
      - carry_in
      - digit_true
      - digit_pred
      - carry_true
      - carry_pred

    Returns summary dict.
    """
    summary = {
        "total_cases": len(case_records),
        "digit_correct": 0,
        "carry_correct": 0,
        "exact_correct": 0,
        "carry_cases_total": 0,
        "carry_cases_digit_correct": 0,
        "noncarry_cases_total": 0,
        "noncarry_cases_digit_correct": 0,
        "by_subcase": defaultdict(lambda: {"count": 0, "digit_correct": 0, "carry_correct": 0, "exact_correct": 0}),
    }

    for rec in case_records:
        digit_ok = int(rec["digit_true"] == rec["digit_pred"])
        carry_ok = int(rec["carry_true"] == rec["carry_pred"])
        exact_ok = int(digit_ok and carry_ok)

        summary["digit_correct"] += digit_ok
        summary["carry_correct"] += carry_ok
        summary["exact_correct"] += exact_ok

        if rec["carry_true"] == 1:
            summary["carry_cases_total"] += 1
            summary["carry_cases_digit_correct"] += digit_ok
        else:
            summary["noncarry_cases_total"] += 1
            summary["noncarry_cases_digit_correct"] += digit_ok

        key = (rec["a"], rec["b"], rec["carry_in"])
        summary["by_subcase"][key]["count"] += 1
        summary["by_subcase"][key]["digit_correct"] += digit_ok
        summary["by_subcase"][key]["carry_correct"] += carry_ok
        summary["by_subcase"][key]["exact_correct"] += exact_ok

    return summary


def print_summary(summary):
    print("\n" + "=" * 80)
    print("BEHAVIORAL ERROR STRUCTURE SUMMARY")
    print("=" * 80)

    total = summary["total_cases"]
    if total == 0:
        print("No case records provided.")
        return

    digit_acc = 100.0 * summary["digit_correct"] / total
    carry_acc = 100.0 * summary["carry_correct"] / total
    exact_acc = 100.0 * summary["exact_correct"] / total

    print(f"Total cases:      {total}")
    print(f"Digit accuracy:   {digit_acc:.2f}%")
    print(f"Carry accuracy:   {carry_acc:.2f}%")
    print(f"Exact match:      {exact_acc:.2f}%")
    print()

    if summary["carry_cases_total"] > 0:
        carry_case_acc = 100.0 * summary["carry_cases_digit_correct"] / summary["carry_cases_total"]
        print(f"Carry-conditioned cases:     {summary['carry_cases_total']}")
        print(f"Digit accuracy on carry cases: {carry_case_acc:.2f}%")
    else:
        print("Carry-conditioned cases: none")

    if summary["noncarry_cases_total"] > 0:
        noncarry_case_acc = 100.0 * summary["noncarry_cases_digit_correct"] / summary["noncarry_cases_total"]
        print(f"Non-carry cases:             {summary['noncarry_cases_total']}")
        print(f"Digit accuracy on non-carry cases: {noncarry_case_acc:.2f}%")
    else:
        print("Non-carry cases: none")


def print_worst_subcases(summary, top_k=15):
    print("\n" + "=" * 80)
    print(f"WORST SUBCASES (TOP {top_k})")
    print("=" * 80)

    rows = []
    for key, stats in summary["by_subcase"].items():
        count = stats["count"]
        digit_acc = stats["digit_correct"] / count
        carry_acc = stats["carry_correct"] / count
        exact_acc = stats["exact_correct"] / count
        rows.append((key, count, digit_acc, carry_acc, exact_acc))

    # sort by lowest digit accuracy first, then count descending
    rows.sort(key=lambda x: (x[2], -x[1]))

    print(f"{'(a,b,c_in)':<15} | {'count':>5} | {'digit_acc':>10} | {'carry_acc':>10} | {'exact_acc':>10}")
    print("-" * 70)

    for key, count, d_acc, c_acc, e_acc in rows[:top_k]:
        print(f"{str(key):<15} | {count:>5} | {100*d_acc:>9.2f}% | {100*c_acc:>9.2f}% | {100*e_acc:>9.2f}%")


def print_interpretation_guidelines():
    print("\n" + "=" * 80)
    print("INTERPRETATION GUIDELINES")
    print("=" * 80)
    print("Use this step to describe behavior conservatively.")
    print()
    print("Appropriate conclusions:")
    print("  ✓ Errors are concentrated in specific subcases")
    print("  ✓ Carry-related inputs appear harder/easier than non-carry cases")
    print("  ✓ The baseline appears broadly competent with localized weak spots")
    print("  ✓ The baseline appears broadly weak with scattered successes")
    print()
    print("Inappropriate conclusions from this step alone:")
    print("  ✗ The internal mechanism is fully understood")
    print("  ✗ The model ignores carry entirely")
    print("  ✗ The architecture has a specific causal internal bug")
    print()
    print("This step is descriptive, not mechanistic.")


# -----------------------------------------------------------------------------
# DEMO / TEMPLATE MODE
# -----------------------------------------------------------------------------
def build_reference_case_space():
    """
    Build the full local reference space of all (a,b,carry_in) subcases.
    This does NOT include predictions; it only defines the evaluation space.
    """
    records = []
    for a in range(10):
        for b in range(10):
            for c_in in [0, 1]:
                total, digit_true, carry_true = single_digit_addition(a, b, c_in)
                records.append({
                    "a": a,
                    "b": b,
                    "carry_in": c_in,
                    "total_sum": total,
                    "digit_true": digit_true,
                    "carry_true": carry_true,
                })
    return records


def print_reference_space():
    print("\n" + "=" * 80)
    print("REFERENCE LOCAL STATE SPACE")
    print("=" * 80)

    records = build_reference_case_space()
    print(f"Total local subcases (a,b,carry_in): {len(records)}")
    print("Expected structure:")
    print("  - 10 values for a")
    print("  - 10 values for b")
    print("  - 2 values for carry_in")
    print("  => 10 x 10 x 2 = 200 total subcases")
    print()

    print("First 20 reference subcases:")
    print(f"{'a':>2} | {'b':>2} | {'c_in':>4} | {'sum':>3} | {'digit_true':>10} | {'carry_true':>10}")
    print("-" * 60)
    for rec in records[:20]:
        print(
            f"{rec['a']:>2} | {rec['b']:>2} | {rec['carry_in']:>4} | {rec['total_sum']:>3} | "
            f"{rec['digit_true']:>10} | {rec['carry_true']:>10}"
        )


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    print("\n" + "=" * 80)
    print("PHASE 26C STEP 2F: BEHAVIORAL ERROR STRUCTURE")
    print("=" * 80)
    print("This script defines the behavioral analysis framework for Phase 26c.")
    print("It is designed to be connected to actual reproduced predictions.")
    print()

    print_reference_space()
    print_interpretation_guidelines()

    print("\n" + "=" * 80)
    print("STEP 2F CURRENT STATUS")
    print("=" * 80)
    print("This script is a verified behavioral-analysis scaffold.")
    print()
    print("What it already establishes:")
    print("  ✓ the correct local arithmetic state space for Project 1 baseline")
    print("  ✓ the correct analysis dimensions for subcase-based error inspection")
    print("  ✓ the correct conservative interpretation boundaries")
    print()
    print("What still remains to be plugged in:")
    print("  - actual digit predictions from reproduced Phase 26c baseline")
    print("  - actual carry predictions if available")
    print()
    print("Once reproduced predictions are available, this script can be used to:")
    print("  - compute worst subcases")
    print("  - compare carry vs non-carry behavior")
    print("  - characterize whether errors are localized or distributed")
    print()
    print("Phase 2 can be considered structurally complete after this step,")
    print("but behavior-level conclusions require reproduced prediction records.")
    print("=" * 80)


if __name__ == "__main__":
    main()
