import csv
from pathlib import Path

csv_file = Path('project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv')
metrics = list(csv.DictReader(csv_file.open()))

# Analyze threshold performance
v31_values = [float(m['v31_boundary']) for m in metrics]
v31_values_sorted = sorted(v31_values)

threshold = 0.85
passes = sum(1 for v in v31_values if v >= threshold)
fails = len(v31_values) - passes

print('V3.1_BOUNDARY THRESHOLD ANALYSIS (threshold=0.85)')
print('='*70)
print(f'Total seeds: {len(v31_values)}')
print(f'Passes (>= 0.85): {passes} ({100*passes/len(v31_values):.1f}%)')
print(f'Fails (< 0.85): {fails} ({100*fails/len(v31_values):.1f}%)')
print()
print(f'Min: {min(v31_values):.6f}')
print(f'Max: {max(v31_values):.6f}')
print(f'Mean: {sum(v31_values)/len(v31_values):.6f}')
std = (sum((x-sum(v31_values)/len(v31_values))**2 for x in v31_values)/len(v31_values))**0.5
print(f'Std: {std:.6f}')
print()
print('Distribution (sorted):')
for i, v in enumerate(v31_values_sorted, 1):
    status = 'PASS' if v >= threshold else 'FAIL'
    print(f'  {i:2d}. {v:.6f} [{status}]')
