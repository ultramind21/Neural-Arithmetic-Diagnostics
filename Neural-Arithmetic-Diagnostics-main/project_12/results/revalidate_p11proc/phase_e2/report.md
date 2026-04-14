# PHASE E2 — Sample Efficiency Report (soft labels)

- holdout points: 800
- true dist: {'family-aware region': 112, 'transition region': 311, 'universal region': 377}
- seeds: [101, 202, 303]
- sizes: [250, 500, 1000, 1500, 2000]
- strategies: ['uniform', 'boundary', 'mixed']
- pool_size: 60000
- elapsed_seconds: 19.88

## Baselines
- V3.1: acc=0.9400 | macroF1=0.9391
- NN41: acc=0.9800 | macroF1=0.9760
- NN81: acc=0.9838 | macroF1=0.9771

## Results (mean over seeds)
| N | strategy | acc_mean | macroF1_mean |
|---:|---|---:|---:|
| 250 | uniform | 0.9104 | 0.8916 |
| 250 | boundary | 0.8408 | 0.6307 |
| 250 | mixed | 0.9608 | 0.9506 |
| 500 | uniform | 0.9383 | 0.9248 |
| 500 | boundary | 0.8429 | 0.6434 |
| 500 | mixed | 0.9767 | 0.9705 |
| 1000 | uniform | 0.9629 | 0.9540 |
| 1000 | boundary | 0.8496 | 0.6739 |
| 1000 | mixed | 0.9817 | 0.9787 |
| 1500 | uniform | 0.9608 | 0.9529 |
| 1500 | boundary | 0.8487 | 0.6693 |
| 1500 | mixed | 0.9858 | 0.9809 |
| 2000 | uniform | 0.9712 | 0.9650 |
| 2000 | boundary | 0.8492 | 0.6682 |
| 2000 | mixed | 0.9842 | 0.9773 |

Artifact:
- `project_12/results/revalidate_p11proc/phase_e2/artifact.json`