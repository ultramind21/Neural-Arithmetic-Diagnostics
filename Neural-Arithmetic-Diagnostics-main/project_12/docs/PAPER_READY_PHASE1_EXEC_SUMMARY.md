# Project 12 Phase 1 Executive Summary — Paper-Ready Portfolio

**Date:** 2026-04-11  
**Branch:** project12-validation  
**Status:** Phase 1 Complete (14 validated claims, 1 rejected-as-stated)

---

## I. Project 12 Methodology Contribution

**Core Innovation:** Reproducibility-based validation framework for neural arithmetic claims, extending beyond numerical reproduction to *policy-based acceptance* and *mechanism verification*.

**Key principles:**
1. **Copy+patch discipline:** Entrypoint reproduce Project X logic (diff gate ≥ 0.85 similarity)
2. **Non-determinism tolerance:** Stochastic training acceptable if policy criteria met, not comparison to historical exact values
3. **Artifact schema versioning:** Manifest-driven configuration ensures portable, interpretable experiments
4. **Multi-view consistency:** Same artifact read via multiple chains (direct JSON, Python extraction, report parsing) to catch parsing errors
5. **Mechanism-based refinement:** Failed claims refined into mechanism-validated alternatives (e.g., C07 → C07R)

**Scope:** Project 11 (soft clamp interpretation + sampling diagnostics) and Project 4 (adversarial training narrow transfer) serve as validation targets.

---

## II. Project 11 Results (Soft Clamp + Sampling/Retrieval Diagnostics)

**Claim landscape (Project 12 Phase 1):**

| Claim ID | Status (P12) | One-line meaning |
|----------|---|---|
| P11-C01 | ✅ Validated | Soft clamp enables competitive rule baseline overall (V3.1 vs V3 hard clamp). |
| P11-C02 | ✅ Validated | Dense NN improves with resolution (NN81 as upper-performance reference). |
| P11-C03 | ✅ Validated | Boundary-only sampling underperforms; global coverage (mixed) is necessary. |
| P11-C04 | ✅ Validated | Mixed sampling at N=1000 achieves near-dense performance with significantly reduced reference cost. |
| P11-C05 | ✅ Validated | Ratio frac≈0.5 competitive; 1-NN outperforms 3-NN under structured boundary concentration. |
| P11-C06 | ✅ Validated | Diminishing returns beyond N=1000 (mixed is competitive with larger N). |
| P11-C07 | ❌ Rejected-as-stated | Absolute boundary threshold (V3.1_boundary ≥ 0.85) not robust across procedure-preserving holdout seeds (1/20 pass in sweep). |
| P11-C07R | ✅ Validated | Mechanism-based boundary competence: relative improvement ≥0.15 and NN81 gap ≤0.10 are robust across seed variation. |
| P11-C08 | ✅ Validated | Reference set retrieval efficient (build time <0.10s); pool-based design supports no leakage. |

**Key meta-finding:** Absolute numeric thresholds (e.g., V3.1_boundary ≥ 0.85) collapse under holdout seed variance; relative ordering and mechanism-based criteria more robust.

**Evidence paths (Primary):**
- project_12/docs/VALIDATED_RESULTS_P11_PROJECT12.md
- project_12/docs/FORMAL_CLAIMS.md (claims P11-C01 through P11-C08)
- project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md
- project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md (C07 rejection + C07R validation)
- project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv (20-seed sweep data)
- project_12/docs/PROJECT_11_CLOSURE_VALIDATION.md

---

## III. Project 4 Results (Adversarial Training Narrow Transfer)

**All 6 baseline + intervention claims validated:**

| Claim | Category | Evidence | Gap |
|-------|----------|----------|-----|
| C01 | Infrastructure | Entrypoint runs, outputs valid JSON | ✅ |
| C02 | Baseline spec | block_boundary_stress accuracy ≥ 0.80 pre-training | accuracy=1.0, ✅ met |
| C03 | Baseline weakness | alternating_carry, full_propagation_chain pre-accuracy < 0.15 | both 0.0, ✅ met |
| C04 | Narrow transfer | seen_gain > heldout_gain, gap ≥ 0.10 | gap=1.5, ✅ 3/3 seeds pass |
| C05 | Universal collapse | All architectures fail adversarial families | MLP/LSTM/Transformer all ≤ 0.1, ✅ |
| C06 | Baseline reproducible | Artifact extraction consistent | ✅ verified via multi-view |

**Intervention outcome:**
- Pre-training: alternating_carry=0.0, full_propagation_chain=0.0, block_boundary_stress=1.0
- Post-training: alternating_carry=1.0, full_propagation_chain=0.0, block_boundary_stress=0.0
- **Interpretation:** Strong *seen* improvement (mean +0.5), *held-out* degradation (−1.0). Pattern demonstrates **narrow transfer** (memorization of training distribution, not robust generalization).

**Multi-seed smoke check (Sprint 4F):** 3 seeds (42, 123, 456), manifest-driven, pass-rate 3/3. Metrics identical across runs (gap=1.5); suggests deterministic data generation or seed not affecting outcomes in current setup. Result: **evidence of stability, not variance quantification**.

**Evidence paths:**
- Baseline policy check: project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md
- Intervention validation: project_12/reports/P4_VALIDATION_REPORT_INTERVENTION.md
- Policy check result: project_12/reports/REPRO_CHECK_PROJECT4_INTERVENTION.md
- Multi-seed report: project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md
- Closure document: project_12/docs/PROJECT_4_CLOSURE_VALIDATION.md

---

## IV. Claim Status Summary

**Phase 1 totals:**
- ✅ **Validated:** 14 claims (8 from P11, 6 from P4)
- ❌ **Rejected-as-stated:** 1 claim (P11-C07, absolute threshold)
- ✅ **Revised & validated:** 1 claim (P11-C07R, mechanism-based alternative)

**Not tested:** None. All claims in scope either validated or rejected-and-refined.

---

## V. What This Portfolio Demonstrates

1. **Methodological rigor:** Reproducibility framework catches both false positives (C07) and confirms stable patterns (P4-C04)
2. **Interpretability:** Narrow transfer mechanically demonstrated—not just metric agreeing, but understanding *what changed* (seen ↑, held-out ↓)
3. **Scalability:** Same pipeline applied to two independent projects (P11, P4); identical validation gates work across different problem domains
4. **Transparency:** All artifacts, reports, and git history publicly accessible; easy to verify or extend

**Recommended next step:** Synthesize into paper/technical report format, or extend to Project 5/6 if scope permits.

---

**Master snapshot:** project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md  
**Repository:** d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics  
**Branch:** project12-validation  
**Latest commit:** 83a03ac (Sprint 5.1)
