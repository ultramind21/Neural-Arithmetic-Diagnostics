# PROJECT 11 — PREDICTION GATE V2 VERDICT

**Date:** April 2026  
**Status:** CLOSED — PASS  
**Gate:** prediction_gate_v2

---

## 1) What Gate V2 tested

Whether a **compressed boundary rule** (inequalities) can predict Project 10 regions in (H, P) space **beyond nearest-neighbor interpolation**.

- H := residual_abs
- P := universal_power

Ground truth is unchanged (Project 10 rule):
- `project_11/docs/PREDICTION_GATE_V1_GROUND_TRUTH_RULE.md`

Protocol (locked):
- `project_11/docs/PREDICTION_GATE_V2_PROTOCOL.md`

Holdout (locked):
- `project_11/results/prediction_gate_v2_holdout_points.json`

Predictions (locked):
- `project_11/results/prediction_gate_v2_predictions.json`

---

## 2) Result (authoritative)

From execution:
- points: 24
- model accuracy: 1.0000
- model macro-F1: 1.0000
- best baseline macro-F1: 0.7077
- PASS: True

Artifacts:
- `project_11/results/prediction_gate_v2_report.md`
- `project_11/results/prediction_gate_v2_artifact.json`

---

## 3) Pass condition (locked)

PASS requires:
- macro-F1 >= best_baseline_macroF1 + 0.15
- AND macro-F1 >= 0.80

Observed:
- 1.0000 >= 0.7077 + 0.15 → TRUE
- 1.0000 >= 0.80 → TRUE

Verdict: ✅ PASS

---

## 4) Integrity requirement (non-negotiable)

Because V2 claims a compressed inequality rule, we require a post-run compliance check:

- The locked predictions file must match the protocol's compressed rule.

If mismatch exists, the gate is considered protocol-invalid even if metrics are high.

(Compliance is checked by: `project_11/experiments/prediction_gate_v2_rule_check.py`)

---
