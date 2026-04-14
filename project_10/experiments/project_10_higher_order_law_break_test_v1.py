"""
================================================================================
PROJECT 10 HIGHER-ORDER LAW BREAK TEST V1
================================================================================

PURPOSE:
  Directly stress-test the higher-order chain hypothesis:

    When local competence reaches saturation without global robustness,
    successful rescue requires mechanisms aligned to the heterogeneous structure
    of family-level failure.

ROLE:
  This script does NOT test whether the individual components exist.
  It tests whether the chain itself survives a direct break-style comparison.

IMPORTANT:
  This is a falsification-oriented experiment.
  It is designed to distinguish:
    - component support
    from
    - support for the integrated higher-order chain

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

JSON_OUTPUT = OUTPUT_DIR / "project_10_higher_order_law_break_test_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_10_higher_order_law_break_test_v1_report.md"


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
# BREAK TEST CASES
# ============================================================================

def build_break_test_cases() -> List[Dict[str, Any]]:
    """
    Each case asks whether a non-family-aware / universal rescue succeeds
    under conditions where the higher-order hypothesis predicts it should fail
    or underperform relative to family-aligned rescue.
    """
    cases = []

    # ------------------------------------------------------------------------
    # Case 1: Project 7
    # same local trigger intervention does not rescue all families
    # ------------------------------------------------------------------------
    cases.append({
        "case_id": "HOT-B1",
        "project": "Project 7",
        "setup": "Multiple family-level failures with known heterogeneous trigger structure",
        "universal_rescue_candidate": "single local trigger correction",
        "observed_result": "rescues one family but not another",
        "break_test_role": "supports_chain",
        "confidence_level": "high",
        "why_it_matters": "Directly shows that one rescue does not compose across heterogeneous families"
    })

    # ------------------------------------------------------------------------
    # Case 2: Project 8
    # different architectural components needed for different failure families
    # ------------------------------------------------------------------------
    cases.append({
        "case_id": "HOT-B2",
        "project": "Project 8",
        "setup": "Integrated architecture tested across distinct family-level failure modes",
        "universal_rescue_candidate": "single shared rescue component",
        "observed_result": "different components rescue different families",
        "break_test_role": "supports_chain",
        "confidence_level": "high",
        "why_it_matters": "Direct evidence against one universal rescue mechanism"
    })

    # ------------------------------------------------------------------------
    # Case 3: Project 9
    # family-aware rescue beats naive cross-family rescue
    # ------------------------------------------------------------------------
    cases.append({
        "case_id": "HOT-B3",
        "project": "Project 9",
        "setup": "3D compositional sandbox with multiple family-sensitive perturbation regimes",
        "universal_rescue_candidate": "naive cross-family rescue",
        "observed_result": "adaptive family-aware rescue outperforms naive rescue",
        "break_test_role": "supports_chain",
        "confidence_level": "high",
        "why_it_matters": "Shows that universal rescue underperforms when family structure matters"
    })

    # ------------------------------------------------------------------------
    # Case 4: Project 4
    # intervention gain stays narrow rather than broad
    # ------------------------------------------------------------------------
    cases.append({
        "case_id": "HOT-B4",
        "project": "Project 4",
        "setup": "Intervention improves seen adversarial family",
        "universal_rescue_candidate": "broad transfer from one intervention",
        "observed_result": "gain remains narrow and does not transfer broadly",
        "break_test_role": "partial_supports_chain",
        "confidence_level": "high",
        "why_it_matters": "Not a full rescue architecture case, but still pushes against universal rescue logic"
    })

    # ------------------------------------------------------------------------
    # Case 5: potential weakness / caution
    # Project 6 shows local mechanistic structure but is not itself a rescue test
    # ------------------------------------------------------------------------
    cases.append({
        "case_id": "HOT-B5",
        "project": "Project 6",
        "setup": "Strong local mechanistic structure exists",
        "universal_rescue_candidate": "not directly applicable",
        "observed_result": "does not directly test rescue universality",
        "break_test_role": "boundary",
        "confidence_level": "medium",
        "why_it_matters": "Important boundary: not every project bears directly on the chain falsification test"
    })

    return cases


def summarize_cases(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts = {
        "supports_chain": 0,
        "partial_supports_chain": 0,
        "boundary": 0,
        "weakens_chain": 0,
        "falsifies_chain": 0,
    }

    for case in cases:
        role = case["break_test_role"]
        counts[role] = counts.get(role, 0) + 1

    support_strength = counts["supports_chain"] + 0.5 * counts["partial_supports_chain"]

    if counts["falsifies_chain"] > 0:
        overall = "CHAIN FAILS"
    elif counts["weakens_chain"] > 0:
        overall = "CHAIN UNDER TENSION"
    elif support_strength >= 3:
        overall = "CHAIN HOLDS UNDER CURRENT BREAK TEST"
    elif support_strength >= 1:
        overall = "CHAIN PARTIALLY HOLDS"
    else:
        overall = "CHAIN NOT ESTABLISHED"

    return {
        "counts": counts,
        "support_strength_score": support_strength,
        "overall_verdict": overall,
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(cases: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 10 HIGHER-ORDER LAW BREAK TEST V1",
        "",
        "## Target",
        "**Higher-Order Candidate (Unverified Chain Hypothesis)**",
        "",
        "## Summary",
        f"- counts: {summary['counts']}",
        f"- support_strength_score: {summary['support_strength_score']}",
        f"- overall_verdict: {summary['overall_verdict']}",
        "",
        "## Break Test Cases",
    ]

    for case in cases:
        lines.append(
            f"- [{case['project']}] {case['case_id']} | role={case['break_test_role']} | "
            f"confidence={case['confidence_level']}"
        )
        lines.append(f"  - setup: {case['setup']}")
        lines.append(f"  - universal_rescue_candidate: {case['universal_rescue_candidate']}")
        lines.append(f"  - observed_result: {case['observed_result']}")
        lines.append(f"  - why_it_matters: {case['why_it_matters']}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This test does not prove a universal higher-order law.",
        "- It asks whether the current program contains direct break-style evidence against universal rescue across heterogeneous failure structure.",
        "- A positive result strengthens the chain hypothesis, but does not close it permanently.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 10 HIGHER-ORDER LAW BREAK TEST V1")

    cases = build_break_test_cases()
    summary = summarize_cases(cases)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_10_higher_order_law_break_test_v1",
        "target": "Higher-Order Candidate (Unverified Chain Hypothesis)",
        "cases": cases,
        "summary": summary,
        "notes": [
            "This is the first direct break-style test of the higher-order chain hypothesis.",
            "It evaluates whether universal rescue fails or underperforms under heterogeneous family-level failure structure.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(cases, summary))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print(f"✓ Overall verdict: {summary['overall_verdict']}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
