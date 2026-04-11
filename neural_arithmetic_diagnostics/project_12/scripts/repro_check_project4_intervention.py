"""
================================================================================
PROJECT 12 — PROJECT 4 INTERVENTION REPRODUCTION CHECK (SPRINT 4B.2C)
================================================================================

PURPOSE:
  Policy-based validation of P4-C04 (narrow transfer) claim.
  NO numeric comparison to Project 4 history (non-deterministic training).
  ONLY evaluates: ordering + gap acceptance criteria.

INPUTS:
  - project_12/results/repro_p4/intervention/artifact.json (from entrypoint)

OUTPUTS:
  - project_12/reports/REPRO_CHECK_PROJECT4_INTERVENTION.md

================================================================================
"""

from pathlib import Path
from typing import Dict, Any
import json
import sys


def load_intervention_artifact(path: Path) -> Dict[str, Any]:
    """Load and validate intervention artifact structure."""
    if not path.exists():
        raise FileNotFoundError(f"Intervention artifact not found: {path}")
    
    with open(path, "r") as f:
        artifact = json.load(f)
    
    required_fields = ["base_arch", "seen_families", "heldout_families", 
                       "pre_exact_match", "post_exact_match", "computed_gains", 
                       "acceptance"]
    
    for field in required_fields:
        if field not in artifact:
            raise ValueError(f"Artifact missing field: {field}")
    
    return artifact


def check_p4c04_acceptance(artifact: Dict[str, Any]) -> Dict[str, Any]:
    """
    Policy-based check for P4-C04 acceptance.
    NO comparison to Project 4 historical values.
    ONLY checks: ordering + gap from computed_gains.
    """
    gains = artifact["computed_gains"]
    acceptance = artifact["acceptance"]
    
    seen_gain = float(gains.get("seen_gain", 0.0))
    heldout_gain = float(gains.get("heldout_gain", 0.0))
    gap = float(gains.get("gap", 0.0))
    
    min_gap = float(acceptance.get("min_gap", 0.10))
    require_ordering = acceptance.get("require_ordering", True)
    
    # Check criteria
    gap_pass = gap >= min_gap
    ordering_pass = (seen_gain > heldout_gain) if require_ordering else True
    
    overall_pass = gap_pass and ordering_pass
    
    return {
        "seen_gain": seen_gain,
        "heldout_gain": heldout_gain,
        "gap": gap,
        "min_gap": min_gap,
        "gap_pass": gap_pass,
        "require_ordering": require_ordering,
        "ordering_pass": ordering_pass,
        "overall_pass": overall_pass,
    }


