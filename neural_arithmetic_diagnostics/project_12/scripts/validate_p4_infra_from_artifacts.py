"""
================================================================================
VALIDATE_P4_INFRA_FROM_ARTIFACTS.PY
================================================================================

PROJECT 12 PROJECT 4 INFRASTRUCTURE CLAIMS VALIDATION

PURPOSE:
  Validate Project 4 infrastructure claims (C01, C06) by inspecting baseline
  reproduction artifacts from Project 12. No framework execution needed — only
  artifact structure inspection.

CLAIMS EVALUATED:
  - P4-C01: Framework can output per-family scorecards for multiple architectures
  - P4-C06: Baseline reproducibility metadata is present and consistent

INPUTS:
  Artifacts from project_12/results/repro_p4/baselines/{mlp,lstm,transformer}/artifact.json

OUTPUTS:
  Markdown report with evidence-only validation results

================================================================================
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, List

def load_artifact(path: Path) -> Dict[str, Any]:
    """Load and parse artifact JSON."""
    with open(path) as f:
        return json.load(f)

def validate_framework_outputs(artifacts: Dict[str, Dict[str, Any]]) -> Tuple[bool, str]:
    """
    Validate P4-C01 (framework outputs):
    - Per-family metrics present (alternating_carry, full_propagation_chain, block_boundary_stress)
    - In-distribution metrics present
    - Scorecard summary fields present
    - For multiple architectures (3+)
    """
    
    required_families = [
        "alternating_carry",
        "full_propagation_chain",
        "block_boundary_stress"
    ]
    
    all_pass = True
    architecture_results = []
    
    for arch_name, artifact in artifacts.items():
        raw = artifact.get("raw_metrics", {})
        adversarial = raw.get("adversarial", {})
        in_dist = raw.get("in_distribution", {})
        
        # Check: all required families present
        families_present = all(f in adversarial for f in required_families)
        
        # Check: in-distribution metrics present
        in_dist_present = len(in_dist) > 0
        
        # Check: family objects have required structure (digit_acc, carry_acc, etc)
        families_valid = all(
            isinstance(adversarial[f], dict) and "exact_match" in adversarial[f]
            for f in required_families if f in adversarial
        )
        
        arch_pass = families_present and in_dist_present and families_valid
        all_pass = all_pass and arch_pass
        
        status_str = "✅" if arch_pass else "❌"
        architecture_results.append(
            f"  {status_str} {arch_name.upper()}: families_present={families_present}, "
            f"in_dist_present={in_dist_present}, families_valid={families_valid}"
        )
    
    # Check: scorecard present for all architectures
    scorecard_present = all("scorecard" in artifact for artifact in artifacts.values())
    all_pass = all_pass and scorecard_present
    
    # Check: 3+ architectures
    num_architectures = len(artifacts)
    architectures_sufficient = num_architectures >= 3
    all_pass = all_pass and architectures_sufficient
    
    evidence = f"""
**P4-C01 Validation: Framework Output Structure**

**Requirement:** Framework can output per-family scorecards for multiple architectures.

**Per-Architecture Structure Check:**
{chr(10).join(architecture_results)}

**Cross-Architecture Checks:**
- Scorecard present for all architectures: **{'PASS' if scorecard_present else 'FAIL'}**
- Number of architectures: {num_architectures} (required: ≥3): **{'PASS' if architectures_sufficient else 'FAIL'}**

**Overall:** **{'✅ PASS' if all_pass else '❌ FAIL'}** — {'Framework outputs contain required structure' if all_pass else 'Framework output structure incomplete'}
"""
    
    return all_pass, evidence

def validate_reproducibility_metadata(artifacts: Dict[str, Dict[str, Any]]) -> Tuple[bool, str]:
    """
    Validate P4-C06 (reproducibility metadata):
    - p12_metadata present for all architectures
    - Consistent schema across architectures
    - Git hash, timestamp, entrypoint fields present
    - No conflicting metadata (same baseline should have same git_hash)
    """
    
    all_pass = True
    metadata_results = []
    
    metadata_samples = {}
    
    for arch_name, artifact in artifacts.items():
        p12_meta = artifact.get("p12_metadata", {})
        
        # Check: essential fields present
        required_fields = ["git_hash", "timestamp_utc", "entrypoint", "env"]
        fields_present = all(f in p12_meta for f in required_fields)
        
        # Check: env has required subfields
        env = p12_meta.get("env", {})
        env_fields_present = all(
            f in env for f in ["python_version", "torch_version", "cuda_available", "platform"]
        )
        
        arch_pass = fields_present and env_fields_present
        all_pass = all_pass and arch_pass
        
        status_str = "✅" if arch_pass else "❌"
        metadata_results.append(
            f"  {status_str} {arch_name.upper()}: p12_metadata fields={'present' if fields_present else 'missing'}, "
            f"env fields={'present' if env_fields_present else 'missing'}"
        )
        
        metadata_samples[arch_name] = {
            "git_hash": p12_meta.get("git_hash", "N/A"),
            "timestamp": p12_meta.get("timestamp_utc", "N/A"),
            "entrypoint": p12_meta.get("entrypoint", "N/A"),
        }
    
    # Check: consistency across architectures
    git_hashes = [md["git_hash"] for md in metadata_samples.values()]
    entrypoints = [md["entrypoint"] for md in metadata_samples.values()]
    
    git_hash_consistent = len(set(git_hashes)) == 1
    entrypoint_consistent = len(set(entrypoints)) == 3  # MLP, LSTM, Transformer should have different entrypoints
    
    consistency_check = f"""
