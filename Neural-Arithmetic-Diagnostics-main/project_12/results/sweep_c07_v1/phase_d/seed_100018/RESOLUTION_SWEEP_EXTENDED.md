# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 110, 'transition region': 322, 'universal region': 368}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8538 | 0.8371 | 0.8371 |
| V3.1 | 0.9525 | 0.9475 | 0.9475 |
| NN11 | 0.9025 | 0.8697 | 0.8697 |
| NN21 | 0.9537 | 0.9365 | 0.9365 |
| NN41 | 0.9762 | 0.9732 | 0.9732 |
| NN81 | 0.9862 | 0.9800 | 0.9800 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7750 | 0.6665 | 0.6665 |
| V3.1 (boundary) | 0.9300 | 0.8558 | 0.8558 |
| NN11 (boundary) | 0.8500 | 0.6079 | 0.6079 |
| NN21 (boundary) | 0.9250 | 0.7389 | 0.7389 |
| NN41 (boundary) | 0.9625 | 0.8861 | 0.8861 |
| NN81 (boundary) | 0.9750 | 0.8957 | 0.8957 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0036 |
| 41x41 | 1681 | 0.0135 |
| 81x81 | 6561 | 0.0528 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100018/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`