# PROJECT 11 — TRANSFER T3 REPORT (Rule V3)

## Summary
- points: 20
- model accuracy: 1.0000
- model macro-F1: 1.0000
- best baseline macro-F1: 0.7802
- PASS: True

## T3 grid label counts (3x3)
- {'family-aware region': 2, 'transition region': 1, 'universal region': 6}

## Baselines
- majority label (from T3 grid): `universal region`
- majority macro-F1: 0.2222
- nearest-neighbor macro-F1: 0.7802

## Per-point table

| id | H | P | predicted | conf | true | maj | nn | gap | uni_wins | fam_wins | near_ties |
|---:|---:|---:|---|---|---|---|---|---:|---:|---:|---:|
| t3_p01 | 0.0025 | 0.285 | family-aware region | high | family-aware region | universal region | transition region | 0.0090 | 0 | 4 | 0 |
| t3_p02 | 0.0050 | 0.285 | family-aware region | high | family-aware region | universal region | transition region | 0.0110 | 0 | 4 | 0 |
| t3_p03 | 0.0095 | 0.285 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0146 | 0 | 4 | 0 |
| t3_p04 | 0.0130 | 0.285 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0174 | 0 | 4 | 0 |
| t3_p05 | 0.0180 | 0.285 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0214 | 0 | 4 | 0 |
| t3_p06 | 0.0025 | 0.305 | transition region | high | transition region | universal region | transition region | -0.0004 | 0 | 0 | 4 |
| t3_p07 | 0.0050 | 0.305 | transition region | high | transition region | universal region | transition region | 0.0016 | 0 | 0 | 4 |
| t3_p08 | 0.0095 | 0.305 | transition region | medium | transition region | universal region | family-aware region | 0.0052 | 0 | 2 | 2 |
| t3_p09 | 0.0130 | 0.305 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0080 | 0 | 4 | 0 |
| t3_p10 | 0.0180 | 0.305 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0120 | 0 | 4 | 0 |
| t3_p11 | 0.0025 | 0.335 | universal region | high | universal region | universal region | universal region | -0.0145 | 4 | 0 | 0 |
| t3_p12 | 0.0050 | 0.335 | universal region | high | universal region | universal region | universal region | -0.0125 | 4 | 0 | 0 |
| t3_p13 | 0.0095 | 0.335 | universal region | high | universal region | universal region | universal region | -0.0089 | 2 | 0 | 2 |
| t3_p14 | 0.0130 | 0.335 | universal region | high | universal region | universal region | universal region | -0.0061 | 2 | 0 | 2 |
| t3_p15 | 0.0180 | 0.335 | universal region | high | universal region | universal region | universal region | -0.0021 | 2 | 0 | 2 |
| t3_p16 | 0.0025 | 0.365 | universal region | high | universal region | universal region | universal region | -0.0286 | 4 | 0 | 0 |
| t3_p17 | 0.0050 | 0.365 | universal region | high | universal region | universal region | universal region | -0.0266 | 4 | 0 | 0 |
| t3_p18 | 0.0095 | 0.365 | universal region | high | universal region | universal region | universal region | -0.0230 | 4 | 0 | 0 |
| t3_p19 | 0.0130 | 0.365 | universal region | high | universal region | universal region | universal region | -0.0202 | 4 | 0 | 0 |
| t3_p20 | 0.0180 | 0.365 | universal region | high | universal region | universal region | universal region | -0.0162 | 3 | 0 | 1 |

Artifact JSON saved to:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_11/results/transfer_t3_artifact.json`