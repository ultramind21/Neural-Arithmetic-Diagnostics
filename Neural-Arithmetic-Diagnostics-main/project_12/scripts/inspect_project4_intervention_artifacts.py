"""
================================================================================
INSPECT_PROJECT4_INTERVENTION_ARTIFACTS.PY (Revised for Raw Field Dumps)
================================================================================

PURPOSE:
  Read-only inspection of Project 4 historical intervention artifacts.
  Outputs raw verbatim field dumps + metadata gaps identification.

OUTPUTS:
  - project_12/reports/PROJECT4_INTERVENTION_ARTIFACT_METADATA.md

================================================================================
"""

import json
from pathlib import Path
from typing import Dict, Any

def load_json(path: Path) -> Dict[str, Any]:
    """Load JSON safely."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  Warning: File not found: {path}")
        return {}

def main():
    artifact_path = Path("project_4/interventions/adversarial_training/results/project_4_adversarial_training_artifact.json")
    validation_runs_path = Path("project_4/interventions/adversarial_training/results/project_4_adversarial_training_validation_runs.json")
    output_path = Path("project_12/reports/PROJECT4_INTERVENTION_ARTIFACT_METADATA.md")
    
    print("Inspecting Project 4 intervention artifacts...")
    print(f"  Artifact: {artifact_path}")
    print(f"  Validation runs: {validation_runs_path}")
    
    artifact = load_json(artifact_path)
    validation_runs = load_json(validation_runs_path)
    
    # Extract the 7 key raw sections (as-is from artifact)
    intervention_type = artifact.get("intervention_type", "<missing>")
    seen_families = artifact.get("seen_families", "<missing>")
    heldout_family = artifact.get("heldout_family", None)
    heldout_families = artifact.get("heldout_families", None)
    baseline_reference = artifact.get("baseline_reference", {})
    seen_results = artifact.get("seen_results", {})
    heldout_results = artifact.get("heldout_results", {})
    in_distribution = artifact.get("in_distribution", {})
    
    # Additional metadata fields (Sprint 4B.2A.1)
    base_model_family = artifact.get("base_model_family", "<missing>")
    framework_version = artifact.get("framework_version", "<missing>")
    timestamp_utc = artifact.get("timestamp_utc", "<missing>")
    
    # Identify metadata gaps
    metadata_gaps = []
    if "p12_metadata" not in artifact:
        metadata_gaps.append("p12_metadata (git_hash, timestamp_utc, env, manifest_path, entrypoint)")
    if "config" not in artifact or "seed" not in artifact.get("config", {}):
        metadata_gaps.append("config.seed (for reproducibility tracking)")
    if "config" not in artifact or "base_checkpoint" not in artifact.get("config", {}):
        metadata_gaps.append("config.base_checkpoint (path tracking)")
    if "config" not in artifact or ("training_steps" not in artifact.get("config", {}) and "epochs" not in artifact.get("config", {})):
        metadata_gaps.append("config.training_steps or config.epochs (missing training duration)")
    
    # Generate report
    report_lines = [
        "# PROJECT4_INTERVENTION_ARTIFACT_METADATA — Raw Field Inspection",
        "",
        "**Purpose:** Verbatim inspection of Project 4 historical intervention artifact.",
        "",
        "**Files Inspected:**",
        "- `project_4/interventions/adversarial_training/results/project_4_adversarial_training_artifact.json`",
        "- `project_4/interventions/adversarial_training/results/project_4_adversarial_training_validation_runs.json`",
        "",
        "---",
        "",
        "## Artifact Structure",
        "",
        f"**Total top-level keys:** {len(artifact)}",
        "",
        "**Keys present:**",
    ]
    
    for key in sorted(artifact.keys()):
        val = artifact[key]
        type_str = type(val).__name__
        if isinstance(val, dict):
            size = len(val)
            report_lines.append(f"- `{key}` (dict, {size} keys)")
        elif isinstance(val, list):
            size = len(val)
            report_lines.append(f"- `{key}` (list, {size} items)")
        else:
            report_lines.append(f"- `{key}` ({type_str})")
    
    report_lines.extend([
        "",
        "---",
        "",
        "## Raw Field Dumps (Verbatim from Artifact)",
        "",
        "### 0a) base_model_family",
        "",
        "```json",
        json.dumps(base_model_family, indent=2),
        "```",
        "",
        "### 0b) framework_version",
        "",
        "```json",
        json.dumps(framework_version, indent=2),
        "```",
        "",
        "### 0c) timestamp_utc",
        "",
        "```json",
        json.dumps(timestamp_utc, indent=2),
        "```",
        "",
        "### 1) intervention_type",
        "",
        "```json",
        json.dumps(intervention_type, indent=2),
        "```",
        "",
        "### 2) seen_families",
        "",
        "```json",
        json.dumps(seen_families, indent=2),
        "```",
        "",
    ])
    
    # heldout_family or heldout_families (whichever exists)
    if heldout_family is not None:
        report_lines.extend([
            "### 3) heldout_family",
            "",
            "```json",
            json.dumps(heldout_family, indent=2),
            "```",
            "",
        ])
    elif heldout_families is not None:
        report_lines.extend([
            "### 3) heldout_families",
            "",
            "```json",
            json.dumps(heldout_families, indent=2),
            "```",
            "",
        ])
    else:
        report_lines.extend([
            "### 3) heldout_family / heldout_families",
            "",
            "```",
            "<MISSING>",
            "```",
            "",
        ])
    
    report_lines.extend([
        "### 4) baseline_reference",
        "",
        "```json",
        json.dumps(baseline_reference, indent=2),
        "```",
        "",
        "### 5) seen_results",
        "",
        "```json",
        json.dumps(seen_results, indent=2),
        "```",
        "",
        "### 6) heldout_results",
        "",
        "```json",
        json.dumps(heldout_results, indent=2),
        "```",
        "",
        "### 7) in_distribution",
        "",
        "```json",
        json.dumps(in_distribution, indent=2),
        "```",
        "",
        "---",
        "",
        "## Metadata Gaps (P12 Standard)",
        "",
    ])
    
    if metadata_gaps:
        report_lines.append(f"**Identified {len(metadata_gaps)} gap(s):**")
        report_lines.append("")
        for i, gap in enumerate(metadata_gaps, 1):
            report_lines.append(f"{i}. `{gap}`")
        report_lines.append("")
    else:
        report_lines.append("**(None—all P12 standard fields present)**")
        report_lines.append("")
    
    report_lines.extend([
        "---",
        "",
        "## Validation Runs Structure",
        "",
        f"**Total runs:** {len(validation_runs)}",
        "",
    ])
    
    if validation_runs:
        if isinstance(validation_runs, dict):
            first_key = list(validation_runs.keys())[0] if validation_runs else None
            if first_key:
                report_lines.append(f"**Sample run key:** `{first_key}`")
                run_data = validation_runs[first_key]
                if isinstance(run_data, dict):
                    report_lines.append(f"  - Type: dict with keys: {list(run_data.keys())}")
                else:
                    report_lines.append(f"  - Type: {type(run_data).__name__}")
        elif isinstance(validation_runs, list):
            report_lines.append(f"(List with {len(validation_runs)} entries)")
    
    report_lines.extend([
        "",
        "---",
        "",
        "**Report Generated:** `project_12/scripts/inspect_project4_intervention_artifacts.py` (revised)",
        "",
    ])
    
    report_text = "\n".join(report_lines)
    
    # Save report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")
    
    print(f"✓ Report saved to: {output_path}")
    print("")


if __name__ == "__main__":
    main()
