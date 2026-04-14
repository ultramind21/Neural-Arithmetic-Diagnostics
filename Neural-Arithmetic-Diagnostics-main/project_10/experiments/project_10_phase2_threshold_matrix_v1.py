"""
================================================================================
PROJECT 10 PHASE 2 THRESHOLD MATRIX V1
================================================================================

PURPOSE:
  Build the first 3x3 threshold matrix for the revised higher-order candidate.

TARGET:
  Map outcomes across:
    - heterogeneity level: low / medium / high
    - universal rescue power: baseline / moderate / strong

IMPORTANT:
  This is the first landscape-level test in Phase 2.
  It is designed to locate where the revised candidate holds, weakens, or
  reaches boundary conditions.

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

JSON_OUTPUT = OUTPUT_DIR / "project_10_phase2_threshold_matrix_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_10_phase2_threshold_matrix_v1_report.md"


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
# MATRIX DEFINITIONS
# ============================================================================

HETEROGENEITY_LEVELS = {
    "low": 0.003,
    "medium": 0.009,
    "high": 0.015,
}

UNIVERSAL_POWER_LEVELS = {
    "baseline": 0.30,
    "moderate": 0.36,
    "strong": 0.42,
}

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
    # family-aware rescue uses baseline shared gain plus residual-aware refinement
    return clamp(base_global + 0.30 * shared_failure + 0.80 * residual_abs)


def evaluate_cell(heterogeneity_label: str, power_label: str) -> Dict:
    residual_abs = HETEROGENEITY_LEVELS[heterogeneity_label]
    universal_power = UNIVERSAL_POWER_LEVELS[power_label]

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
            "base_global": case["base_global"],
            "shared_failure": case["shared_failure"],
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
        "heterogeneity": heterogeneity_label,
        "universal_power": power_label,
        "residual_abs": residual_abs,
        "universal_power_value": universal_power,
        "avg_universal_score": avg_uni,
        "avg_family_aware_score": avg_fam,
        "gap_family_minus_universal": gap,
        "universal_wins": universal_wins,
        "family_aware_wins": family_aware_wins,
        "near_ties": near_ties,
        "verdict": verdict,
        "rows": rows,
    }


# ============================================================================
# MATRIX BUILDING
# ============================================================================

def build_matrix() -> List[Dict]:
    cells = []
    for heterogeneity_label in ["low", "medium", "high"]:
        for power_label in ["baseline", "moderate", "strong"]:
            cells.append(evaluate_cell(heterogeneity_label, power_label))
    return cells


def summarize_matrix(cells: List[Dict]) -> Dict:
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

def render_report(cells: List[Dict], summary: Dict) -> str:
    lines = [
        "# PROJECT 10 PHASE 2 THRESHOLD MATRIX V1",
        "",
        "## Purpose",
        "First 3x3 threshold map for the revised higher-order candidate.",
        "",
        "## Verdict Counts",
        f"- {summary['counts']}",
        "",
        "## Matrix Cells",
    ]

    for cell in cells:
        lines.append(
            f"- heterogeneity={cell['heterogeneity']} | power={cell['universal_power']} | "
            f"avg_uni={cell['avg_universal_score']:.4f} | "
            f"avg_fam={cell['avg_family_aware_score']:.4f} | "
            f"gap={cell['gap_family_minus_universal']:.4f} | "
            f"verdict={cell['verdict']}"
        )

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This matrix is a first landscape map, not a final theory closure.",
        "- Its purpose is to locate where the revised candidate tends to hold, weaken, or become mixed.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 10 PHASE 2 THRESHOLD MATRIX V1")

    cells = build_matrix()
    summary = summarize_matrix(cells)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_10_phase2_threshold_matrix_v1",
        "target": "Revised higher-order candidate V1",
        "cells": cells,
        "summary": summary,
        "notes": [
            "This is the first threshold matrix in Project 10 Phase 2.",
            "It maps revised-candidate behavior across heterogeneity and universal-power levels.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(cells, summary))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print(f"✓ Verdict counts: {summary['counts']}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
