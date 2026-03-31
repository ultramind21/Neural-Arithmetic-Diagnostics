"""
================================================================================
PHASE 27C STEP 3B DIAGNOSTIC: SHUFFLE ORDER FAIRNESS
================================================================================

OFFICIAL TARGET:
  File: src/train/phase_27c_architecture_audit.py

PURPOSE:
  Verify whether the actual shuffle logic in Phase 27c gives all 3 architectures
  (MLP, LSTM, Transformer) IDENTICAL test_pairs in the same trial.

CRITICAL QUESTION:
  In the official source, all_pairs is created ONCE, then shuffled in-place
  across MLP -> LSTM -> Transformer.

  Does random.seed(trial) guarantee identical test_pairs across architectures
  despite the list entering each architecture in a different order?
  Or does in-place shuffle create a comparability bias?

THIS SCRIPT:
  1. Reproduces the ACTUAL loop structure from the official source
  2. Tracks test_pairs for all architectures across all 30 trials
  3. Compares same-trial test_pairs across architectures
  4. Optionally runs a CONTROL simulation with reset-per-architecture
  5. Outputs one verdict:
       - FAIR
       - BIASED
       - AMBIGUOUS

SCOPE:
  This diagnostic verifies shuffle-order fairness only.
  It does NOT train models, verify metrics, or reproduce official results.

================================================================================
"""

import random
import sys


# ============================================================================
# CONFIG
# ============================================================================

ARCHITECTURES = ["MLP", "LSTM", "Transformer"]
TRIALS = list(range(30))
SAMPLE_TRIALS = [0, 1, 14, 29]


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_subheader(title):
    print("\n" + "-" * 80)
    print(title)
    print("-" * 80)


def make_all_pairs():
    return [(a, b) for a in range(10) for b in range(10)]


def simulate_actual_source_behavior():
    """
    Simulate the official source behavior EXACTLY at the split logic level:

        all_pairs = [...]
        for arch in architectures:
            for trial in range(30):
                random.seed(trial)
                random.shuffle(all_pairs)
                test_pairs = all_pairs[70:]

    Important:
      all_pairs is created ONCE and reused across architectures.
      This is the main diagnostic path and the official basis for verdict.
    """
    all_pairs = make_all_pairs()
    results = {}

    for arch_name in ARCHITECTURES:
        arch_results = {}

        for trial in TRIALS:
            random.seed(trial)
            random.shuffle(all_pairs)

            train_pairs = all_pairs[:70]
            test_pairs = all_pairs[70:]

            arch_results[trial] = {
                "train_pairs": list(train_pairs),
                "test_pairs": list(test_pairs),
            }

        results[arch_name] = arch_results

    return results


def simulate_reset_control_behavior():
    """
    Control simulation ONLY for interpretation:

    Reset all_pairs at the start of each architecture, then run the same trial loop.

    This is NOT the official verdict path.
    It helps show what happens if every architecture starts from the same initial order.
    """
    results = {}

    for arch_name in ARCHITECTURES:
        all_pairs = make_all_pairs()
        arch_results = {}

        for trial in TRIALS:
            random.seed(trial)
            random.shuffle(all_pairs)

            train_pairs = all_pairs[:70]
            test_pairs = all_pairs[70:]

            arch_results[trial] = {
                "train_pairs": list(train_pairs),
                "test_pairs": list(test_pairs),
            }

        results[arch_name] = arch_results

    return results


def compare_architectures(results, field="test_pairs"):
    """
    Compare same-trial lists across architectures.

    Returns:
      summary dict with:
        - all_trials_identical
        - mismatched_trials
        - detailed_matches
    """
    mismatched_trials = []
    detailed_matches = {}

    for trial in TRIALS:
        mlp_list = results["MLP"][trial][field]
        lstm_list = results["LSTM"][trial][field]
        transformer_list = results["Transformer"][trial][field]

        mlp_lstm = (mlp_list == lstm_list)
        lstm_transformer = (lstm_list == transformer_list)
        mlp_transformer = (mlp_list == transformer_list)
        all_match = mlp_lstm and lstm_transformer and mlp_transformer

        detailed_matches[trial] = {
            "MLP_vs_LSTM": mlp_lstm,
            "LSTM_vs_Transformer": lstm_transformer,
            "MLP_vs_Transformer": mlp_transformer,
            "all_match": all_match,
        }

        if not all_match:
            mismatched_trials.append(trial)

    return {
        "all_trials_identical": len(mismatched_trials) == 0,
        "mismatched_trials": mismatched_trials,
        "detailed_matches": detailed_matches,
    }


def print_sample_trials(results, label):
    print_subheader(f"SAMPLE TRIAL INSPECTION: {label}")

    for trial in SAMPLE_TRIALS:
        print(f"\nTrial {trial}:")
        for arch_name in ARCHITECTURES:
            test_pairs = results[arch_name][trial]["test_pairs"]
            print(f"  {arch_name:<12} first3={test_pairs[:3]}  last3={test_pairs[-3:]}")


