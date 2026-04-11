# VALIDATED_RESULTS_P4_PROJECT12 — Project 4 Validated Claims Snapshot

**Purpose:** Snapshot of Project 4 claims validated in Project 12 (baseline reproductions).

**Scope:** Baseline (non-intervention) claims only. Infrastructure and reproducibility claims untested.

---

## Claim Status Summary

| Claim ID | Type | Title | Status | Evidence |
|----------|------|-------|--------|----------|
| P4-C01 | weak (infra) | Framework execution | **Untested** | (infrastructure only) |
| **P4-C02** | **strong** | **Block-boundary split** | **✅ Validated** | `P4_VALIDATION_REPORT_BASELINES.md` |
| **P4-C03** | **strong** | **Weak in-distribution** | **✅ Validated** | `P4_VALIDATION_REPORT_BASELINES.md` |
| P4-C04 | strong | Narrow transfer (intervention) | **Untested** | (requires intervention artifacts) |
| **P4-C05** | **medium** | **Alternating/fullprop collapse** | **✅ Validated** | `P4_VALIDATION_REPORT_BASELINES.md` |
| P4-C06 | weak (infra) | Baseline reproducibility | **Untested** | (infrastructure only) |

---

## Validated Claims Detail

### ✅ P4-C02: Block-Boundary Split

**Status:** Validated (Project 12; baseline repro)

**Claim:** A meaningful architecture-dependent difference exists on block-boundary-stress: MLP and Transformer show substantially higher robustness than LSTM on this adversarial family.

**Observed (Project 12 baseline repro):**
- MLP block-boundary: 1.0000 ✅
- Transformer block-boundary: 1.0000 ✅
- LSTM block-boundary: 0.0000 ✅
- Gap: 1.0000 ✅

**Pre-registered Targets Met:**
- ✅ MLP ≥ 0.80 (observed: 1.0)
- ✅ Transformer ≥ 0.80 (observed: 1.0)
- ✅ LSTM ≤ 0.20 (observed: 0.0)
- ✅ Gap ≥ 0.50 (observed: 1.0)

**Evidence Pointers:**
- Validation report: `project_12/reports/P4_VALIDATION_REPORT_BASELINES.md`
- Baseline artifacts: `project_12/results/repro_p4/baselines/mlp/artifact.json` (block_boundary_stress: 1.0)
- Baseline artifacts: `project_12/results/repro_p4/baselines/lstm/artifact.json` (block_boundary_stress: 0.0)
- Baseline artifacts: `project_12/results/repro_p4/baselines/transformer/artifact.json` (block_boundary_stress: 1.0)
- Repro check: `project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md`

---

### ✅ P4-C03: Weak In-Distribution

**Status:** Validated (Project 12; baseline repro)

**Claim:** In-distribution exact-match accuracy is universally weak across MLP, LSTM, and Transformer under the Project 4 bounded arithmetic task, with no architecture achieving strong performance.

**Observed (Project 12 baseline repro):**
- MLP in-dist: 0.0625 ✅
- LSTM in-dist: 0.0391 ✅
- Transformer in-dist: 0.0391 ✅

**Pre-registered Targets Met:**
- ✅ All three ≤ 0.20 (max observed: 0.0625)
- ✅ No architecture exceeds 0.20 threshold

**Evidence Pointers:**
- Validation report: `project_12/reports/P4_VALIDATION_REPORT_BASELINES.md`
- Baseline artifacts: `project_12/results/repro_p4/baselines/mlp/artifact.json` (in_distribution.exact_match: 0.0625)
- Baseline artifacts: `project_12/results/repro_p4/baselines/lstm/artifact.json` (in_distribution.exact_match: 0.0391)
- Baseline artifacts: `project_12/results/repro_p4/baselines/transformer/artifact.json` (in_distribution.exact_match: 0.0391)
- Repro check: `project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md`

---

### ✅ P4-C05: Alternating-Carry & Full-Propagation-Chain Collapse

**Status:** Validated (Project 12; baseline repro)

**Claim:** Alternating-carry and full-propagation-chain adversarial families are equally hard across all three baseline architectures: all show universal collapse with no architecture-dependent differentiation.

**Observed (Project 12 baseline repro):**

**Alternating-Carry:**
- MLP: 0.0000
- LSTM: 0.0000
- Transformer: 0.0000
- Max accuracy: 0.0000 ✅
- No split (gap): 0.0000 ✅

**Full-Propagation-Chain:**
- MLP: 0.0000
- LSTM: 0.0000
- Transformer: 0.0000
- Max accuracy: 0.0000 ✅
- No split (gap): 0.0000 ✅

**Pre-registered Targets Met:**
- ✅ For each family: max ≤ 0.10 (observed max: 0.0)
- ✅ No architecture split: gap ≤ 0.10 (observed gap: 0.0 for both)

**Evidence Pointers:**
- Validation report: `project_12/reports/P4_VALIDATION_REPORT_BASELINES.md`
- Baseline artifacts: `project_12/results/repro_p4/baselines/mlp/artifact.json` (adversarial families)
- Baseline artifacts: `project_12/results/repro_p4/baselines/lstm/artifact.json` (adversarial families)
- Baseline artifacts: `project_12/results/repro_p4/baselines/transformer/artifact.json` (adversarial families)
- Repro check: `project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md`

---

## Untested Claims

### ⏳ P4-C01: Framework Execution (Infrastructure)
- Type: Weak (methodology)
- Reason untested: Infrastructure/reproducibility validation only; no empirical claim.
- Plan: May validate as part of final framework closure, not prioritized for baseline sprint.

### ⏳ P4-C04: Narrow Transfer (Intervention)
- Type: Strong
- Reason untested: Requires intervention training artifacts (Sprint 4B.2); baseline sprint excludes interventions.
- Plan: Defer to Sprint 4B.2 when intervention training reproducible artifacts available.

### ⏳ P4-C06: Baseline Reproducibility (Infrastructure)
- Type: Weak (reproducibility)
- Reason untested: Framework reproducibility validation; deprioritized for baseline sprint.
- Plan: May validate together with P4-C01 framework closure.

---

## Summary

**Overall Validation Status: ✅ 3 Claims Validated (Baseline Scope)**

- ✅ 3 empirical baseline claims validated (C02, C03, C05)
- ⏳ 1 empirical intervention claim untested (C04—requires intervention artifacts)
- ⏳ 2 infrastructure claims untested (C01, C06—deprioritized)

**Next Steps:**
- Sprint 4B.2: Reproduce intervention artifacts → validate P4-C04
- Sprint 4C.2 (optional): Infrastructure closure → validate P4-C01/C06

---

**Report Generated:** Project 12 Sprint 4C (April 2026)
**Validation Methodology:** Evidence-only validation against Project 12 baseline reproductions
**Scope:** Baseline (non-intervention) claims only
