# PHASE E1 — Adaptive NN Report (soft labels)

- holdout points: 800 (from C3 holdout)
- true dist: {'family-aware region': 127, 'transition region': 310, 'universal region': 363}

## Overall (macro_f1_present)
| model | acc | macroF1 |
|---|---:|---:|
| V3.1 | 0.9300 | 0.9353 |
| NN_adaptive_2000 | 0.9800 | 0.9752 |
| NN41 | 0.9700 | 0.9674 |
| NN81 | 0.9862 | 0.9847 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1 |
|---|---:|---:|
| V3.1 | 0.8875 | 0.8693 |
| NN_adaptive_2000 | 0.9850 | 0.9053 |
| NN41 | 0.9525 | 0.8625 |
| NN81 | 0.9800 | 0.9291 |

## Cost
- adaptive ref points: 2000
- NN41 grid points: 1681 | seconds=0.50
- NN81 grid points: 6561 | seconds=2.37

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_11/results/phase_e1_adaptive_nn/artifact.json`