import json
from pathlib import Path

# Check the phase_d manifests for different seeds
for seed_num in [100001, 100002, 100003]:
    manifest_file = Path(f'project_12/results/sweep_c07_v1/tmp_manifests/seed_{seed_num}_phase_d.json')
    if manifest_file.exists():
        data = json.loads(manifest_file.read_text())
        holdout_path = data.get('holdout_path', 'N/A')
        print(f'Seed {seed_num}: {holdout_path.split("/")[-2:]}')
    else:
        print(f'Manifest not found for seed {seed_num}')
