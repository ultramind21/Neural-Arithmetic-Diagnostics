# Project 12 Phase 1 Evidence Index

## Purpose
Map each claim validation to its supporting evidence paths. Use this to navigate from research questions to raw data.

---

## Evidence Index Table

| Evidence Item | What It Proves | Claim(s) | Primary Path | Secondary Paths |
|---|---|---|---|---|
| P11 Baseline Validation Report | V3.1 soft clamp competitive overall | P11-C01, P11-C02 | project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md | FORMAL_CLAIMS.md P11-C01, P11-C02 sections |
| P11 Resolution Sweep Artifact (P12) | NN performance increases monotonically; NN81 highest | P11-C02 | project_12/results/revalidate_p11proc/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json | FORMAL_CLAIMS.md P11-C02 section |
| P11 Sampling Efficiency Report (P12) | Mixed sampling >> boundary-only; N=1000 near-dense | P11-C03, P11-C04, P11-C06 | project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md | project_12/results/revalidate_p11proc/phase_e2/artifact.json |
| P11 Phase E3 Ratio+kNN Artifact (P12) | Frac≈0.5 competitive; 1-NN vs 3-NN behavior | P11-C05 | project_12/results/revalidate_p11proc/phase_e3/artifact.json | FORMAL_CLAIMS.md P11-C05 section |
| P11 Phase D Exact Replication (REPRO_CHECK) | Phase D outputs match P11 exactly | P11-C01, P11-C02, P11-C06 | project_12/reports/REPRO_CHECK_PROJECT11.md | FORMAL_CLAIMS.md P11-C06 section |
| P11 C07 Sensitivity Sweep Report | Absolute threshold (0.85) fails: 1/20 seeds pass | P11-C07 (REJECTED) | project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md | project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv |
| P11 C07R Mechanism Validation | Relative improvement ≥0.15, NN81 gap ≤0.10 hold across seeds | P11-C07R (VALIDATED) | project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md section "Revised Criterion" | project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv |
| P11 Build Efficiency + Leakage Check | Build time <0.10s; pool separation maintained | P11-C08 | project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md | FORMAL_CLAIMS.md P11-C08 section |
| P4 Baseline Policy Check | Baseline metrics correct per family | P4-C01, P4-C02, P4-C03, P4-C06 | project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md | project_12/results/repro_p4/baselines/mlp/artifact.json |
| P4 Baseline Validation Report | Baseline spec verified (C02: acc≥0.80, C03: acc<0.15) | P4-C02, P4-C03 | project_12/reports/P4_VALIDATION_REPORT_BASELINES.md | FORMAL_CLAIMS.md P4-C02, P4-C03 sections |
| P4 Intervention Policy Check | Policy accepts: gap=1.5 ≥ 0.10, seen_gain > heldout_gain | P4-C04 | project_12/reports/REPRO_CHECK_PROJECT4_INTERVENTION.md | project_12/results/repro_p4/intervention/artifact.json |
| P4 Intervention Validation Report | Narrow transfer mechanism: seen +0.5, heldout −1.0 | P4-C04 | project_12/reports/P4_VALIDATION_REPORT_INTERVENTION.md | FORMAL_CLAIMS.md P4-C04 section |
| P4 Multi-Seed Sweep (Sprint 4F) | 3/3 seeds pass policy (gap=1.5 stable) | P4-C04 (stability) | project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md | project_12/reports/P4_C04_STABILITY_SWEEP_RESULTS.csv |
| P4 Universal Collapse (Architecture Comparison) | All architectures fail adversarial families | P4-C05 | project_12/docs/FORMAL_CLAIMS.md P4-C05 section | project_4/results/architecture_comparison/ |
| P4 Baseline Reproducibility | Artifact consistency across multi-view reads | P4-C06 | project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md | FORMAL_CLAIMS.md P4-C06 section |
| Master Phase 1 Snapshot | Central index of all 14+1 claims (8 P11 + 6 P4 validated, 1 P11 rejected-as-stated) | All | project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md | VALIDATED_RESULTS_P11_PROJECT12.md, VALIDATED_RESULTS_P4_PROJECT12.md |

---

## How to Use This Index

**Scenario 1: Verify P11-C07 rejection + P11-C07R validation**  
→ Primary: project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md  
→ Support: project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv (check: 1/20 seeds >= 0.85 on absolute threshold, both relative criteria pass all seeds)

**Scenario 2: Understand P4-C04 narrow transfer in detail**  
→ Primary: project_12/reports/P4_VALIDATION_REPORT_INTERVENTION.md  
→ Support: project_12/results/repro_p4/intervention/artifact.json  
→ Multi-seed: project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md

**Scenario 3: Get top-level Phase 1 overview**  
→ Start: project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md

---

## File Organization (by type)

### Documentation
- VALIDATED_RESULTS_MASTER_PHASE1.md (top-level Phase 1 snapshot)
- VALIDATED_RESULTS_P11_PROJECT12.md (P11 summaries)
- VALIDATED_RESULTS_P4_PROJECT12.md (P4 summaries)
- PROJECT_11_CLOSURE_VALIDATION.md (P11 gate + metadata)
- PROJECT_4_CLOSURE_VALIDATION.md (P4 gate + metadata)
- FORMAL_CLAIMS.md (locked definitions of all claims)

### Reports (Policy checks + validation narratives)
- project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md (P11 baselines)
- project_12/reports/REPRO_CHECK_PROJECT11.md (Phase D/E2/E3 fidelity)
- project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md (C07 rejection + C07R validation)
- project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md (P4 baseline policy check)
- project_12/reports/P4_VALIDATION_REPORT_BASELINES.md (P4 baseline narrative)
- project_12/reports/REPRO_CHECK_PROJECT4_INTERVENTION.md (P4-C04 policy check)
- project_12/reports/P4_VALIDATION_REPORT_INTERVENTION.md (P4-C04 narrative)
- project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md (3-seed smoke check)

### Artifacts (JSON/CSV data)
- project_12/results/revalidate_p11proc/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json
- project_12/results/revalidate_p11proc/phase_e2/artifact.json
- project_12/results/revalidate_p11proc/phase_e3/artifact.json
- project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv (C07 sweep data)
- project_12/results/repro_p4/baselines/mlp/artifact.json (baseline)
- project_12/results/repro_p4/intervention/artifact.json (intervention)
- project_12/results/repro_p4/intervention_sweep/{seed_42,seed_123,seed_456}/artifact.json (3-seed sweep)

---

**Last updated:** 2026-04-11 (Sprint 6)  
**Repository:** neural_arithmetic_diagnostics (project12-validation)
