# PROJECT 11 HOLDOUT SYSTEM V1 MECHANISTIC DIAGNOSIS
## Why P Survived and H Collapsed (Code-Linked)

**Date:** April 2026  
**Project:** 11  
**Status:** COMPLETE MECHANISTIC DIAGNOSIS (V1)

---

## 1. Purpose

This document explains, using the actual evaluator code, why:

- P_obs retained a strong monotonic relationship with u_power
- H_obs collapsed and did not track h_scale

This is not a numeric summary. It is a mechanism-level explanation.

---

## 2. What Survived vs Collapsed (Observed)

From diagnostics:

- Spearman(u_power, P_obs) ≈ strong positive
- Spearman(h_scale, H_obs) ≈ ~0

Therefore:
- P is a robust signal under this holdout system
- H (as currently defined) is not

All claims are bounded to:
> under Holdout System V1 and current metric definitions.

---

## 3. Mechanistic Path for P (Why It Survives)

### Where u_power enters the system
In `project_11_holdout_system_v1_eval.py`, universal rescue probability is controlled via:

- `u_power` influences `eff_u`
- `eff_u` influences `uni_logit_delta`
- `uni_logit_delta` shifts `uni_p`
- Monte Carlo rollouts produce `G_uni`
- `P_obs` is computed as mean_f (G_uni - G_base)

### Why this tends to preserve monotonicity
Even with noise and nonlinearities:
- increasing `u_power` tends to increase `eff_u` (when not fully suppressed)
- increased `eff_u` tends to increase `G_uni` on average
- therefore mean universal gain tends to track u_power

This explains why P_obs can remain strongly correlated with u_power.

---

## 4. Mechanistic Path for H (Why It Collapses)

### How H is defined
In this experiment:
- gains per family are computed: Δ_uni[f] = G_uni[f] - G_base[f]
- H_obs is computed as Var_f(Δ_uni[f])

Therefore, H_obs can only track h_scale if h_scale produces meaningful cross-family dispersion in Δ_uni.

### Why cross-family dispersion can collapse
In this holdout system:

1) The interference term depends on the per-family `mode` magnitude.
2) If the per-family mode magnitude is effectively similar across families in a given point,
   then suppression of universal rescue becomes similar across families.
3) If Δ_uni[f] becomes similar across families, Var_f(Δ_uni[f]) becomes small.
4) Nonlinear saturation (sigmoid) and stochastic averaging can further compress differences.

Therefore, even if h_scale changes, H_obs can fail to track it because the metric requires cross-family dispersion that is not reliably generated under this system.

This is an identifiability problem:
- the system may still contain heterogeneity,
- but this particular H definition fails to preserve it under these dynamics.

---

## 5. Key Conclusion (Bounded)

The correct safe statement is:

> Under Holdout System V1, P_obs remains an identifiable and robust effect metric for universal rescue, but H_obs (defined as Var_f(Δ_uni)) collapses because the system does not reliably induce cross-family dispersion in Δ_uni as h_scale varies.

---

## 6. Implication for Next Step

This implies Project 11 must choose one controlled next move:

### Option A — Metric Revision V2
Define a heterogeneity metric that remains informative even when Δ_uni dispersion is suppressed.

### Option B — Holdout System V2 (Identifiability-Preserving)
Modify the holdout system so that changing h_scale reliably produces cross-family dispersion in Δ_uni, making H_obs track heterogeneity.

No mixed uncontrolled changes.

---
