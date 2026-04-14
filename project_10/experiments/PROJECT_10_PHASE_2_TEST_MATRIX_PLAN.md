# PROJECT 10 PHASE 2 TEST MATRIX PLAN
## Mapping the Revised Higher-Order Candidate

**Date:** April 2026  
**Project:** 10  
**Status:** ACTIVE PHASE 2 TEST MATRIX PLAN

---

## 1. Purpose

This document defines the first structured test matrix for Phase 2 of Project 10.

The purpose is to test the revised higher-order candidate not through one isolated regime, but through a controlled landscape of conditions.

This is necessary because the revised candidate is now:
- bounded
- comparative
- and threshold-sensitive

---

## 2. Active Candidate

The Phase 2 target remains:

> When local competence saturates without global robustness, family-aligned rescue tends to outperform universal rescue when family-level failure heterogeneity is substantive and universal mechanism power is not sufficient to override that heterogeneity.

This is the candidate the matrix should test.

---

## 3. Main Axes of the Matrix

Phase 2 should vary at least two central dimensions.

### Axis A — Heterogeneity Level
Possible levels:

- **Low heterogeneity**
- **Medium heterogeneity**
- **High heterogeneity**

This tests how much family-level differentiation is needed before family-aware rescue gains an advantage.

---

### Axis B — Universal Rescue Power
Possible levels:

- **Baseline power**
- **Moderately amplified power**
- **Strongly amplified power**

This tests when universal rescue becomes competitive, tied, or dominant.

---

## 4. Matrix Logic

The matrix should therefore contain regime cells formed by:

- heterogeneity level × universal rescue power

A minimal first matrix would include:

| Heterogeneity | Universal Power |
|--------------|-----------------|
| Low | Baseline |
| Low | Moderate |
| Low | Strong |
| Medium | Baseline |
| Medium | Moderate |
| Medium | Strong |
| High | Baseline |
| High | Moderate |
| High | Strong |

This creates a 3x3 test map.

---

## 5. What the Matrix Should Reveal

The matrix should help reveal:

1. where family-aware rescue clearly wins
2. where results become near-ties
3. where universal rescue overtakes
4. where the revised higher-order candidate holds
5. where it weakens
6. and where its boundary lies

This is the central Phase 2 objective.

---

## 6. Minimal Interpretation Scheme

Each matrix cell should be interpreted using at least one of:

- **supports revised candidate**
- **boundary / mixed**
- **weakens revised candidate**

This keeps the matrix aligned with Project 10's bounded-theory discipline.

---

## 7. Immediate Next Step

The next implementation step is:

- `project_10/experiments/project_10_phase2_threshold_matrix_v1.py`

This script should build the first minimal 3x3 threshold matrix.

---
