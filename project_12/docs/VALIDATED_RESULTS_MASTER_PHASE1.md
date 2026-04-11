# Project 12 — Phase 1 Master Validated Results Snapshot

**Date:** 2026-04-11  
**Branch:** project12-validation

---

## Scope

This snapshot aggregates Phase 1 validated results for:
- Project 11 (soft clamp + sampling/retrieval diagnostics)
- Project 4 (baseline diagnostics + adversarial training narrow transfer)

---

## Project 11 (P11) — Status Summary

**Validated claims:** 8  
**Rejected-as-stated:** 1

- **Validated (Project 12):** P11-C01, P11-C02, P11-C03, P11-C04, P11-C05, P11-C06, P11-C08, P11-C07R
- **Rejected-as-stated (Project 12):** P11-C07 (absolute threshold not robust across seeds)

**Primary evidence (paths):**
- project_12/docs/VALIDATED_RESULTS_P11_PROJECT12.md
- project_12/docs/FORMAL_CLAIMS.md
- project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md
- project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md
- project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv
- project_12/docs/PROJECT_11_CLOSURE_VALIDATION.md

---

## Project 4 (P4) — Status Summary

**Validated claims:** 6  
**Untested:** 0

- **Validated (Project 12):** P4-C01, P4-C02, P4-C03, P4-C04, P4-C05, P4-C06

**Primary evidence (paths):**
- project_12/docs/VALIDATED_RESULTS_P4_PROJECT12.md
- project_12/docs/FORMAL_CLAIMS.md
- project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md
- project_12/reports/P4_VALIDATION_REPORT_BASELINES.md
- project_12/reports/REPRO_CHECK_PROJECT4_INTERVENTION.md
- project_12/reports/P4_VALIDATION_REPORT_INTERVENTION.md
- project_12/docs/PROJECT_4_CLOSURE_VALIDATION.md

**Additional Evidence (Sprint 4F):**
- P4-C04 multi-seed smoke check: 3-seed manifest-driven stability sweep (seeds: 42, 123, 456)
- Pass-rate: 3/3; metrics stable (gap=1.5 across all seeds)
- Reports: project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md, project_12/reports/P4_C04_STABILITY_SWEEP_RESULTS.csv

---

## Phase 1 Totals

- **Total validated claims:** 14
- **Total rejected-as-stated claims:** 1

---

## Notes (Methodological)

**Training Interventions:** Stochastic; evaluation logic is reproducible. The P4-C04 validation is policy-based and tied to recorded run artifacts. Multi-seed stability demonstrated via Sprint 4F (3-seed sweep, pass-rate 3/3).

**Project 11 Closure:** Sensitivity sweep (C07 rejected-as-stated) revealed that absolute thresholds are brittle across different seed/sampling conditions; this finding informs design of more robust evaluation criteria for future projects.

**Sprint 4F Enhancement:** P4-C04 multi-seed smoke check executed post-Phase-1-close to strengthen evidence. Same manifest-driven setup, only seed varied; metrics stable across all 3 runs. Evidence of robustness, not variance measurement.

---

## Next Phase (Phase 2)

- Extended intervention studies (if warranted by project scope)
- New projects or hypothesis refinement
- Scaling to larger architectures/tasks

**Repository:** d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics  
**Branch:** project12-validation
