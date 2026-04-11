# PROJECT 11 — TRANSFER T1 REPORT

## Summary
- points: 20
- model accuracy: 1.0000
- model macro-F1: 1.0000
- best baseline macro-F1: 0.7802
- PASS: True

## T1 grid label counts (3x3)
- {'family-aware region': 2, 'transition region': 1, 'universal region': 6}

## Baselines
- majority label (from T1 grid): `universal region`
- majority macro-F1: 0.2222
- nearest-neighbor macro-F1: 0.7802

## Per-point table

| id | H | P | predicted | conf | true | maj | nn | gap | uni_wins | fam_wins | near_ties |
|---:|---:|---:|---|---|---|---|---|---:|---:|---:|---:|
| t1_p01 | 0.0026 | 0.272 | family-aware region | high | family-aware region | universal region | transition region | 0.0135 | 0 | 4 | 0 |
| t1_p02 | 0.0054 | 0.272 | family-aware region | high | family-aware region | universal region | transition region | 0.0157 | 0 | 4 | 0 |
| t1_p03 | 0.0098 | 0.272 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0192 | 0 | 4 | 0 |
| t1_p04 | 0.0136 | 0.272 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0223 | 0 | 4 | 0 |
| t1_p05 | 0.0182 | 0.272 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0260 | 0 | 4 | 0 |
| t1_p06 | 0.0026 | 0.308 | transition region | high | transition region | universal region | transition region | -0.0012 | 0 | 0 | 4 |
| t1_p07 | 0.0054 | 0.308 | transition region | high | transition region | universal region | transition region | 0.0011 | 0 | 0 | 4 |
| t1_p08 | 0.0098 | 0.308 | transition region | medium | transition region | universal region | family-aware region | 0.0046 | 0 | 0 | 4 |
| t1_p09 | 0.0136 | 0.308 | family-aware region | medium | family-aware region | universal region | family-aware region | 0.0076 | 0 | 4 | 0 |
| t1_p10 | 0.0182 | 0.308 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0113 | 0 | 4 | 0 |
| t1_p11 | 0.0026 | 0.352 | universal region | high | universal region | universal region | universal region | -0.0191 | 4 | 0 | 0 |
| t1_p12 | 0.0054 | 0.352 | universal region | high | universal region | universal region | universal region | -0.0169 | 4 | 0 | 0 |
| t1_p13 | 0.0098 | 0.352 | universal region | high | universal region | universal region | universal region | -0.0133 | 4 | 0 | 0 |
| t1_p14 | 0.0136 | 0.352 | universal region | high | universal region | universal region | universal region | -0.0103 | 4 | 0 | 0 |
| t1_p15 | 0.0182 | 0.352 | universal region | high | universal region | universal region | universal region | -0.0066 | 3 | 0 | 1 |
| t1_p16 | 0.0026 | 0.407 | universal region | high | universal region | universal region | universal region | -0.0415 | 4 | 0 | 0 |
| t1_p17 | 0.0054 | 0.407 | universal region | high | universal region | universal region | universal region | -0.0393 | 4 | 0 | 0 |
| t1_p18 | 0.0098 | 0.407 | universal region | high | universal region | universal region | universal region | -0.0358 | 4 | 0 | 0 |
| t1_p19 | 0.0136 | 0.407 | universal region | high | universal region | universal region | universal region | -0.0327 | 4 | 0 | 0 |
| t1_p20 | 0.0182 | 0.407 | universal region | high | universal region | universal region | universal region | -0.0290 | 4 | 0 | 0 |

Artifact JSON saved to:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_11/results/transfer_t1_artifact.json`