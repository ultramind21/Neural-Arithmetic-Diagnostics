# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 101, 'transition region': 327, 'universal region': 372}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8475 | 0.8267 | 0.8267 |
| V3.1 | 0.9450 | 0.9373 | 0.9373 |
| NN11 | 0.9075 | 0.8790 | 0.8790 |
| NN21 | 0.9637 | 0.9469 | 0.9469 |
| NN41 | 0.9875 | 0.9821 | 0.9821 |
| NN81 | 0.9862 | 0.9772 | 0.9772 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7400 | 0.6012 | 0.6012 |
| V3.1 (boundary) | 0.9025 | 0.7718 | 0.7718 |
| NN11 (boundary) | 0.8425 | 0.5942 | 0.5942 |
| NN21 (boundary) | 0.9500 | 0.7598 | 0.7598 |
| NN41 (boundary) | 0.9875 | 0.9003 | 0.9003 |
| NN81 (boundary) | 0.9775 | 0.7265 | 0.7265 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0015 |
| 21x21 | 441 | 0.0078 |
| 41x41 | 1681 | 0.0163 |
| 81x81 | 6561 | 0.0669 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100006/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`