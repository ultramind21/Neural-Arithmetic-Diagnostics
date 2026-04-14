"""
================================================================================
PROJECT 10 PHASE DIAGRAM REFINEMENT V1
================================================================================

PURPOSE:
  Densify the current transition bands in the Project 10 rescue phase diagram.

TARGET:
  Sharpen two local boundaries:
    1. heterogeneity transition at baseline universal power
    2. universal-power transition at medium/high heterogeneity

IMPORTANT:
  This is a local densification pass, not a full grid expansion.
  Its purpose is to test whether current boundaries look sharp or extended.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


# ============================================================================
# PATHS
# ============================================================================
ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "project_10" / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_10_phase_diagram_refinement_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_10_phase_diagram_refinement_v1_report.md"


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def save_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


# ============================================================================
# BASE CASES
# ============================================================================

BASE_CASES = [
    {"family": "A", "base_global": 0.48, "shared_failure": 0.41},
    {"family": "B", "base_global": 0.47, "shared_failure": 0.40},
    {"family": "C", "base_global": 0.46, "shared_failure": 0.41},
    {"family": "D", "base_global": 0.47, "shared_failure": 0.40},
]

RESIDUAL_SIGNS = [1, -1, 1, -1]


# ============================================================================
# CORE SCORING
# ============================================================================

def universal_rescue_score(base_global: float, shared_failure: float, universal_power: float) -> float:
    return clamp(base_global + universal_power * shared_failure)


def family_aware_rescue_score(base_global: float, shared_failure: float, residual_abs: float) -> float:
    return clamp(base_global + 0.30 * shared_failure + 0.80 * residual_abs)


def evaluate_cell(residual_abs: float, universal_power: float) -> Dict:
    universal_wins = 0
    family_aware_wins = 0
    near_ties = 0

    rows = []

    for i, case in enumerate(BASE_CASES):
        residual = RESIDUAL_SIGNS[i] * residual_abs

        uni = universal_rescue_score(case["base_global"], case["shared_failure"], universal_power)
        fam = family_aware_rescue_score(case["base_global"], case["shared_failure"], abs(residual))

        if uni > fam + 0.005:
            winner = "universal"
            universal_wins += 1
        elif fam > uni + 0.005:
            winner = "family_aware"
            family_aware_wins += 1
        else:
            winner = "near_tie"
            near_ties += 1

        rows.append({
            "family": case["family"],
            "universal_score": uni,
            "family_aware_score": fam,
            "winner": winner,
        })

    avg_uni = sum(r["universal_score"] for r in rows) / len(rows)
    avg_fam = sum(r["family_aware_score"] for r in rows) / len(rows)
    gap = avg_fam - avg_uni

    if family_aware_wins >= 3 and gap > 0.005:
        verdict = "family-aware region"
    elif universal_wins >= 2 or gap < -0.003:
        verdict = "universal region"
    else:
        verdict = "transition region"

    return {
        "residual_abs": residual_abs,
        "universal_power": universal_power,
        "avg_universal_score": avg_uni,
        "avg_family_aware_score": avg_fam,
        "gap_family_minus_universal": gap,
        "universal_wins": universal_wins,
        "family_aware_wins": family_aware_wins,
        "near_ties": near_ties,
        "verdict": verdict,
    }


# ============================================================================
# LOCAL DENSIFICATION
# ============================================================================

def build_heterogeneity_band_probe() -> List[Dict]:
    """
    Dense probe around the heterogeneity transition at baseline power.
    """
    baseline_power = 0.30
    residual_values = [0.0060, 0.0065, 0.0070, 0.0075]
    return [evaluate_cell(r, baseline_power) for r in residual_values]


def build_power_band_probe() -> List[Dict]:
    """
    Dense probe around the power transition for medium/high heterogeneity.
    """
    power_values = [0.320, 0.325, 0.330, 0.335, 0.340]
    residual_levels = {
        "medium": 0.009,
        "high": 0.015,
    }

    out = []
    for label, residual_abs in residual_levels.items():
        for power in power_values:
            cell = evaluate_cell(residual_abs, power)
            cell["heterogeneity_label"] = label
            out.append(cell)
    return out


def summarize_probe(cells: List[Dict]) -> Dict:
    counts = {
        "family-aware region": 0,
        "transition region": 0,
        "universal region": 0,
    }
    for cell in cells:
        counts[cell["verdict"]] += 1
    return counts


# ============================================================================
# REPORT
# ============================================================================

def render_report(heterogeneity_probe: List[Dict], power_probe: List[Dict], summary: Dict) -> str:
    lines = [
        "# PROJECT 10 PHASE DIAGRAM REFINEMENT V1",
        "",
        "## Purpose",
        "Densified local probe of current transition bands in the Project 10 phase diagram.",
        "",
        "## Summary Counts",
        f"- heterogeneity_band_probe: {summary['heterogeneity_band_probe']}",
        f"- power_band_probe: {summary['power_band_probe']}",
        "",
        "## Heterogeneity Band Probe (power = 0.30)",
    ]

    for cell in heterogeneity_probe:
        lines.append(
            f"- residual={cell['residual_abs']:.4f} | "
            f"gap={cell['gap_family_minus_universal']:.4f} | "
            f"verdict={cell['verdict']}"
        )

    lines.append("")
    lines.append("## Power Band Probe")

    for cell in power_probe:
        lines.append(
            f"- heterogeneity={cell['heterogeneity_label']} | "
            f"power={cell['universal_power']:.3f} | "
            f"gap={cell['gap_family_minus_universal']:.4f} | "
            f"verdict={cell['verdict']}"
        )

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This is a local densification pass only.",
        "- It is designed to sharpen current phase boundaries, not to close the theory.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 10 PHASE DIAGRAM REFINEMENT V1")

    heterogeneity_probe = build_heterogeneity_band_probe()
    power_probe = build_power_band_probe()

    summary = {
        "heterogeneity_band_probe": summarize_probe(heterogeneity_probe),
        "power_band_probe": summarize_probe(power_probe),
    }

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_10_phase_diagram_refinement_v1",
        "heterogeneity_band_probe": heterogeneity_probe,
        "power_band_probe": power_probe,
        "summary": summary,
        "notes": [
            "This is the first local phase-diagram densification pass in Project 10.",
            "It sharpens the heterogeneity and universal-power transition bands identified earlier.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(heterogeneity_probe, power_probe, summary))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print(f"✓ Summary: {summary}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
