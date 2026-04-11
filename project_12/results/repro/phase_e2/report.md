# PHASE E2 — Sample Efficiency Report (soft labels)

- holdout points: 800
- true dist: {'family-aware region': 127, 'transition region': 310, 'universal region': 363}
- seeds: [101, 202, 303]
- sizes: [250, 500, 1000, 1500, 2000]
- strategies: ['uniform', 'boundary', 'mixed']
- pool_size: 60000
- elapsed_seconds: 19.56

## Baselines
- V3.1: acc=0.9300 | macroF1=0.9353
- NN41: acc=0.9700 | macroF1=0.9674
- NN81: acc=0.9862 | macroF1=0.9847

## Results (mean over seeds)
| N | strategy | acc_mean | macroF1_mean |
|---:|---|---:|---:|
| 250 | uniform | 0.9062 | 0.8957 |
| 250 | boundary | 0.8308 | 0.6776 |
| 250 | mixed | 0.9396 | 0.9252 |
| 500 | uniform | 0.9254 | 0.9150 |
| 500 | boundary | 0.8412 | 0.7024 |
| 500 | mixed | 0.9525 | 0.9388 |
| 1000 | uniform | 0.9621 | 0.9574 |
| 1000 | boundary | 0.8421 | 0.7011 |
| 1000 | mixed | 0.9800 | 0.9780 |
| 1500 | uniform | 0.9696 | 0.9647 |
| 1500 | boundary | 0.8471 | 0.7133 |
| 1500 | mixed | 0.9762 | 0.9714 |
| 2000 | uniform | 0.9696 | 0.9683 |
| 2000 | boundary | 0.8508 | 0.7238 |
| 2000 | mixed | 0.9775 | 0.9748 |

Artifact:
- `project_12/results/repro/phase_e2/artifact.json`