# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 108, 'transition region': 318, 'universal region': 374}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8525 | 0.8349 | 0.8349 |
| V3.1 | 0.9563 | 0.9561 | 0.9561 |
| NN11 | 0.8938 | 0.8652 | 0.8652 |
| NN21 | 0.9637 | 0.9536 | 0.9536 |
| NN41 | 0.9800 | 0.9748 | 0.9748 |
| NN81 | 0.9925 | 0.9898 | 0.9898 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7550 | 0.5744 | 0.5744 |
| V3.1 (boundary) | 0.9325 | 0.7692 | 0.7692 |
| NN11 (boundary) | 0.8450 | 0.6052 | 0.6052 |
| NN21 (boundary) | 0.9575 | 0.6996 | 0.6996 |
| NN41 (boundary) | 0.9775 | 0.8041 | 0.8041 |
| NN81 (boundary) | 0.9925 | 0.8857 | 0.8857 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0015 |
| 21x21 | 441 | 0.0035 |
| 41x41 | 1681 | 0.0161 |
| 81x81 | 6561 | 0.0535 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100011/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`