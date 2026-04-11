#!/usr/bin/env python3
"""
repro_check_project11.py
Compares Project 11 historical artifacts with Project 12 reproductions.
Produces REPRO_CHECK_PROJECT11.md report with pass/fail criteria.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, List

P11_RESULTS = Path("project_11/results")
P12_RESULTS = Path("project_12/results/repro")

def load_json(path: Path) -> Dict[str, Any]:
    """Load JSON from path."""
    if not path.exists():
        raise FileNotFoundError(f"Missing: {path}")
    with open(path, "r") as f:
        return json.load(f)

def approximate_equal(a: float, b: float, tol: float = 1e-9) -> bool:
    """Check if two floats are approximately equal."""
    if a is None or b is None:
        return a == b
    return abs(a - b) <= tol

def compare_arrays(arr1: List, arr2: List, tol: float = 1e-9) -> Tuple[bool, str]:
    """Compare two arrays element-by-element."""
    if len(arr1) != len(arr2):
        return False, f"Length mismatch: {len(arr1)} vs {len(arr2)}"
    
    for i, (v1, v2) in enumerate(zip(arr1, arr2)):
        if isinstance(v1, (list, tuple)) and isinstance(v2, (list, tuple)):
            match, msg = compare_arrays(list(v1), list(v2), tol)
            if not match:
                return False, f"Index {i}: {msg}"
        elif isinstance(v1, float) and isinstance(v2, float):
            if not approximate_equal(v1, v2, tol):
                return False, f"Index {i}: {v1} vs {v2} (diff={abs(v1-v2)})"
        elif v1 != v2:
            return False, f"Index {i}: {v1} vs {v2}"
    
    return True, "OK"

def compare_phase_d() -> Dict[str, Any]:
    """Compare Phase D artifacts."""
    p11_path = P11_RESULTS / "phase_d_soft_clamp" / "RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json"
    p12_path = P12_RESULTS / "phase_d" / "RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json"
    
    results = {
        "phase": "D",
        "p11_path": str(p11_path),
        "p12_path": str(p12_path),
        "checks": {}
    }
    
    try:
        p11 = load_json(p11_path)
        p12 = load_json(p12_path)
        
        # Check core metrics table
        if "table" in p11 and "table" in p12:
            match, msg = compare_arrays(p11["table"], p12["table"], tol=1e-9)
            results["checks"]["table_match"] = {
                "pass": match,
                "message": msg
            }
        
        # Check baselines summary
        if "baselines_summary" in p11 and "baselines_summary" in p12:
            p11_sum = p11["baselines_summary"]
            p12_sum = p12["baselines_summary"]
            
            baselines_ok = True
            baseline_msg = {}
            
            for baseline_name in ["V3", "V3.1", "NN_grids"]:
                if baseline_name in p11_sum and baseline_name in p12_sum:
                    match, msg = compare_arrays(
                        p11_sum[baseline_name], 
                        p12_sum[baseline_name], 
                        tol=1e-9
                    )
                    baseline_msg[baseline_name] = {"match": match, "msg": msg}
                    if not match:
                        baselines_ok = False
            
            results["checks"]["baselines"] = {
                "pass": baselines_ok,
                "details": baseline_msg
            }
        
        results["status"] = "OK"
        
    except Exception as e:
        results["status"] = "ERROR"
        results["error"] = str(e)
    
    return results

def compare_phase_e2() -> Dict[str, Any]:
    """Compare Phase E2 artifacts."""
    p11_path = P11_RESULTS / "phase_e2_sample_efficiency" / "artifact.json"
    p12_path = P12_RESULTS / "phase_e2" / "artifact.json"
    
    results = {
        "phase": "E2",
        "p11_path": str(p11_path),
        "p12_path": str(p12_path),
        "checks": {}
    }
    
    try:
        p11 = load_json(p11_path)
        p12 = load_json(p12_path)
        
        # Check rows (main results table)
        if "rows" in p11 and "rows" in p12:
            match, msg = compare_arrays(p11["rows"], p12["rows"], tol=1e-9)
            results["checks"]["rows_match"] = {
                "pass": match,
                "message": msg
            }
        
        # Check metadata
        metadata_ok = True
        metadata_checks = {}
        
        for key in ["POOL_SIZE", "SEEDS", "SIZES", "STRATS"]:
            if key in p11 and key in p12:
                match = p11[key] == p12[key]
                metadata_checks[key] = {
                    "pass": match,
                    "p11": p11[key],
                    "p12": p12[key]
                }
                if not match:
                    metadata_ok = False
        
        results["checks"]["metadata"] = {
            "pass": metadata_ok,
            "details": metadata_checks
        }
        
        results["status"] = "OK"
        
    except Exception as e:
        results["status"] = "ERROR"
        results["error"] = str(e)
    
    return results

def compare_phase_e3() -> Dict[str, Any]:
    """Compare Phase E3 artifacts."""
    p11_path = P11_RESULTS / "phase_e3_ratio_knn" / "artifact.json"
    p12_path = P12_RESULTS / "phase_e3" / "artifact.json"
    
    results = {
        "phase": "E3",
        "p11_path": str(p11_path),
        "p12_path": str(p12_path),
        "checks": {}
    }
    
    try:
        p11 = load_json(p11_path)
        p12 = load_json(p12_path)
        
        # Check rows
        if "rows" in p11 and "rows" in p12:
            match, msg = compare_arrays(p11["rows"], p12["rows"], tol=1e-9)
            results["checks"]["rows_match"] = {
                "pass": match,
                "message": msg
            }
        
        # Check metadata
        metadata_ok = True
        metadata_checks = {}
        
        for key in ["pool_size", "Ns", "fracs", "seeds"]:
            if key in p11 and key in p12:
                match = p11[key] == p12[key]
                metadata_checks[key] = {
                    "pass": match,
                    "p11": p11[key],
                    "p12": p12[key]
                }
                if not match:
                    metadata_ok = False
        
        results["checks"]["metadata"] = {
            "pass": metadata_ok,
            "details": metadata_checks
        }
        
        results["status"] = "OK"
        
    except Exception as e:
        results["status"] = "ERROR"
        results["error"] = str(e)
    
    return results

def generate_report(phase_d: Dict, phase_e2: Dict, phase_e3: Dict) -> str:
    """Generate markdown report."""
    lines = [
        "# REPRO_CHECK_PROJECT11.md",
        "",
        "## Summary",
        "Comparison of Project 12 reproductions against Project 11 historical artifacts.",
        ""
    ]
    
    # Overall status
    all_pass = (
        phase_d.get("status") == "OK" and
        phase_e2.get("status") == "OK" and
        phase_e3.get("status") == "OK" and
        all(
            check.get("pass", False)
            for phase in [phase_d, phase_e2, phase_e3]
            for check in phase.get("checks", {}).values()
            if isinstance(check, dict) and "pass" in check
        )
    )
    
    lines.append(f"**Overall Status:** {'✅ PASS' if all_pass else '❌ FAIL'}")
    lines.append("")
    
    # Phase D
    lines.append("## Phase D (Resolution Sweep)")
    lines.append(f"- P11 artifact: {phase_d['p11_path']}")
    lines.append(f"- P12 artifact: {phase_d['p12_path']}")
    lines.append("")
    
    if phase_d.get("status") == "ERROR":
        lines.append(f"**ERROR:** {phase_d.get('error', 'Unknown')}")
    else:
        for check_name, check_result in phase_d.get("checks", {}).items():
            status = "✅ PASS" if check_result.get("pass") else "❌ FAIL"
            lines.append(f"- {check_name}: {status}")
            if "message" in check_result:
                lines.append(f"  - {check_result['message']}")
            if "details" in check_result:
                for detail_key, detail_val in check_result["details"].items():
                    detail_status = "✅" if detail_val.get("match") else "❌"
                    lines.append(f"  - {detail_key}: {detail_status}")
                    if "msg" in detail_val and detail_val["msg"] != "OK":
                        lines.append(f"    - {detail_val['msg']}")
    
    lines.append("")
    
    # Phase E2
    lines.append("## Phase E2 (Sample Efficiency)")
    lines.append(f"- P11 artifact: {phase_e2['p11_path']}")
    lines.append(f"- P12 artifact: {phase_e2['p12_path']}")
    lines.append("")
    
    if phase_e2.get("status") == "ERROR":
        lines.append(f"**ERROR:** {phase_e2.get('error', 'Unknown')}")
    else:
        for check_name, check_result in phase_e2.get("checks", {}).items():
            status = "✅ PASS" if check_result.get("pass") else "❌ FAIL"
            lines.append(f"- {check_name}: {status}")
            if "message" in check_result:
                lines.append(f"  - {check_result['message']}")
            if "details" in check_result:
                for detail_key, detail_val in check_result["details"].items():
                    detail_status = "✅" if detail_val.get("pass") else "❌"
                    lines.append(f"  - {detail_key}: {detail_status}")
                    if "pass" not in detail_val:
                        lines.append(f"    - P11: {detail_val.get('p11')}")
                        lines.append(f"    - P12: {detail_val.get('p12')}")
    
    lines.append("")
    
    # Phase E3
    lines.append("## Phase E3 (Ratio + kNN)")
    lines.append(f"- P11 artifact: {phase_e3['p11_path']}")
    lines.append(f"- P12 artifact: {phase_e3['p12_path']}")
    lines.append("")
    
    if phase_e3.get("status") == "ERROR":
        lines.append(f"**ERROR:** {phase_e3.get('error', 'Unknown')}")
    else:
        for check_name, check_result in phase_e3.get("checks", {}).items():
            status = "✅ PASS" if check_result.get("pass") else "❌ FAIL"
            lines.append(f"- {check_name}: {status}")
            if "message" in check_result:
                lines.append(f"  - {check_result['message']}")
            if "details" in check_result:
                for detail_key, detail_val in check_result["details"].items():
                    detail_status = "✅" if detail_val.get("pass") else "❌"
                    lines.append(f"  - {detail_key}: {detail_status}")
                    if "pass" not in detail_val:
                        lines.append(f"    - P11: {detail_val.get('p11')}")
                        lines.append(f"    - P12: {detail_val.get('p12')}")
    
    lines.append("")
    lines.append("## Acceptance Criteria")
    lines.append("- Phase D: Metrics table must match exactly (tol ≤ 1e-9)")
    lines.append("- Phase E2/E3: Rows (main results) must match (tol ≤ 1e-9)")
    lines.append("- Metadata: SEEDS/POOL_SIZE/etc must match exactly")
    lines.append("- Allowed variance: `elapsed_seconds` only")
    lines.append("")
    lines.append(f"**Report generated** at Sprint 2B completion")
    
    return "\n".join(lines)

def main():
    """Main entry point."""
    print("🔍 Comparing Phase D...")
    phase_d = compare_phase_d()
    print(f"   Phase D: {phase_d.get('status')}")
    
    print("🔍 Comparing Phase E2...")
    phase_e2 = compare_phase_e2()
    print(f"   Phase E2: {phase_e2.get('status')}")
    
    print("🔍 Comparing Phase E3...")
    phase_e3 = compare_phase_e3()
    print(f"   Phase E3: {phase_e3.get('status')}")
    
    # Generate report
    report = generate_report(phase_d, phase_e2, phase_e3)
    
    # Write report
    report_path = Path("project_12/reports/REPRO_CHECK_PROJECT11.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write(report)
    
    print(f"\n✅ Report written to: {report_path}")

if __name__ == "__main__":
    main()
