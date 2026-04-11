# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 110, 'transition region': 336, 'universal region': 354}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8425 | 0.8309 | 0.8309 |
| V3.1 | 0.9250 | 0.9260 | 0.9260 |
| NN11 | 0.8800 | 0.8541 | 0.8541 |
| NN21 | 0.9550 | 0.9448 | 0.9448 |
| NN41 | 0.9750 | 0.9693 | 0.9693 |
| NN81 | 0.9825 | 0.9801 | 0.9801 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7300 | 0.5973 | 0.5973 |
| V3.1 (boundary) | 0.8725 | 0.7639 | 0.7639 |
| NN11 (boundary) | 0.8075 | 0.5761 | 0.5761 |
| NN21 (boundary) | 0.9350 | 0.7275 | 0.7275 |
| NN41 (boundary) | 0.9675 | 0.8367 | 0.8367 |
| NN81 (boundary) | 0.9750 | 0.8353 | 0.8353 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0000 |
| 21x21 | 441 | 0.0038 |
| 41x41 | 1681 | 0.0145 |
| 81x81 | 6561 | 0.0528 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100005/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`