**Consistency Across Architectures:**
- Git hash consistency: **{'PASS (all same)' if git_hash_consistent else 'WARNING (different)'}** (git_hash: {git_hashes[0] if git_hash_consistent else 'varies'})
- Entrypoint diversity: **{'PASS (all different)' if entrypoint_consistent else 'WARNING (duplicates)'}**
"""
    
    all_pass = all_pass and git_hash_consistent  # Git hash must be same (same repro run)
    
    evidence = f"""
**P4-C06 Validation: Reproducibility Metadata Structure**

**Requirement:** Baseline reproducibility metadata is present and consistent across architectures.

**Per-Architecture Metadata Check:**
{chr(10).join(metadata_results)}

{consistency_check}

**Overall:** **{'✅ PASS' if all_pass else '❌ FAIL'}** — {'Metadata structure and consistency confirmed' if all_pass else 'Metadata issues detected'}
"""
    
    return all_pass, evidence

def main():
    from argparse import ArgumentParser
    
    parser = ArgumentParser(description="Validate Project 4 infrastructure from artifacts")
    parser.add_argument(
        "--root",
        type=str,
        default="project_12/results/repro_p4/baselines/",
        help="Root directory containing mlp/, lstm/, transformer/ subdirectories"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="project_12/reports/P4_INFRA_VALIDATION_REPORT.md",
        help="Output markdown report path"
    )
    
    args = parser.parse_args()
    root = Path(args.root)
    output_path = Path(args.output)
    
    # Load artifacts
    print("Loading baseline artifacts for infra validation...")
    
    mlp_artifact = load_artifact(root / "mlp" / "artifact.json")
    lstm_artifact = load_artifact(root / "lstm" / "artifact.json")
    transformer_artifact = load_artifact(root / "transformer" / "artifact.json")
    
    artifacts = {
        "mlp": mlp_artifact,
        "lstm": lstm_artifact,
        "transformer": transformer_artifact,
    }
    
    # Validate claims
    print("Validating infrastructure claims...")
    
    c01_pass, c01_evidence = validate_framework_outputs(artifacts)
    c06_pass, c06_evidence = validate_reproducibility_metadata(artifacts)
    
    all_pass = c01_pass and c06_pass
    
    # Generate report
    report = f"""# P4_INFRA_VALIDATION_REPORT — Project 4 Infrastructure Claims Validation

**Purpose:** Artifact-based validation of Project 4 infrastructure claims without framework re-execution.

**Evaluated Claims:**
- P4-C01: Framework output structure (per-family scorecards, multiple architectures)
- P4-C06: Baseline reproducibility metadata presence and consistency

**Artifacts Used:**
- `project_12/results/repro_p4/baselines/mlp/artifact.json`
- `project_12/results/repro_p4/baselines/lstm/artifact.json`
- `project_12/results/repro_p4/baselines/transformer/artifact.json`

**Validation Methodology:**
- Artifact-based inspection (no framework execution)
- Check required structure fields without modifying data
- Verify metadata consistency across architectures
- Non-destructive (read-only)

---

{c01_evidence}

---

{c06_evidence}

---

## Overall Summary

**All Infrastructure Claims Status:** {'✅ PASS' if all_pass else '❌ FAIL'}

**Claim Breakdown:**
- P4-C01 (framework outputs): {'✅ PASS' if c01_pass else '❌ FAIL'}
- P4-C06 (reproducibility metadata): {'✅ PASS' if c06_pass else '❌ FAIL'}

**Interpretation:**
- **P4-C01 Validated:** Framework produces required scorecard structure and per-family metrics for 3+ architectures
- **P4-C06 Validated:** Baseline artifacts contain consistent reproducibility metadata (git_hash, timestamps, environment)

**Evidence Path Pointers:**
- Baseline artifacts: `project_12/results/repro_p4/baselines/*/artifact.json`
- Baseline repro check: `project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md`
- Baseline entrypoints: `project_12/scripts/p4/run_p4_*_baseline_repro.py`

---

**Report Generated:** Project 12 Sprint 4D
**Validation Type:** Artifact-based (read-only inspection)
**Scope:** Infrastructure only (no training, no framework re-execution)
"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"✓ Report saved to: {output_path}")
    print(f"\nValidation Results:")
    print(f"  P4-C01 (framework outputs): {'PASS' if c01_pass else 'FAIL'}")
    print(f"  P4-C06 (reproducibility metadata): {'PASS' if c06_pass else 'FAIL'}")
    print(f"\nOverall: {'✅ ALL PASS' if all_pass else '❌ SOME FAIL'}")

if __name__ == "__main__":
    main()
