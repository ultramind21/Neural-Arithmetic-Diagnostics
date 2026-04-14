#!/usr/bin/env python
"""
inspect_project11_artifacts.py — Read-only inspection of Project 11 artifacts.

Usage:
    python inspect_project11_artifacts.py

Output:
    Writes markdown report to: project_12/reports/PROJECT11_ARTIFACT_METADATA.md

Restrictions:
    - Read-only (no modifications to project_11/)
    - Output only to project_12/reports/
"""

import json
from pathlib import Path
from typing import Dict, Any, List

ROOT = Path(__file__).resolve().parents[3]
ND = ROOT / "neural_arithmetic_diagnostics"
P11_RESULTS = ND / "project_11" / "results"
P12_REPORTS = ND / "project_12" / "reports"

ARTIFACTS = [
    {
        "name": "Phase D (Soft Clamp Resolution Sweep)",
        "path": P11_RESULTS / "phase_d_soft_clamp" / "RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json",
        "expected_fields": ["results", "metadata", "timestamp", "git_hash"],
        "phase": "D"
    },
    {
        "name": "Phase E2 (Sample Efficiency)",
        "path": P11_RESULTS / "phase_e2_sample_efficiency" / "artifact.json",
        "expected_fields": ["results", "metadata", "timestamp"],
        "phase": "E2"
    },
    {
        "name": "Phase E3 (Ratio + kNN)",
        "path": P11_RESULTS / "phase_e3_ratio_knn" / "artifact.json",
        "expected_fields": ["results", "metadata", "timestamp"],
        "phase": "E3"
    }
]

