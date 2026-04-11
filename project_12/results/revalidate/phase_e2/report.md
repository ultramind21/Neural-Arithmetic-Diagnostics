# PHASE E2 — Sample Efficiency Report (soft labels)

- holdout points: 800
- true dist: {'family-aware region': 194, 'transition region': 118, 'universal region': 488}
- seeds: [101, 202, 303]
- sizes: [250, 500, 1000, 1500, 2000]
- strategies: ['uniform', 'boundary', 'mixed']
- pool_size: 60000
- elapsed_seconds: 18.24

## Baselines
- V3.1: acc=0.9825 | macroF1=0.9732
- NN41: acc=0.9925 | macroF1=0.9874
- NN81: acc=0.9912 | macroF1=0.9868

## Results (mean over seeds)
| N | strategy | acc_mean | macroF1_mean |
|---:|---|---:|---:|
| 250 | uniform | 0.9529 | 0.9274 |
| 250 | boundary | 0.7125 | 0.5227 |
| 250 | mixed | 0.9425 | 0.9167 |
| 500 | uniform | 0.9621 | 0.9394 |
| 500 | boundary | 0.7188 | 0.5262 |
| 500 | mixed | 0.9583 | 0.9382 |
| 1000 | uniform | 0.9779 | 0.9637 |
| 1000 | boundary | 0.7200 | 0.5317 |
| 1000 | mixed | 0.9771 | 0.9651 |
| 1500 | uniform | 0.9846 | 0.9757 |
| 1500 | boundary | 0.7312 | 0.5505 |
| 1500 | mixed | 0.9742 | 0.9619 |
| 2000 | uniform | 0.9854 | 0.9769 |
| 2000 | boundary | 0.7325 | 0.5537 |
| 2000 | mixed | 0.9804 | 0.9706 |

Artifact:
- `project_12/results/revalidate/phase_e2/artifact.json`