#!/usr/bin/env python3
"""
validate_claims_p11.py

Evaluates re-validation artifacts against pre-registered targets from FORMAL_CLAIMS.md.
Produces a comprehensive validation report.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Re-validation artifact paths
REPRO_PHASE_D = Path("project_12/results/repro/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json")
REVALIDATE_PHASE_D = Path("project_12/results/revalidate/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json")
REPRO_PHASE_E2 = Path("project_12/results/repro/phase_e2/artifact.json")
REVALIDATE_PHASE_E2 = Path("project_12/results/revalidate/phase_e2/artifact.json")
REPRO_PHASE_E3 = Path("project_12/results/repro/phase_e3/artifact.json")
REVALIDATE_PHASE_E3 = Path("project_12/results/revalidate/phase_e3/artifact.json")

def load_json(path: Path) -> Dict:
    """Load JSON from path."""
    if not path.exists():
        raise FileNotFoundError(f"Missing: {path}")
    with open(path) as f:
        return json.load(f)

def mean(xs: List[float]) -> float:
    """Compute mean."""
    return sum(xs) / max(1, len(xs)) if xs else 0.0

def validate_claims() -> Tuple[Dict[str, Any], str]:
    """
    Validate claims against re-validation results.
    Returns (results_dict, markdown_report)
    """
    results = {}
    lines = []
    
    lines.append("# P11_VALIDATION_REPORT_REVALIDATE.md")
    lines.append("")
    lines.append("## Summary")
    lines.append("Re-validation of Project 11 claims using independent holdout, pool, and seeds.")
    lines.append("")
    
    # ====== CLAIM P11-C01 (Phase D) ======
    lines.append("---")
    lines.append("## Claim P11-C01: Soft clamp performance")
    lines.append("")
    
    try:
        d_repro = load_json(REVALIDATE_PHASE_D)
        c01_results = {}
        
        # Extract V3.1 and V3 macroF1_present
        v31_overall = d_repro["rules"]["V3.1"]["overall"]["macro_f1_present"]
        v3_overall = d_repro["rules"]["V3"]["overall"]["macro_f1_present"]
        gap = v31_overall - v3_overall
        
        c01_results["V3.1_overall"] = v31_overall
        c01_results["V3_overall"] = v3_overall
        c01_results["gap"] = gap
        
        # Validation targets
        target_v31 = 0.93
        target_gap = 0.07
        
        pass_v31 = v31_overall >= target_v31
        pass_gap = gap >= target_gap
        c01_pass = pass_v31 and pass_gap
        
        lines.append("**Observed:**")
        lines.append(f"- V3.1 macroF1_present: {v31_overall:.6f}")
        lines.append(f"- V3 macroF1_present: {v3_overall:.6f}")
        lines.append(f"- Gap (V3.1 − V3): {gap:.6f}")
        lines.append("")
        lines.append("**Targets:**")
        lines.append(f"- V3.1 ≥ {target_v31}: {'✅ PASS' if pass_v31 else '❌ FAIL'}")
        lines.append(f"- Gap ≥ {target_gap}: {'✅ PASS' if pass_gap else '❌ FAIL'}")
        lines.append("")
        lines.append(f"**Status:** {'✅ PASS' if c01_pass else '❌ FAIL'}")
        
        c01_results["pass"] = c01_pass
        results["P11-C01"] = c01_results
        
    except Exception as e:
        lines.append(f"**ERROR:** {e}")
        c01_results["pass"] = False
        results["P11-C01"] = c01_results
    
    # ====== CLAIM P11-C02 (Phase D) ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C02: NN resolution monotonicity")
    lines.append("")
    
    try:
        d_repro = load_json(REVALIDATE_PHASE_D)
        c02_results = {}
        
        # Extract NN performance
        nn_f1 = {}
        for n in [11, 21, 41, 81]:
            f1 = d_repro["nn"][f"NN{n}"]["overall"]["macro_f1_present"]
            nn_f1[n] = f1
        
        c02_results["nn_f1"] = nn_f1
        
        # Validation targets
        target_nn81 = 0.97
        pass_nn81 = nn_f1[81] >= target_nn81
        
        # Check monotonicity
        monotonic = (nn_f1[11] <= nn_f1[21] <= nn_f1[41] <= nn_f1[81])
        pass_monotonic = monotonic
        
        c02_pass = pass_nn81 and pass_monotonic
        
        lines.append("**Observed:**")
        for n in [11, 21, 41, 81]:
            lines.append(f"- NN{n} macroF1_present: {nn_f1[n]:.6f}")
        lines.append("")
        lines.append("**Targets:**")
        lines.append(f"- NN81 ≥ {target_nn81}: {'✅ PASS' if pass_nn81 else '❌ FAIL'}")
        lines.append(f"- Monotonicity (11→21→41→81): {'✅ PASS' if pass_monotonic else '❌ FAIL'}")
        lines.append("")
        lines.append(f"**Status:** {'✅ PASS' if c02_pass else '❌ FAIL'}")
        
        c02_results["pass"] = c02_pass
        results["P11-C02"] = c02_results
        
    except Exception as e:
        lines.append(f"**ERROR:** {e}")
        c02_results["pass"] = False
        results["P11-C02"] = c02_results
    
    # ====== CLAIM P11-C03 (Phase E2) ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C03: Boundary-only poor, mixed necessary")
    lines.append("")
    
    try:
        e2_revalidate = load_json(REVALIDATE_PHASE_E2)
        c03_results = {}
        
        # Extract @ N=1000
        rows = e2_revalidate["rows"]
        boundary_1000 = [r["macro_f1_present"] for r in rows if r["N"] == 1000 and r["strategy"] == "boundary"]
        uniform_1000 = [r["macro_f1_present"] for r in rows if r["N"] == 1000 and r["strategy"] == "uniform"]
        mixed_1000 = [r["macro_f1_present"] for r in rows if r["N"] == 1000 and r["strategy"] == "mixed"]
        
        boundary_mean = mean(boundary_1000)
        uniform_mean = mean(uniform_1000)
        mixed_mean = mean(mixed_1000)
        boundary_mixed_gap = mixed_mean - boundary_mean
        
        c03_results["boundary_mean"] = boundary_mean
        c03_results["uniform_mean"] = uniform_mean
        c03_results["mixed_mean"] = mixed_mean
        c03_results["seeds"] = len(boundary_1000)
        
        # Targets
        target_boundary = 0.80
        target_mixed = 0.97
        target_uniform = 0.94
        target_gap = 0.15
        
        pass_boundary = boundary_mean <= target_boundary
        pass_mixed = mixed_mean >= target_mixed
        pass_uniform = uniform_mean >= target_uniform
        pass_gap = boundary_mixed_gap >= target_gap
        
        c03_pass = pass_boundary and pass_mixed and pass_uniform and pass_gap
        
        lines.append("**Observed (N=1000, mean over seeds):**")
        lines.append(f"- Boundary-only: {boundary_mean:.6f} (n={len(boundary_1000)} seeds)")
        lines.append(f"- Uniform: {uniform_mean:.6f}")
        lines.append(f"- Mixed: {mixed_mean:.6f}")
        lines.append(f"- Gap (mixed − boundary): {boundary_mixed_gap:.6f}")
        lines.append("")
        lines.append("**Targets:**")
        lines.append(f"- Boundary ≤ {target_boundary}: {'✅ PASS' if pass_boundary else '❌ FAIL'}")
        lines.append(f"- Mixed ≥ {target_mixed}: {'✅ PASS' if pass_mixed else '❌ FAIL'}")
        lines.append(f"- Uniform ≥ {target_uniform}: {'✅ PASS' if pass_uniform else '❌ FAIL'}")
        lines.append(f"- Gap ≥ {target_gap}: {'✅ PASS' if pass_gap else '❌ FAIL'}")
        lines.append("")
        lines.append(f"**Status:** {'✅ PASS' if c03_pass else '❌ FAIL'}")
        
        c03_results["pass"] = c03_pass
        results["P11-C03"] = c03_results
        
    except Exception as e:
        lines.append(f"**ERROR:** {e}")
        c03_results["pass"] = False
        results["P11-C03"] = c03_results
    
    # ====== CLAIM P11-C04 (Phase E2) ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C04: Mixed sampling efficiency (flagship)")
    lines.append("")
    
    try:
        e2_revalidate = load_json(REVALIDATE_PHASE_E2)
        c04_results = {}
        
        rows = e2_revalidate["rows"]
        mixed_1000 = [r["macro_f1_present"] for r in rows if r["N"] == 1000 and r["strategy"] == "mixed"]
        mixed_mean = mean(mixed_1000)
        
        # NN81 baseline
        nn81_f1 = e2_revalidate["nn81"]["macro_f1_present"]
        
        gap = nn81_f1 - mixed_mean
        cost_ratio = 1000.0 / 6561.0
        
        c04_results["mixed"] = mixed_mean
        c04_results["nn81"] = nn81_f1
        c04_results["gap"] = gap
        c04_results["cost_ratio"] = cost_ratio
        
        # Targets
        target_mixed = 0.97
        target_nn81 = 0.97
        target_gap = 0.02
        target_cost = 0.20
        
        pass_mixed = mixed_mean >= target_mixed
        pass_nn81 = nn81_f1 >= target_nn81
        pass_gap = gap <= target_gap
        pass_cost = cost_ratio <= target_cost
        
        c04_pass = pass_mixed and pass_nn81 and pass_gap and pass_cost
        
        lines.append("**Observed:**")
        lines.append(f"- Mixed @ N=1000: {mixed_mean:.6f}")
        lines.append(f"- NN81 baseline: {nn81_f1:.6f}")
        lines.append(f"- Performance gap: {gap:.6f}")
        lines.append(f"- Cost ratio (1000/6561): {cost_ratio:.4f}")
        lines.append("")
        lines.append("**Targets:**")
        lines.append(f"- Mixed ≥ {target_mixed}: {'✅ PASS' if pass_mixed else '❌ FAIL'}")
        lines.append(f"- NN81 ≥ {target_nn81}: {'✅ PASS' if pass_nn81 else '❌ FAIL'}")
        lines.append(f"- Gap ≤ {target_gap}: {'✅ PASS' if pass_gap else '❌ FAIL'}")
        lines.append(f"- Cost ratio ≤ {target_cost}: {'✅ PASS' if pass_cost else '❌ FAIL'}")
        lines.append("")
        lines.append(f"**Status:** {'✅ PASS' if c04_pass else '❌ FAIL'}")
        
        c04_results["pass"] = c04_pass
        results["P11-C04"] = c04_results
        
    except Exception as e:
        lines.append(f"**ERROR:** {e}")
        c04_results["pass"] = False
        results["P11-C04"] = c04_results
    
    # ====== CLAIM P11-C05 (Phase E3) ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C05: kNN with balanced frac competitive")
    lines.append("")
    
    try:
        e3_revalidate = load_json(REVALIDATE_PHASE_E3)
        c05_results = {}
        
        rows = e3_revalidate["rows"]
        
        # Best config: 1500, frac=0.5, 1-NN
        best_1nn = [r["nn1"]["f1"] for r in rows if r["N"] == 1500 and r["uniform_frac"] == 0.5]
        best_1nn_mean = mean(best_1nn)
        
        # Same config 3-NN
        best_3nn = [r["nn3"]["f1"] for r in rows if r["N"] == 1500 and r["uniform_frac"] == 0.5]
        best_3nn_mean = mean(best_3nn)
        
        knn_gap = best_1nn_mean - best_3nn_mean
        
        # Check all fracs at N=1500
        frac_f1_1nn = {}
        for frac in [0.2, 0.5, 0.8]:
            vals = [r["nn1"]["f1"] for r in rows if r["N"] == 1500 and r["uniform_frac"] == frac]
            frac_f1_1nn[frac] = mean(vals)
        
        best_frac_f1 = max(frac_f1_1nn.values())
        frac_range = [abs(v - best_frac_f1) for v in frac_f1_1nn.values()]
        frac_within_01 = all(d <= 0.01 for d in frac_range)
        
        c05_results["best_1nn"] = best_1nn_mean
        c05_results["best_3nn"] = best_3nn_mean
        c05_results["knn_gap"] = knn_gap
        c05_results["frac_f1"] = frac_f1_1nn
        
        # Targets
        target_best = 0.97
        target_knn_gap = 0.005
        
        pass_best = best_1nn_mean >= target_best
        pass_knn_gap = knn_gap >= target_knn_gap
        pass_frac = frac_within_01
        
        c05_pass = pass_best and pass_knn_gap and pass_frac
        
        lines.append("**Observed:**")
        lines.append(f"- Best config (N=1500, frac=0.5, k=1): {best_1nn_mean:.6f}")
        lines.append(f"- Same config 3-NN: {best_3nn_mean:.6f}")
        lines.append(f"- kNN gap (1-NN − 3-NN): {knn_gap:.6f}")
        lines.append(f"- Frac performance @ N=1500 (1-NN):")
        for frac, f1 in frac_f1_1nn.items():
            lines.append(f"  - frac={frac}: {f1:.6f}")
        lines.append("")
        lines.append("**Targets:**")
        lines.append(f"- Best config ≥ {target_best}: {'✅ PASS' if pass_best else '❌ FAIL'}")
        lines.append(f"- kNN gap ≥ {target_knn_gap}: {'✅ PASS' if pass_knn_gap else '❌ FAIL'}")
        lines.append(f"- All fracs within 0.01 of best: {'✅ PASS' if pass_frac else '❌ FAIL'}")
        lines.append("")
        lines.append(f"**Status:** {'✅ PASS' if c05_pass else '❌ FAIL'}")
        
        c05_results["pass"] = c05_pass
        results["P11-C05"] = c05_results
        
    except Exception as e:
        lines.append(f"**ERROR:** {e}")
        c05_results["pass"] = False
        results["P11-C05"] = c05_results
    
    # ====== SUMMARY ======
    lines.append("")
    lines.append("---")
    lines.append("## Summary Table")
    lines.append("")
    lines.append("| Claim | Type | Status |")
    lines.append("|-------|------|--------|")
    
    for claim_id in ["P11-C01", "P11-C02", "P11-C03", "P11-C04", "P11-C05"]:
        if claim_id in results:
            status = "✅ PASS" if results[claim_id].get("pass") else "❌ FAIL"
            lines.append(f"| {claim_id} | strong/medium | {status} |")
    
    lines.append("")
    lines.append("**Report generated:** Sprint 2C re-validation completion")
    
    return results, "\n".join(lines)

def main():
    results, report = validate_claims()
    
    # Write report
    report_path = Path("project_12/reports/P11_VALIDATION_REPORT_REVALIDATE.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    
    print(report)
    print(f"\n✅ Report written to: {report_path}")

if __name__ == "__main__":
    main()
