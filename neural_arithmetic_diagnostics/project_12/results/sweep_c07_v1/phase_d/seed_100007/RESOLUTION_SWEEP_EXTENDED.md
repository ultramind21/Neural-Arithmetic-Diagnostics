# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 120, 'transition region': 339, 'universal region': 341}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8287 | 0.8141 | 0.8141 |
| V3.1 | 0.9337 | 0.9300 | 0.9300 |
| NN11 | 0.8912 | 0.8682 | 0.8682 |
| NN21 | 0.9575 | 0.9488 | 0.9488 |
| NN41 | 0.9850 | 0.9812 | 0.9812 |
| NN81 | 0.9812 | 0.9774 | 0.9774 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7100 | 0.5759 | 0.5759 |
| V3.1 (boundary) | 0.8975 | 0.7582 | 0.7582 |
| NN11 (boundary) | 0.8450 | 0.6109 | 0.6109 |
| NN21 (boundary) | 0.9400 | 0.7434 | 0.7434 |
| NN41 (boundary) | 0.9725 | 0.8556 | 0.8556 |
| NN81 (boundary) | 0.9725 | 0.8408 | 0.8408 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0036 |
| 41x41 | 1681 | 0.0208 |
| 81x81 | 6561 | 0.0610 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100007/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`