"""
================================================================================
PROJECT 10 HIGHER-ORDER LAW EVIDENCE MATRIX V1
================================================================================

PURPOSE:
  Build the first structured evidence matrix for the higher-order law candidate:

    When local competence reaches saturation without global robustness,
    successful rescue requires mechanisms aligned to the heterogeneous structure
    of family-level failure.

ROLE:
  This script checks whether the current program supports the full chain behind
  the higher-order candidate, rather than only isolated parts of it.

IMPORTANT:
  This is not a final law verdict.
  It is the first structured test of whether the higher-order claim is real.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


# ============================================================================
# PATHS
# ============================================================================
ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "project_10" / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_10_higher_order_law_evidence_matrix_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_10_higher_order_law_evidence_matrix_v1_report.md"


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def save_json(path: Path, obj: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def save_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ============================================================================
# EVIDENCE MATRIX
# ============================================================================

def build_higher_order_matrix() -> List[Dict[str, Any]]:
    rows = []

    # Layer 1: local competence saturation without global robustness
    rows.append({
        "project": "Project 5",
        "result_id": "P5-R9",
        "result_title": "Strong local performance still fails compositionally",
        "chain_component": "local_competence_without_global_robustness",
        "evidence_role": "support",
        "confidence_level": "high",
        "comments": "Direct support for the first half of the higher-order candidate"
    })

    rows.append({
        "project": "Project 6",
        "result_id": "P6-R10",
        "result_title": "Carry direction is causally important locally",
        "chain_component": "local_competence_without_global_robustness",
        "evidence_role": "boundary",
        "confidence_level": "high",
        "comments": "Local mechanistic strength alone does not guarantee family-level explanation"
    })

    # Layer 2: family-level heterogeneity
    rows.append({
        "project": "Project 7",
        "result_id": "P7-R2",
        "result_title": "One family is trigger-correctable, another is not",
        "chain_component": "family_level_heterogeneity",
        "evidence_role": "support",
        "confidence_level": "high",
        "comments": "Strong support for heterogeneous family-level failure"
    })

    rows.append({
        "project": "Project 6",
        "result_id": "P6-R8",
        "result_title": "Trajectory dynamics differ sharply across families",
        "chain_component": "family_level_heterogeneity",
        "evidence_role": "support",
        "confidence_level": "high",
        "comments": "Strong support that family-level internal dynamics are not uniform"
    })

    # Layer 3: family-sensitive rescue
    rows.append({
        "project": "Project 8",
        "result_id": "P8-R2",
        "result_title": "Different family-level failures respond to different architectural components",
        "chain_component": "family_sensitive_rescue",
        "evidence_role": "support",
        "confidence_level": "high",
        "comments": "Strong architecture-level support"
    })

    rows.append({
        "project": "Project 9",
        "result_id": "P9-R5",
        "result_title": "Adaptive family-aware rescue outperforms naive rescue",
        "chain_component": "family_sensitive_rescue",
        "evidence_role": "support",
        "confidence_level": "high",
        "comments": "Strong sandbox-level support"
    })

    rows.append({
        "project": "Project 4",
        "result_id": "P4-I1",
        "result_title": "Seen-family gain without broad held-out transfer",
        "chain_component": "family_sensitive_rescue",
        "evidence_role": "partial_support",
        "confidence_level": "high",
        "comments": "Supports narrow intervention gain pattern but not full architecture-level rescue"
    })

    # Layer 4: candidate boundary
    rows.append({
        "project": "Project 6",
        "result_id": "P6-R11",
        "result_title": "Trajectory smoothing does not rescue failing family",
        "chain_component": "boundary_on_naive_rescue",
        "evidence_role": "boundary",
        "confidence_level": "high",
        "comments": "Shows that not all rescue-like interventions are valid causal levers"
    })

    return rows


def summarize_matrix(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts = {
        "support": 0,
        "partial_support": 0,
        "boundary": 0,
        "no_evidence": 0,
        "contradiction": 0,
        "falsification_candidate": 0,
    }

    chain_counts = {}

    for row in rows:
        role = row["evidence_role"]
        counts[role] = counts.get(role, 0) + 1

        comp = row["chain_component"]
        chain_counts[comp] = chain_counts.get(comp, 0) + 1

    support_strength = counts["support"] + 0.5 * counts["partial_support"]

    if counts["contradiction"] > 0 or counts["falsification_candidate"] > 0:
        overall = "MIXED / UNDER TENSION"
    elif support_strength >= 5 and len(chain_counts) >= 3:
        overall = "STRONG SUPPORT"
    elif support_strength >= 2:
        overall = "PARTIAL SUPPORT"
    else:
        overall = "WEAK SUPPORT"

    return {
        "counts": counts,
        "chain_counts": chain_counts,
        "support_strength_score": support_strength,
        "overall_verdict": overall,
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(rows: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 10 HIGHER-ORDER LAW EVIDENCE MATRIX V1",
        "",
        "## Higher-Order Candidate",
        "**When local competence reaches saturation without global robustness, successful rescue requires mechanisms aligned to the heterogeneous structure of family-level failure.**",
        "",
        "## Summary",
        f"- counts: {summary['counts']}",
        f"- chain_counts: {summary['chain_counts']}",
        f"- support_strength_score: {summary['support_strength_score']}",
        f"- overall_verdict: {summary['overall_verdict']}",
        "",
        "## Matrix Rows",
    ]

    for row in rows:
        lines.append(
            f"- [{row['project']}] {row['result_id']} | component={row['chain_component']} | "
            f"role={row['evidence_role']} | confidence={row['confidence_level']} | {row['result_title']}"
        )
        lines.append(f"  - comments: {row['comments']}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This matrix tests whether the higher-order law is supported as a chain, not just as isolated statements.",
        "- It is the first structured higher-order law test in Project 10.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 10 HIGHER-ORDER LAW EVIDENCE MATRIX V1")

    rows = build_higher_order_matrix()
    summary = summarize_matrix(rows)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_10_higher_order_law_evidence_matrix_v1",
        "candidate_law": "When local competence reaches saturation without global robustness, successful rescue requires mechanisms aligned to the heterogeneous structure of family-level failure",
        "rows": rows,
        "summary": summary,
        "notes": [
            "This is the first higher-order law test in Project 10.",
            "It evaluates whether the full chain behind the candidate law is supported by the current program.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(rows, summary))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print(f"✓ Overall verdict: {summary['overall_verdict']}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
