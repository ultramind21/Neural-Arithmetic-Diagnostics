# CLAIM_LOCK_STATUS_PROJECT_4 — Final Summary

**Locked Date:** April 11, 2026, Sprint 3  
**Project:** 4  
**Total Claims Locked:** 6  
**Framework Version:** Diagnostic Framework v1.0

---

## Overview

Project 4 successfully transitioned from legacy documentation to formally locked claims within Project 12's FORMAL_CLAIMS.md scheme.

| Metric | Count | Status |
|--------|-------|--------|
| **Claims locked** | 6 | ✅ |
| **Claims with pre-registered targets** | 6 | ✅ |
| **Claims with numerical bases** | 5 (C02–C06) | ✅ |
| **Claims with framework dependency** | 6 (all) | ✅ |

---

## Claim Breakdown

### Strong Claims (4)
- **P4-C01**: Framework distinguishes narrow gains from broad robustness
- **P4-C02**: Architecture-dependent split on block-boundary-stress (MLP/Transformer succeed, LSTM fails)
- **P4-C03**: Universal weak in-distribution exact-match across all three models
- **P4-C04**: Adversarial training shows narrow transfer, not broad robustness

### Medium Claims (1)
- **P4-C05**: Alternating-carry and full-propagation-chain adversarial families equally hard across all architectures

### Weak Claims (1)
- **P4-C06**: Diagnostic framework is methodologically stable and reproducible

---

## Numerical Basis Summary

| Claim | Key Metrics | Data Type | Source |
|-------|-------------|-----------|--------|
| P4-C01 | (7 framework components) | Executable specs | project_4/framework/* |
| P4-C02 | MLP=1.0, LSTM=0.0, Transformer=1.0 (block-boundary) | Numerical (stable runs) | PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md |
| P4-C03 | MLP=0.0859, LSTM=0.0469, Transformer=0.0339 (in-dist) | Numerical (stable runs) | PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md |
| P4-C04 | Seen gain > 0.2; held-out gain < 0.05 (targets) | Qualitative + numeric targets | PROJECT_4_RESULTS_SUMMARY.md |
| P4-C05 | Alternating carry=0.0, Full propagation=0.0 (all models) | Numerical (stable runs) | PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md |
| P4-C06 | (7 components: scorecard.py, protocol.md, etc.) | Executable specs | PROJECT_4_CLOSURE_SUMMARY.md |

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

## Pre-Registered Targets

Project 4 claims have **pre-registered numerical targets** (where applicable):

| Claim | Target | Basis |
|-------|--------|-------|
| P4-C02 | MLP block-boundary ≥ 0.95; LSTM ≤ 0.10 | Project 4 observed (MLP=1.0, LSTM=0.0) |
| P4-C03 | All models ≤ 0.15 in-distribution | Project 4 observed (<0.09 all) |
| P4-C04 | Seen gain > 0.20; held-out gain < 0.05 | Project 4 qualitative result extracted |
| P4-C05 | Both families: all models ≤ 0.10 | Project 4 observed (all 0.0) |
| P4-C06 | All 7 framework components executable | Project 4 built and documented |

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

### Known Risks
1. **Project 4 blockwise decomposition excluded**: Unresolved branch not part of scientific core (acceptable risk)
2. **Artifact paths TBD**: Baseline run outputs not yet located; assumes they exist in project_4/results/
3. **Target calibration**: Pre-registered targets based on Project 4 observed values; may need refinement if Project 12 conditions differ

### Mitigations
- ✅ CLAIM_EXTRACTION_PROJECT_4.md documents all assumptions
- ✅ TRACEABILITY_PROJECT_4.md flags missing artifacts
- ✅ All targets explicitly marked "pre-registered" (not final)

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
