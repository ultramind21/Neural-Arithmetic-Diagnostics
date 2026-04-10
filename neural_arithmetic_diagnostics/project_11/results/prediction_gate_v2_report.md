# PROJECT 11 — PREDICTION GATE V2 REPORT

## Summary
- points: 24
- model accuracy: 1.0000
- model macro-F1: 1.0000
- best baseline macro-F1: 0.7077
- PASS: True

## Baselines
- majority label: `universal region`
- majority macro-F1: 0.1505
- nearest-neighbor macro-F1: 0.7077

## Per-point table

| id | H | P | predicted | conf | true | maj | nn | gap | uni_wins | fam_wins | near_ties |
|---:|---:|---:|---|---|---|---|---|---:|---:|---:|---:|
| v2_p01 | 0.0028 | 0.275 | family-aware region | high | family-aware region | universal region | transition region | 0.0124 | 0 | 4 | 0 |
| v2_p02 | 0.0048 | 0.275 | family-aware region | high | family-aware region | universal region | transition region | 0.0140 | 0 | 4 | 0 |
| v2_p03 | 0.0082 | 0.275 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0167 | 0 | 4 | 0 |
| v2_p04 | 0.0118 | 0.275 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0196 | 0 | 4 | 0 |
| v2_p05 | 0.0165 | 0.275 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0233 | 0 | 4 | 0 |
| v2_p06 | 0.0190 | 0.275 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0253 | 0 | 4 | 0 |
| v2_p07 | 0.0028 | 0.295 | transition region | medium | transition region | universal region | transition region | 0.0043 | 0 | 0 | 4 |
| v2_p08 | 0.0048 | 0.295 | family-aware region | high | family-aware region | universal region | transition region | 0.0059 | 0 | 4 | 0 |
| v2_p09 | 0.0082 | 0.295 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0086 | 0 | 4 | 0 |
| v2_p10 | 0.0118 | 0.295 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0115 | 0 | 4 | 0 |
| v2_p11 | 0.0165 | 0.295 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0152 | 0 | 4 | 0 |
| v2_p12 | 0.0190 | 0.295 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0172 | 0 | 4 | 0 |
| v2_p13 | 0.0028 | 0.315 | universal region | medium | universal region | universal region | transition region | -0.0038 | 0 | 0 | 4 |
| v2_p14 | 0.0048 | 0.315 | transition region | medium | transition region | universal region | transition region | -0.0022 | 0 | 0 | 4 |
| v2_p15 | 0.0082 | 0.315 | transition region | high | transition region | universal region | family-aware region | 0.0005 | 0 | 0 | 4 |
| v2_p16 | 0.0118 | 0.315 | transition region | high | transition region | universal region | family-aware region | 0.0034 | 0 | 0 | 4 |
| v2_p17 | 0.0165 | 0.315 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0071 | 0 | 4 | 0 |
| v2_p18 | 0.0190 | 0.315 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0091 | 0 | 4 | 0 |
| v2_p19 | 0.0028 | 0.345 | universal region | high | universal region | universal region | universal region | -0.0160 | 4 | 0 | 0 |
| v2_p20 | 0.0048 | 0.345 | universal region | high | universal region | universal region | universal region | -0.0144 | 4 | 0 | 0 |
| v2_p21 | 0.0082 | 0.345 | universal region | high | universal region | universal region | universal region | -0.0117 | 4 | 0 | 0 |
| v2_p22 | 0.0118 | 0.345 | universal region | high | universal region | universal region | universal region | -0.0088 | 4 | 0 | 0 |
| v2_p23 | 0.0165 | 0.345 | universal region | high | universal region | universal region | universal region | -0.0050 | 2 | 0 | 2 |
| v2_p24 | 0.0190 | 0.345 | universal region | high | universal region | universal region | universal region | -0.0030 | 0 | 0 | 4 |

Artifact JSON saved to:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_11/results/prediction_gate_v2_artifact.json`