# PHASE E3 — Ratio + kNN Sweep (soft labels)

- holdout points: 800
- true dist: {'family-aware region': 127, 'transition region': 310, 'universal region': 363}
- seeds: [111, 222, 333, 444, 555]
- Ns: [1000, 1500]
- uniform_fracs: [0.2, 0.5, 0.8]
- pool_size: 60000
- elapsed_seconds: 36.82

## Baselines (macroF1_present)
- V3.1: 0.9353
- NN41: 0.9674
- NN81: 0.9847

## Results (mean over seeds) — macroF1_present
| N | uniform_frac | 1-NN mean F1 | 3-NN mean F1 |
|---:|---:|---:|---:|
| 1000 | 0.2 | 0.9494 | 0.9273 |
| 1000 | 0.5 | 0.9682 | 0.9513 |
| 1000 | 0.8 | 0.9666 | 0.9628 |
| 1500 | 0.2 | 0.9663 | 0.9483 |
| 1500 | 0.5 | 0.9747 | 0.9627 |
| 1500 | 0.8 | 0.9722 | 0.9665 |

Artifact:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_11/results/phase_e3_ratio_knn/artifact.json`