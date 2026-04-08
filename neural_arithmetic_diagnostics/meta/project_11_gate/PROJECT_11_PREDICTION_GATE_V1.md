# PROJECT 11 — PREDICTION GATE V1
## Pre-Project Gate for Predictive Escalation

**Date:** April 2026  
**Status:** ACTIVE GATE (MUST PASS BEFORE PROJECT 11)

---

## 1. Objective

Test whether the Project 10 regime/threshold/phase-structure can be used for **pre-run prediction**, not post-hoc explanation.

This gate must be passed before creating `project_11/`.

---

## 2. Prediction Task

Given unseen regime points in:

- heterogeneity (H)
- universal rescue power (P)

predict the qualitative region:

- `family_aware_region`
- `transition_region`
- `universal_region`

Predictions must be written **before** running the evaluation script.

---

## 3. Holdout Rule

Gate test points must:

- not match any previously tested exact points from Project 10 grids/refinement passes
- include both:
  - interior points (easy)
  - boundary-near points (risky)

This gate is not meant to be trivially obvious.

---

## 4. Strict Submission Rule (No Post-Hoc)

Predictions must be submitted in:

- `PROJECT_11_PREDICTIONS_SUBMISSION_V1.json`

No edits are allowed after submission.

**Commit-before-run rule:**
The predictions submission file must be committed to git before the evaluation script is executed.

---

## 5. Evaluation Metrics

Compute:

- overall accuracy
- confusion matrix
- accuracy vs random baseline (1/3)
- accuracy vs majority-class baseline
- boundary subset accuracy (on points marked as boundary probes)

---

## 6. Pass Condition (V1)

Gate is PASSED if:

- overall accuracy ≥ 0.66
AND
- boundary subset accuracy ≥ 0.50

If PASSED:
- Project 11 can be created

If FAILED:
- Project 11 must NOT be created
- theory/metrics must be revised first

---

## 7. Prohibitions

- no post-hoc adjustment
- no reinterpretation of predictions
- no selective reporting
- no creating `project_11/` before gate verdict

---

## 8. Output

The evaluation script must produce:

- JSON artifact
- Markdown report
- explicit PASS/FAIL verdict

---
