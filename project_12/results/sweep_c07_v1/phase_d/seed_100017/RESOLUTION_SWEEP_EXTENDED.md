# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 116, 'transition region': 331, 'universal region': 353}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8237 | 0.8065 | 0.8065 |
| V3.1 | 0.9475 | 0.9465 | 0.9465 |
| NN11 | 0.8950 | 0.8660 | 0.8660 |
| NN21 | 0.9513 | 0.9396 | 0.9396 |
| NN41 | 0.9762 | 0.9757 | 0.9757 |
| NN81 | 0.9838 | 0.9835 | 0.9835 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7075 | 0.5758 | 0.5758 |
| V3.1 (boundary) | 0.9225 | 0.8300 | 0.8300 |
| NN11 (boundary) | 0.8400 | 0.6052 | 0.6052 |
| NN21 (boundary) | 0.9425 | 0.7337 | 0.7337 |
| NN41 (boundary) | 0.9700 | 0.8866 | 0.8866 |
| NN81 (boundary) | 0.9800 | 0.8944 | 0.8944 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0033 |
| 41x41 | 1681 | 0.0143 |
| 81x81 | 6561 | 0.0517 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100017/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`