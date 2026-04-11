"""
================================================================================
VALIDATE_CLAIMS_P4_BASELINES.PY
================================================================================

PROJECT 12 PROJECT 4 BASELINE CLAIMS VALIDATION

PURPOSE:
  Validate Project 4 baseline claims (C02, C03, C05) against Project 12
  baseline repro artifacts.

CLAIMS EVALUATED:
  - P4-C02: Block-boundary split (MLP/Transformer > LSTM)
  - P4-C03: Weak in-distribution (all ≤ 0.20)
  - P4-C05: Alternating/fullprop collapse (universal ≤ 0.10)

INPUTS:
  Artifacts from project_12/results/repro_p4/baselines/{mlp,lstm,transformer}/artifact.json

OUTPUTS:
  Markdown report with evidence-only validation results

================================================================================
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, Tuple

def load_artifact(path: Path) -> Dict[str, Any]:
    """Load and parse artifact JSON."""
    with open(path) as f:
        return json.load(f)

def extract_claim_metrics(artifact: Dict[str, Any]) -> Dict[str, float]:
    """Extract metrics needed for P4-C02, C03, C05 from artifact."""
    raw = artifact.get("raw_metrics", {})
    
    metrics = {
        "in_distribution_exact_match": raw.get("in_distribution", {}).get("exact_match", None),
        "alternating_carry_exact_match": raw.get("adversarial", {}).get("alternating_carry", {}).get("exact_match", None),
        "full_propagation_chain_exact_match": raw.get("adversarial", {}).get("full_propagation_chain", {}).get("exact_match", None),
        "block_boundary_stress_exact_match": raw.get("adversarial", {}).get("block_boundary_stress", {}).get("exact_match", None),
    }
    return metrics

def validate_c02_block_boundary_split(metrics: Dict[str, Dict[str, float]]) -> Tuple[bool, str]:
    """
    Validate P4-C02 (block-boundary split):
    - MLP block-boundary accuracy ≥ 0.80
    - Transformer block-boundary accuracy ≥ 0.80
    - LSTM block-boundary accuracy ≤ 0.20
    - Gap: min(MLP, Transformer) − LSTM ≥ 0.50
    """
    mlp_bb = metrics["mlp"]["block_boundary_stress_exact_match"]
    lstm_bb = metrics["lstm"]["block_boundary_stress_exact_match"]
    transformer_bb = metrics["transformer"]["block_boundary_stress_exact_match"]
    
    # Criterion 1: MLP ≥ 0.80
    c1_pass = mlp_bb is not None and mlp_bb >= 0.80
    
    # Criterion 2: Transformer ≥ 0.80
    c2_pass = transformer_bb is not None and transformer_bb >= 0.80
    
    # Criterion 3: LSTM ≤ 0.20
    c3_pass = lstm_bb is not None and lstm_bb <= 0.20
    
    # Criterion 4: Gap ≥ 0.50
    gap = min(mlp_bb, transformer_bb) - lstm_bb if (mlp_bb is not None and transformer_bb is not None and lstm_bb is not None) else None
    c4_pass = gap is not None and gap >= 0.50
    
    all_pass = c1_pass and c2_pass and c3_pass and c4_pass
    
    gap_str = f"{gap:.4f}" if gap is not None else "N/A"
    
    evidence = f"""
**P4-C02 Validation: Block-Boundary Split**

Targets (pre-registered):
1. MLP block-boundary ≥ 0.80: **{'PASS' if c1_pass else 'FAIL'}** (observed: {mlp_bb:.4f})
2. Transformer block-boundary ≥ 0.80: **{'PASS' if c2_pass else 'FAIL'}** (observed: {transformer_bb:.4f})
3. LSTM block-boundary ≤ 0.20: **{'PASS' if c3_pass else 'FAIL'}** (observed: {lstm_bb:.4f})
4. Gap (min(MLP,Transformer) − LSTM) ≥ 0.50: **{'PASS' if c4_pass else 'FAIL'}** (observed: {gap_str})

