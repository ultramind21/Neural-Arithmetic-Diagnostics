import json
import hashlib

for seed in [100001, 100002, 100003]:
    path = f"project_12/results/sweep_c07_v1/tmp_holdouts/seed_{seed}/holdout_points.json"
    with open(path) as f:
        data = json.load(f)
    # Hash the POINTS array, not the 'test' string!
    points_json = json.dumps(data["points"], sort_keys=True)
    points_hash = hashlib.sha256(points_json.encode()).hexdigest()
    print(f"Seed {seed}:")
    print(f"  Seed in file: {data.get('seed')}")
    print(f"  Points count: {len(data['points'])}")
    print(f"  Points hash: {points_hash[:16]}")
    print(f"  First point: {data['points'][0]}")
    print()
