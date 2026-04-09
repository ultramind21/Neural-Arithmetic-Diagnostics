# PROJECT 11 OPERATIONAL METRICS
## Concrete Metrics for Predictive and Transfer Testing

**Date:** April 2026  
**Status:** ACTIVE

---

## 1. Purpose

Project 11 requires metrics that can travel beyond one sandbox.

This document defines **concrete** operational metrics (V1) with:
- explicit formulas
- computation steps
- defined inputs

---

## 2. Required Quantities

Project 11 needs operational measures for:

1) **Local competence saturation** (L)  
2) **Global robustness** (G)  
3) **Family-level heterogeneity** (H)  
4) **Universal rescue power** (P)

---

## 3. Global and Local Metrics (V1)

### A) Local competence (L)
**Input:** per-step or short-horizon correctness signal.

**Definition (V1):**
- \( L = \mathbb{E}[\text{local\_correct}] \)

**Saturation rule (V1):**
- "local competence saturated" if \(L \ge L_{min}\) (threshold set per system)

---

### B) Global robustness (G)
**Input:** long-horizon success per family (sequence-level or task-level).

**Definition (V1):**
- for each family \(f\): \(G_f = \mathbb{E}[\text{global\_success} \mid f]\)
- overall \(G = \mathbb{E}_f[G_f]\)

**Failure rule (V1):**
- "global robustness failure" if \(G \le G_{max}\) (threshold set per system)

---

## 4. Universal Rescue Power (P) — Effect Metric (V1)

**Goal:** measure the effect size of a universal (non-family-aware) rescue.

**Inputs:**
- per-family global success before rescue: \(G^{base}_f\)
- per-family global success after universal rescue: \(G^{uni}_f\)

**Per-family gain:**
- \(\Delta^{uni}_f = G^{uni}_f - G^{base}_f\)

**Universal rescue power:**
- \( P = \mathbb{E}_f[\Delta^{uni}_f] \)

**Computation steps:**
1. compute \(G^{base}_f\) for each family
2. apply universal rescue and compute \(G^{uni}_f\)
3. compute \(\Delta^{uni}_f\)
4. take mean across families → \(P\)

---

## 5. Family-Level Heterogeneity (H) — Response-Heterogeneity Metric (V1)

**Goal:** measure meaningful heterogeneity via intervention response, not labels.

**Definition (V1):**
- \( H = \mathrm{Var}_f(\Delta^{uni}_f) \)

**Computation steps:**
1. compute \(G^{base}_f\) for each family
2. compute \(G^{uni}_f\) for each family
3. compute gains \(\Delta^{uni}_f\)
4. compute variance of gains across families → \(H\)

---

## 6. Notes on Exportability

This (H, P) definition is exportable because:
- it uses observable outcome changes
- it does not assume family labels are intrinsically meaningful
- it can be computed in modified systems

---

## 7. Immediate Next Step

Lock:
- \(L_{min}\)
- \(G_{max}\)

for the first holdout system,
and define the first holdout system in the prediction protocol.

---
