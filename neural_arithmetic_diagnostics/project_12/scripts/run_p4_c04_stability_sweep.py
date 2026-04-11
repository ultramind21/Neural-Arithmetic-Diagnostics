"""
================================================================================
SPRINT 4F — P4-C04 STABILITY MINI-SWEEP (3 SEEDS)
================================================================================

PURPOSE:
  Demonstrate P4-C04 (narrow transfer) pass-rate across 3 different seeds.
  All runs use same manifest-driven setup (only seed varies).

OUTPUT:
  - project_12/reports/P4_C04_STABILITY_SWEEP_RESULTS.csv
  - project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md

================================================================================
"""

import subprocess
import json
import csv
from pathlib import Path
from datetime import datetime


def run_training(manifest_path: str) -> bool:
    """Run adversarial training with given manifest. Return True if success."""
    print(f"\n{'='*80}")
    print(f"Running training: {manifest_path}")
    print(f"{'='*80}")
    
    cmd = [
        "python",
        "project_12/scripts/p4/run_p4_adversarial_training_repro.py",
        "--manifest", manifest_path,
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_policy_check(artifact_path: str) -> tuple[bool, dict]:
    """
    Run policy check on artifact. Return (success, metrics_dict).
    """
    print(f"Running policy check: {artifact_path}")
    
    cmd = [
        "python",
        "project_12/scripts/repro_check_project4_intervention.py",
        "--artifact", artifact_path,
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    success = result.returncode == 0
    
    # Extract metrics from artifact JSON
    metrics = {}
    if Path(artifact_path).exists():
        try:
            with open(artifact_path, "r") as f:
                artifact = json.load(f)
                gains = artifact.get("computed_gains", {})
                metrics = {
                    "seen_gain": float(gains.get("seen_gain", 0.0)),
                    "heldout_gain": float(gains.get("heldout_gain", 0.0)),
                    "gap": float(gains.get("gap", 0.0)),
                }
        except Exception as e:
            print(f"⚠️  Could not parse artifact metrics: {e}")
    
    return success, metrics


def main():
    print("\n" + "="*80)
    print("SPRINT 4F — P4-C04 STABILITY MINI-SWEEP")
    print("="*80)
    
    manifests = [
        ("seed_42", "project_12/manifests/p4_adversarial_training_sweep_seed_42.json"),
        ("seed_123", "project_12/manifests/p4_adversarial_training_sweep_seed_123.json"),
        ("seed_456", "project_12/manifests/p4_adversarial_training_sweep_seed_456.json"),
    ]
    
    results = []
    
    for seed_label, manifest_path in manifests:
        print(f"\n{'#'*80}")
        print(f"# {seed_label.upper()}")
        print(f"{'#'*80}")
        
        # Run training
        training_ok = run_training(manifest_path)
        if not training_ok:
            print(f"❌ Training failed for {seed_label}")
            results.append({
                "seed_label": seed_label,
                "seed": seed_label.split("_")[1],
                "training_ok": False,
                "policy_check_ok": False,
                "status": "FAIL",
                "seen_gain": None,
                "heldout_gain": None,
                "gap": None,
            })
            continue
        
        # Extract manifest to find output_dir
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
        output_dir = manifest.get("output_dir")
        artifact_path = str(Path(output_dir) / "artifact.json")
        
        # Run policy check
        policy_ok, metrics = run_policy_check(artifact_path)
        
        results.append({
            "seed_label": seed_label,
            "seed": seed_label.split("_")[1],
            "training_ok": training_ok,
            "policy_check_ok": policy_ok,
            "status": "PASS" if policy_ok else "FAIL",
            "seen_gain": metrics.get("seen_gain"),
            "heldout_gain": metrics.get("heldout_gain"),
            "gap": metrics.get("gap"),
        })
    
    # Write CSV
    csv_path = Path("project_12/reports/P4_C04_STABILITY_SWEEP_RESULTS.csv")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(csv_path, "w", newline="") as f:
        fieldnames = ["seed", "status", "seen_gain", "heldout_gain", "gap"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({
                "seed": r["seed"],
                "status": r["status"],
                "seen_gain": r["seen_gain"],
                "heldout_gain": r["heldout_gain"],
                "gap": r["gap"],
            })
    
    print(f"\n✅ CSV results: {csv_path}")
    
    # Write markdown report
    md_path = Path("project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md")
    md_lines = [
        "# P4-C04 Stability Mini-Sweep Report",
        "",
        f"**Date:** {datetime.utcnow().isoformat()}Z",
        "**Purpose:** Demonstrate P4-C04 (narrow transfer) pass-rate across 3 seeds.",
        "",
        "## Summary",
        "",
    ]
    
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    md_lines.append(f"- **Pass rate:** {pass_count}/{len(results)} runs")
    md_lines.append(f"- **Overall:** {'✅ ALL PASS' if pass_count == len(results) else '⚠️ SOME FAILED'}")
    md_lines.append("")
    md_lines.append("## Per-Seed Results")
    md_lines.append("")
    md_lines.append("| Seed | Status | Seen Gain | Heldout Gain | Gap |")
    md_lines.append("|------|--------|-----------|--------------|-----|")
    
    for r in results:
        seed = r["seed"]
        status = r["status"]
        seen = f"{r['seen_gain']:.3f}" if r["seen_gain"] is not None else "N/A"
        heldout = f"{r['heldout_gain']:.3f}" if r["heldout_gain"] is not None else "N/A"
        gap = f"{r['gap']:.3f}" if r["gap"] is not None else "N/A"
        md_lines.append(f"| {seed} | {status} | {seen} | {heldout} | {gap} |")
    
    md_lines.append("")
    md_lines.append("## Interpretation")
    
    if pass_count == len(results):
        md_lines.append("")
        md_lines.append("✅ **All seeds pass P4-C04 policy criteria.**")
        md_lines.append("")
        md_lines.append("This demonstrates that narrow transfer (seen improvement >> held-out degradation)")
        md_lines.append("is stable across different random seeds under identical manifest configuration.")
    else:
        md_lines.append("")
        md_lines.append(f"⚠️ **{pass_count}/{len(results)} seeds pass. Some variance present.**")
        md_lines.append("")
        md_lines.append("Not all random seeds maintain same ordering/gap criteria,")
        md_lines.append("suggesting potential seed sensitivity.")
    
    md_lines.append("")
    md_lines.append("## Methodology Notes")
    md_lines.append("")
    md_lines.append("- Same manifest-driven setup for all seeds (only `seed` field varies)")
    md_lines.append("- Policy check: gap ≥ 0.10 AND seen_gain > heldout_gain")
    md_lines.append("- Non-deterministic training acceptable (policy-based validation)")
    md_lines.append("- No comparison to Project 4 historical values")
    
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    
    print(f"✅ Markdown report: {md_path}")
    
    print(f"\n{'='*80}")
    print(f"SPRINT 4F COMPLETE")
    print(f"{'='*80}")
    print(f"Pass rate: {pass_count}/{len(results)}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
