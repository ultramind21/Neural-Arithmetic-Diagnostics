# PROJECT 11 — PHASE A TRANSFER SYNTHESIS V1

**Date:** April 2026  
**Status:** ACTIVE SYNTHESIS (Phase A)

---

## 1) What Phase A tested

Whether the compressed predictive rule (Gate V2) is:
- predictive beyond nearest-neighbor
- transferable across modified systems

---

## 2) Results (locked)

### Gate V2 (Project 10 system)
- PASS
- accuracy: 1.0000 (24/24)
- macro-F1: 1.0000
- best baseline macro-F1: 0.7077
- rule compliance: PASS

### Transfer T1 (moderate system change)
- PASS
- accuracy: 1.0000 (20/20)
- macro-F1: 1.0000
- best baseline macro-F1: 0.7802
- rule compliance: PASS

### Transfer T2 (stress system change)
- FAIL (protocol-valid fail)
- accuracy: 0.9000 (18/20)
- macro-F1: 0.8491
- best baseline macro-F1: 0.7802
- rule compliance: PASS

---

## 3) Key interpretation (mechanistic, no hype)

The V2 compressed rule is:
- strongly predictive in the Project 10 system
- perfectly transferable to T1
- but shows a measurable breakdown under stress transfer T2

This indicates a real **transfer boundary**.

Likely missing factor:
- the distribution of family shared_failure values (e.g., top-2 vs average effects)
- and saturation/clamp potential in extreme parameter regimes

Therefore:
- a purely (H, P) regime theory is insufficient under extreme family-parameter heterogeneity.
- the regime space likely requires an additional axis capturing system-level shared_failure structure.

---

## 4) Actionable next step

Define and pre-register an additional system descriptor axis (example candidates):
- shared_failure spread / variance
- top-2 shared_failure (order statistics)
- saturation potential: fraction of families likely to clamp at 1.0 under universal rescue

Then test the revised theory on a new stress system (T3) not used to design the revision.

---