Overall: **{'✅ PASS' if all_pass else '❌ FAIL'}** — {'All targets met' if all_pass else 'Some targets not met'}
"""
    
    return all_pass, evidence

def validate_c03_weak_in_distribution(metrics: Dict[str, Dict[str, float]]) -> Tuple[bool, str]:
    """
    Validate P4-C03 (weak in-distribution):
    - All three ≤ 0.20
    """
    mlp_id = metrics["mlp"]["in_distribution_exact_match"]
    lstm_id = metrics["lstm"]["in_distribution_exact_match"]
    transformer_id = metrics["transformer"]["in_distribution_exact_match"]
    
    c_mlp = mlp_id is not None and mlp_id <= 0.20
    c_lstm = lstm_id is not None and lstm_id <= 0.20
    c_transformer = transformer_id is not None and transformer_id <= 0.20
    
    all_pass = c_mlp and c_lstm and c_transformer
    
    evidence = f"""
**P4-C03 Validation: Weak In-Distribution**

Targets (pre-registered):
- MLP in-dist ≤ 0.20: **{'PASS' if c_mlp else 'FAIL'}** (observed: {mlp_id:.4f})
- LSTM in-dist ≤ 0.20: **{'PASS' if c_lstm else 'FAIL'}** (observed: {lstm_id:.4f})
- Transformer in-dist ≤ 0.20: **{'PASS' if c_transformer else 'FAIL'}** (observed: {transformer_id:.4f})

Overall: **{'✅ PASS' if all_pass else '❌ FAIL'}** — {'All architectures weak' if all_pass else 'Some architectures strong'}
"""
    
    return all_pass, evidence

def validate_c05_alternating_fullprop_collapse(metrics: Dict[str, Dict[str, float]]) -> Tuple[bool, str]:
    """
    Validate P4-C05 (alternating/fullprop collapse):
    - For each family: max(model accuracy) ≤ 0.10 (universal weakness)
    - No architecture split: max − min ≤ 0.10 (no differentiation)
    """
    
    # Alternating carry
    alt_mlp = metrics["mlp"]["alternating_carry_exact_match"]
    alt_lstm = metrics["lstm"]["alternating_carry_exact_match"]
    alt_transformer = metrics["transformer"]["alternating_carry_exact_match"]
    
    alt_max = max(alt_mlp, alt_lstm, alt_transformer) if all(x is not None for x in [alt_mlp, alt_lstm, alt_transformer]) else None
    alt_min = min(alt_mlp, alt_lstm, alt_transformer) if all(x is not None for x in [alt_mlp, alt_lstm, alt_transformer]) else None
    alt_gap = alt_max - alt_min if (alt_max is not None and alt_min is not None) else None
    
    alt_universal_weak = alt_max is not None and alt_max <= 0.10
    alt_no_split = alt_gap is not None and alt_gap <= 0.10
    
    # Full propagation chain
    fpc_mlp = metrics["mlp"]["full_propagation_chain_exact_match"]
    fpc_lstm = metrics["lstm"]["full_propagation_chain_exact_match"]
    fpc_transformer = metrics["transformer"]["full_propagation_chain_exact_match"]
    
    fpc_max = max(fpc_mlp, fpc_lstm, fpc_transformer) if all(x is not None for x in [fpc_mlp, fpc_lstm, fpc_transformer]) else None
    fpc_min = min(fpc_mlp, fpc_lstm, fpc_transformer) if all(x is not None for x in [fpc_mlp, fpc_lstm, fpc_transformer]) else None
    fpc_gap = fpc_max - fpc_min if (fpc_max is not None and fpc_min is not None) else None
    
    fpc_universal_weak = fpc_max is not None and fpc_max <= 0.10
    fpc_no_split = fpc_gap is not None and fpc_gap <= 0.10
    
    all_pass = alt_universal_weak and alt_no_split and fpc_universal_weak and fpc_no_split
    
    alt_gap_str = f"{alt_gap:.4f}" if alt_gap is not None else "N/A"
    fpc_gap_str = f"{fpc_gap:.4f}" if fpc_gap is not None else "N/A"
    
    evidence = f"""
**P4-C05 Validation: Alternating-Carry & Full-Propagation-Chain Collapse**

Alternating-Carry Family:
- MLP: {alt_mlp:.4f}
- LSTM: {alt_lstm:.4f}
- Transformer: {alt_transformer:.4f}
- Max accuracy: {alt_max:.4f}
- Universal weak (max ≤ 0.10): **{'PASS' if alt_universal_weak else 'FAIL'}**
- No split (gap ≤ 0.10): **{'PASS' if alt_no_split else 'FAIL'}** (gap = {alt_gap_str})

