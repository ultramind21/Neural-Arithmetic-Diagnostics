# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 110, 'transition region': 344, 'universal region': 346}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8550 | 0.8405 | 0.8405 |
| V3.1 | 0.9475 | 0.9472 | 0.9472 |
| NN11 | 0.8988 | 0.8717 | 0.8717 |
| NN21 | 0.9625 | 0.9524 | 0.9524 |
| NN41 | 0.9825 | 0.9774 | 0.9774 |
| NN81 | 0.9900 | 0.9882 | 0.9882 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7525 | 0.5807 | 0.5807 |
| V3.1 (boundary) | 0.9100 | 0.7440 | 0.7440 |
| NN11 (boundary) | 0.8400 | 0.6026 | 0.6026 |
| NN21 (boundary) | 0.9425 | 0.7135 | 0.7135 |
| NN41 (boundary) | 0.9675 | 0.7554 | 0.7554 |
| NN81 (boundary) | 0.9825 | 0.8579 | 0.8579 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0030 |
| 41x41 | 1681 | 0.0144 |
| 81x81 | 6561 | 0.0525 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100012/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`