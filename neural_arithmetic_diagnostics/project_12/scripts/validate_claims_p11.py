#!/usr/bin/env python3
"""
validate_claims_p11.py (Updated for Sprint 2C.1)

Evaluates procedure-preserving re-validation artifacts against pre-registered targets.
NOW COVERS C01-C08 (complete claim validation).

Supports:
- --root: root directory for artifacts (e.g., project_12/results/revalidate_p11proc/)
- Computes mean ± std for E2/E3 rows
"""

import argparse
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Any


def load_json(path: Path) -> Dict:
    """Load JSON from path."""
    if not path.exists():
        raise FileNotFoundError(f"Missing: {path}")
    with open(path) as f:
        return json.load(f)

def mean(xs: List[float]) -> float:
    """Compute mean."""
    return sum(xs) / max(1, len(xs)) if xs else 0.0


def std(xs: List[float]) -> float:
    """Compute standard deviation."""
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    var = sum((x - m) ** 2 for x in xs) / len(xs)
    return math.sqrt(var)

def validate_claims(root_dir: Path) -> str:
    """
    Validate claims against re-validation artifacts.
    Returns markdown report string.
    """
    
    # Construct artifact paths from root_dir
    PHASE_D = root_dir / "phase_d" / "RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json"
    PHASE_E2 = root_dir / "phase_e2" / "artifact.json"
    PHASE_E3 = root_dir / "phase_e3" / "artifact.json"
    
    lines = []
    lines.append("# P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md")
    lines.append("")
    lines.append("## Summary")
    lines.append("Procedure-Preserving Re-validation of Project 11 Claims (Sprint 2C.1)")
    lines.append("")
    lines.append("**Key Design:**")
    lines.append("- Holdout: Generated with Project 11 Phase C3 procedure (seed=424242)")
    lines.append("- Pool: Internal RNG-based (Project 11 procedure, no external file)")
    lines.append("- Seeds: Independent from Project 11")
    lines.append("- Statistics: Mean ± Std for E2/E3 rows")
    lines.append("")
    
    results = {}
    
    # ====== CLAIM P11-C01 (Phase D) ======
    lines.append("---")
    lines.append("## Claim P11-C01: Soft clamp performance")
    lines.append("")
    
    try:
        d_artifact = load_json(PHASE_D)
        c01_results = {}
        
        # Extract V3.1 and V3 macroF1_present
        v31_overall = d_artifact["rules"]["V3.1"]["overall"]["macro_f1_present"]
        v3_overall = d_artifact["rules"]["V3"]["overall"]["macro_f1_present"]
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
    
    # ====== CLAIM P11-C02: NN resolution monotonicity ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C02: NN resolution monotonicity (Type: STRONG)")
    lines.append("")
    
    try:
        d_artifact = load_json(PHASE_D)
        c02_results = {}
        
        # Extract NN performance
        nn_f1 = {}
        for n in [11, 21, 41, 81]:
            f1 = d_artifact["nn"][f"NN{n}"]["overall"]["macro_f1_present"]
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
    
    # ====== CLAIM P11-C03: Boundary-only poor, mixed necessary ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C03: Boundary-only poor, mixed necessary (Type: STRONG)")
    lines.append("")
    
    try:
        e2_artifact = load_json(PHASE_E2)
        c03_results = {}
        
        # Extract @ N=1000
        rows = e2_artifact["rows"]
        boundary_1000 = [r["macro_f1_present"] for r in rows if r["N"] == 1000 and r["strategy"] == "boundary"]
        uniform_1000 = [r["macro_f1_present"] for r in rows if r["N"] == 1000 and r["strategy"] == "uniform"]
        mixed_1000 = [r["macro_f1_present"] for r in rows if r["N"] == 1000 and r["strategy"] == "mixed"]
        
        boundary_mean = mean(boundary_1000)
        boundary_std = std(boundary_1000)
        uniform_mean = mean(uniform_1000)
        mixed_mean = mean(mixed_1000)
        mixed_std = std(mixed_1000)
        boundary_mixed_gap = mixed_mean - boundary_mean
        
        c03_results["boundary_mean"] = boundary_mean
        c03_results["boundary_std"] = boundary_std
        c03_results["uniform_mean"] = uniform_mean
        c03_results["mixed_mean"] = mixed_mean
        c03_results["mixed_std"] = mixed_std
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
        
        lines.append("**Observed (N=1000, mean ± std over seeds):**")
        lines.append(f"- Boundary-only: {boundary_mean:.6f} ± {boundary_std:.6f} (n={len(boundary_1000)} seeds)")
        lines.append(f"- Uniform: {uniform_mean:.6f}")
        lines.append(f"- Mixed: {mixed_mean:.6f} ± {mixed_std:.6f}")
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
    
    # ====== CLAIM P11-C04: Mixed sampling efficiency ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C04: Mixed sampling efficiency (flagship) (Type: STRONG)")
    lines.append("")
    
    try:
        e2_artifact = load_json(PHASE_E2)
        c04_results = {}
        
        rows = e2_artifact["rows"]
        mixed_1000 = [r["macro_f1_present"] for r in rows if r["N"] == 1000 and r["strategy"] == "mixed"]
        mixed_mean = mean(mixed_1000)
        mixed_std = std(mixed_1000)
        
        # NN81 baseline
        nn81_f1 = e2_artifact["nn81"]["macro_f1_present"]
        
        gap = nn81_f1 - mixed_mean
        cost_ratio = 1000.0 / 6561.0
        
        c04_results["mixed_mean"] = mixed_mean
        c04_results["mixed_std"] = mixed_std
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
        lines.append(f"- Mixed @ N=1000: {mixed_mean:.6f} ± {mixed_std:.6f}")
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
    
    # ====== CLAIM P11-C05: kNN with balanced frac ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C05: kNN with balanced frac competitive (Type: MEDIUM)")
    lines.append("")
    
    try:
        e3_artifact = load_json(PHASE_E3)
        c05_results = {}
        
        rows = e3_artifact["rows"]
        
        # Best config: 1500, frac=0.5, 1-NN
        best_1nn = [r["nn1"]["f1"] for r in rows if r["N"] == 1500 and r["uniform_frac"] == 0.5]
        best_1nn_mean = mean(best_1nn)
        best_1nn_std = std(best_1nn)
        
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
        c05_results["best_1nn_std"] = best_1nn_std
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
        
        lines.append("**Observed (mean ± std over seeds):**")
        lines.append(f"- Best config (N=1500, frac=0.5, k=1): {best_1nn_mean:.6f} ± {best_1nn_std:.6f}")
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
        lines.append(f"**ERROR:** {e}\n")
        results["P11-C05"] = {"pass": False}
    
    # ====== CLAIM P11-C06: Resolution tradeoff ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C06: Resolution tradeoff (Type: MEDIUM)")
    lines.append("")
    
    try:
        d_artifact = load_json(PHASE_D)
        c06_results = {}
        
        # Look at NN11 vs NN41 macro_f1_present
        nn11_f1 = d_artifact["nn"]["NN11"]["overall"]["macro_f1_present"]
        nn41_f1 = d_artifact["nn"]["NN41"]["overall"]["macro_f1_present"]
        
        improvement = nn41_f1 - nn11_f1
        
        c06_results["nn11"] = nn11_f1
        c06_results["nn41"] = nn41_f1
        c06_results["improvement"] = improvement
        
        # Target: 4x resolution improves F1
        target_improvement = 0.02
        pass_improvement = improvement >= target_improvement
        
        c06_pass = pass_improvement
        
        lines.append("**Observed:**")
        lines.append(f"- NN11 macroF1_present: {nn11_f1:.6f}")
        lines.append(f"- NN41 macroF1_present: {nn41_f1:.6f}")
        lines.append(f"- Improvement (NN41 − NN11): {improvement:.6f}")
        lines.append("")
        lines.append("**Targets:**")
        lines.append(f"- Improvement ≥ {target_improvement}: {'✅ PASS' if pass_improvement else '❌ FAIL'}")
        lines.append("")
        lines.append(f"**Status:** {'✅ PASS' if c06_pass else '❌ FAIL'}")
        
        c06_results["pass"] = c06_pass
        results["P11-C06"] = c06_results
        
    except Exception as e:
        lines.append(f"**ERROR:** {e}\n")
        results["P11-C06"] = {"pass": False}
    
    # ====== CLAIM P11-C07: Uniform sampling baseline ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C07: Uniform sampling baseline (Type: MEDIUM)")
    lines.append("")
    
    try:
        e2_artifact = load_json(PHASE_E2)
        c07_results = {}
        
        rows = e2_artifact["rows"]
        
        # N=1000 uniform performance
        uniform_1000 = [r["macro_f1_present"] for r in rows if r["N"] == 1000 and r["strategy"] == "uniform"]
        uniform_mean = mean(uniform_1000)
        uniform_std = std(uniform_1000)
        
        c07_results["uniform_mean"] = uniform_mean
        c07_results["uniform_std"] = uniform_std
        
        # Target: uniform should be ≥0.94
        target_uniform = 0.94
        pass_uniform = uniform_mean >= target_uniform
        
        c07_pass = pass_uniform
        
        lines.append("**Observed (mean ± std over seeds):**")
        lines.append(f"- Uniform @ N=1000: {uniform_mean:.6f} ± {uniform_std:.6f}")
        lines.append("")
        lines.append("**Targets:**")
        lines.append(f"- Uniform ≥ {target_uniform}: {'✅ PASS' if pass_uniform else '❌ FAIL'}")
        lines.append("")
        lines.append(f"**Status:** {'✅ PASS' if c07_pass else '❌ FAIL'}")
        
        c07_results["pass"] = c07_pass
        results["P11-C07"] = c07_results
        
    except Exception as e:
        lines.append(f"**ERROR:** {e}\n")
        results["P11-C07"] = {"pass": False}
    
    # ====== CLAIM P11-C08: kNN scalability ======
    lines.append("")
    lines.append("---")
    lines.append("## Claim P11-C08: kNN scalability (Type: WEAK)")
    lines.append("")
    
    try:
        e3_artifact = load_json(PHASE_E3)
        c08_results = {}
        
        rows = e3_artifact["rows"]
        
        # Check performance scaling: N=1000 vs N=1500
        best_1000_1nn = [r["nn1"]["f1"] for r in rows if r["N"] == 1000 and r["uniform_frac"] == 0.5]
        best_1500_1nn = [r["nn1"]["f1"] for r in rows if r["N"] == 1500 and r["uniform_frac"] == 0.5]
        
        perf_1000 = mean(best_1000_1nn)
        perf_1500 = mean(best_1500_1nn)
        scaling = perf_1500 - perf_1000
        
        c08_results["perf_n1000"] = perf_1000
        c08_results["perf_n1500"] = perf_1500
        c08_results["scaling"] = scaling
        
        # Target: should show improvement with more data
        target_scaling = 0.0
        pass_scaling = scaling >= target_scaling
        
        c08_pass = pass_scaling
        
        lines.append("**Observed (N=1000 vs N=1500, frac=0.5, 1-NN):**")
        lines.append(f"- N=1000: {perf_1000:.6f}")
        lines.append(f"- N=1500: {perf_1500:.6f}")
        lines.append(f"- Scaling gain: {scaling:.6f}")
        lines.append("")
        lines.append("**Target:**")
        lines.append(f"- Scaling ≥ {target_scaling}: {'✅ PASS' if pass_scaling else '❌ FAIL'}")
        lines.append("")
        lines.append(f"**Status:** {'✅ PASS' if c08_pass else '❌ FAIL'}")
        
        c08_results["pass"] = c08_pass
        results["P11-C08"] = c08_results
        
    except Exception as e:
        lines.append(f"**ERROR:** {e}\n")
        results["P11-C08"] = {"pass": False}
    
    # ====== SUMMARY TABLE ======
    lines.append("")
    lines.append("---")
    lines.append("## Summary Table")
    lines.append("")
    lines.append("| Claim | Type | Status |")
    lines.append("|-------|------|--------|")
    
    claim_types = {
        "P11-C01": "STRONG",
        "P11-C02": "STRONG",
        "P11-C03": "STRONG",
        "P11-C04": "STRONG",
        "P11-C05": "MEDIUM",
        "P11-C06": "MEDIUM",
        "P11-C07": "MEDIUM",
        "P11-C08": "WEAK",
    }
    
    pass_count = 0
    for claim_id in ["P11-C01", "P11-C02", "P11-C03", "P11-C04", "P11-C05", "P11-C06", "P11-C07", "P11-C08"]:
        if claim_id in results:
            status = "✅ PASS" if results[claim_id].get("pass") else "❌ FAIL"
            if results[claim_id].get("pass"):
                pass_count += 1
            lines.append(f"| {claim_id} | {claim_types.get(claim_id, '?')} | {status} |")
    
    lines.append("")
    lines.append(f"**Total: {pass_count}/8 PASS**")
    lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Project 11 claims against procedure-preserving re-validation artifacts"
    )
    parser.add_argument(
        "--root",
        type=str,
        default="project_12/results/revalidate_p11proc/",
        help="Root directory for re-validation artifacts (default: project_12/results/revalidate_p11proc/)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md",
        help="Output markdown report path"
    )
    
    args = parser.parse_args()
    
    root_dir = Path(args.root)
    output_path = Path(args.output)
    
    # Validate and generate report
    report = validate_claims(root_dir)
    
    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n✅ Report written to: {output_path}")
    print(f"Root directory: {root_dir}")


if __name__ == "__main__":
    main()
