import csv
from pathlib import Path

csv_file = Path('project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv')
metrics = list(csv.DictReader(csv_file.open()))

v31_values = sorted([float(m['v31_boundary']) for m in metrics])

print('REALISTIC THRESHOLD ANALYSIS')
print('='*70)
print()
print('Pass rates by threshold:')
for pct in [50, 60, 70, 80, 90, 95, 100]:
    idx = max(0, int(len(v31_values) * pct / 100) - 1)
    threshold = v31_values[idx]
    passes = sum(1 for v in v31_values if v >= threshold)
    rate = 100 * passes / len(v31_values)
    print(f'  {pct:3d}% pass rate would need threshold ≤ {threshold:.6f} ({passes} seeds pass)')
print()
print('Percentile analysis:')
for pct in [50, 75, 90, 95]:
    idx = int(len(v31_values) * pct / 100)
    if idx >= len(v31_values):
        idx = len(v31_values) - 1
    threshold = v31_values[idx]
    print(f'  {pct:2d}th percentile: {threshold:.6f}')
