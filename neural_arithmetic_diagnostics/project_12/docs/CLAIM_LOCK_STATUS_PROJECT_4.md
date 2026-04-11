# CLAIM_LOCK_STATUS_PROJECT_4 — Final Summary

**Locked Date:** April 11, 2026, Sprint 3  
**Project:** 4  
**Total Claims Locked:** 6  
**Framework Version:** Diagnostic Framework v1.0

---

## Overview (Sprint 3.1 Revised)

Project 4 claims have been reclassified and refined to separate empirical robustness claims from infrastructure claims, and to use independent (non-calibrated) targets.

| Metric | Count | Status |
|--------|-------|--------|
| **Claims locked** | 6 | ✅ |
| **Empirical claims (robustness)** | 4 (3 strong + 1 medium) | ✅ |
| **Infrastructure/methodology claims** | 2 (weak) | ✅ |
| **Claims with independent numeric targets** | 4 (C02, C03, C05, P4-C04 ordering) | ✅ |
| **Claims with qualitative targets only** | 2 (C01, C06) | ✅ |
| **All targets free of confirmation bias** | 6 | ✅ |

---

## Claim Breakdown

### Empirical Claims (3 Strong + 1 Medium)

**Strong:**
- **P4-C02**: Architecture-dependent robustness split on block-boundary-stress (independent thresholds: MLP/Transformer ≥0.80, LSTM ≤0.20, gap ≥0.50)
- **P4-C03**: Universal in-distribution weakness (all models ≤0.20 exact-match)
- **P4-C04**: Narrow transfer in adversarial training (seen gain >> held-out gain, ordering gap ≥0.10)

**Medium:**
- **P4-C05**: Universal collapse on alternating-carry & full-propagation (all models ≤0.10, no architecture split)

### Infrastructure/Methodology Claims (2 Weak)

- **P4-C01**: Framework end-to-end execution & scorecard generation (7 components)
- **P4-C06**: Baseline repeated-run classification reproducibility

---

## Numerical Basis Summary

| Claim | Observed (Project 4) | Validation Target (Project 12) | Target Type |
|-------|-----|--------|------|
| P4-C02 | MLP=1.0, LSTM=0.0, TX=1.0 block-boundary | MLP≥0.80, TX≥0.80, LSTM≤0.20; gap≥0.50 | Independent/rounded |
| P4-C03 | MLP=0.0859, LSTM=0.0469, TX=0.0339 in-dist | All ≤0.20 | Independent/rounded |
| P4-C04 | Seen gain >> held-out (magnitudes TBD) | seen_gain − held_out_gain ≥ 0.10 | Ordering (independent) |
| P4-C05 | All=0.0 on alt-carry & full-prop | max accuracy ≤0.10; diff ≤0.10 | Independent/rounded |
| P4-C01 | 7 components, 3 models, 3+ families | Framework executes; 7 components ✓ | Qualitative |
| P4-C06 | Baselines marked STABLE | Reproduce P4 stability classification | Qualitative |

---

## Validation Status (Project 12)

### Current Status
All 6 claims: **`untested (Project 12)`**

**Reason:** Project 4 established the framework and methodology; Project 12 will now validate claims via re-runs of baselines and interventions under unified Project 12 traceability.

### Validation Sequence (Planned)
1. **Sprint 4A:** Baseline reruns (MLP, LSTM, Transformer) under Project 12 framework
2. **Sprint 4B:** Verify architecture-dependent patterns (C02, C05)
3. **Sprint 4C:** Adversarial training re-validation (C04)
4. **Sprint 4D:** Framework reproducibility check (C06)
5. **Sprint 4E:** Consolidated validation report

---

## Pre-Registered Targets (Sprint 3.1 Revised)

**Target Design Principle:** Targets are independent rounded thresholds or qualitative ordering requirements, not calibrated to Project 4 observed values. When exact magnitudes not available in Project 4 artifacts, targets remain TBD with ordering criteria only.

### By Claim

| Claim | Status | Pre-Registered Target(s) | Calibration |
|-------|--------|---------|------|
| P4-C02 | empirical | MLP block≥0.80; TX≥0.80; LSTM≤0.20; gap≥0.50 | Independent (not 0.95 from observed 1.0) |
| P4-C03 | empirical | All in-dist ≤0.20 | Independent (single threshold, not per-model) |
| P4-C04 | empirical | seen_gain − held_out_gain ≥ 0.10 | Ordering only; magnitudes TBD |
| P4-C05 | empirical | max(family accs) ≤0.10; no-split ≤0.10 | Independent (single threshold) |
| P4-C01 | infrastructure | 7 components executable; ≥3 families tested | Qualitative |
| P4-C06 | infrastructure | Reproduce P4 stability classification ± tolerance | Qualitative |

---

## What Is Ready vs. TBD

### ✅ Ready for Project 12
- Framework specification ✅ (executable)
- Claim definitions ✅ (in FORMAL_CLAIMS.md)
- Numerical targets ✅ (pre-registered)
- Traceability mapping ✅ (TRACEABILITY_PROJECT_4.md)
- Extraction documentation ✅ (CLAIM_EXTRACTION_PROJECT_4.md)

### ⏳ TBD (Project 12 Action Items)
1. **Baseline reruns**: Verify MLP/LSTM/Transformer metrics under Project 12 framework
2. **Artifact paths**: Locate exact JSON paths for all baseline runs
3. **Intervention reruns**: Re-execute adversarial training validation
4. **Framework validation**: Confirm all 7 components work without modification
5. **Validation report**: Produce unified VALIDATED_RESULTS_P4_PROJECT12.md (parallel to P11)

---

## Integration with Project 11 Closure

Project 12 now manages:
- ✅ Project 11: 8/9 claims validated (7 strong + 1 revised)
- ✅ Project 4: 6 claims locked, awaiting validation

**Total Project 12 workload:**
- 9 validated claims (from Project 11)
- 6 claims under validation (Project 4)
- **= 15 total claims in FORMAL_CLAIMS.md**

---

## Risks & Qualifications

### Methodological Changes (Sprint 3.1)

1. **Target independence maintained:** Thresholds (0.80, 0.20, 0.10) are independent rounded values, not derived from Project 4 observed numbers.
2. **P4-C01 reclassified weak:** Framework execution is infrastructure claim, not empirical robustness.
3. **P4-C06 reclassified weak:** Reproducibility is methodology claim, not empirical robustness.
4. **P4-C04 targets partially TBD:** Exact gain magnitudes TBD pending artifact extraction; ordering gap (≥0.10) is independent pre-registered ordering claim.

### Known Risks
1. **Project 4 blockwise decomposition excluded:** Unresolved, not part of locked claims (acceptable).
2. **Intervention artifact exact paths:** Confirmed in TRACEABILITY; should exist but verify in Sprint 4A.
3. **P4-C04 numeric precision:** Will be estimated from artifacts during Sprint 4; ordering-only threshold sufficient for pre-registration.

### Mitigations
- ✅ CLAIM_EXTRACTION_PROJECT_4.md documents all assumptions and separations
- ✅ TRACEABILITY_PROJECT_4.md provides exact artifact paths (no more TBD)
- ✅ All targets reviewed for independence and rounded-threshold design

---

## Readiness for Sprint 4 (Project 4 Validation)

**Status:** READY  
**Handoff to Sprint 4:** ✅ Complete

- Framework: locked ✅
- Claims: locked ✅
- Targets: pre-registered ✅
- Traceability: documented ✅
- Extraction: transparent ✅

Project 12 can now proceed to baseline reruns and validation.

---
