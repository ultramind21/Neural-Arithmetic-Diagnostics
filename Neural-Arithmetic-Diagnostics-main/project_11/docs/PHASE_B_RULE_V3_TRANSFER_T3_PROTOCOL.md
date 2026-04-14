# PROJECT 11 — PHASE B1
## Rule V3 (System-aware) — Transfer Validation T3 (Pre-Registered)

**Date:** April 2026  
**Status:** DRAFT → LOCKED after predictions are saved  
**Test:** transfer_t3_rule_v3

---

## 0) Purpose

Transfer T2 showed V2 fails under stress because it ignores extreme shared_failure distribution effects.

This test validates a revised predictive rule:

> Rule V3 uses the system's shared_failure distribution (but not base_global) to predict region labels.

T3 is a NEW system not used in T2.

---

## 1) What stays fixed

- Region labels: {family-aware region, transition region, universal region}
- Ground truth rule remains the same (wins + gap thresholds) and uses clamp.

---

## 2) What changes (Rule V3)

Rule V3 uses system shared_failure values sf_i and computes an estimated per-family advantage:

For each family i:
- delta_i_est(H,P) = 0.80*H + (0.30 - P) * sf_i

Estimated counts:
- fam_wins_est = count(delta_i_est > 0.005)
- uni_wins_est = count(delta_i_est < -0.005)

Estimated average gap:
- gap_est = mean(delta_i_est)

Predicted region:
- family-aware region if (fam_wins_est >= 3 AND gap_est > 0.005)
- universal region if (uni_wins_est >= 2 OR gap_est < -0.003)
- else transition region

Important:
- V3 does NOT use base_global in prediction.
- V3 does NOT apply clamp in prediction.

Predictions must match Rule V3 exactly (rule-compliance enforced).

---

## 3) System + Holdout + Predictions (locked)

- System: `project_11/results/transfer_t3_system.json`
- Holdout: `project_11/results/transfer_t3_holdout_points.json`
- Predictions: `project_11/results/transfer_t3_predictions.json`

---

## 4) Ground Truth (for evaluation)

Using the T3 system parameters:

For each family:
- universal_score = clamp(base_global + P * shared_failure)
- family_aware_score = clamp(base_global + 0.30*shared_failure + 0.80*H)

Per-family winner:
- universal if uni > fam + 0.005
- family_aware if fam > uni + 0.005
- else near_tie

Region:
- family-aware region if (fam_wins >= 3 AND gap > 0.005)
- universal region if (uni_wins >= 2 OR gap < -0.003)
- else transition region

---

## 5) Baselines (required)

Baselines use a 3x3 grid (same coordinates as Project 10, but labels come from T3 ground truth):
- H in {0.003, 0.009, 0.015}
- P in {0.30, 0.36, 0.42}

Baselines:
- majority label from the T3 3x3 grid
- nearest-neighbor on the T3 3x3 grid

---

## 6) Pass Condition (LOCKED)

PASS if:
- macro-F1 >= best_baseline_macroF1 + 0.10
- AND macro-F1 >= 0.70

Otherwise FAIL.

---

## 7) Prohibitions

- No edits after lock
- No tuning after results
- No selective reporting

---
