# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 100, 'transition region': 343, 'universal region': 357}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8413 | 0.8287 | 0.8287 |
| V3.1 | 0.9375 | 0.9392 | 0.9392 |
| NN11 | 0.9012 | 0.8683 | 0.8683 |
| NN21 | 0.9625 | 0.9530 | 0.9530 |
| NN41 | 0.9812 | 0.9747 | 0.9747 |
| NN81 | 0.9825 | 0.9784 | 0.9784 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7200 | 0.5889 | 0.5889 |
| V3.1 (boundary) | 0.8925 | 0.7916 | 0.7916 |
| NN11 (boundary) | 0.8525 | 0.6040 | 0.6040 |
| NN21 (boundary) | 0.9475 | 0.7696 | 0.7696 |
| NN41 (boundary) | 0.9750 | 0.8216 | 0.8216 |
| NN81 (boundary) | 0.9800 | 0.8673 | 0.8673 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0000 |
| 21x21 | 441 | 0.0040 |
| 41x41 | 1681 | 0.0133 |
| 81x81 | 6561 | 0.0514 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100016/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`