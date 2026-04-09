# PROJECT 11 HOLDOUT SYSTEM V2 SPEC
## Identifiability-Preserving Structural OOD System

**Date:** April 2026  
**Project:** 11  
**Status:** ACTIVE HOLDOUT SYSTEM SPEC (V2)

---

## 1. Purpose

Holdout System V2 is designed to test whether the collapse of H in V1 was:

- an unavoidable metric failure, or
- an identifiability failure caused by V1 dynamics suppressing cross-family dispersion in Δ_uni.

V2 preserves structural-OOD properties (stochastic + nonlinear) but introduces a signed heterogeneity interaction so that increasing h_scale can produce real cross-family dispersion in universal gains.

---

## 2. Key Structural Change vs V1

In V1, universal suppression depended mainly on |mode|, which can compress per-family gains.

In V2, universal rescue is modified by a **signed mode interaction**, so different families can experience different effective universal strength.

This should allow Var_f(Δ_uni) to increase with heterogeneity when heterogeneity truly matters.

---

## 3. Inputs (Pre-run Observables)

Each point is defined by:

- h_scale
- u_power
- k_signed (strength of signed interaction)
- noise_sigma
- n_runs

No direct H/P inputs.

---

## 4. Observed Metrics

Compute from outcomes:

- Δ_uni[f] = G_uni[f] - G_base[f]
- P_obs = mean_f(Δ_uni[f])
- H_obs = var_f(Δ_uni[f])

---

## 5. Region Decision (same as V1)

Use win-pattern decision, not Project 10 gap-threshold:

Let D[f] = G_fam[f] - G_uni[f]

- family_aware_region if ≥3 families have D[f] > +0.01
- universal_region if ≥3 families have D[f] < -0.01
- transition_region otherwise

---

## 6. Immediate Next Step

Implement:

- POINTS_V2
- SEALED PREDICTIONS V2
- evaluator script V2 (artifact + report)

Then compute:
- accuracy, boundary accuracy
- spearman(h_scale, H_obs)
- spearman(u_power, P_obs)

---
