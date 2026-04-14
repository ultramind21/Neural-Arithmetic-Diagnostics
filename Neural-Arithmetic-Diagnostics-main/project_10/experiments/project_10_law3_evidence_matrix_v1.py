"""
================================================================================
PROJECT 10 LAW 3 EVIDENCE MATRIX V1
================================================================================

PURPOSE:
  Build the first structured evidence matrix for Candidate Law 3:

    Rescue mechanisms are family-sensitive rather than universal.

ROLE:
  This script replaces loose text matching with a structured evidence table.

IMPORTANT:
  This is not a final law verdict.
  It is a stronger methodology layer for evaluating the candidate law.

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

JSON_OUTPUT = OUTPUT_DIR / "project_10_law3_evidence_matrix_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_10_law3_evidence_matrix_v1_report.md"


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

def build_law3_matrix() -> List[Dict[str, Any]]:
    """
    First explicit evidence matrix for Candidate Law 3.

    Candidate Law 3:
      Rescue mechanisms are family-sensitive rather than universal.
    """
    rows = []

    # ------------------------------------------------------------------------
    # Project 4
    # ------------------------------------------------------------------------
    rows.append({
        "project": "Project 4",
        "result_id": "P4-I1",
        "result_title": "Adversarial training improves seen family without broad held-out transfer",
        "candidate_law": "Law 3",
        "evidence_role": "partial_support",
        "confidence_level": "high",
        "boundary_note": "Intervention gain was real but structurally narrow rather than broad",
        "falsification_relevance": "not a direct falsifier",
        "comments": "Supports family-sensitive gain logic, but was not framed as explicit family-specific rescue architecture"
    })

    # ------------------------------------------------------------------------
    # Project 5
    # ------------------------------------------------------------------------
    rows.append({
        "project": "Project 5",
        "result_id": "P5-R5",
        "result_title": "Explicit carry-conditioned representation rescues only the structurally simplest family",
        "candidate_law": "Law 3",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Rescue appears family-limited rather than broad",
        "falsification_relevance": "not a falsifier",
        "comments": "Strong support: one family rescued, others still fail"
    })

    rows.append({
        "project": "Project 5",
        "result_id": "P5-R8",
        "result_title": "Local context expansion does not rescue other failing families",
        "candidate_law": "Law 3",
        "evidence_role": "boundary",
        "confidence_level": "high",
        "boundary_note": "Simple richer context does not universalize rescue",
        "falsification_relevance": "not a falsifier",
        "comments": "Supports the idea that rescue is structurally constrained"
    })

    # ------------------------------------------------------------------------
    # Project 7
    # ------------------------------------------------------------------------
    rows.append({
        "project": "Project 7",
        "result_id": "P7-R2",
        "result_title": "Trigger intervention rescues one family but not another",
        "candidate_law": "Law 3",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "The same local trigger fix is sufficient for one family and insufficient for another",
        "falsification_relevance": "not a falsifier",
        "comments": "One of the strongest direct supports for Law 3"
    })

    # ------------------------------------------------------------------------
    # Project 8
    # ------------------------------------------------------------------------
    rows.append({
        "project": "Project 8",
        "result_id": "P8-R1",
        "result_title": "Interface and controller rescue different family-level failure modes",
        "candidate_law": "Law 3",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "No single rescue mechanism handles all tested family types by itself",
        "falsification_relevance": "not a falsifier",
        "comments": "Strong architecture-level support"
    })

    rows.append({
        "project": "Project 8",
        "result_id": "P8-R2",
        "result_title": "Integrated architecture combines family-sensitive rescue mechanisms successfully",
        "candidate_law": "Law 3",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Different sub-mechanisms appear necessary for different families",
        "falsification_relevance": "not a falsifier",
        "comments": "Strong support at architecture-design level"
    })

    # ------------------------------------------------------------------------
    # Project 9
    # ------------------------------------------------------------------------
    rows.append({
        "project": "Project 9",
        "result_id": "P9-R4",
        "result_title": "Cross-family rescue can be harmful while same-family rescue can be safe",
        "candidate_law": "Law 3",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Rescue quality depends on family alignment",
        "falsification_relevance": "not a falsifier",
        "comments": "Strong support inside the 3D sandbox"
    })

    rows.append({
        "project": "Project 9",
        "result_id": "P9-R5",
        "result_title": "Adaptive family-aware rescue outperforms naive cross-family rescue",
        "candidate_law": "Law 3",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Adaptive rescue improves because it respects family structure",
        "falsification_relevance": "not a falsifier",
        "comments": "One of the strongest supports for Law 3"
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

    for row in rows:
        role = row["evidence_role"]
        counts[role] = counts.get(role, 0) + 1

    # simple support summary
    support_strength = counts["support"] + 0.5 * counts["partial_support"]

    if counts["contradiction"] > 0 or counts["falsification_candidate"] > 0:
        overall = "MIXED / UNDER TENSION"
    elif support_strength >= 5:
        overall = "STRONG SUPPORT"
    elif support_strength >= 2:
        overall = "PARTIAL SUPPORT"
    else:
        overall = "WEAK SUPPORT"

    return {
        "counts": counts,
        "support_strength_score": support_strength,
        "overall_verdict": overall,
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(rows: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 10 LAW 3 EVIDENCE MATRIX V1",
        "",
        "## Candidate Law",
        "**Rescue mechanisms are family-sensitive rather than universal.**",
        "",
        "## Summary",
        f"- counts: {summary['counts']}",
        f"- support_strength_score: {summary['support_strength_score']}",
        f"- overall_verdict: {summary['overall_verdict']}",
        "",
        "## Matrix Rows",
    ]

    for row in rows:
        lines.append(
            f"- [{row['project']}] {row['result_id']} | role={row['evidence_role']} | "
            f"confidence={row['confidence_level']} | {row['result_title']}"
        )
        lines.append(f"  - boundary_note: {row['boundary_note']}")
        lines.append(f"  - falsification_relevance: {row['falsification_relevance']}")
        lines.append(f"  - comments: {row['comments']}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This matrix is a stronger methodological step than plain textual pattern matching.",
        "- It is still an early law-testing layer, not a final theory verdict.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 10 LAW 3 EVIDENCE MATRIX V1")

    rows = build_law3_matrix()
    summary = summarize_matrix(rows)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_10_law3_evidence_matrix_v1",
        "candidate_law": "Rescue mechanisms are family-sensitive rather than universal",
        "rows": rows,
        "summary": summary,
        "notes": [
            "This is the first structured evidence-matrix test in Project 10.",
            "It is meant to replace weak summary-language matching with explicit role-based evidence classification.",
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