Full-Propagation-Chain Family:
- MLP: {fpc_mlp:.4f}
- LSTM: {fpc_lstm:.4f}
- Transformer: {fpc_transformer:.4f}
- Max accuracy: {fpc_max:.4f}
- Universal weak (max ≤ 0.10): **{'PASS' if fpc_universal_weak else 'FAIL'}**
- No split (gap ≤ 0.10): **{'PASS' if fpc_no_split else 'FAIL'}** (gap = {fpc_gap_str})

Overall: **{'✅ PASS' if all_pass else '❌ FAIL'}** — {'Both families universally weak with no architecture split' if all_pass else 'Family patterns do not match expectation'}
"""
    
    return all_pass, evidence

def main():
    parser = argparse.ArgumentParser(description="Validate Project 4 baseline claims")
    parser.add_argument(
        "--root",
        type=str,
        default="project_12/results/repro_p4/baselines/",
        help="Root directory containing mlp/, lstm/, transformer/ subdirectories"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="project_12/reports/P4_VALIDATION_REPORT_BASELINES.md",
        help="Output markdown report path"
    )
    
    args = parser.parse_args()
    root = Path(args.root)
    output_path = Path(args.output)
    
    # Load artifacts
    print("Loading baseline artifacts...")
    
    mlp_artifact = load_artifact(root / "mlp" / "artifact.json")
    lstm_artifact = load_artifact(root / "lstm" / "artifact.json")
    transformer_artifact = load_artifact(root / "transformer" / "artifact.json")
    
    # Extract metrics
    mlp_metrics = extract_claim_metrics(mlp_artifact)
    lstm_metrics = extract_claim_metrics(lstm_artifact)
    transformer_metrics = extract_claim_metrics(transformer_artifact)
    
    metrics = {
        "mlp": mlp_metrics,
        "lstm": lstm_metrics,
        "transformer": transformer_metrics,
    }
    
    # Validate claims
    print("Validating claims...")
    
    c02_pass, c02_evidence = validate_c02_block_boundary_split(metrics)
    c03_pass, c03_evidence = validate_c03_weak_in_distribution(metrics)
    c05_pass, c05_evidence = validate_c05_alternating_fullprop_collapse(metrics)
    
    all_pass = c02_pass and c03_pass and c05_pass
    
    # Generate report
    report = f"""# P4_VALIDATION_REPORT_BASELINES — Project 4 Baseline Claims Validation

**Purpose:** Evidence-only validation of Project 4 baseline claims against Project 12 baseline reproductions.

**Evaluated Claims:**
- P4-C02: Block-boundary split (strong architecture difference)
- P4-C03: Weak in-distribution (universal baseline weakness)
- P4-C05: Alternating-carry and full-propagation-chain collapse (universal robustness failure)

**Artifacts Used:**
- `project_12/results/repro_p4/baselines/mlp/artifact.json`
- `project_12/results/repro_p4/baselines/lstm/artifact.json`
- `project_12/results/repro_p4/baselines/transformer/artifact.json`

---

{c02_evidence}

---

{c03_evidence}

---

{c05_evidence}

---

## Overall Summary

**All Claims Status:** {'✅ PASS' if all_pass else '❌ FAIL'}

**Claim Breakdown:**
- P4-C02 (block-boundary split): {'✅ PASS' if c02_pass else '❌ FAIL'}
- P4-C03 (weak in-dist): {'✅ PASS' if c03_pass else '❌ FAIL'}
- P4-C05 (alternating/fullprop collapse): {'✅ PASS' if c05_pass else '❌ FAIL'}

**Interpretation:**
- **P4-C01 (framework):** Untested (infrastructure only)
- **P4-C04 (intervention):** Untested (requires intervention artifacts)
- **P4-C06 (reproducibility):** Untested (infrastructure only)

**Evidence Path Pointers:**
- Baseline repro check: `project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md`
- Baseline artifacts: `project_12/results/repro_p4/baselines/*/artifact.json`
- Manifest specifications: `project_12/manifests/p4_*_baseline_repro.json`

---

**Report Generated:** Project 12 Sprint 4C
"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"✓ Report saved to: {output_path}")
    print(f"\nValidation Results:")
    print(f"  P4-C02 (block-boundary split): {'PASS' if c02_pass else 'FAIL'}")
    print(f"  P4-C03 (weak in-dist): {'PASS' if c03_pass else 'FAIL'}")
    print(f"  P4-C05 (alternating/fullprop collapse): {'PASS' if c05_pass else 'FAIL'}")
    print(f"\nOverall: {'✅ ALL PASS' if all_pass else '❌ SOME FAIL'}")

if __name__ == "__main__":
    main()
