"""
================================================================================
PROJECT 4 REGIME CLASSIFICATION
================================================================================

PURPOSE:
  Rule-guided regime classification helper for Project 4.

ROLE:
  This module does NOT fully automate regime assignment.
  Instead, it provides:
    - structured regime signals
    - tentative regime suggestion
    - rationale lines
    - caution flags

IMPORTANT:
  Final regime assignment must remain human-reviewed and documented.

WORKING REGIMES:
  - Regime 1: Distribution-bound fit
  - Regime 2: Bounded compositional competence
  - Regime 3: Stronger algorithm-like generalization

================================================================================
"""

from typing import Dict, Any, List, Optional


# ============================================================================
# HELPERS
# ============================================================================

def _append(target: List[str], condition: bool, label: str):
    if condition:
        target.append(label)


def _get(scorecard: Dict[str, Any], key: str, default=None):
    return scorecard.get(key, default)


# ============================================================================
# CLASSIFICATION
# ============================================================================

def classify_regime(scorecard: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rule-guided regime helper.

    Input:
      scorecard dictionary (usually output of scorecard_to_dict)

    Output:
      {
        "tentative_regime": ...,
        "regime_1_signals": [...],
        "regime_2_signals": [...],
        "regime_3_signals": [...],
        "cautions": [...],
        "rationale": [...],
      }
    """

    regime_1_signals: List[str] = []
    regime_2_signals: List[str] = []
    regime_3_signals: List[str] = []
    cautions: List[str] = []
    rationale: List[str] = []

    ida = _get(scorecard, "in_distribution_accuracy")
    maa = _get(scorecard, "mean_adversarial_accuracy")
    wpa = _get(scorecard, "worst_case_pattern_accuracy")
    rs = _get(scorecard, "rounding_sensitivity")

    length_summary = _get(scorecard, "length_summary")
    carry_summary = _get(scorecard, "carry_corruption_summary")
    pattern_breakdown = _get(scorecard, "pattern_breakdown", {})

    # ------------------------------------------------------------------------
    # In-distribution
    # ------------------------------------------------------------------------
    if ida is not None:
        if ida >= 0.95:
            regime_2_signals.append("strong_in_distribution_accuracy")
            regime_3_signals.append("strong_in_distribution_accuracy")
            rationale.append(f"in-distribution accuracy is strong ({ida:.4f})")
        elif ida >= 0.80:
            regime_2_signals.append("moderate_in_distribution_accuracy")
            rationale.append(f"in-distribution accuracy is moderate ({ida:.4f})")
        else:
            regime_1_signals.append("weak_in_distribution_accuracy")
            rationale.append(f"in-distribution accuracy is weak ({ida:.4f})")
    else:
        cautions.append("missing_in_distribution_accuracy")

    # ------------------------------------------------------------------------
    # Adversarial mean
    # ------------------------------------------------------------------------
    if maa is not None:
        if maa < 0.70:
            regime_1_signals.append("low_mean_adversarial_accuracy")
            rationale.append(f"mean adversarial accuracy is low ({maa:.4f})")
        elif maa < 0.90:
            regime_2_signals.append("moderate_mean_adversarial_accuracy")
            rationale.append(f"mean adversarial accuracy is moderate ({maa:.4f})")
        else:
            regime_3_signals.append("high_mean_adversarial_accuracy")
            rationale.append(f"mean adversarial accuracy is high ({maa:.4f})")
    else:
        cautions.append("missing_mean_adversarial_accuracy")

    # ------------------------------------------------------------------------
    # Worst-case pattern
    # ------------------------------------------------------------------------
    if wpa is not None:
        if wpa < 0.60:
            regime_1_signals.append("poor_worst_case_pattern_accuracy")
            rationale.append(f"worst-case pattern accuracy is poor ({wpa:.4f})")
        elif wpa < 0.85:
            regime_2_signals.append("bounded_worst_case_pattern_accuracy")
            rationale.append(f"worst-case pattern accuracy is bounded ({wpa:.4f})")
        else:
            regime_3_signals.append("strong_worst_case_pattern_accuracy")
            rationale.append(f"worst-case pattern accuracy is strong ({wpa:.4f})")
    else:
        cautions.append("missing_worst_case_pattern_accuracy")

    # ------------------------------------------------------------------------
    # Pattern-specific vulnerability signals
    # ------------------------------------------------------------------------
    if pattern_breakdown:
        low_patterns = [k for k, v in pattern_breakdown.items() if v < 0.60]
        if low_patterns:
            regime_1_signals.append("pattern_specific_collapse_present")
            rationale.append(f"low-performing adversarial patterns detected: {low_patterns}")

    # ------------------------------------------------------------------------
    # Rounding sensitivity
    # ------------------------------------------------------------------------
    if rs is not None:
        if rs > 0.10:
            regime_1_signals.append("high_rounding_sensitivity")
            cautions.append("substantial_rounding_dependence")
            rationale.append(f"rounding sensitivity is high ({rs:.4f})")
        elif rs > 0.02:
            regime_2_signals.append("moderate_rounding_sensitivity")
            rationale.append(f"rounding sensitivity is moderate ({rs:.4f})")
        else:
            regime_3_signals.append("low_rounding_sensitivity")
            rationale.append(f"rounding sensitivity is low ({rs:.4f})")
    else:
        cautions.append("missing_rounding_sensitivity")

    # ------------------------------------------------------------------------
    # Length trend
    # ------------------------------------------------------------------------
    if length_summary is not None:
        trend = length_summary.get("trend_label")
        if trend == "sharp_collapse":
            regime_1_signals.append("sharp_length_collapse")
            rationale.append("length extrapolation shows sharp collapse")
        elif trend == "gradual_decline":
            regime_2_signals.append("bounded_length_robustness")
            rationale.append("length extrapolation shows bounded decline")
        elif trend == "stable":
            regime_3_signals.append("stable_length_behavior")
            rationale.append("length extrapolation is stable")
        else:
            cautions.append("mixed_length_trend")
    else:
        cautions.append("missing_length_summary")

    # ------------------------------------------------------------------------
    # Carry corruption
    # ------------------------------------------------------------------------
    if carry_summary is not None:
        ctrend = carry_summary.get("trend_label")
        cautions.append("carry_corruption_requires_joint_interpretation")

        if ctrend == "flat":
            regime_1_signals.append("flat_carry_corruption_response")
            rationale.append("carry corruption shows flat response")
        elif ctrend == "graceful":
            regime_3_signals.append("graceful_carry_corruption_response")
            rationale.append("carry corruption degrades gracefully")
        elif ctrend == "moderate":
            regime_2_signals.append("moderate_carry_corruption_response")
            rationale.append("carry corruption shows moderate degradation")
        elif ctrend == "steep":
            regime_1_signals.append("steep_carry_corruption_response")
            rationale.append("carry corruption shows steep degradation")
        else:
            cautions.append("mixed_carry_corruption_trend")
    else:
        cautions.append("missing_carry_corruption_summary")

    # ------------------------------------------------------------------------
    # Tentative regime
    # ------------------------------------------------------------------------
    r1 = len(regime_1_signals)
    r2 = len(regime_2_signals)
    r3 = len(regime_3_signals)

    if r3 >= 3 and r1 == 0:
        tentative_regime = "Regime 3"
    elif r1 >= 3 and r3 == 0:
        tentative_regime = "Regime 1"
    elif r2 >= 2:
        tentative_regime = "Regime 2"
    else:
        tentative_regime = "Mixed / Borderline"

    cautions.append("final_regime_assignment_must_not_be_single_metric_based")

    return {
        "tentative_regime": tentative_regime,
        "regime_1_signals": regime_1_signals,
        "regime_2_signals": regime_2_signals,
        "regime_3_signals": regime_3_signals,
        "cautions": cautions,
        "rationale": rationale,
    }


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    demo_scorecard = {
        "model_name": "demo_model",
        "in_distribution_accuracy": 0.98,
        "mean_adversarial_accuracy": 0.69,
        "worst_case_pattern_accuracy": 0.52,
        "rounding_sensitivity": 0.37,
        "pattern_breakdown": {
            "alternating_carry": 0.52,
            "full_propagation_chain": 0.95,
            "block_boundary_stress": 0.61,
        },
        "length_summary": {
            "trend_label": "sharp_collapse"
        },
        "carry_corruption_summary": {
            "trend_label": "steep"
        },
    }

    result = classify_regime(demo_scorecard)

    print("=" * 80)
    print("PROJECT 4 REGIME CLASSIFICATION DEMO")
    print("=" * 80)
    for k, v in result.items():
        print(f"{k}: {v}")
