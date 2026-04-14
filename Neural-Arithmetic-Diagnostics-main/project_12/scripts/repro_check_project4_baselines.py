"""
================================================================================
REPRO_CHECK_PROJECT4_BASELINES.PY
================================================================================

PROJECT 12 BASELINE REPRODUCTION CHECK

PURPOSE:
  Compare Project 12 baseline reproduction artifacts against Project 4 historical
  artifacts using load-bearing metrics comparison.

METHODOLOGY:
  1. Load historical artifacts from project_4/results/baseline_runs/
  2. Load P12 reproduction artifacts from project_12/results/repro_p4/baselines/
  3. Compare scorecard metrics (exact-match accuracies)
  4. Apply tolerance policy (1e-6 absolute difference = exact match)
  5. Generate detailed repro check report

TOLERANCE POLICY:
  - Tolerance: 1e-6 (assume deterministic evaluation)
  - PASS: All metrics within tolerance OR metrics match exactly
  - FAIL: Any metric differs by > tolerance

================================================================================
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def load_json(p: Path) -> Dict[str, Any]:
    """Load JSON file."""
    if not p.exists():
        return {"error": f"File not found: {p}"}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": f"Failed to load {p}: {e}"}


def extract_key_metrics(artifact: Dict[str, Any], arch: str) -> Dict[str, float]:
    """
    Extract load-bearing metrics from artifact.
    
    Load-bearing metrics:
    - in_distribution_accuracy
    - pattern_breakdown (alternating_carry, full_propagation_chain, block_boundary_stress)
    - mean_adversarial_accuracy
    """
    if "error" in artifact:
        return {}
    
    metrics = {}
    scorecard = artifact.get("scorecard", {})
    
    # In-distribution accuracy
    if "in_distribution_accuracy" in scorecard:
        metrics["in_distribution_accuracy"] = scorecard["in_distribution_accuracy"]
    
    # Pattern breakdown
    pattern_breakdown = scorecard.get("pattern_breakdown", {})
    for pattern_name in ["alternating_carry", "full_propagation_chain", "block_boundary_stress"]:
        if pattern_name in pattern_breakdown:
            metrics[f"pattern_{pattern_name}"] = pattern_breakdown[pattern_name]
    
    # Mean adversarial accuracy
    if "mean_adversarial_accuracy" in scorecard:
        metrics["mean_adversarial_accuracy"] = scorecard["mean_adversarial_accuracy"]
    
    return metrics


def compare_metrics(
    hist_metrics: Dict[str, float],
    p12_metrics: Dict[str, float],
    tolerance: float = 1e-6,
) -> Tuple[bool, List[str]]:
    """
    Compare historical and P12 metrics.
    
    Returns (pass, list_of_diffs).
    """
    if not hist_metrics or not p12_metrics:
        return False, ["Missing metrics (empty dict)"]
    
    diffs = []
    for key in sorted(set(hist_metrics.keys()) | set(p12_metrics.keys())):
        hist_val = hist_metrics.get(key)
        p12_val = p12_metrics.get(key)
        
        if hist_val is None:
            diffs.append(f"  - `{key}`: MISSING in historical")
        elif p12_val is None:
            diffs.append(f"  - `{key}`: MISSING in P12")
        else:
            abs_diff = abs(hist_val - p12_val)
            if abs_diff > tolerance:
                diffs.append(f"  - `{key}`: historical={hist_val:.8f}, p12={p12_val:.8f}, diff={abs_diff:.2e}")
    
    # PASS if no diffs > tolerance
    pass_status = len(diffs) == 0
    return pass_status, diffs


def main():
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    PROJECT_4_ROOT = PROJECT_ROOT / "project_4"
    PROJECT_12_ROOT = PROJECT_ROOT / "project_12"
    
    # Paths to artifacts
    HIST_ARTIFACTS = {
        "mlp": PROJECT_4_ROOT / "results" / "baseline_runs" / "phase30_mlp_baseline_artifact.json",
        "lstm": PROJECT_4_ROOT / "results" / "baseline_runs" / "phase30_lstm_baseline_artifact.json",
        "transformer": PROJECT_4_ROOT / "results" / "baseline_runs" / "phase30_transformer_baseline_artifact.json",
    }
    
    P12_ARTIFACTS = {
        "mlp": PROJECT_12_ROOT / "results" / "repro_p4" / "baselines" / "mlp" / "artifact.json",
        "lstm": PROJECT_12_ROOT / "results" / "repro_p4" / "baselines" / "lstm" / "artifact.json",
        "transformer": PROJECT_12_ROOT / "results" / "repro_p4" / "baselines" / "transformer" / "artifact.json",
    }
    
    REPORT_PATH = PROJECT_12_ROOT / "reports" / "REPRO_CHECK_PROJECT4_BASELINES.md"
    
    print("\n" + "=" * 80)
    print("PROJECT 12 — PROJECT 4 BASELINE REPRO CHECK")
    print("=" * 80)
    
    # Run comparison for each architecture
    report_lines = [
        "# REPRO_CHECK_PROJECT4_BASELINES — Project 12 Baseline Reproduction Report",
        "",
        "**Purpose:** Verify that Project 12 baseline reproductions match Project 4 historical artifacts.",
        "",
        "**Methodology:**",
        "- Compare scorecard metrics (in-distribution accuracy, pattern accuracies, mean adversarial)",
        "- Tolerance: 1e-6 absolute difference (quasi-deterministic evaluation)",
        "- PASS: All metrics within tolerance",
        "- FAIL: Any metric differs beyond tolerance",
        "",
        "---",
        "",
    ]
    
    all_pass = True
    results = {}
    
    for arch in ["mlp", "lstm", "transformer"]:
        print(f"\n[{arch.upper()}] Comparing artifacts...")
        
        hist_artifact = load_json(HIST_ARTIFACTS[arch])
        p12_artifact = load_json(P12_ARTIFACTS[arch])
        
        hist_metrics = extract_key_metrics(hist_artifact, arch)
        p12_metrics = extract_key_metrics(p12_artifact, arch)
        
        pass_status, diffs = compare_metrics(hist_metrics, p12_metrics, tolerance=1e-6)
        results[arch] = {"pass": pass_status, "diffs": diffs, "p12_metadata": p12_artifact.get("p12_metadata", {})}
        
        if not pass_status:
            all_pass = False
        
        # Add to report
        status_str = "✅ PASS" if pass_status else "❌ FAIL"
        report_lines.append(f"## {arch.upper()} Baseline")
        report_lines.append(f"**Status:** {status_str}")
        report_lines.append("")
        
        if pass_status:
            report_lines.append("All load-bearing metrics match within tolerance (1e-6).")
        else:
            report_lines.append("**Metric Differences:**")
            report_lines.extend(diffs)
        
        report_lines.append("")
        
        # Add metadata
        if "p12_metadata" in p12_artifact:
            metadata = p12_artifact["p12_metadata"]
            report_lines.extend([
                "**P12 Metadata:**",
                f"- Git Hash: `{metadata.get('git_hash', 'UNKNOWN')}`",
                f"- Timestamp: {metadata.get('timestamp_utc', 'UNKNOWN')}",
                f"- Entrypoint: `{metadata.get('entrypoint', 'UNKNOWN')}`",
                f"- Python Version: {metadata.get('env', {}).get('python_version', 'UNKNOWN')}",
                f"- PyTorch Version: {metadata.get('env', {}).get('torch_version', 'UNKNOWN')}",
                "",
            ])
        
        report_lines.append("---")
        report_lines.append("")
        
        status_emoji = "✅" if pass_status else "❌"
        print(f"  {status_emoji} {arch.upper()}: {'PASS' if pass_status else 'FAIL'}")
        if diffs:
            for diff in diffs[:3]:  # Show first 3 diffs
                print(f"    {diff}")
    
    # Summary
    report_lines.extend([
        "## Summary",
        "",
    ])
    
    if all_pass:
        report_lines.append("**Overall Status:** ✅ ALL ARCHITECTURES PASS REPRO CHECK")
        report_lines.append("")
        report_lines.append("All Project 12 baseline reproductions match Project 4 historical artifacts within tolerance.")
    else:
        report_lines.append("**Overall Status:** ❌ SOME ARCHITECTURES FAILED REPRO CHECK")
        report_lines.append("")
        report_lines.append("Failures:")
        for arch, result in results.items():
            if not result["pass"]:
                report_lines.append(f"- **{arch.upper()}**: {len(result['diffs'])} metric(s) differ beyond tolerance")
    
    report_lines.extend([
        "",
        "---",
        "",
        "## Tolerance Policy",
        "",
        "Tolerance: 1e-6 absolute difference",
        "",
        "Rationale: Project 4 baseline artifacts lack seed/environment metadata, so we assume",
        "quasi-deterministic evaluation (same code, same hyperparameters, same hardware should",
        "produce identical results within floating-point precision).",
        "",
        "## Load-Bearing Metrics",
        "",
        "Compared metrics:",
        "- `in_distribution_accuracy`: Exact match on in-distribution test set",
        "- `pattern_*`: Accuracy per adversarial family (alternating_carry, full_propagation_chain, block_boundary_stress)",
        "- `mean_adversarial_accuracy`: Average accuracy across all adversarial families",
        "",
    ])
    
    # Write report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    
    print(f"\n✓ Report saved to: {REPORT_PATH}")
    print(f"\n{'=' * 80}")
    print(f"Overall: {'✅ ALL PASS' if all_pass else '❌ SOME FAILED'}")
    print("=" * 80 + "\n")
    
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
