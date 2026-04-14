# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 122, 'transition region': 338, 'universal region': 340}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8250 | 0.8121 | 0.8121 |
| V3.1 | 0.9400 | 0.9429 | 0.9429 |
| NN11 | 0.8762 | 0.8584 | 0.8584 |
| NN21 | 0.9563 | 0.9455 | 0.9455 |
| NN41 | 0.9825 | 0.9810 | 0.9810 |
| NN81 | 0.9788 | 0.9771 | 0.9771 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.6975 | 0.5685 | 0.5685 |
| V3.1 (boundary) | 0.8975 | 0.7956 | 0.7956 |
| NN11 (boundary) | 0.8425 | 0.5928 | 0.5928 |
| NN21 (boundary) | 0.9425 | 0.6793 | 0.6793 |
| NN41 (boundary) | 0.9775 | 0.9041 | 0.9041 |
| NN81 (boundary) | 0.9675 | 0.8393 | 0.8393 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0043 |
| 41x41 | 1681 | 0.0189 |
| 81x81 | 6561 | 0.0571 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100020/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`