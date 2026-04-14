"""
================================================================================
PROJECT 4 DIAGNOSTIC SCORECARD
================================================================================

PURPOSE:
  Core scorecard logic for Project 4.

ROLE:
  This module computes the Project 4 diagnostic scorecard dimensions from
  already-measured experiment outputs.

IMPORTANT:
  This module does NOT fully automate final regime classification.
  It produces:
    - normalized reporting structures
    - derived indicators
    - scorecard summaries
  Final regime assignment must remain rule-guided and documented.

CORE DIMENSIONS:
  1. in_distribution_accuracy
  2. structured_adversarial_accuracy
  3. worst_case_pattern_accuracy
  4. length_extrapolation
  5. rounding_sensitivity
  6. carry_corruption_sensitivity

STATUS:
  Framework v1.0 skeleton

================================================================================
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
import statistics


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class LengthTrendSummary:
    training_max_length: int
    tested_lengths: List[int]
    accuracies: List[float]
    reference_accuracy: Optional[float]
    relative_drops: List[float]
    trend_label: str  # stable / gradual_decline / sharp_collapse / mixed


@dataclass
class CarryCorruptionSummary:
    corruption_levels: List[float]
    accuracies: List[float]
    baseline_accuracy: Optional[float]
    degradation: List[float]
    trend_label: str  # graceful / moderate / steep / flat / mixed


@dataclass
class DiagnosticScorecard:
    model_name: str

    # Core scalar dimensions
    in_distribution_accuracy: Optional[float]
    mean_adversarial_accuracy: Optional[float]
    worst_case_pattern_accuracy: Optional[float]
    rounding_sensitivity: Optional[float]

    # Structured details
    pattern_breakdown: Dict[str, float]
    length_summary: Optional[LengthTrendSummary]
    carry_corruption_summary: Optional[CarryCorruptionSummary]

    # Optional metadata
    notes: List[str]
    tags: List[str]


# ============================================================================
# HELPERS
# ============================================================================

def mean_or_none(values: List[float]) -> Optional[float]:
    return statistics.mean(values) if values else None


def safe_min(values: List[float]) -> Optional[float]:
    return min(values) if values else None


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def relative_drop(reference: float, current: float) -> float:
    """
    Relative drop from reference:
      (reference - current) / reference
    """
    if reference <= 0:
        return 0.0
    return (reference - current) / reference


# ============================================================================
# LENGTH EXTRAPOLATION
# ============================================================================

def summarize_length_extrapolation(
    training_max_length: int,
    accuracy_by_length: Dict[int, float],
    reference_accuracy: Optional[float] = None,
) -> LengthTrendSummary:
    """
    Build a minimal operational summary of length robustness.

    If reference_accuracy is not provided, use the best accuracy at or below
    training_max_length if available, otherwise the first tested value.
    """
    tested_lengths = sorted(accuracy_by_length.keys())
    accuracies = [accuracy_by_length[L] for L in tested_lengths]

    if reference_accuracy is None:
        in_range = [accuracy_by_length[L] for L in tested_lengths if L <= training_max_length]
        if in_range:
            reference_accuracy = max(in_range)
        elif accuracies:
            reference_accuracy = accuracies[0]
        else:
            reference_accuracy = None

    relative_drops = []
    if reference_accuracy is not None:
        relative_drops = [relative_drop(reference_accuracy, acc) for acc in accuracies]

    # Simple v1.0 trend heuristic
    if not relative_drops:
        trend_label = "mixed"
    else:
        max_drop = max(relative_drops)
        final_drop = relative_drops[-1]

        if max_drop < 0.05 and final_drop < 0.05:
            trend_label = "stable"
        elif max_drop < 0.20 and final_drop < 0.20:
            trend_label = "gradual_decline"
        elif final_drop >= 0.20:
            trend_label = "sharp_collapse"
        else:
            trend_label = "mixed"

    return LengthTrendSummary(
        training_max_length=training_max_length,
        tested_lengths=tested_lengths,
        accuracies=accuracies,
        reference_accuracy=reference_accuracy,
        relative_drops=relative_drops,
        trend_label=trend_label,
    )


# ============================================================================
# CARRY CORRUPTION
# ============================================================================

def summarize_carry_corruption(
    accuracy_by_corruption: Dict[float, float],
    baseline_accuracy: Optional[float] = None,
) -> CarryCorruptionSummary:
    """
    Build a minimal operational summary of corruption sensitivity.

    corruption levels are expected in [0,1].
    """
    levels = sorted(accuracy_by_corruption.keys())
    accuracies = [accuracy_by_corruption[p] for p in levels]

    if baseline_accuracy is None:
        baseline_accuracy = accuracy_by_corruption.get(0.0, accuracies[0] if accuracies else None)

    degradation = []
    if baseline_accuracy is not None:
        degradation = [baseline_accuracy - acc for acc in accuracies]

    if not degradation:
        trend_label = "mixed"
    else:
        final_deg = degradation[-1]
        max_deg = max(degradation)

        if max_deg < 0.05:
            trend_label = "flat"
        elif final_deg < 0.10:
            trend_label = "graceful"
        elif final_deg < 0.25:
            trend_label = "moderate"
        elif final_deg >= 0.25:
            trend_label = "steep"
        else:
            trend_label = "mixed"

    return CarryCorruptionSummary(
        corruption_levels=levels,
        accuracies=accuracies,
        baseline_accuracy=baseline_accuracy,
        degradation=degradation,
        trend_label=trend_label,
    )


# ============================================================================
# SCORECARD BUILDING
# ============================================================================

def build_scorecard(
    model_name: str,
    in_distribution_accuracy: Optional[float],
    pattern_breakdown: Dict[str, float],
    training_max_length: Optional[int] = None,
    accuracy_by_length: Optional[Dict[int, float]] = None,
    accuracy_with_rounding: Optional[float] = None,
    accuracy_without_rounding: Optional[float] = None,
    accuracy_by_corruption: Optional[Dict[float, float]] = None,
    notes: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
) -> DiagnosticScorecard:
    """
    Main Project 4 scorecard builder.
    """

    notes = notes or []
    tags = tags or []

    mean_adversarial_accuracy = mean_or_none(list(pattern_breakdown.values()))
    worst_case_pattern_accuracy = safe_min(list(pattern_breakdown.values()))

    rounding_sensitivity = None
    if accuracy_with_rounding is not None and accuracy_without_rounding is not None:
        rounding_sensitivity = abs(accuracy_with_rounding - accuracy_without_rounding)

    length_summary = None
    if training_max_length is not None and accuracy_by_length:
        length_summary = summarize_length_extrapolation(
            training_max_length=training_max_length,
            accuracy_by_length=accuracy_by_length,
            reference_accuracy=in_distribution_accuracy,
        )

    carry_corruption_summary = None
    if accuracy_by_corruption:
        carry_corruption_summary = summarize_carry_corruption(
            accuracy_by_corruption=accuracy_by_corruption,
            baseline_accuracy=in_distribution_accuracy,
        )

    return DiagnosticScorecard(
        model_name=model_name,
        in_distribution_accuracy=in_distribution_accuracy,
        mean_adversarial_accuracy=mean_adversarial_accuracy,
        worst_case_pattern_accuracy=worst_case_pattern_accuracy,
        rounding_sensitivity=rounding_sensitivity,
        pattern_breakdown=pattern_breakdown,
        length_summary=length_summary,
        carry_corruption_summary=carry_corruption_summary,
        notes=notes,
        tags=tags,
    )


# ============================================================================
# REGIME GUIDANCE (NOT FINAL AUTOMATION)
# ============================================================================

def generate_regime_guidance(scorecard: DiagnosticScorecard) -> Dict[str, Any]:
    """
    Produce non-binding regime guidance indicators.

    IMPORTANT:
      This is NOT the final regime classification.
      It is a helper summary only.
    """
    indicators = {
        "possible_regime_1_signals": [],
        "possible_regime_2_signals": [],
        "possible_regime_3_signals": [],
        "cautions": [],
    }

    ida = scorecard.in_distribution_accuracy
    maa = scorecard.mean_adversarial_accuracy
    wpa = scorecard.worst_case_pattern_accuracy
    rs = scorecard.rounding_sensitivity

    if ida is not None and ida >= 0.95:
        indicators["possible_regime_2_signals"].append("strong_in_distribution_accuracy")
        indicators["possible_regime_3_signals"].append("strong_in_distribution_accuracy")

    if maa is not None:
        if maa < 0.70:
            indicators["possible_regime_1_signals"].append("low_mean_adversarial_accuracy")
        elif maa < 0.90:
            indicators["possible_regime_2_signals"].append("moderate_mean_adversarial_accuracy")
        else:
            indicators["possible_regime_3_signals"].append("high_mean_adversarial_accuracy")

    if wpa is not None:
        if wpa < 0.60:
            indicators["possible_regime_1_signals"].append("poor_worst_case_pattern_accuracy")
        elif wpa < 0.85:
            indicators["possible_regime_2_signals"].append("bounded_worst_case_pattern_accuracy")
        else:
            indicators["possible_regime_3_signals"].append("strong_worst_case_pattern_accuracy")

    if rs is not None:
        if rs > 0.10:
            indicators["possible_regime_1_signals"].append("high_rounding_sensitivity")
            indicators["cautions"].append("rounding_dependence_may_be_significant")
        elif rs > 0.02:
            indicators["possible_regime_2_signals"].append("moderate_rounding_sensitivity")
        else:
            indicators["possible_regime_3_signals"].append("low_rounding_sensitivity")

    if scorecard.length_summary is not None:
        if scorecard.length_summary.trend_label == "sharp_collapse":
            indicators["possible_regime_1_signals"].append("length_collapse")
        elif scorecard.length_summary.trend_label == "gradual_decline":
            indicators["possible_regime_2_signals"].append("bounded_length_robustness")
        elif scorecard.length_summary.trend_label == "stable":
            indicators["possible_regime_3_signals"].append("stable_length_behavior")

    if scorecard.carry_corruption_summary is not None:
        indicators["cautions"].append(
            "carry_corruption_must_be_interpreted_jointly_with_baseline_and_curve_shape"
        )

    indicators["cautions"].append(
        "final_regime_assignment_must_use_multiple_dimensions_not_single_metrics"
    )

    return indicators


# ============================================================================
# SERIALIZATION
# ============================================================================

def scorecard_to_dict(scorecard: DiagnosticScorecard) -> Dict[str, Any]:
    """
    Convert nested dataclass scorecard to dictionary.
    """
    output = asdict(scorecard)
    return output


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    demo = build_scorecard(
        model_name="demo_model",
        in_distribution_accuracy=0.98,
        pattern_breakdown={
            "alternating_carry": 0.52,
            "full_propagation_chain": 0.95,
            "block_boundary_stress": 0.61,
        },
        training_max_length=5,
        accuracy_by_length={
            5: 0.98,
            10: 0.95,
            20: 0.88,
            50: 0.62,
        },
        accuracy_with_rounding=0.98,
        accuracy_without_rounding=0.61,
        accuracy_by_corruption={
            0.0: 0.98,
            0.1: 0.85,
            0.2: 0.72,
            0.5: 0.41,
        },
        notes=["demo only"],
        tags=["v1.0", "scorecard-demo"],
    )

    print("=" * 80)
    print("PROJECT 4 DIAGNOSTIC SCORECARD DEMO")
    print("=" * 80)
    print(scorecard_to_dict(demo))
    print("\nREGIME GUIDANCE:")
    print(generate_regime_guidance(demo))
