# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 115, 'transition region': 353, 'universal region': 332}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8438 | 0.8398 | 0.8398 |
| V3.1 | 0.9313 | 0.9359 | 0.9359 |
| NN11 | 0.8925 | 0.8750 | 0.8750 |
| NN21 | 0.9537 | 0.9423 | 0.9423 |
| NN41 | 0.9775 | 0.9759 | 0.9759 |
| NN81 | 0.9875 | 0.9855 | 0.9855 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7375 | 0.6021 | 0.6021 |
| V3.1 (boundary) | 0.8950 | 0.7969 | 0.7969 |
| NN11 (boundary) | 0.8375 | 0.5880 | 0.5880 |
| NN21 (boundary) | 0.9300 | 0.7143 | 0.7143 |
| NN41 (boundary) | 0.9650 | 0.8678 | 0.8678 |
| NN81 (boundary) | 0.9800 | 0.9103 | 0.9103 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0031 |
| 41x41 | 1681 | 0.0144 |
| 81x81 | 6561 | 0.0531 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100008/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`