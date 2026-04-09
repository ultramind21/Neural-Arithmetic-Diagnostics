# PROJECT 11 HOLDOUT SYSTEM V1 SPEC
## Structural-OOD Rescue World with Stochastic Outcomes and Interference

**Date:** April 2026  
**Project:** 11  
**Status:** ACTIVE HOLDOUT SYSTEM SPEC

---

## 1. Purpose

Define a first **structural-OOD** evaluation system for Project 11.

This holdout must differ from Project 10 in structure, not just parameters:
- stochastic outcomes (not deterministic scoring)
- nonlinear response curves
- interference dynamics that depend on heterogeneity and family mode
- region decision based on per-family win patterns (not the same gap-threshold rule used in Project 10)

This reduces evaluation leakage.

---

## 2. Inputs (Pre-run Observable Parameters)

Each evaluation point is defined by:

- `h_scale` : heterogeneity scale (controls family-mode magnitude)
- `u_power` : universal intervention strength
- `k_interference` : how much heterogeneity suppresses universal effectiveness
- `noise_sigma` : stochasticity in outcomes
- `n_runs` : Monte Carlo runs per family

Important: we do **not** input H,P directly.  
H and P are computed **after simulation** using operational metrics.

---

## 3. Outputs (Observed Metrics)

From simulated outcomes we compute:

- per-family baseline global success: G_base[f]
- per-family universal global success: G_uni[f]
- per-family family-aware global success: G_fam[f]

Then compute:
- P_obs = mean_f (G_uni[f] - G_base[f])
- H_obs = var_f  (G_uni[f] - G_base[f])

---

## 4. Region Definition (Non-leaky style)

We decide the actual region using per-family win patterns:

Let D[f] = G_fam[f] - G_uni[f].

- family_aware_region if at least 3/4 families have D[f] > +0.01
- universal_region if at least 3/4 families have D[f] < -0.01
- transition_region otherwise

This avoids reusing Project 10's exact region logic.

---

## 5. Integrity Requirements

- Predictions must be sealed and committed before running evaluation.
- The evaluator must not reuse Project 10 evaluation functions or the same decision thresholds.

---
