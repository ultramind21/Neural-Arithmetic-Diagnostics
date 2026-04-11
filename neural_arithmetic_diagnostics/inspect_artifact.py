import json
from pathlib import Path

# Check artifacts from multiple seeds
for seed in [100001, 100002, 100003]:
    artifact = Path(f'project_12/results/sweep_c07_v1/phase_d/seed_{seed}/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json')
    if artifact.exists():
        data = json.loads(artifact.read_text())
        print(f'\nArtifact for seed {seed}:')
        print(f'  true_dist: {data.get("true_dist")}')
        print(f'  V3.1 boundary: {data["rules"]["V3.1"]["boundary"]["macro_f1_present"]}')
        
        # Check metadata to see which holdout it references
        if 'p12_metadata' in data:
            meta = data['p12_metadata']
            print(f'  Holdout manifest: {meta.get("holdout_manifest", "N/A")[-40:] if meta.get("holdout_manifest") else "N/A"}')
            print(f'  Holdout path: {meta.get("holdout_path", "N/A")[-40:] if meta.get("holdout_path") else "N/A"}')
    else:
        print(f'\n❌ Artifact not found for seed {seed}')