def render_report(
    artifact: Dict[str, Any],
    check_result: Dict[str, Any],
    artifact_path: Path,
) -> str:
    """Render markdown report."""
    lines = [
        "# REPRO_CHECK_PROJECT4_INTERVENTION — P4-C04 Policy Validation",
        "",
        f"**Artifact:** {artifact_path.name}",
        f"**Timestamp:** {artifact['p12_metadata'].get('timestamp_utc', 'unknown')}",
        f"**Base architecture:** {artifact.get('base_arch', 'unknown')}",
        "",
        "---",
        "",
        "## P4-C04 Claim: Narrow Transfer",
        "",
        "**Definition:** Adversarial training improves seen-family accuracy significantly more than held-out family accuracy.",
        "",
        "**Measurement:** Exact_match per family (post-training - baseline).",
        "",
        "---",
        "",
        "## Baseline Metrics (Pre-Intervention)",
        "",
    ]
    
    pre_exact = artifact.get("pre_exact_match", {})
    lines.append("| Family | Baseline exact_match |")
    lines.append("|--------|----------------------|")
    for family, val in pre_exact.items():
        lines.append(f"| {family} | {val:.6f} |")
    
    lines.extend([
        "",
        "---",
        "",
        "## Post-Training Metrics",
        "",
    ])
    
    post_exact = artifact.get("post_exact_match", {})
    lines.append("| Family | Post-Train exact_match |")
    lines.append("|--------|----------------------|")
    for family, val in post_exact.items():
        lines.append(f"| {family} | {val:.6f} |")
    
    lines.extend([
        "",
        "---",
        "",
        "## Computed Gains",
        "",
    ])
    
    gains = artifact.get("computed_gains", {})
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| seen_gain (post_mean - pre_mean) | {gains.get('seen_gain', 0.0):.6f} |")
    lines.append(f"| heldout_gain (post_mean - pre_mean) | {gains.get('heldout_gain', 0.0):.6f} |")
    lines.append(f"| gap (seen_gain - heldout_gain) | {gains.get('gap', 0.0):.6f} |")
    
    lines.extend([
        "",
        "---",
        "",
        "## Acceptance Criteria (Policy-Based)",
        "",
        f"1. **Gap Threshold:** gap >= {check_result['min_gap']:.2f}",
        f"   - Result: {check_result['gap']:.6f} {'✅ PASS' if check_result['gap_pass'] else '❌ FAIL'}",
        "",
        f"2. **Ordering Criterion:** seen_gain > heldout_gain",
        f"   - Required: {check_result['require_ordering']}",
        f"   - Result: {check_result['seen_gain']:.6f} > {check_result['heldout_gain']:.6f} = {'✅ PASS' if check_result['ordering_pass'] else '❌ FAIL'}",
        "",
        "---",
        "",
        "## Verdict",
        "",
    ])
    
    if check_result["overall_pass"]:
        lines.extend([
            "✅ **P4-C04 PASS**",
            "",
            "Narrow transfer criterion satisfied:",
            "- Seen-family improvement exceeds held-out improvement",
            "- Gap exceeds minimum threshold",
            "",
        ])
    else:
        lines.extend([
            "❌ **P4-C04 FAIL**",
            "",
            "Narrow transfer criterion not satisfied.",
            "Check gap and ordering requirements above.",
            "",
        ])
    
    lines.extend([
        "---",
        "",
        "## Metadata",
        "",
        f"- **Base architecture:** {artifact.get('base_arch', 'unknown')}",
        f"- **Seen families:** {', '.join(artifact.get('seen_families', []))}",
        f"- **Held-out families:** {', '.join(artifact.get('heldout_families', []))}",
        f"- **Device:** {artifact['p12_metadata'].get('device', 'unknown')}",
        f"- **Git commit:** {artifact['p12_metadata'].get('git', {}).get('commit', 'unknown')[:8]}",
        "",
        "---",
        "",
        "**Generated by:** project_12/scripts/repro_check_project4_intervention.py (Sprint 4B.2C)",
        "",
    ])
    
    return "\n".join(lines)


def main():
    artifact_path = Path("project_12/results/repro_p4/intervention/artifact.json")
    report_path = Path("project_12/reports/REPRO_CHECK_PROJECT4_INTERVENTION.md")
    
    print(f"\n{'=' * 80}")
    print("PROJECT 4 INTERVENTION REPRODUCTION CHECK (P4-C04)")
    print(f"{'=' * 80}")
    print(f"Artifact: {artifact_path}")
    
    try:
        artifact = load_intervention_artifact(artifact_path)
        print(f"✓ Artifact loaded")
    except Exception as e:
        print(f"❌ Failed to load artifact: {e}")
        sys.exit(1)
    
    try:
        check_result = check_p4c04_acceptance(artifact)
        print(f"✓ Acceptance check completed")
    except Exception as e:
        print(f"❌ Failed to check acceptance: {e}")
        sys.exit(1)
    
    # Render report
    report_text = render_report(artifact, check_result, artifact_path)
    
    try:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_text, encoding="utf-8")
        print(f"✓ Report saved to: {report_path}")
    except Exception as e:
        print(f"❌ Failed to save report: {e}")
        sys.exit(1)
    
    # Print summary
    print(f"\n{'=' * 80}")
    if check_result["overall_pass"]:
        print("✅ P4-C04 PASS")
    else:
        print("❌ P4-C04 FAIL")
    print(f"{'=' * 80}\n")
    
    sys.exit(0 if check_result["overall_pass"] else 1)


if __name__ == "__main__":
    main()

