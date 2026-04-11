# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 119, 'transition region': 341, 'universal region': 340}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8325 | 0.8263 | 0.8263 |
| V3.1 | 0.9400 | 0.9436 | 0.9436 |
| NN11 | 0.8825 | 0.8592 | 0.8592 |
| NN21 | 0.9587 | 0.9531 | 0.9531 |
| NN41 | 0.9850 | 0.9830 | 0.9830 |
| NN81 | 0.9888 | 0.9867 | 0.9867 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7175 | 0.5592 | 0.5592 |
| V3.1 (boundary) | 0.9025 | 0.8047 | 0.8047 |
| NN11 (boundary) | 0.8350 | 0.5929 | 0.5929 |
| NN21 (boundary) | 0.9550 | 0.7532 | 0.7532 |
| NN41 (boundary) | 0.9750 | 0.8587 | 0.8587 |
| NN81 (boundary) | 0.9800 | 0.8394 | 0.8394 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0012 |
| 21x21 | 441 | 0.0059 |
| 41x41 | 1681 | 0.0142 |
| 81x81 | 6561 | 0.0497 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_12/results/sweep_c07_v1/phase_d/seed_100019/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`