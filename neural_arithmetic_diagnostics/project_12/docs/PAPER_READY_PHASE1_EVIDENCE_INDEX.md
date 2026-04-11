# Project 12 Phase 1 Evidence Index

## Purpose
Map each claim validation to its supporting evidence paths. Use this to navigate from research questions to raw data.

---

## Evidence Index Table

| Evidence Item | What It Proves | Claim(s) | Primary Path | Secondary Paths |
|---|---|---|---|---|
| P11 Baseline Validation Report | V3.1 rule baseline achieves registered targets | P11-C01, P11-C02, P11-C06 | project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md | FORMAL_CLAIMS.md P11-C01 section |
| P11 Resolution Sweep Artifact | NN performance increases monotonically w/ resolution | P11-C02 | project_12/results/revalidate_p11proc/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json | FORMAL_CLAIMS.md P11-C02 section |
| P11 Boundary-Only Sampling Report | Mixed sampling >> boundary-only sampling | P11-C03 | project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md | project_12/results/revalidate_p11proc/phase_e2/sampling_comparison.json |
| P11 Phase E2/E3 Procedure Match | Sampling efficiency reproducible | P11-C04 | project_12/reports/REPRO_CHECK_PROJECT11.md | FORMAL_CLAIMS.md P11-C04 section |
| P11 Soft Clamp Learning Curves | Soft clamp restores smooth regime | P11-C05 | project_12/docs/VALIDATED_RESULTS_P11_PROJECT12.md section C05 | project_12/results/revalidate_p11proc/phase_d/learning_curves.md |
| P11 Phase D Exact Replication | Resolution sweep outputs match P11 exactly | P11-C06 | project_12/reports/REPRO_CHECK_PROJECT11.md | git log (diff gate report TBD) |
| P11 C07 Sensitivity Sweep | Absolute threshold (0.93) fails seeds 101, 303 | P11-C07 (REJECTED) | project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md | project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv |
| P11 C07R Mechanism Test | Relative ordering V3.1 > V3 holds all seeds | P11-C07R (VALIDATED) | project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md section "Revised Criterion" | FORMAL_CLAIMS.md P11-C07R section |
| P11 Soft Label Init Benefit | Learning acceleration evident in Phase D | P11-C08 | project_12/docs/VALIDATED_RESULTS_P11_PROJECT12.md section C08 | project_12/results/revalidate_p11proc/phase_d/combined_curves.json |
| P4 Baseline Policy Check | Baseline metrics correct: block_boundary_stress=1.0, others=0.0 | P4-C01, P4-C02, P4-C03, P4-C06 | project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md | project_12/results/repro_p4/baselines/mlp/artifact.json |
| P4 Baseline Validation Report | Baseline spec verified (C02: acc≥0.80, C03: acc<0.15) | P4-C02, P4-C03 | project_12/reports/P4_VALIDATION_REPORT_BASELINES.md | FORMAL_CLAIMS.md P4-C02, P4-C03 sections |
| P4 Intervention Policy Check | Policy accepts: gap=1.5 ≥ 0.10, seen > heldout | P4-C04 | project_12/reports/REPRO_CHECK_PROJECT4_INTERVENTION.md | project_12/results/repro_p4/intervention/artifact.json |
| P4 Intervention Validation Report | Narrow transfer mechanism: seen +0.5, heldout −1.0 | P4-C04 | project_12/reports/P4_VALIDATION_REPORT_INTERVENTION.md | FORMAL_CLAIMS.md P4-C04 section |
| P4 Multi-Seed Sweep (Sprint 4F) | 3/3 seeds pass policy check (gap=1.5 stable) | P4-C04 (stability) | project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md | project_12/reports/P4_C04_STABILITY_SWEEP_RESULTS.csv |
| P4 Universal Collapse Check | All 3 architectures fail on adversarial families | P4-C05 | project_12/docs/FORMAL_CLAIMS.md P4-C05 section | project_4/results/architecture_comparison/ |
| Master Phase 1 Snapshot | Central index of all 14+1 claims, paths, totals | All | project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md | VALIDATED_RESULTS_P11_PROJECT12.md, VALIDATED_RESULTS_P4_PROJECT12.md |
| Diff Gate Report (P11) | Entrypoint fidelity verified for P11 procedures | P11-C06 | project_12/reports/DIFF_GATE_P11_ENTRYPOINT.md | (if generated) |
| Diff Gate Report (P4) | Entrypoint fidelity verified for P4 intervention | P4-C06 | project_12/reports/DIFF_GATE_P4_INTERVENTION_ENTRYPOINT.md | git diff project_4/.../run.py vs project_12/.../run_*.py |

---

## How to Use This Index

**Scenario 1: Verify P11-C07 rejection**  
→ Go to: project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md  
→ Then cross-check: project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv

**Scenario 2: Understand P4-C04 in detail**  
→ Primary: project_12/reports/P4_VALIDATION_REPORT_INTERVENTION.md  
→ Support: project_12/results/repro_p4/intervention/artifact.json  
→ Multi-seed: project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md

**Scenario 3: Get highest-level summary**  
→ Start: project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md

---

## File Organization (by type)

### Documentation
- VALIDATED_RESULTS_MASTER_PHASE1.md (top-level snapshot)
- VALIDATED_RESULTS_P11_PROJECT12.md (P11 details)
- VALIDATED_RESULTS_P4_PROJECT12.md (P4 details)
- PROJECT_11_CLOSURE_VALIDATION.md (P11 final gate)
- PROJECT_4_CLOSURE_VALIDATION.md (P4 final gate)
- FORMAL_CLAIMS.md (all claims, locked definitions)

### Reports
- project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md
- project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md
- project_12/reports/REPRO_CHECK_PROJECT11.md
- project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md
- project_12/reports/P4_VALIDATION_REPORT_BASELINES.md
- project_12/reports/REPRO_CHECK_PROJECT4_INTERVENTION.md
- project_12/reports/P4_VALIDATION_REPORT_INTERVENTION.md
- project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md
- project_12/reports/P4_C04_STABILITY_SWEEP_RESULTS.csv

### Artifacts (JSON/Data)
- project_12/results/revalidate_p11proc/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json
- project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv
- project_12/results/repro_p4/baselines/mlp/artifact.json
- project_12/results/repro_p4/intervention/artifact.json
- project_12/results/repro_p4/intervention_sweep/seed_{42,123,456}/artifact.json

---

**Last updated:** 2026-04-11 (Sprint 6)  
**Repository:** neural_arithmetic_diagnostics (project12-validation)
