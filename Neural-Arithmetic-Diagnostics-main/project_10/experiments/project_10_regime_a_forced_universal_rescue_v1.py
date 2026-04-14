"""
================================================================================
PROJECT 10 REGIME A FORCED UNIVERSAL RESCUE V1
================================================================================

PURPOSE:
  First adversarial falsification construction for the higher-order candidate.

TARGET:
  Test whether a universal rescue can succeed when multiple nominal families
  are constructed to share a more aligned underlying failure structure.

IMPORTANT:
  This is a synthetic falsification sandbox.
  It does not retrain historical models.
  It creates a minimal operational regime for attacking the current theory.

================================================================================
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List


# ============================================================================
# PATHS
# ============================================================================
ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "project_10" / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_10_regime_a_forced_universal_rescue_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_10_regime_a_forced_universal_rescue_v1_report.md"


# ============================================================================
# DATA MODEL
# ============================================================================

@dataclass
class FamilyCase:
    family: str
    local_competence: float
    base_global_score: float
    shared_failure_factor: float
    family_noise: float


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
# REGIME CONSTRUCTION
# ============================================================================

def build_regime() -> List[FamilyCase]:
    """
    Construct nominally distinct families with:
      - high local competence
      - weak/failing global robustness
      - strongly aligned underlying failure structure
      - only small family-specific noise
    """
    return [
        FamilyCase("family_A", 0.93, 0.48, 0.42, 0.01),
        FamilyCase("family_B", 0.91, 0.46, 0.40, -0.01),
        FamilyCase("family_C", 0.94, 0.47, 0.41, 0.02),
        FamilyCase("family_D", 0.92, 0.45, 0.39, -0.02),
    ]


# ============================================================================
# RESCUE LOGIC
# ============================================================================

def universal_rescue(case: FamilyCase) -> float:
    """
    Universal rescue targets the shared failure factor directly.
    Because regime A intentionally aligns failure structure, universal rescue
    is given a real chance to succeed.
    """
    gain = 0.30 * case.shared_failure_factor
    residual_penalty = abs(case.family_noise) * 0.05
    return clamp(case.base_global_score + gain - residual_penalty)


def family_aware_rescue(case: FamilyCase) -> float:
    """
    Family-aware rescue gets slightly better adaptation to family-specific noise.
    """
    gain = 0.30 * case.shared_failure_factor
    extra = 0.03 - abs(case.family_noise) * 0.01
    return clamp(case.base_global_score + gain + extra)


# ============================================================================
# ANALYSIS
# ============================================================================

def analyze(cases: List[FamilyCase]) -> Dict:
    rows = []

    universal_wins = 0
    family_aware_wins = 0
    near_ties = 0

    for case in cases:
        base = case.base_global_score
        uni = universal_rescue(case)
        fam = family_aware_rescue(case)

        if uni > fam + 0.01:
            winner = "universal"
            universal_wins += 1
        elif fam > uni + 0.01:
            winner = "family_aware"
            family_aware_wins += 1
        else:
            winner = "near_tie"
            near_ties += 1

        rows.append({
            "family": case.family,
            "local_competence": case.local_competence,
            "base_global_score": base,
            "shared_failure_factor": case.shared_failure_factor,
            "family_noise": case.family_noise,
            "universal_rescue_score": uni,
            "family_aware_rescue_score": fam,
            "winner": winner,
        })

    avg_base = sum(r["base_global_score"] for r in rows) / len(rows)
    avg_uni = sum(r["universal_rescue_score"] for r in rows) / len(rows)
    avg_fam = sum(r["family_aware_rescue_score"] for r in rows) / len(rows)

    # Verdict logic:
    # If universal rescue performs broadly and is close to family-aware rescue,
    # the higher-order candidate weakens.
    if universal_wins >= 2 or (avg_uni >= avg_fam - 0.02):
        verdict = "WEAKENS HIGHER-ORDER CANDIDATE"
    elif family_aware_wins >= 3 and avg_fam > avg_uni + 0.03:
        verdict = "SUPPORTS HIGHER-ORDER CANDIDATE"
    else:
        verdict = "BOUNDARY / MIXED"

    return {
        "rows": rows,
        "summary": {
            "avg_base_global_score": avg_base,
            "avg_universal_rescue_score": avg_uni,
            "avg_family_aware_rescue_score": avg_fam,
            "universal_wins": universal_wins,
            "family_aware_wins": family_aware_wins,
            "near_ties": near_ties,
            "verdict": verdict,
        }
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict) -> str:
    s = artifact["summary"]
    lines = [
        "# PROJECT 10 REGIME A FORCED UNIVERSAL RESCUE V1",
        "",
        "## Purpose",
        "Synthetic adversarial falsification test for the higher-order candidate.",
        "",
        "## Summary",
        f"- avg_base_global_score: {s['avg_base_global_score']:.3f}",
        f"- avg_universal_rescue_score: {s['avg_universal_rescue_score']:.3f}",
        f"- avg_family_aware_rescue_score: {s['avg_family_aware_rescue_score']:.3f}",
        f"- universal_wins: {s['universal_wins']}",
        f"- family_aware_wins: {s['family_aware_wins']}",
        f"- near_ties: {s['near_ties']}",
        f"- verdict: {s['verdict']}",
        "",
        "## Per-Family Results",
    ]

    for row in artifact["rows"]:
        lines.append(
            f"- {row['family']}: base={row['base_global_score']:.3f}, "
            f"universal={row['universal_rescue_score']:.3f}, "
            f"family_aware={row['family_aware_rescue_score']:.3f}, "
            f"winner={row['winner']}"
        )

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This is a synthetic adversarial regime, not a historical reproduction.",
        "- Its value lies in whether aligned failure structure reduces the need for family-sensitive rescue.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 10 REGIME A FORCED UNIVERSAL RESCUE V1")

    cases = build_regime()
    analysis = analyze(cases)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_10_regime_a_forced_universal_rescue_v1",
        "regime": "Regime A — Forced Universal Rescue",
        "cases": [asdict(c) for c in cases],
        "rows": analysis["rows"],
        "summary": analysis["summary"],
        "notes": [
            "This is the first adversarial synthetic regime in Project 10.",
            "It tests whether universal rescue can become competitive when failure structure is intentionally aligned across nominal families.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print(f"✓ Verdict: {artifact['summary']['verdict']}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
