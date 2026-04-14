"""
================================================================================
PROJECT 10 LAW 1 EVIDENCE MATRIX V1
================================================================================

PURPOSE:
  Build the first structured evidence matrix for Candidate Law 1:

    Local competence is not sufficient for global robustness.

ROLE:
  This script organizes explicit evidence across Projects 5–9 into
  a law-oriented matrix.

IMPORTANT:
  This is not a final law verdict.
  It is the first structured law-testing layer for Candidate Law 1.

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

JSON_OUTPUT = OUTPUT_DIR / "project_10_law1_evidence_matrix_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_10_law1_evidence_matrix_v1_report.md"


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

def build_law1_matrix() -> List[Dict[str, Any]]:
    rows = []

    # ------------------------------------------------------------------------
    # Project 5
    # ------------------------------------------------------------------------
    rows.append({
        "project": "Project 5",
        "result_id": "P5-R1",
        "result_title": "Oracle decomposition works but learned local composition fails",
        "candidate_law": "Law 1",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Structural feasibility does not transfer automatically to learned composition",
        "falsification_relevance": "not a falsifier",
        "comments": "Direct strong support: local correctness in principle does not guarantee global learned success"
    })

    rows.append({
        "project": "Project 5",
        "result_id": "P5-R5",
        "result_title": "Explicit carry-conditioned representation improves local behavior but rescues only one family",
        "candidate_law": "Law 1",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Improved local competence still does not imply broad family-level robustness",
        "falsification_relevance": "not a falsifier",
        "comments": "Very strong support"
    })

    rows.append({
        "project": "Project 5",
        "result_id": "P5-R9",
        "result_title": "Strong local transition-aware performance still fails compositionally",
        "candidate_law": "Law 1",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Even strong local metrics do not guarantee successful composition",
        "falsification_relevance": "not a falsifier",
        "comments": "One of the strongest supports for Law 1"
    })

    # ------------------------------------------------------------------------
    # Project 6
    # ------------------------------------------------------------------------
    rows.append({
        "project": "Project 6",
        "result_id": "P6-R10",
        "result_title": "Carry-related direction is causally important for local arithmetic behavior",
        "candidate_law": "Law 1",
        "evidence_role": "boundary",
        "confidence_level": "high",
        "boundary_note": "Shows strong local causal structure, but does not itself guarantee family-level success",
        "falsification_relevance": "not a falsifier",
        "comments": "Important boundary evidence"
    })

    rows.append({
        "project": "Project 6",
        "result_id": "P6-SYN",
        "result_title": "Mechanistic structure is real but not globally sufficient",
        "candidate_law": "Law 1",
        "candidate_law": "Law 1",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Internal arithmetic structure can be real without complete family-level explanation",
        "falsification_relevance": "not a falsifier",
        "comments": "Strong support from synthesis"
    })

    # ------------------------------------------------------------------------
    # Project 7
    # ------------------------------------------------------------------------
    rows.append({
        "project": "Project 7",
        "result_id": "P7-R1",
        "result_title": "Stepwise trace reveals local recurring failures driving global mismatch",
        "candidate_law": "Law 1",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Local correctness is not uniformly enough for global exact success",
        "falsification_relevance": "not a falsifier",
        "comments": "Strong bridge support"
    })

    rows.append({
        "project": "Project 7",
        "result_id": "P7-R2",
        "result_title": "One trigger correction rescues one family but not another",
        "candidate_law": "Law 1",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Fixing one local trigger is insufficient for universal family-level rescue",
        "falsification_relevance": "not a falsifier",
        "comments": "Very strong support"
    })

    # ------------------------------------------------------------------------
    # Project 8
    # ------------------------------------------------------------------------
    rows.append({
        "project": "Project 8",
        "result_id": "P8-R2",
        "result_title": "Integrated architecture rescues multiple families through distinct mechanisms",
        "candidate_law": "Law 1",
        "evidence_role": "support",
        "confidence_level": "high",
        "boundary_note": "Architecture-level support is needed beyond local competence alone",
        "falsification_relevance": "not a falsifier",
        "comments": "Strong architecture-level support"
    })

    # ------------------------------------------------------------------------
    # Project 9
    # ------------------------------------------------------------------------
    rows.append({
        "project": "Project 9",
        "result_id": "P9-R4",
        "result_title": "Rescue in higher-dimensional sandbox is itself family-sensitive",
        "candidate_law": "Law 1",
        "evidence_role": "boundary",
        "confidence_level": "medium",
        "boundary_note": "Higher-dimensional composition still needs structured rescue logic",
        "falsification_relevance": "not a falsifier",
        "comments": "Supports extension of the law into richer spaces"
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
        "# PROJECT 10 LAW 1 EVIDENCE MATRIX V1",
        "",
        "## Candidate Law",
        "**Local competence is not sufficient for global robustness.**",
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
        "- This matrix evaluates whether strong local competence repeatedly fails to guarantee robust global success.",
        "- It is a structured law test, not a rhetorical summary.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 10 LAW 1 EVIDENCE MATRIX V1")

    rows = build_law1_matrix()
    summary = summarize_matrix(rows)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_10_law1_evidence_matrix_v1",
        "candidate_law": "Local competence is not sufficient for global robustness",
        "rows": rows,
        "summary": summary,
        "notes": [
            "This is the first structured evidence-matrix test for Law 1.",
            "It evaluates whether local competence repeatedly fails to scale into global robust compositional success.",
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
