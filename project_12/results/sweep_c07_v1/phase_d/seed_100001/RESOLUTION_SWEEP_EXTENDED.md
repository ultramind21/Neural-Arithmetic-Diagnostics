# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 96, 'transition region': 332, 'universal region': 372}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8450 | 0.8338 | 0.8338 |
| V3.1 | 0.9400 | 0.9357 | 0.9357 |
| NN11 | 0.9062 | 0.8724 | 0.8724 |
| NN21 | 0.9537 | 0.9345 | 0.9345 |
| NN41 | 0.9725 | 0.9626 | 0.9626 |
| NN81 | 0.9862 | 0.9796 | 0.9796 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7325 | 0.6067 | 0.6067 |
| V3.1 (boundary) | 0.9000 | 0.7751 | 0.7751 |
| NN11 (boundary) | 0.8600 | 0.6042 | 0.6042 |
| NN21 (boundary) | 0.9425 | 0.7791 | 0.7791 |
| NN41 (boundary) | 0.9575 | 0.7884 | 0.7884 |
| NN81 (boundary) | 0.9750 | 0.8577 | 0.8577 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0000 |
| 21x21 | 441 | 0.0031 |
| 41x41 | 1681 | 0.0145 |
| 81x81 | 6561 | 0.0533 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100001/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`