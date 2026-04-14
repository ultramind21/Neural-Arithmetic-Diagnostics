# PHASE E3 — Ratio + kNN Sweep (soft labels)

- holdout points: 800
- true dist: {'family-aware region': 194, 'transition region': 118, 'universal region': 488}
- seeds: [111, 222, 333, 444, 555]
- Ns: [1000, 1500]
- uniform_fracs: [0.2, 0.5, 0.8]
- pool_size: 60000
- elapsed_seconds: 39.65

## Baselines (macroF1_present)
- V3.1: 0.9732
- NN41: 0.9874
- NN81: 0.9868

## Results (mean over seeds) — macroF1_present
| N | uniform_frac | 1-NN mean F1 | 3-NN mean F1 |
|---:|---:|---:|---:|
| 1000 | 0.2 | 0.9208 | 0.8869 |
| 1000 | 0.5 | 0.9570 | 0.9326 |
| 1000 | 0.8 | 0.9695 | 0.9579 |
| 1500 | 0.2 | 0.9407 | 0.9115 |
| 1500 | 0.5 | 0.9637 | 0.9503 |
| 1500 | 0.8 | 0.9725 | 0.9660 |

Artifact:
- `project_12/results/revalidate/phase_e3/artifact.json`