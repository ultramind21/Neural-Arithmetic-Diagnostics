# PROJECT 10 THRESHOLD REFINEMENT PLAN V1
## From Coarse Regime Map to Sharper Transition Structure

**Date:** April 2026  
**Project:** 10  
**Status:** ACTIVE THRESHOLD REFINEMENT PLAN

---

## 1. Purpose

This document defines the next refinement step after the first coarse 3x3 regime-space map in Project 10.

The purpose is not to expand the map blindly.

It is to sharpen the transition zones that now appear to control the most important changes in rescue behavior.

---

## 2. Why Refinement Is Needed

The current regime map already shows a strong pattern:

- family-aware advantage at baseline under medium/high heterogeneity
- boundary behavior at low heterogeneity with baseline power
- universal dominance once universal power is increased

This is important, but still coarse.

To build a stronger theory, Project 10 now needs to ask:

> where exactly do these transitions happen?

That is the goal of threshold refinement.

---

## 3. Main Refinement Targets

The current map suggests at least two important transition zones.

### A. Heterogeneity transition zone
At baseline universal power:
- low heterogeneity gives a boundary result
- medium heterogeneity gives family-aware advantage

This suggests a threshold may exist between low and medium heterogeneity.

### B. Universal power transition zone
At medium and high heterogeneity:
- baseline power gives family-aware advantage
- moderate power gives universal dominance

This suggests a threshold may exist between baseline and moderate universal power.

These two transition zones are the most important current targets.

---

## 4. Refinement Principle

Refinement should focus on:

- adding more values near the suspected transition boundaries
- not adding arbitrary values everywhere
- preserving interpretability
- and identifying where verdicts flip:
  - support
  - boundary
  - weaken

This is boundary-focused refinement.

---

## 5. First Refinement Strategy

The first refinement pass should likely:

### For heterogeneity
Test intermediate values between:
- 0.003 and 0.009

### For universal power
Test intermediate values between:
- 0.30 and 0.36

These are the most meaningful first refinements.

---

## 6. What the Refinement Should Produce

The next refinement should produce:

1. a finer local map around suspected thresholds
2. a clearer sense of where family-aware advantage begins
3. a clearer sense of where universal dominance begins
4. a better theory of rescue transition structure

This is the immediate scientific value.

---

## 7. Immediate Next Step

The next implementation step is:

- `project_10/experiments/project_10_phase2_threshold_refinement_v1.py`

This script should probe the first local transition zones near the current boundaries.

---
