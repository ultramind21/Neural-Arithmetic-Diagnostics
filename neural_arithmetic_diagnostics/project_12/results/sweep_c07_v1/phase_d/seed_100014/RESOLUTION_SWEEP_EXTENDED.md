# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 117, 'transition region': 324, 'universal region': 359}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8425 | 0.8314 | 0.8314 |
| V3.1 | 0.9337 | 0.9360 | 0.9360 |
| NN11 | 0.8888 | 0.8622 | 0.8622 |
| NN21 | 0.9575 | 0.9461 | 0.9461 |
| NN41 | 0.9812 | 0.9775 | 0.9775 |
| NN81 | 0.9825 | 0.9774 | 0.9774 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7200 | 0.6220 | 0.6220 |
| V3.1 (boundary) | 0.8900 | 0.8294 | 0.8294 |
| NN11 (boundary) | 0.8275 | 0.5879 | 0.5879 |
| NN21 (boundary) | 0.9425 | 0.8063 | 0.8063 |
| NN41 (boundary) | 0.9725 | 0.9121 | 0.9121 |
| NN81 (boundary) | 0.9700 | 0.8743 | 0.8743 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0038 |
| 41x41 | 1681 | 0.0147 |
| 81x81 | 6561 | 0.0527 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100014/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`