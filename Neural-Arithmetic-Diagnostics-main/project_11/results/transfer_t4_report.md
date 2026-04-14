# PROJECT 11 — TRANSFER T4 REPORT (Rule V3)

## Summary
- points: 20
- model accuracy: 1.0000
- model macro-F1: 1.0000
- best baseline macro-F1: 0.7222
- PASS: True

## T4 grid label counts (3x3)
- {'family-aware region': 2, 'transition region': 1, 'universal region': 6}

## Baselines
- majority label (from T4 grid): `universal region`
- majority macro-F1: 0.2222
- nearest-neighbor macro-F1: 0.7222

## Per-point table

| id | H | P | predicted | conf | true | maj | nn | gap | uni_wins | fam_wins | near_ties |
|---:|---:|---:|---|---|---|---|---|---:|---:|---:|---:|
| t4_p01 | 0.0025 | 0.280 | family-aware region | high | family-aware region | universal region | transition region | 0.0118 | 0 | 4 | 0 |
| t4_p02 | 0.0055 | 0.280 | family-aware region | high | family-aware region | universal region | transition region | 0.0141 | 0 | 4 | 0 |
| t4_p03 | 0.0095 | 0.280 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0164 | 0 | 4 | 0 |
| t4_p04 | 0.0135 | 0.280 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0189 | 0 | 4 | 0 |
| t4_p05 | 0.0185 | 0.280 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0219 | 0 | 4 | 0 |
| t4_p06 | 0.0025 | 0.310 | transition region | high | transition region | universal region | transition region | -0.0021 | 0 | 0 | 4 |
| t4_p07 | 0.0055 | 0.310 | transition region | high | transition region | universal region | transition region | 0.0002 | 0 | 0 | 4 |
| t4_p08 | 0.0095 | 0.310 | transition region | high | transition region | universal region | family-aware region | 0.0026 | 0 | 0 | 4 |
| t4_p09 | 0.0135 | 0.310 | transition region | medium | transition region | universal region | family-aware region | 0.0050 | 0 | 2 | 2 |
| t4_p10 | 0.0185 | 0.310 | family-aware region | high | family-aware region | universal region | family-aware region | 0.0080 | 0 | 3 | 1 |
| t4_p11 | 0.0025 | 0.350 | universal region | high | universal region | universal region | universal region | -0.0144 | 3 | 0 | 1 |
| t4_p12 | 0.0055 | 0.350 | universal region | high | universal region | universal region | universal region | -0.0121 | 3 | 0 | 1 |
| t4_p13 | 0.0095 | 0.350 | universal region | high | universal region | universal region | universal region | -0.0097 | 3 | 0 | 1 |
| t4_p14 | 0.0135 | 0.350 | universal region | high | universal region | universal region | universal region | -0.0073 | 1 | 0 | 3 |
| t4_p15 | 0.0185 | 0.350 | universal region | high | universal region | universal region | universal region | -0.0043 | 1 | 0 | 3 |
| t4_p16 | 0.0025 | 0.410 | universal region | high | universal region | universal region | universal region | -0.0312 | 3 | 0 | 1 |
| t4_p17 | 0.0055 | 0.410 | universal region | high | universal region | universal region | universal region | -0.0289 | 3 | 0 | 1 |
| t4_p18 | 0.0095 | 0.410 | universal region | high | universal region | universal region | universal region | -0.0265 | 3 | 0 | 1 |
| t4_p19 | 0.0135 | 0.410 | universal region | high | universal region | universal region | universal region | -0.0241 | 3 | 0 | 1 |
| t4_p20 | 0.0185 | 0.410 | universal region | high | universal region | universal region | universal region | -0.0211 | 3 | 0 | 1 |

Artifact JSON saved to:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_11/results/transfer_t4_artifact.json`