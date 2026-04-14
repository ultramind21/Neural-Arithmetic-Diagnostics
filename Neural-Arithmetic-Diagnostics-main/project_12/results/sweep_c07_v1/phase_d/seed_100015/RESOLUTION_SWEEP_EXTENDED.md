# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 108, 'transition region': 351, 'universal region': 341}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8137 | 0.8016 | 0.8016 |
| V3.1 | 0.9350 | 0.9327 | 0.9327 |
| NN11 | 0.8938 | 0.8706 | 0.8706 |
| NN21 | 0.9575 | 0.9495 | 0.9495 |
| NN41 | 0.9812 | 0.9754 | 0.9754 |
| NN81 | 0.9812 | 0.9762 | 0.9762 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.6900 | 0.5160 | 0.5160 |
| V3.1 (boundary) | 0.8975 | 0.6877 | 0.6877 |
| NN11 (boundary) | 0.8500 | 0.6046 | 0.6046 |
| NN21 (boundary) | 0.9400 | 0.7124 | 0.7124 |
| NN41 (boundary) | 0.9775 | 0.7510 | 0.7510 |
| NN81 (boundary) | 0.9775 | 0.7654 | 0.7654 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0015 |
| 21x21 | 441 | 0.0036 |
| 41x41 | 1681 | 0.0148 |
| 81x81 | 6561 | 0.0541 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100015/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`