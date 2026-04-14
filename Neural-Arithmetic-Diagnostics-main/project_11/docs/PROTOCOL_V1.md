# PROJECT 11 — PROTOCOL V1
## Prediction Gate V1 (Pre-Registered)

**Date:** April 2026  
**Status:** DRAFT → LOCKED after submission  
**Scope:** Gate only (no Project 11 expansion allowed before PASS)

---

## 0) Core Principle

This gate tests **pre-run prediction**.

- Predictions must be written and locked BEFORE any evaluation runs.
- No post-hoc reinterpretation.
- No selective reporting.

If this gate fails: Project 11 must not proceed to full regime theory.

---

## 1) Objective

Test whether the **Project 10 phase-structure** can be used to predict outcomes for unseen regime points in (H, P), **before running experiments**.

---

## 2) Prediction Task

For each unseen point (H, P), predict the region label:

- **Family-aware region**
- **Transition region**
- **Universal region**

Predictions must be produced BEFORE running the evaluation experiments.

---

## 3) Ground Truth (Locked Rule)

Ground-truth region labels must be computed using:
- the same operational metrics used in Project 10
- the same evaluation pipeline used in Project 10
- and a deterministic labeling rule (thresholds/criteria) that is written down BEFORE the runs

**No manual region labeling is allowed.**

> NOTE: The deterministic labeling rule will be filled in after extracting the exact Project 10 operational definitions and thresholds from the repository docs/scripts, but MUST be locked before evaluation.

---

## 4) Holdout Rule (Anti-Leakage)

Holdout (H, P) points must be:
- outside the exact grids used in Project 10
- outside refinement bands used in Project 10
- not used in any threshold estimation, law extraction, or theory refinement

All holdout points must be listed explicitly and locked in a JSON file before any run.

---

## 5) Prediction Lock Format (STRICT)

Create:
- `project_11/results/prediction_gate_v1_predictions.json`

For each point:
- H
- P
- predicted_region
- confidence: low | medium | high
- optional_notes

**No edits after lock.**

Lock mechanism:
- commit the JSON file
- record the commit hash in the gate report

---

## 6) Evaluation Outputs (Required)

After running:
- accuracy
- macro-F1
- confusion matrix
- full per-point table (H, P, predicted, true, confidence)

All points must be evaluated. No dropping.

---

## 7) Baselines (Minimum)

We compare predictions against:
1) Majority-class baseline
2) Nearest-neighbor baseline from Project 10 labeled grid

(Additional baselines may be added later, but these two are mandatory for V1.)

---

## 8) Pass Condition (Locked)

Gate PASSES if:
- macro-F1 ≥ (best baseline macro-F1 + 0.15)
- AND macro-F1 ≥ 0.60
- AND no evidence of leakage or post-hoc edits

Otherwise: FAIL.

---

## 9) Prohibitions

- No post-hoc adjustment of thresholds
- No reinterpretation of region labels
- No selective reporting
- No "we meant a different region" explanations

---

## 10) Artifacts (Paths)

- Predictions (locked):
  - `project_11/results/prediction_gate_v1_predictions.json`

- Gate report (generated after runs):
  - `project_11/results/prediction_gate_v1_report.md`

- Evaluation script(s):
  - to be created after ground-truth rule is locked

---
