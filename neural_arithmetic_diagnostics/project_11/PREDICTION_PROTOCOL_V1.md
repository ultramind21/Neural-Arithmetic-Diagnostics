# PROJECT 11 PREDICTION PROTOCOL V1
## Pre-Run Prediction Discipline Under Distribution Shift

**Date:** April 2026  
**Status:** ACTIVE

---

## 1. Purpose

This protocol defines how Project 11 makes and evaluates predictions.

The goal is to prevent:
- post-hoc reinterpretation
- evaluation leakage
- and self-confirmation

---

## 2. Blind Prediction Requirement (MANDATORY)

Predictions must be made without access to:
- final region labels
- internal per-point evaluation outputs
- or direct evaluation signals

Only observable metrics (L, G, H, P) are allowed.

---

## 3. Holdout System Design Requirement (MANDATORY)

At least one holdout system must:
- preserve the local vs global tension
but modify at least one of:
- failure propagation dynamics, OR
- intervention effect structure, OR
- scoring rule

Examples:
- introduce stochastic failures
- add noise to transitions
- change dependency structure between steps
- partial observability

---

## 4. Prediction Object

Each prediction must specify:

- system identifier
- measured metrics (H, P) for that system
- predicted region label:
  - `family_aware_region`
  - `transition_region`
  - `universal_region`
- confidence (low/medium/high)

---

## 5. Sealing Rule (MANDATORY)

Before running evaluation:
1. write predictions into a submission file
2. commit that file to git
3. only then run evaluation

No edits allowed after commit.

---

## 6. One-Shot Rule

For a given prediction submission version:
- one submission
- one run
- then analysis

No iterative tweaking before recording the first outcome.

---

## 7. Evaluation Outputs

Each evaluation run must produce:
- artifact JSON
- report MD
- accuracy vs random baseline
- accuracy vs majority baseline
- boundary subset accuracy
- confusion matrix

---

## 8. Fail Policy

If predictions fail:
- do not rationalize
- revise metrics or the boundary model
- create a new submission version (V2) and repeat

---

## 9. Immediate Next Step

Define the first holdout system (V1) and the first prediction submission for it.

No grid expansion until one holdout system prediction cycle is completed.

---
