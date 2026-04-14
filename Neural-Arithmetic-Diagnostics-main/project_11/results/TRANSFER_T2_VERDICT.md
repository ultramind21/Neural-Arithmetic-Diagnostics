# PROJECT 11 — TRANSFER T2 VERDICT (STRESS TRANSFER)

**Date:** April 2026  
**Status:** CLOSED — FAIL (Predictive under stress)  
**Test:** transfer_t2

---

## 1) What was tested

Stress transfer of the **same V2 compressed inequality rule** to an extreme system (T2) with:
- significantly changed shared_failure distribution
- potential clamp saturation effects

Rule compliance was enforced:
- `project_11/experiments/transfer_t2_rule_check.py`

---

## 2) Integrity

✅ Rule-compliance: PASS  
- points checked: 20  
- mismatches: 0  

So predictions matched the V2 compressed rule exactly (no hand tuning).

---

## 3) Performance (authoritative)

From execution:
- points: 20
- model accuracy: 0.9000
- model macro-F1: 0.8491
- best baseline macro-F1: 0.7802
- PASS: False

Pass condition (locked in protocol):
- macro-F1 >= best_baseline + 0.10
- AND macro-F1 >= 0.70

Observed:
- 0.8491 >= 0.7802 + 0.10 (=0.8802)  → FALSE
- 0.8491 >= 0.70                     → TRUE

Verdict: ❌ FAIL

Artifacts:
- `project_11/results/transfer_t2_report.md`
- `project_11/results/transfer_t2_artifact.json`

---

## 4) Failure mode (mechanistic)

Two errors occurred near boundary conditions:
- t2_p08: predicted family-aware, true transition
- t2_p15: predicted transition, true universal

This suggests the V2 compressed rule has a transfer boundary when the system's shared_failure distribution becomes extreme (top-2 effects / saturation), because the Project 10-derived constants no longer approximate winner-count behavior.

---

## 5) Next step

- Do not change any T2 files.
- Update Project 11 theory to include an additional system-axis capturing shared_failure distribution / saturation potential.
- Validate revised theory on a new system (T3) not used to build the revision.

---