def print_trial_comparisons(comparison, label):
    print_subheader(f"TRIAL COMPARISONS: {label}")

    for trial in SAMPLE_TRIALS:
        info = comparison["detailed_matches"][trial]
        print(f"\nTrial {trial}:")
        print(f"  MLP == LSTM?           {info['MLP_vs_LSTM']}")
        print(f"  LSTM == Transformer?   {info['LSTM_vs_Transformer']}")
        print(f"  MLP == Transformer?    {info['MLP_vs_Transformer']}")
        print(f"  All 3 identical?       {info['all_match']}")

    print("\nAll 30 trials identical?",
          comparison["all_trials_identical"])
    if not comparison["all_trials_identical"]:
        print("Mismatched trials:", comparison["mismatched_trials"])


def decide_verdict(actual_comparison):
    """
    Official verdict is based on ACTUAL source behavior only.
    """
    if actual_comparison["all_trials_identical"]:
        return "FAIR"
    return "BIASED"


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PHASE 27C STEP 3B DIAGNOSTIC: SHUFFLE ORDER FAIRNESS")

    print("Diagnostic scope:")
    print("  - Reproduce actual split logic from phase_27c_architecture_audit.py")
    print("  - Compare same-trial test_pairs across MLP / LSTM / Transformer")
    print("  - Determine whether shuffle order is FAIR or BIASED")
    print("  - Do NOT train models or verify metrics")

    # ------------------------------------------------------------------------
    # 1) ACTUAL SOURCE BEHAVIOR
    # ------------------------------------------------------------------------
    print_header("1) ACTUAL SOURCE SIMULATION (OFFICIAL VERDICT PATH)")

    actual_results = simulate_actual_source_behavior()
    actual_comparison = compare_architectures(actual_results, field="test_pairs")

    print_sample_trials(actual_results, "ACTUAL SOURCE BEHAVIOR")
    print_trial_comparisons(actual_comparison, "ACTUAL SOURCE BEHAVIOR")

    # ------------------------------------------------------------------------
    # 2) RESET CONTROL BEHAVIOR
    # ------------------------------------------------------------------------
    print_header("2) RESET CONTROL SIMULATION (INTERPRETIVE ONLY)")

    control_results = simulate_reset_control_behavior()
    control_comparison = compare_architectures(control_results, field="test_pairs")

    print_sample_trials(control_results, "RESET-PER-ARCHITECTURE CONTROL")
    print_trial_comparisons(control_comparison, "RESET-PER-ARCHITECTURE CONTROL")

    # ------------------------------------------------------------------------
    # 3) FINAL VERDICT
    # ------------------------------------------------------------------------
    verdict = decide_verdict(actual_comparison)

    print_header("3) FINAL VERDICT")

    if verdict == "FAIR":
        print("✓ FAIR")
        print()
        print("Finding:")
        print("  Under the ACTUAL source behavior, all 3 architectures receive")
        print("  identical test_pairs in every trial.")
        print()
        print("Conclusion:")
        print("  Shuffle order does not create cross-architecture test-pair bias")
        print("  at the level checked by this diagnostic.")
    else:
        print("✗ BIASED")
        print()
        print("Finding:")
        print("  Under the ACTUAL source behavior, at least one trial gives")
        print("  different test_pairs across architectures.")
        print()
        print("Affected trials:")
        print(f"  {actual_comparison['mismatched_trials']}")
        print()
        print("Conclusion:")
        print("  In-place shuffle creates a cross-architecture comparability issue.")
        print("  The architectures are not being evaluated on identical test_pairs")
        print("  in the same trial.")

    # ------------------------------------------------------------------------
    # 4) QUALIFICATIONS
    # ------------------------------------------------------------------------
    print_header("4) QUALIFICATIONS & SCOPE")

    print("This diagnostic VERIFIED:")
    print("  ✓ Whether same-trial test_pairs are identical across architectures")
    print("  ✓ Whether actual in-place shuffle behavior preserves fairness")
    print("  ✓ Whether reset-per-architecture changes the outcome (control only)")
    print()
    print("This diagnostic DID NOT verify:")
    print("  ✗ Ground-truth correctness")
    print("  ✗ Metric correctness")
    print("  ✗ Model training behavior")
    print("  ✗ Whether official reported results are numerically correct")
    print()
    print("Methodological note:")
    print("  Official verdict is based ONLY on the actual-source simulation.")
    print("  The reset control is included for interpretation, not for the verdict.")

    # ------------------------------------------------------------------------
    # 5) RECOMMENDATION
    # ------------------------------------------------------------------------
    print_header("5) RECOMMENDATION")

    print("Next action:")
    print("  Document this finding and present it to the user.")
    print("  Do NOT auto-progress to Phase 3C without explicit user approval.")

    print(f"\nDIAGNOSTIC COMPLETE: {verdict}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
