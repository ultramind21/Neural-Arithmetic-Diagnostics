# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 113, 'transition region': 316, 'universal region': 371}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8438 | 0.8281 | 0.8281 |
| V3.1 | 0.9437 | 0.9416 | 0.9416 |
| NN11 | 0.9025 | 0.8774 | 0.8774 |
| NN21 | 0.9575 | 0.9452 | 0.9452 |
| NN41 | 0.9788 | 0.9732 | 0.9732 |
| NN81 | 0.9900 | 0.9861 | 0.9861 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7350 | 0.6158 | 0.6158 |
| V3.1 (boundary) | 0.9175 | 0.8142 | 0.8142 |
| NN11 (boundary) | 0.8500 | 0.6011 | 0.6011 |
| NN21 (boundary) | 0.9400 | 0.7837 | 0.7837 |
| NN41 (boundary) | 0.9700 | 0.8845 | 0.8845 |
| NN81 (boundary) | 0.9800 | 0.8923 | 0.8923 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0012 |
| 21x21 | 441 | 0.0037 |
| 41x41 | 1681 | 0.0136 |
| 81x81 | 6561 | 0.0525 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100003/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`