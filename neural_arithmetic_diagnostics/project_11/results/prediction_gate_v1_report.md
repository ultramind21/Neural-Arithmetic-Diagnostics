# PROJECT 11 — PREDICTION GATE V1 REPORT

## Summary
- points: 16
- model accuracy: 0.8125
- model macro-F1: 0.7460
- best baseline macro-F1: 0.7460
- PASS: False

## Baselines
- majority label (from Project 10 grid): `universal region`
- majority baseline macro-F1: 0.2222
- nearest-neighbor baseline macro-F1: 0.7460

## Per-point table

| id | H | P | predicted | conf | true | maj | nn | gap | uni_wins | fam_wins | near_ties |
|---:|---:|---:|---|---|---|---|---|---:|---:|---:|---:|
| p01 | 0.0035 | 0.290 | transition region | high | family-aware region | universal region | transition region | 0.0069 | 0 | 4 | 0 |
| p02 | 0.0055 | 0.290 | transition region | medium | family-aware region | universal region | transition region | 0.0084 | 0 | 4 | 0 |
| p03 | 0.0105 | 0.290 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0124 | 0 | 4 | 0 |
| p04 | 0.0140 | 0.290 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0152 | 0 | 4 | 0 |
| p05 | 0.0035 | 0.310 | transition region | high | transition region | universal region | transition region | -0.0012 | 0 | 0 | 4 |
| p06 | 0.0055 | 0.310 | transition region | low | transition region | universal region | transition region | 0.0003 | 0 | 0 | 4 |
| p07 | 0.0105 | 0.310 | family-aware region | high | transition region | universal region | family-aware region | 0.0043 | 0 | 0 | 4 |
| p08 | 0.0140 | 0.310 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0071 | 0 | 4 | 0 |
| p09 | 0.0035 | 0.370 | universal region | high | universal region | universal region | universal region | -0.0255 | 4 | 0 | 0 |
| p10 | 0.0055 | 0.370 | universal region | high | universal region | universal region | universal region | -0.0240 | 4 | 0 | 0 |
| p11 | 0.0105 | 0.370 | universal region | high | universal region | universal region | universal region | -0.0200 | 4 | 0 | 0 |
| p12 | 0.0140 | 0.370 | universal region | high | universal region | universal region | universal region | -0.0171 | 4 | 0 | 0 |
| p13 | 0.0035 | 0.410 | universal region | high | universal region | universal region | universal region | -0.0417 | 4 | 0 | 0 |
| p14 | 0.0055 | 0.410 | universal region | high | universal region | universal region | universal region | -0.0402 | 4 | 0 | 0 |
| p15 | 0.0105 | 0.410 | universal region | high | universal region | universal region | universal region | -0.0362 | 4 | 0 | 0 |
| p16 | 0.0140 | 0.410 | universal region | high | universal region | universal region | universal region | -0.0333 | 4 | 0 | 0 |

## Notes
- Ground truth uses the exact Project 10 phase-diagram rule (wins + gap thresholds).
- Predictions were loaded from the locked JSON file; integrity checks enforce id and H,P match.

Artifact JSON saved to:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_11/results/prediction_gate_v1_artifact.json`