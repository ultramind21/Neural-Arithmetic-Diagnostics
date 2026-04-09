# PROJECT 11 HOLDOUT SYSTEM V1 METRIC COLLAPSE DIAGNOSIS
## Why (H,P) Failed to Transfer Under Structural OOD

**Date:** April 2026  
**Project:** 11  
**Status:** COMPLETE DIAGNOSIS (V1)

---

## 1. Purpose

This document records the metric-collapse diagnosis for Holdout System V1.

The goal is to answer:

- what failed?
- why did it fail?
- what does this imply for Project 11 next steps?

All claims must be bounded:

> under this system and this definition

No absolute statements.

---

## 2. Inputs vs Observed Metrics

We record:

- input controls: `h_scale`, `u_power`
- observed metrics extracted from outcomes: `H_obs`, `P_obs`

Key observation:
- `H_obs` values are small and do not track `h_scale` cleanly
- `P_obs` values do not track `u_power` in a clean monotonic way

This is evidence that the current (H,P) representation is not invariant under this OOD system.

---

## 3. What This Means

This implies:

1) The theory is not automatically transferable by carrying over a boundary from Project 10.
2) The representation layer (the operationalization of heterogeneity and universal power) is fragile under structural changes.
3) Project 11 must now decide between:
   - revising metrics
   - revising the holdout system design to make heterogeneity identifiable under the allowed observables
   - or expanding observables (explicitly) as part of the theory

---

## 4. Strict Interpretation Clause

The correct safe statement is:

> Under Holdout System V1 and the current operational definitions, (H,P) fails to preserve heterogeneity and universal-power information in a way that supports the Project 10 boundary intuition.

---

## 5. Immediate Next Step

Compute correlation-style diagnostics (monotonicity / rank correlation) rather than raw MAE comparisons.

Then choose one controlled path:
- Metric Revision V2
or
- Holdout System V2 with identifiability improvements

No mixed uncontrolled changes.

---
