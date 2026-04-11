"""
================================================================================
PROJECT 10 LAW 3 FAMILY-SENSITIVE RESCUE TEST V1
================================================================================

PURPOSE:
  First explicit law-level test for Candidate Law 3:

    Rescue mechanisms are family-sensitive rather than universal.

ROLE:
  This script gathers already-established evidence from Projects 4, 7, 8, and 9
  and organizes it into a single law-oriented test summary.

IMPORTANT:
  This is not a new benchmark or model-training script.
  It is a theory-facing cross-project synthesis test.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


# ============================================================================
# PATHS
# ============================================================================
ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = ROOT / "project_10" / "results"
JSON_OUTPUT = OUTPUT_DIR / "project_10_law3_family_sensitive_rescue_test_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_10_law3_family_sensitive_rescue_test_v1_report.md"

# Source files used as evidence
P4_FILE = ROOT / "project_4" / "interventions" / "adversarial_training" / "PROJECT_4_ADVERSARIAL_TRAINING_RESULTS.md"
P7_FILE = ROOT / "project_7" / "results" / "PROJECT_7_CONTEXT_TRIGGER_RESULTS.md"
P8_FILE = ROOT / "project_8" / "results" / "PROJECT_8_INTEGRATED_ARCHITECTURE_V3_RESULTS.md"
P9_FILE = ROOT / "project_9" / "results" / "PROJECT_9_ADAPTIVE_FAMILY_RESCUE_RESULTS.md"


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


def exists(path: Path) -> bool:
    return path.exists() and path.is_file()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def contains_all(text: str, required_strings) -> bool:
    return all(s in text for s in required_strings)


# ============================================================================
# EVIDENCE TESTS
# ============================================================================

def inspect_project4():
    """
    Project 4 expected evidence:
      seen-family gain without broad transfer
    """
    result = {"source": str(P4_FILE), "present": exists(P4_FILE), "supports_law": False, "notes": []}

    if not result["present"]:
        result["notes"].append("missing file")
        return result

    text = read(P4_FILE)

    signals = [
        "seen adversarial family",
        "held-out adversarial family",
        "without producing broad structural robustness transfer",
    ]

    result["supports_law"] = contains_all(text, signals)
    result["notes"].append("checks for seen-family gain vs held-out transfer pattern")

    return result


def inspect_project7():
    """
    Project 7 expected evidence:
      one family trigger-correctable, another not
    """
    result = {"source": str(P7_FILE), "present": exists(P7_FILE), "supports_law": False, "notes": []}

    if not result["present"]:
        result["notes"].append("missing file")
        return result

    text = read(P7_FILE)

    signals = [
        "trigger-correctable failure mode",
        "trigger-insensitive failure mode",
    ]

    result["supports_law"] = contains_all(text, signals)
    result["notes"].append("checks for heterogeneous family-level rescue behavior")

    return result


def inspect_project8():
    """
    Project 8 expected evidence:
      interface rescues some families, controller rescues another
    """
    result = {"source": str(P8_FILE), "present": exists(P8_FILE), "supports_law": False, "notes": []}

    if not result["present"]:
        result["notes"].append("missing file")
        return result

    text = read(P8_FILE)

    signals = [
        "different family-level failures respond to different architectural components",
        "interface and controller mechanisms are not interchangeable",
    ]

    result["supports_law"] = contains_all(text, signals)
    result["notes"].append("checks for family-sensitive architecture rescue")

    return result


def inspect_project9():
    """
    Project 9 expected evidence:
      adaptive family-aware rescue beats naive rescue
    """
    result = {"source": str(P9_FILE), "present": exists(P9_FILE), "supports_law": False, "notes": []}

    if not result["present"]:
        result["notes"].append("missing file")
        return result

    text = read(P9_FILE)

    signals = [
        "family-aware rescue",
        "cross-family interference",
    ]

    result["supports_law"] = contains_all(text, signals)
    result["notes"].append("checks for family-sensitive rescue in 3D sandbox")

    return result


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 10 LAW 3 TEST V1",
        "",
        "## Candidate Law",
        "**Rescue mechanisms are family-sensitive rather than universal.**",
        "",
        "## Evidence Summary",
    ]

    for name, item in artifact["evidence"].items():
        lines.append(
            f"- {name}: present={item['present']}, supports_law={item['supports_law']}, notes={item['notes']}"
        )

    lines.extend([
        "",
        f"## Overall Verdict\n- {artifact['overall_verdict']}",
        "",
        "## Interpretation Boundary",
        "- This is the first cross-project law-oriented test.",
        "- It does not prove a universal law in the strongest sense yet, but tests whether the current evidence converges on a family-sensitive rescue pattern.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 10 LAW 3 FAMILY-SENSITIVE RESCUE TEST V1")

    evidence = {
        "project_4": inspect_project4(),
        "project_7": inspect_project7(),
        "project_8": inspect_project8(),
        "project_9": inspect_project9(),
    }

    support_count = sum(1 for item in evidence.values() if item["supports_law"])

    if support_count == len(evidence):
        overall_verdict = "STRONG SUPPORT"
    elif support_count >= 2:
        overall_verdict = "PARTIAL SUPPORT"
    else:
        overall_verdict = "WEAK SUPPORT"

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_10_law3_family_sensitive_rescue_test_v1",
        "candidate_law": "Rescue mechanisms are family-sensitive rather than universal",
        "evidence": evidence,
        "support_count": support_count,
        "overall_verdict": overall_verdict,
        "notes": [
            "This is the first explicit law-level synthesis test in Project 10.",
            "It checks whether multiple projects converge on family-sensitive rescue rather than universal rescue.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print(f"✓ Overall verdict: {overall_verdict}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