def inspect_artifact(artifact_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Inspect a single artifact JSON file."""
    path = artifact_spec["path"]
    result = {
        "name": artifact_spec["name"],
        "path": str(path),
        "exists": path.exists(),
        "file_size_bytes": None,
        "fields_present": [],
        "fields_missing": [],
        "metadata_gaps": [],
        "sample_result": None,
        "seeds_detected": [],
        "error": None
    }

    if not path.exists():
        result["error"] = f"File not found: {path}"
        return result

    try:
        result["file_size_bytes"] = path.stat().st_size
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Check top-level keys
        if isinstance(data, dict):
            result["fields_present"] = list(data.keys())
            expected = artifact_spec.get("expected_fields", [])
            result["fields_missing"] = [f for f in expected if f not in data]
        
        # Check for metadata
        metadata_fields = ["git_hash", "git_branch", "timestamp", "environment"]
        if "metadata" in data and isinstance(data["metadata"], dict):
            metadata_text = ", ".join(data["metadata"].keys())
            result["metadata_gaps"] = [f for f in metadata_fields if f not in data["metadata"]]
        else:
            result["metadata_gaps"] = metadata_fields
        
        # Extract seeds
        if "results" in data and isinstance(data["results"], list):
            if len(data["results"]) > 0:
                first_result = data["results"][0]
                result["sample_result"] = {
                    "keys": list(first_result.keys()),
                    "values_sample": {k: str(v)[:50] for k, v in first_result.items()}
                }
                
                # Detect seeds
                seeds_set = set()
                for res in data["results"]:
                    if "seed" in res:
                        seeds_set.add(res["seed"])
                result["seeds_detected"] = sorted(list(seeds_set))

    except Exception as e:
        result["error"] = f"Error reading file: {str(e)}"

    return result

def generate_report(inspections: List[Dict[str, Any]]) -> str:
    """Generate a markdown report from inspections."""
    report = []
    report.append("# PROJECT11_ARTIFACT_METADATA")
    report.append("")
    report.append("**Purpose:** Audit trail of Project 11 artifact structure and metadata completeness.")
    report.append("")
    report.append("**Date:** 2026-04-11  ")
    report.append("**Inspection method:** Read-only Python script (inspect_project11_artifacts.py)  ")
    report.append("")
    report.append("---")
    report.append("")

    # Summary table
    report.append("## Summary (All Artifacts)")
    report.append("")
    report.append("| Artifact | Exists | Size (bytes) | Error | Metadata gaps |")
    report.append("|---|---|---|---|---|")
    
    for insp in inspections:
        exists = "✅" if insp["exists"] else "❌"
        size = insp["file_size_bytes"] if insp["file_size_bytes"] else "N/A"
        error = insp["error"][:30] if insp["error"] else "None"
        gaps = ", ".join(insp["metadata_gaps"]) if insp["metadata_gaps"] else "None"
        report.append(f"| {insp['name']} | {exists} | {size} | {error} | {gaps} |")
    
    report.append("")
    report.append("---")
    report.append("")

    # Detailed inspection per artifact
    for insp in inspections:
        report.append(f"## {insp['name']}")
        report.append("")
        report.append(f"**File:** `{insp['path']}`  ")
        report.append(f"**Exists:** {insp['exists']}  ")

        if insp["error"]:
            report.append(f"**Error:** {insp['error']}")
            report.append("")
            continue

        report.append(f"**Size:** {insp['file_size_bytes']} bytes  ")
        report.append("")

        # Fields present
        if insp["fields_present"]:
            report.append("**Top-level fields:**")
            for field in insp["fields_present"]:
                report.append(f"  - {field}")
            report.append("")

        # Fields missing
        if insp["fields_missing"]:
            report.append(f"**Missing expected fields:** {', '.join(insp['fields_missing'])}")
            report.append("")

        # Sample result structure
        if insp["sample_result"]:
            report.append("**Sample result object (first entry):**")
            report.append("  ```python")
            for key in insp["sample_result"]["keys"]:
                value = insp["sample_result"]["values_sample"][key]
                report.append(f"  '{key}': {value}...")
            report.append("  ```")
            report.append("")

        # Seeds detected
        if insp["seeds_detected"]:
            report.append(f"**Seeds detected in artifact:** {insp['seeds_detected']}")
            report.append("")

        # Metadata gaps
        if insp["metadata_gaps"]:
            report.append(f"**Metadata gaps (missing in artifact.metadata):** {', '.join(insp['metadata_gaps'])}")
            report.append("")

        report.append("---")
        report.append("")

    # Critical gaps section
    report.append("## CRITICAL METADATA GAPS (Sprint 2A)")
    report.append("")
    report.append("Project 12 must ensure the following for re-validation artifacts:")
    report.append("")
    report.append("| Field | Current (P11) | Required (P12) |")
    report.append("|---|---|---|")
    report.append("| git_hash | Missing/Present | ✅ Must capture |")
    report.append("| timestamp | Unclear | ✅ ISO 8601 format |")
    report.append("| environment | Not found | ✅ Python, Torch versions |")
    report.append("| seeds | Found in results | ✅ Explicit array at top level |")
    report.append("| holdout_path | Not in metadata | ✅ Must reference |")
    report.append("| pool_config | Not in metadata | ✅ pool_size + composition |")
    report.append("| baseline_implementations | Not explicit | ✅ Reference commit IDs |")
    report.append("")

    return "\n".join(report)

def main():
    """Main inspection flow."""
    print("=" * 60)
    print("PROJECT 11 ARTIFACT INSPECTION")
    print("=" * 60)

    # Create output directory
    P12_REPORTS.mkdir(parents=True, exist_ok=True)
    
    # Inspect all artifacts
    inspections = []
    for artifact_spec in ARTIFACTS:
        print(f"\nInspecting: {artifact_spec['name']}...")
        insp = inspect_artifact(artifact_spec)
        inspections.append(insp)
        
        if insp["error"]:
            print(f"  ❌ {insp['error']}")
        else:
            print(f"  ✅ Fields: {len(insp['fields_present'])}")
            if insp["seeds_detected"]:
                print(f"  ✅ Seeds: {insp['seeds_detected']}")

    # Generate report
    report_text = generate_report(inspections)
    
    # Write report
    report_path = P12_REPORTS / "PROJECT11_ARTIFACT_METADATA.md"
    report_path.write_text(report_text, encoding="utf-8")
    
    print(f"\n{'=' * 60}")
    print(f"Report written to: {report_path}")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
