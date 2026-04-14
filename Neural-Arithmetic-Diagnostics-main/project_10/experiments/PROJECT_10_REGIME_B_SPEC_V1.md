# PROJECT 10 REGIME B SPEC V1
## Synthetic Homogeneous Family Regime

**Date:** April 2026  
**Project:** 10  
**Status:** ACTIVE REGIME SPEC

---

## 1. Purpose

This document specifies Regime B, the second adversarial falsification regime for the higher-order candidate in Project 10.

Regime B is designed to test whether family-sensitive rescue is still needed when nominally distinct families are made deeply homogeneous in their actual failure mechanism.

This is a stronger pressure test than Regime A.

---

## 2. Core Idea

The higher-order candidate currently suggests that successful rescue requires alignment to heterogeneous family-level failure structure.

Regime B tests the opposite extreme:

> what if the families remain distinct at the naming or partition level, but the underlying failure mechanism is intentionally made homogeneous?

If family-sensitive rescue is no longer needed, that would pressure the current higher-order formulation.

---

## 3. Desired Construction

Regime B should create:

- multiple nominal families
- strong local competence
- weak/failing global robustness
- and one shared deeper failure mechanism across all families

Unlike Regime A, residual family-specific structure should now be reduced much further.

The goal is not just alignment.
The goal is near-homogeneity.

---

## 4. What Must Remain

To keep the regime meaningful, the construction should still preserve:

- strong local competence
- global failure before rescue
- multiple family labels or partitions

This keeps the test nontrivial.

---

## 5. What Must Change

Relative to Regime A V2, Regime B must:

- reduce residual family-specific structure much more aggressively
- make family identity less informative than shared failure structure
- create a realistic chance for universal rescue to match or beat family-aware rescue

This is what makes Regime B a stronger adversarial construction.

---

## 6. Main Test Question

The main question is:

> When family differences are mostly nominal and the deeper failure mechanism is homogeneous, does universal rescue become sufficient?

This is the key falsification pressure.

---

## 7. What Would Count Against the Higher-Order Candidate

Any of the following would strongly pressure the current higher-order candidate:

- universal rescue matches family-aware rescue across most families
- universal rescue wins broadly
- family identity stops mattering materially once failure homogeneity is enforced

These would suggest that the current formulation is too strong and needs narrowing.

---

## 8. What Would Count in Favor of the Higher-Order Candidate

Any of the following would support the current higher-order candidate:

- family-aware rescue still clearly outperforms universal rescue
- even deep homogenization fails to remove family-sensitive rescue advantage
- nominal family partition still predicts rescue outcome despite strong mechanistic homogenization

This would be a strong result.

---

## 9. Immediate Next Step

The next implementation step is:

- `project_10/experiments/project_10_regime_b_synthetic_homogeneous_families_v1.py`

This script should implement the first operational version of Regime B.

---
