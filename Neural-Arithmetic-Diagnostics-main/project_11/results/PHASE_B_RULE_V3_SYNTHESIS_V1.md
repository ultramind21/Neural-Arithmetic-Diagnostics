# PROJECT 11 — PHASE B SYNTHESIS V1 (Rule V3)

**Date:** April 2026  
**Status:** ACTIVE SYNTHESIS (Phase B)

---

## 1) Why Phase B exists

Phase A showed:
- Rule V2 works in several systems
- but fails under stress (T2) due to extreme shared_failure distribution / top-2 effects

Phase B introduced Rule V3:
- system-aware (uses shared_failure distribution)
- still compact (inequality + win-count logic)
- predictions do NOT use base_global, do NOT use clamp

---

## 2) Locked results

### Transfer T2 (Rule V2) — FAIL (stress boundary)
- macro-F1: 0.8491
- best baseline macro-F1: 0.7802
- PASS: False
- failure concentrated near boundary + extreme shared_failure effects

### Transfer T3 (Rule V3) — PASS (new system)
- accuracy: 1.0000 (20/20)
- macro-F1: 1.0000
- best baseline macro-F1: 0.7802
- rule compliance: PASS

### Transfer T4 (Rule V3) — PASS (new stress system)
- accuracy: 1.0000 (20/20)
- macro-F1: 1.0000
- best baseline macro-F1: 0.7222
- rule compliance: PASS

---

## 3) Key scientific takeaways (no hype)

1) A purely (H,P) rule with fixed shared_failure constants (Rule V2) has a real transfer boundary under stress.
2) Adding a system-level descriptor (the actual shared_failure distribution) enables robust transfer (Rule V3).
3) Current evidence supports a regime theory that is:
   - predictive
   - compact
   - but not fully "universal" without specifying system family/mechanics.

---

## 4) What is still missing

- Larger-scale validation (hundreds of points), especially near decision boundaries.
- Geometry-break / identifiability tests:
  - measurement noise on H,P
  - coordinate corruption / monotone transforms
  - mechanism shifts (nonlinear universal effect, interactions, etc.)

---

## 5) Next planned step

Run **T4-Large (500 points)**:
- same T4 system
- half uniform sampling, half boundary-focused sampling
- stronger NN baseline using a denser 11×11 grid

Then proceed to Phase C (geometry-break tests).

---
