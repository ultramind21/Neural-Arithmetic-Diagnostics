# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 124, 'transition region': 319, 'universal region': 357}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8538 | 0.8434 | 0.8434 |
| V3.1 | 0.9437 | 0.9430 | 0.9430 |
| NN11 | 0.9000 | 0.8738 | 0.8738 |
| NN21 | 0.9637 | 0.9554 | 0.9554 |
| NN41 | 0.9775 | 0.9743 | 0.9743 |
| NN81 | 0.9875 | 0.9858 | 0.9858 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7625 | 0.6318 | 0.6318 |
| V3.1 (boundary) | 0.9075 | 0.8090 | 0.8090 |
| NN11 (boundary) | 0.8600 | 0.6109 | 0.6109 |
| NN21 (boundary) | 0.9550 | 0.8214 | 0.8214 |
| NN41 (boundary) | 0.9650 | 0.8699 | 0.8699 |
| NN81 (boundary) | 0.9775 | 0.9015 | 0.9015 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0012 |
| 21x21 | 441 | 0.0035 |
| 41x41 | 1681 | 0.0145 |
| 81x81 | 6561 | 0.0538 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100013/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`