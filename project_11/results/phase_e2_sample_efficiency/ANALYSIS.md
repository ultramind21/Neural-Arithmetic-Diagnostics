# PHASE E2 — Artifact Analysis

- rows: 45
- elapsed_seconds: 19.750627040863037

## Baselines (from artifact)
- true_dist: {'family-aware region': 127, 'transition region': 310, 'universal region': 363}
- V3.1: {'acc': 0.93, 'macro_f1_present': 0.9352584140643304}
- NN41: {'acc': 0.97, 'macro_f1_present': 0.9673707467962881, 'grid_points': 1681}
- NN81: {'acc': 0.98625, 'macro_f1_present': 0.9847195725541383, 'grid_points': 6561}

## Mean ± sd over seeds (macroF1_present)
| N | strategy | mean | sd |
|---:|---|---:|---:|
| 250 | uniform | 0.8957 | 0.0180 |
| 250 | boundary | 0.6776 | 0.0300 |
| 250 | mixed | 0.9252 | 0.0174 |
| 500 | uniform | 0.9150 | 0.0076 |
| 500 | boundary | 0.7024 | 0.0087 |
| 500 | mixed | 0.9388 | 0.0164 |
| 1000 | uniform | 0.9574 | 0.0034 |
| 1000 | boundary | 0.7011 | 0.0084 |
| 1000 | mixed | 0.9780 | 0.0038 |
| 1500 | uniform | 0.9647 | 0.0063 |
| 1500 | boundary | 0.7133 | 0.0109 |
| 1500 | mixed | 0.9714 | 0.0059 |
| 2000 | uniform | 0.9683 | 0.0090 |
| 2000 | boundary | 0.7238 | 0.0025 |
| 2000 | mixed | 0.9748 | 0.0029 |

## Per-seed table (macroF1_present)
| seed | N | uniform | boundary | mixed |
|---:|---:|---:|---:|---:|
| 101 | 250 | 0.8811 | 0.6886 | 0.9446 |
| 101 | 500 | 0.9227 | 0.6961 | 0.9231 |
| 101 | 1000 | 0.9610 | 0.6942 | 0.9818 |
| 101 | 1500 | 0.9704 | 0.7129 | 0.9781 |
| 101 | 2000 | 0.9702 | 0.7250 | 0.9714 |
| 202 | 250 | 0.8901 | 0.7006 | 0.9110 |
| 202 | 500 | 0.9150 | 0.6989 | 0.9557 |
| 202 | 1000 | 0.9566 | 0.6985 | 0.9742 |
| 202 | 1500 | 0.9657 | 0.7244 | 0.9675 |
| 202 | 2000 | 0.9761 | 0.7254 | 0.9761 |
| 303 | 250 | 0.9158 | 0.6437 | 0.9199 |
| 303 | 500 | 0.9074 | 0.7123 | 0.9375 |
| 303 | 1000 | 0.9544 | 0.7105 | 0.9779 |
| 303 | 1500 | 0.9580 | 0.7026 | 0.9684 |
| 303 | 2000 | 0.9585 | 0.7210 | 0.9768 |

## Monotonicity check on mean curve
- uniform: non-decreasing = True | means = [0.8957, 0.915, 0.9574, 0.9647, 0.9683]
- boundary: non-decreasing = False | means = [0.6776, 0.7024, 0.7011, 0.7133, 0.7238]
- mixed: non-decreasing = False | means = [0.9252, 0.9388, 0.978, 0.9714, 0.9748]