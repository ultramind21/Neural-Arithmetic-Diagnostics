# PROJECT 11 — FOUNDATION
## Minimal System for Testing Metric Reality (H, P)

**Date:** April 2026  
**Status:** ACTIVE (V0.1 System)

---

## 1. Purpose

Project 11 does NOT start with large experiments.

It starts with a minimal controlled system to answer one question:

> Do H (heterogeneity) and P (universal power) represent real, stable quantities,
> or are they artifacts of a specific system design?

This FOUNDATION phase is strictly about validating metric mechanics before any prediction gate.

---

## 2. Core Variables (Control Knobs)

We define two input controls:

- **h_scale**: controls heterogeneity strength across families
- **u_power**: controls universal intervention strength

These are NOT yet validated metrics — they are control knobs.

---

## 3. Minimal System (V0.1)

We construct the simplest possible system with:

### Families:
- A
- B
- C
- D

### Each family has:
- base performance
- response to universal intervention
- response to heterogeneity

---

## 4. System Mechanics (V0.1)

### 4.1 Base Performance

Each family starts with a baseline:

G_base_f = base_f

Fixed values:

- A: 0.50
- B: 0.48
- C: 0.47
- D: 0.49

---

### 4.2 Universal Effect

Universal intervention applies equally to all families:

G_uni_f = G_base_f + U(u_power)

Where:

U(u_power) = 1 - exp(-u_power)

This ensures:
- monotonic increase
- diminishing returns
- smooth behavior

---

### 4.3 Heterogeneity Effect (CRITICAL: SIGNED)

Heterogeneity affects families differently using signed offsets:

residual_f = sign_f * h_scale

Where:

- A: +1
- B: -1
- C: +1
- D: -1

Then:

G_fam_f = G_uni_f + residual_f

This means:
- some families get a positive heterogeneity shift
- others get a negative heterogeneity shift
- heterogeneity is real (not erased by abs)

---

## 5. Observable Quantities

We define measurable outputs:

### 5.1 Universal Gain (per family)

Δ_uni_f = G_uni_f - G_base_f

---

### 5.2 Heterogeneity Gain (per family)

Δ_fam_f = G_fam_f - G_uni_f

In V0.1, this equals the signed residual:
Δ_fam_f = residual_f

---

## 6. Metrics Under Test

We test whether these definitions hold meaning:

### 6.1 Universal Power (P)

P = mean_f(Δ_uni_f)

Expected behavior:
- increases with u_power (monotonic)
- independent of h_scale (no cross-coupling)

---

### 6.2 Heterogeneity (H)

H = Var_f(Δ_fam_f)

Expected behavior:
- increases with h_scale (monotonic)
- independent of u_power (no cross-coupling)

Note:
- Because we use variance, in V0.1 we expect **H ∝ h_scale²** (quadratic growth is expected and correct).

---

## 7. Critical Test Questions

We are NOT evaluating prediction yet.

We are testing metric reality:

### Q1:
Does P track u_power monotonically?

### Q2:
Does H track h_scale monotonically?

### Q3:
Are P and H independent (no cross-coupling)?

---

## 8. Failure Conditions

The system fails if:

- P does NOT increase with u_power
- H does NOT increase with h_scale
- H depends strongly on u_power
- P depends strongly on h_scale
- H collapses to ~0 for h_scale > 0

If any of these happen:

→ The metric definitions are NOT stable.

---

## 9. Philosophy

This phase is about:

- isolating mechanics
- eliminating confounding
- testing metric validity

NOT about:
- prediction
- classification
- phase diagrams

---

## 10. Next Step (after PASS)

After V0.1 passes:

- we may introduce a slightly richer heterogeneity model (e.g., per-family weights)
- then we proceed to the Prediction Gate (pre-registered predictions before runs)

---
