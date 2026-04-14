#!/usr/bin/env python3
"""
run_c07_sensitivity_sweep.py

Executes C07 boundary sensitivity sweep:
- Generates 20 holdouts with different seeds (100001-100020)
- Runs Phase D on each
- Extracts boundary metrics (V3, V3.1, NN81)
- Computes statistics and generates report
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List
import numpy as np
import csv

def load_manifest(manifest_path: Path) -> Dict:
    """Load sweep manifest."""
    with open(manifest_path, 'r') as f:
        return json.load(f)

def run_command(cmd: List[str], description: str) -> bool:
    """Run command and return success status."""
    try:
        print(f"  → {description}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"    ❌ FAILED (exit code {result.returncode})")
            print(f"    stderr: {result.stderr[:500]}")
            return False
        print(f"    ✅ Done")
        return True
    except subprocess.TimeoutExpired:
        print(f"    ❌ TIMEOUT")
        return False
    except Exception as e:
        print(f"    ❌ ERROR: {e}")
        return False

def extract_boundary_metrics(artifact_path: Path) -> Dict:
    """Extract boundary metrics from Phase D artifact."""
    try:
        with open(artifact_path, 'r') as f:
            artifact = json.load(f)
        
        # Extract boundary-specific metrics
        v3_boundary = artifact["rules"]["V3"]["boundary"]["macro_f1_present"]
        v31_boundary = artifact["rules"]["V3.1"]["boundary"]["macro_f1_present"]
        nn81_boundary = artifact["nn"]["NN81"]["boundary"]["macro_f1_present"]
        
        return {
            "v3_boundary": v3_boundary,
            "v31_boundary": v31_boundary,
            "nn81_boundary": nn81_boundary,
            "improvement_v31_v3": v31_boundary - v3_boundary,
            "gap_nn81_v31": nn81_boundary - v31_boundary,
        }
    except Exception as e:
        print(f"      ERROR extracting metrics: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="C07 boundary sensitivity sweep")
    parser.add_argument("--manifest", required=True, help="Sweep manifest path")
    args = parser.parse_args()
    
    manifest_path = Path(args.manifest)
    manifest = load_manifest(manifest_path)
    
    project_root = Path(__file__).parent.parent.parent
    manifest["output_root"] = str(project_root / manifest["output_root"])
    
    output_root = Path(manifest["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)
    
    summary_dir = output_root / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    
    seeds = manifest["holdout_seeds"]
    results = []
    
    print(f"\n{'='*70}")
    print(f"C07 BOUNDARY SENSITIVITY SWEEP")
    print(f"{'='*70}")
    print(f"Seeds: {len(seeds)} ({seeds[0]}-{seeds[-1]})")
    print(f"Output: {output_root}")
    print(f"\n")
    
    successful = 0
    failed = 0
    
    for i, seed in enumerate(seeds, 1):
        seed_dir = output_root / f"phase_d/seed_{seed}"
        seed_dir.mkdir(parents=True, exist_ok=True)
        
        holdout_file = output_root / f"tmp_holdouts/seed_{seed}/holdout_points.json"
        
        print(f"[{i}/{len(seeds)}] Seed {seed}:")
        
        # 1. Generate holdout
        holdout_manifest = {
            "description": f"Holdout for sweep seed {seed}",
            "fixed_params": {
                "holdout_seed": seed,  # ← Correct location for generator script
                "holdout_size": 800,
                "h_min": manifest["holdout_config"]["h_range"][0],
                "h_max": manifest["holdout_config"]["h_range"][1],
                "p_min": manifest["holdout_config"]["p_range"][0],
                "p_max": manifest["holdout_config"]["p_range"][1],
                "boundary_pool": 90000
            },
            "output_dir": str(holdout_file.parent)
        }
        
        holdout_manifest_path = output_root / f"tmp_manifests/seed_{seed}_holdout.json"
        holdout_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(holdout_manifest_path, 'w') as f:
            json.dump(holdout_manifest, f, indent=2)
        
        cmd_holdout = [
            sys.executable,
            str(project_root / manifest["holdout_entrypoint"]),
            "--manifest", str(holdout_manifest_path)
        ]
        if not run_command(cmd_holdout, f"Generate holdout"):
            failed += 1
            continue
        
        # 2. Run Phase D
        phase_d_manifest = {
            "description": f"Phase D for C07 sweep seed {seed}",
            "fixed_params": {
                "holdout_path": str(holdout_file)
            },
            "output_dir": str(seed_dir)
        }
        
        phase_d_manifest_path = output_root / f"tmp_manifests/seed_{seed}_phase_d.json"
        with open(phase_d_manifest_path, 'w') as f:
            json.dump(phase_d_manifest, f, indent=2)
        
        cmd_phase_d = [
            sys.executable,
            str(project_root / manifest["phase_d_entrypoint"]),
            "--manifest", str(phase_d_manifest_path)
        ]
        if not run_command(cmd_phase_d, f"Phase D"):
            failed += 1
            continue
        
        # 3. Extract metrics
        artifact_path = seed_dir / "RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json"
        if not artifact_path.exists():
            print(f"    ❌ Artifact not found: {artifact_path}")
            failed += 1
            continue
        
        metrics = extract_boundary_metrics(artifact_path)
        if not metrics:
            failed += 1
            continue
        
        result = {
            "seed": seed,
            **metrics
        }
        results.append(result)
        successful += 1
        
        print(f"    → V3.1_boundary: {metrics['v31_boundary']:.6f} | NN81_boundary: {metrics['nn81_boundary']:.6f} | Improvement: {metrics['improvement_v31_v3']:.6f}")
    
    print(f"\n{'='*70}")
    print(f"SUMMARY: {successful} succeeded, {failed} failed")
    print(f"{'='*70}\n")
    
    if not results:
        print("ERROR: No successful results!")
        return
    
    # Compute statistics
    v31_bounds = [r["v31_boundary"] for r in results]
    improvements = [r["improvement_v31_v3"] for r in results]
    gaps_nn81 = [r["gap_nn81_v31"] for r in results]
    
    stats = {
        "v31_boundary": {
            "mean": float(np.mean(v31_bounds)),
            "std": float(np.std(v31_bounds)),
            "min": float(np.min(v31_bounds)),
            "p5": float(np.percentile(v31_bounds, 5)),
            "p50": float(np.percentile(v31_bounds, 50)),
            "p95": float(np.percentile(v31_bounds, 95)),
            "max": float(np.max(v31_bounds)),
        },
        "improvement_v31_v3": {
            "mean": float(np.mean(improvements)),
            "std": float(np.std(improvements)),
            "all_pass_01": sum(1 for x in improvements if x >= 0.15) == len(improvements),
        },
        "gap_nn81_v31": {
            "mean": float(np.mean(gaps_nn81)),
            "std": float(np.std(gaps_nn81)),
            "all_pass_01": sum(1 for x in gaps_nn81 if x <= 0.10) == len(gaps_nn81),
        },
        "pass_rate_threshold": {
            "0.80": sum(1 for x in v31_bounds if x >= 0.80) / len(v31_bounds),
            "0.85": sum(1 for x in v31_bounds if x >= 0.85) / len(v31_bounds),
            "0.90": sum(1 for x in v31_bounds if x >= 0.90) / len(v31_bounds),
        }
    }
    
    # Write CSV
    csv_path = summary_dir / "per_seed_metrics.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        for r in results:
            writer.writerow(r)
    
    # Write JSON stats
    json_path = summary_dir / "statistics.json"
    with open(json_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    # Generate markdown report
    report_path = Path(project_root / "project_12" / "reports" / "C07_SENSITIVITY_SWEEP_REPORT.md")
    report_lines = []
    report_lines.append("# C07 Boundary Sensitivity Sweep Report")
    report_lines.append("")
    report_lines.append(f"**Experiment ID:** {manifest['experiment_id']}")
    report_lines.append(f"**Seeds tested:** {len(seeds)} seeds (100001–100020)")
    report_lines.append(f"**Successful runs:** {successful}/{len(seeds)}")
    report_lines.append("")
    report_lines.append("## Results Summary")
    report_lines.append("")
    report_lines.append("### V3.1 Boundary macroF1_present Distribution")
    report_lines.append("")
    report_lines.append(f"| Statistic | Value |")
    report_lines.append(f"|-----------|-------|")
    report_lines.append(f"| Mean | {stats['v31_boundary']['mean']:.6f} |")
    report_lines.append(f"| Std Dev | {stats['v31_boundary']['std']:.6f} |")
    report_lines.append(f"| Min | {stats['v31_boundary']['min']:.6f} |")
    report_lines.append(f"| 5th percentile | {stats['v31_boundary']['p5']:.6f} |")
    report_lines.append(f"| Median (50th) | {stats['v31_boundary']['p50']:.6f} |")
    report_lines.append(f"| 95th percentile | {stats['v31_boundary']['p95']:.6f} |")
    report_lines.append(f"| Max | {stats['v31_boundary']['max']:.6f} |")
    report_lines.append("")
    
    report_lines.append("### Pass Rate vs Thresholds")
    report_lines.append("")
    report_lines.append(f"| Threshold | Pass Rate | Count |")
    report_lines.append(f"|-----------|-----------|-------|")
    for thresh in ["0.80", "0.85", "0.90"]:
        rate = stats['pass_rate_threshold'][thresh]
        count = int(rate * len(v31_bounds))
        report_lines.append(f"| ≥ {thresh} | {rate*100:.1f}% | {count}/{len(v31_bounds)} |")
    report_lines.append("")
    
    report_lines.append("### Mechanism Conditions")
    report_lines.append("")
    report_lines.append(f"**Improvement (V3.1 − V3) ≥ 0.15:**")
    report_lines.append(f"- Mean: {stats['improvement_v31_v3']['mean']:.6f}")
    report_lines.append(f"- All seeds pass: {'✅ YES' if stats['improvement_v31_v3']['all_pass_01'] else '❌ NO'}")
    report_lines.append("")
    report_lines.append(f"**Closeness to NN81 (NN81 − V3.1) ≤ 0.10:**")
    report_lines.append(f"- Mean gap: {stats['gap_nn81_v31']['mean']:.6f}")
    report_lines.append(f"- All seeds pass: {'✅ YES' if stats['gap_nn81_v31']['all_pass_01'] else '❌ NO'}")
    report_lines.append("")
    
    report_lines.append("## Interpretation (for C07 Revision)")
    report_lines.append("")
    report_lines.append(f"1. **Absolute threshold 0.85:** Only {stats['pass_rate_threshold']['0.85']*100:.1f}% of seeds pass")
    report_lines.append(f"2. **Absolute threshold 0.80:** {stats['pass_rate_threshold']['0.80']*100:.1f}% of seeds pass")
    report_lines.append(f"3. **Mechanism conditions:** Improvement and NN81-closeness are {'ROBUST' if (stats['improvement_v31_v3']['all_pass_01'] and stats['gap_nn81_v31']['all_pass_01']) else 'NOT ROBUST'}")
    report_lines.append("")
    
    report_lines.append("## Recommendation")
    report_lines.append("")
    if stats['improvement_v31_v3']['all_pass_01'] and stats['gap_nn81_v31']['all_pass_01']:
        report_lines.append("✅ **Mechanism is robust:** Soft clamp reliably improves boundary and stays near NN81.")
        report_lines.append("")
        report_lines.append(f"**Option A (Mechanism-based revision):** Remove absolute threshold 0.85; keep only:")
        report_lines.append(f"- (V3.1_boundary − V3_boundary) ≥ 0.15")
        report_lines.append(f"- (NN81_boundary − V3.1_boundary) ≤ 0.10")
        report_lines.append("")
        report_lines.append(f"**Option B (Data-driven threshold):** Propose new absolute target based on percentiles:")
        report_lines.append(f"- P50 = {stats['v31_boundary']['p50']:.4f} (median)")
        report_lines.append(f"- P5 = {stats['v31_boundary']['p5']:.4f} (conservative lower bound)")
    else:
        report_lines.append("❌ **Mechanism not robust:** Conditions fail in some seeds.")
    
    report_lines.append("")
    report_lines.append("## Artifacts")
    report_lines.append(f"- Per-seed metrics (CSV): `project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv`")
    report_lines.append(f"- Statistics (JSON): `project_12/results/sweep_c07_v1/summary/statistics.json`")
    report_lines.append(f"- Phase D artifacts: `project_12/results/sweep_c07_v1/phase_d/seed_*/`")
    
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        f.write("\n".join(report_lines))
    
    print(f"\n✅ Report written: {report_path}")
    print(f"✅ CSV written: {csv_path}")
    print(f"✅ Statistics written: {json_path}")

if __name__ == "__main__":
    main()
