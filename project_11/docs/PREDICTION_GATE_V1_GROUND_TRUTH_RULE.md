# PROJECT 11 — PREDICTION GATE V1
## Ground Truth Rule (LOCKED from Project 10 Code)

**Date:** April 2026  
**Status:** LOCKED (Do not edit after Gate start)  
**Source of Truth:** `project_10/experiments/project_10_phase_diagram_refinement_v1.py`

---

## 0) Definitions (What H and P mean in Gate V1)

In Prediction Gate V1, we use the exact Project 10 control-space:

- **H := residual_abs** (family-level heterogeneity magnitude)
- **P := universal_power** (universal rescue power parameter)

So each evaluation point is a pair:

> (H, P) = (residual_abs, universal_power)

This matches the Project 10 Phase 2 threshold matrix and refinement scripts.

---

## 1) Base Cases (Project 10)

Families and fixed base parameters:

- A: base_global=0.48, shared_failure=0.41
- B: base_global=0.47, shared_failure=0.40
- C: base_global=0.46, shared_failure=0.41
- D: base_global=0.47, shared_failure=0.40

Residual signs (not used by family-aware because abs is taken, but retained for fidelity):
- signs = [ +1, -1, +1, -1 ]

Clamping:
- clamp(x) := min(1.0, max(0.0, x))

---

## 2) Scoring Functions (Project 10)

### 2.1 Universal rescue score
For each family:

universal_score = clamp(base_global + universal_power * shared_failure)

### 2.2 Family-aware rescue score
For each family:

family_aware_score = clamp(base_global + 0.30 * shared_failure + 0.80 * residual_abs)

Note:
- This uses residual_abs (magnitude), not signed residual.

---

## 3) Per-Family Winner Rule (Project 10)

For each family:

- if universal_score > family_aware_score + 0.005:
  winner = "universal"
- else if family_aware_score > universal_score + 0.005:
  winner = "family_aware"
- else:
  winner = "near_tie"

Counts:
- universal_wins = number of families with winner="universal"
- family_aware_wins = number of families with winner="family_aware"
- near_ties = number of families with winner="near_tie"

---

## 4) Aggregate Gap (Project 10)

Compute:

avg_universal_score = mean(universal_score over families)  
avg_family_aware_score = mean(family_aware_score over families)  
gap = avg_family_aware_score - avg_universal_score

---

## 5) Region Label Rule (Ground Truth)

This is the LOCKED ground-truth region rule:

### 5.1 Family-aware region
Label is **"family-aware region"** if:

- family_aware_wins >= 3
- AND gap > 0.005

### 5.2 Universal region
Label is **"universal region"** if:

- universal_wins >= 2
- OR gap < -0.003

### 5.3 Transition region
Otherwise label is:

- **"transition region"**

This is copied from the Project 10 phase diagram refinement logic.

---

## 6) Holdout Constraints (Anti-Leakage)

Holdout points (H, P) must be:

### 6.1 Not equal to Project 10 grid values
H must not equal: {0.003, 0.009, 0.015}  
P must not equal: {0.30, 0.36, 0.42}

### 6.2 Outside transition-band densification intervals (strict)
Because Project 10 densified these transition bands:

- H band at baseline power (from `build_heterogeneity_band_probe`):
  H in [0.0060, 0.0075] is considered "refinement band" and is disallowed for holdout.

- P band at medium/high heterogeneity (from `build_power_band_probe`):
  P in [0.320, 0.340] is considered "refinement band" and is disallowed for holdout.

Additionally, exact refinement probe points from `project_10_phase2_threshold_refinement_v1.py` are disallowed.

---

## 7) Non-Negotiable Integrity Rules

- Ground-truth rule cannot be changed after predictions are locked.
- Holdout points cannot be changed after predictions are locked.
- Predictions cannot be edited after lock.

---
