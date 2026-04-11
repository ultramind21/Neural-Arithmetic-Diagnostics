# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 121, 'transition region': 335, 'universal region': 344}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8413 | 0.8272 | 0.8272 |
| V3.1 | 0.9425 | 0.9408 | 0.9408 |
| NN11 | 0.9000 | 0.8795 | 0.8795 |
| NN21 | 0.9587 | 0.9491 | 0.9491 |
| NN41 | 0.9725 | 0.9671 | 0.9671 |
| NN81 | 0.9850 | 0.9838 | 0.9838 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7150 | 0.5643 | 0.5643 |
| V3.1 (boundary) | 0.9075 | 0.7510 | 0.7510 |
| NN11 (boundary) | 0.8350 | 0.6013 | 0.6013 |
| NN21 (boundary) | 0.9300 | 0.7185 | 0.7185 |
| NN41 (boundary) | 0.9550 | 0.7344 | 0.7344 |
| NN81 (boundary) | 0.9700 | 0.8309 | 0.8309 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0048 |
| 41x41 | 1681 | 0.0134 |
| 81x81 | 6561 | 0.0528 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100004/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`