# PHASE E3 — Ratio + kNN Sweep (soft labels)

- holdout points: 800
- true dist: {'family-aware region': 112, 'transition region': 311, 'universal region': 377}
- seeds: [111, 222, 333, 444, 555]
- Ns: [1000, 1500]
- uniform_fracs: [0.2, 0.5, 0.8]
- pool_size: 60000
- elapsed_seconds: 36.36

## Baselines (macroF1_present)
- V3.1: 0.9391
- NN41: 0.9760
- NN81: 0.9771

## Results (mean over seeds) — macroF1_present
| N | uniform_frac | 1-NN mean F1 | 3-NN mean F1 |
|---:|---:|---:|---:|
| 1000 | 0.2 | 0.9623 | 0.9460 |
| 1000 | 0.5 | 0.9739 | 0.9662 |
| 1000 | 0.8 | 0.9641 | 0.9647 |
| 1500 | 0.2 | 0.9720 | 0.9577 |
| 1500 | 0.5 | 0.9756 | 0.9705 |
| 1500 | 0.8 | 0.9748 | 0.9738 |

Artifact:
- `project_12/results/revalidate_p11proc/phase_e3/artifact.json`