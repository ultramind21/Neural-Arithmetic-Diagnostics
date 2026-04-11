# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 103, 'transition region': 326, 'universal region': 371}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8488 | 0.8326 | 0.8326 |
| V3.1 | 0.9313 | 0.9237 | 0.9237 |
| NN11 | 0.8850 | 0.8504 | 0.8504 |
| NN21 | 0.9475 | 0.9286 | 0.9286 |
| NN41 | 0.9750 | 0.9670 | 0.9670 |
| NN81 | 0.9812 | 0.9728 | 0.9728 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7375 | 0.6253 | 0.6253 |
| V3.1 (boundary) | 0.8850 | 0.7762 | 0.7762 |
| NN11 (boundary) | 0.8225 | 0.5903 | 0.5903 |
| NN21 (boundary) | 0.9225 | 0.7370 | 0.7370 |
| NN41 (boundary) | 0.9575 | 0.8409 | 0.8409 |
| NN81 (boundary) | 0.9725 | 0.8678 | 0.8678 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0030 |
| 41x41 | 1681 | 0.0131 |
| 81x81 | 6561 | 0.0530 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100002/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`