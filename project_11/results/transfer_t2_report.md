# PROJECT 11 — TRANSFER T2 REPORT

## Summary
- points: 20
- model accuracy: 0.9000
- model macro-F1: 0.8491
- best baseline macro-F1: 0.7802
- PASS: False

## T2 grid label counts (3x3)
- {'family-aware region': 2, 'transition region': 1, 'universal region': 6}

## Baselines
- majority label (from T2 grid): `universal region`
- majority macro-F1: 0.2222
- nearest-neighbor macro-F1: 0.7802

## Per-point table

| id | H | P | predicted | conf | true | maj | nn | gap | uni_wins | fam_wins | near_ties |
|---:|---:|---:|---|---|---|---|---|---:|---:|---:|---:|
| t2_p01 | 0.0022 | 0.270 | family-aware region | high | family-aware region | universal region | transition region | 0.0166 | 0 | 4 | 0 |
| t2_p02 | 0.0046 | 0.270 | family-aware region | high | family-aware region | universal region | transition region | 0.0185 | 0 | 4 | 0 |
| t2_p03 | 0.0088 | 0.270 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0219 | 0 | 4 | 0 |
| t2_p04 | 0.0124 | 0.270 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0248 | 0 | 4 | 0 |
| t2_p05 | 0.0186 | 0.270 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0297 | 0 | 4 | 0 |
| t2_p06 | 0.0022 | 0.305 | transition region | high | transition region | universal region | transition region | -0.0007 | 0 | 0 | 4 |
| t2_p07 | 0.0046 | 0.305 | transition region | high | transition region | universal region | transition region | 0.0012 | 0 | 0 | 4 |
| t2_p08 | 0.0088 | 0.305 | family-aware region | medium | transition region | universal region | family-aware region | 0.0046 | 0 | 2 | 2 |
| t2_p09 | 0.0124 | 0.305 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0074 | 0 | 4 | 0 |
| t2_p10 | 0.0186 | 0.305 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0124 | 0 | 4 | 0 |
| t2_p11 | 0.0022 | 0.335 | universal region | high | universal region | universal region | universal region | -0.0156 | 4 | 0 | 0 |
| t2_p12 | 0.0046 | 0.335 | universal region | high | universal region | universal region | universal region | -0.0136 | 4 | 0 | 0 |
| t2_p13 | 0.0088 | 0.335 | universal region | high | universal region | universal region | universal region | -0.0103 | 2 | 0 | 2 |
| t2_p14 | 0.0124 | 0.335 | universal region | high | universal region | universal region | universal region | -0.0074 | 2 | 0 | 2 |
| t2_p15 | 0.0186 | 0.335 | transition region | medium | universal region | universal region | universal region | -0.0024 | 2 | 1 | 1 |
| t2_p16 | 0.0022 | 0.375 | universal region | high | universal region | universal region | universal region | -0.0329 | 4 | 0 | 0 |
| t2_p17 | 0.0046 | 0.375 | universal region | high | universal region | universal region | universal region | -0.0309 | 4 | 0 | 0 |
| t2_p18 | 0.0088 | 0.375 | universal region | high | universal region | universal region | universal region | -0.0276 | 4 | 0 | 0 |
| t2_p19 | 0.0124 | 0.375 | universal region | high | universal region | universal region | universal region | -0.0247 | 4 | 0 | 0 |
| t2_p20 | 0.0186 | 0.375 | universal region | high | universal region | universal region | universal region | -0.0197 | 4 | 0 | 0 |

Artifact JSON saved to:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_11/results/transfer_t2_artifact.json`