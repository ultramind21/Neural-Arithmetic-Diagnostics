"""
================================================================================
PROJECT 10 PHASE 2 THRESHOLD REFINEMENT V1
================================================================================

PURPOSE:
  Probe the first local transition zones in the Phase 2 rescue regime space.

TARGET:
  Refine two suspected threshold regions:
    1. heterogeneity transition near baseline universal power
    2. universal-power transition near medium/high heterogeneity

IMPORTANT:
  This is a local threshold probe, not a full map expansion.
  Its purpose is to identify where verdict flips begin to occur.

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

JSON_OUTPUT = OUTPUT_DIR / "project_10_phase2_threshold_refinement_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_10_phase2_threshold_refinement_v1_report.md"


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
    rows = []
    universal_wins = 0
    family_aware_wins = 0
    near_ties = 0

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
            "residual_family_factor": residual,
            "universal_score": uni,
            "family_aware_score": fam,
            "winner": winner,
        })

    avg_uni = sum(r["universal_score"] for r in rows) / len(rows)
    avg_fam = sum(r["family_aware_score"] for r in rows) / len(rows)
    gap = avg_fam - avg_uni

    if family_aware_wins >= 3 and gap > 0.005:
        verdict = "supports revised candidate"
    elif universal_wins >= 2 or gap < -0.003:
        verdict = "weakens revised candidate"
    else:
        verdict = "boundary / mixed"

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
# REFINEMENT ZONES
# ============================================================================

def build_heterogeneity_probe() -> List[Dict]:
    """
    Probe between low and medium heterogeneity at baseline power.
    """
    residual_values = [0.003, 0.0045, 0.006, 0.0075, 0.009]
    universal_power = 0.30
    return [evaluate_cell(r, universal_power) for r in residual_values]


def build_power_probe() -> List[Dict]:
    """
    Probe between baseline and moderate universal power at medium/high heterogeneity.
    """
    power_values = [0.30, 0.32, 0.34, 0.36]
    residual_values = {
        "medium": 0.009,
        "high": 0.015,
    }

    out = []
    for label, residual_abs in residual_values.items():
        for power in power_values:
            cell = evaluate_cell(residual_abs, power)
            cell["heterogeneity_label"] = label
            out.append(cell)
    return out


def summarize_probe(cells: List[Dict]) -> Dict:
    counts = {
        "supports revised candidate": 0,
        "boundary / mixed": 0,
        "weakens revised candidate": 0,
    }
    for cell in cells:
        counts[cell["verdict"]] += 1
    return {"counts": counts}


# ============================================================================
# REPORT
# ============================================================================

def render_report(heterogeneity_probe: List[Dict], power_probe: List[Dict], summary: Dict) -> str:
    lines = [
        "# PROJECT 10 PHASE 2 THRESHOLD REFINEMENT V1",
        "",
        "## Purpose",
        "Local probe of the first transition zones in the rescue regime space.",
        "",
        "## Summary Counts",
        f"- heterogeneity_probe: {summary['heterogeneity_probe']}",
        f"- power_probe: {summary['power_probe']}",
        "",
        "## Heterogeneity Probe (baseline power = 0.30)",
    ]

    for cell in heterogeneity_probe:
        lines.append(
            f"- residual={cell['residual_abs']:.4f} | "
            f"gap={cell['gap_family_minus_universal']:.4f} | "
            f"verdict={cell['verdict']}"
        )

    lines.append("")
    lines.append("## Power Probe")

    for cell in power_probe:
        lines.append(
            f"- heterogeneity={cell['heterogeneity_label']} | "
            f"power={cell['universal_power']:.2f} | "
            f"gap={cell['gap_family_minus_universal']:.4f} | "
            f"verdict={cell['verdict']}"
        )

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This is a local threshold probe only.",
        "- It is intended to locate likely transition regions, not to close the theory.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 10 PHASE 2 THRESHOLD REFINEMENT V1")

    heterogeneity_probe = build_heterogeneity_probe()
    power_probe = build_power_probe()

    summary = {
        "heterogeneity_probe": summarize_probe(heterogeneity_probe)["counts"],
        "power_probe": summarize_probe(power_probe)["counts"],
    }

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_10_phase2_threshold_refinement_v1",
        "heterogeneity_probe": heterogeneity_probe,
        "power_probe": power_probe,
        "summary": summary,
        "notes": [
            "This is the first threshold refinement probe in Project 10 Phase 2.",
            "It focuses on the low→medium heterogeneity transition and the baseline→moderate universal-power transition.",
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
