# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 106, 'transition region': 337, 'universal region': 357}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8187 | 0.8027 | 0.8027 |
| V3.1 | 0.9313 | 0.9315 | 0.9315 |
| NN11 | 0.8812 | 0.8493 | 0.8493 |
| NN21 | 0.9537 | 0.9446 | 0.9446 |
| NN41 | 0.9800 | 0.9759 | 0.9759 |
| NN81 | 0.9862 | 0.9827 | 0.9827 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7000 | 0.5716 | 0.5716 |
| V3.1 (boundary) | 0.8850 | 0.7804 | 0.7804 |
| NN11 (boundary) | 0.8150 | 0.5868 | 0.5868 |
| NN21 (boundary) | 0.9325 | 0.7670 | 0.7670 |
| NN41 (boundary) | 0.9675 | 0.8465 | 0.8465 |
| NN81 (boundary) | 0.9775 | 0.8608 | 0.8608 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0031 |
| 41x41 | 1681 | 0.0137 |
| 81x81 | 6561 | 0.0532 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100010/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`