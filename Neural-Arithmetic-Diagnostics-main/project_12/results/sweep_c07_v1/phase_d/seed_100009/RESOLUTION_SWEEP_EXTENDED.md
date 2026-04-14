# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 103, 'transition region': 364, 'universal region': 333}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8075 | 0.7959 | 0.7959 |
| V3.1 | 0.9337 | 0.9391 | 0.9391 |
| NN11 | 0.8662 | 0.8351 | 0.8351 |
| NN21 | 0.9625 | 0.9547 | 0.9547 |
| NN41 | 0.9712 | 0.9700 | 0.9700 |
| NN81 | 0.9875 | 0.9836 | 0.9836 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.6625 | 0.5321 | 0.5321 |
| V3.1 (boundary) | 0.8850 | 0.8031 | 0.8031 |
| NN11 (boundary) | 0.8025 | 0.5677 | 0.5677 |
| NN21 (boundary) | 0.9475 | 0.7556 | 0.7556 |
| NN41 (boundary) | 0.9625 | 0.8801 | 0.8801 |
| NN81 (boundary) | 0.9875 | 0.9028 | 0.9028 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0030 |
| 41x41 | 1681 | 0.0149 |
| 81x81 | 6561 | 0.0552 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100009/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`