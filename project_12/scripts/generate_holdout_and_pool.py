#!/usr/bin/env python3
"""
generate_holdout_and_pool.py

Generates independent holdout and pool datasets for re-validation.
Uses explicit seeds and domain bounds (no randomness in bounds).
"""

import json
import random
import argparse
from pathlib import Path
from typing import List, Tuple

# Domain bounds (from Project 11 scripts)
H_MIN, H_MAX = 0.0010, 0.0200
P_MIN, P_MAX = 0.2600, 0.4200

def generate_points(seed: int, count: int) -> List[Tuple[float, float]]:
    """Generate random points in [H_MIN, H_MAX] x [P_MIN, P_MAX]."""
    rng = random.Random(seed)
    points = []
    for _ in range(count):
        h = rng.uniform(H_MIN, H_MAX)
        p = rng.uniform(P_MIN, P_MAX)
        points.append([h, p])
    return points

def load_manifest(path: str) -> dict:
    """Load manifest JSON."""
    with open(path, "r") as f:
        return json.load(f)

def ensure_output_dir_safe(output_dir: Path):
    """Ensure output_dir is inside project_12/results."""
    if "project_12" not in str(output_dir) or "results" not in str(output_dir):
        raise ValueError(f"Output dir must be inside project_12/results: {output_dir}")

def write_json(path: Path, obj: dict):
    """Write JSON to path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Generate holdout and pool for re-validation")
    parser.add_argument("--holdout_seed", type=int, default=424242, help="Seed for holdout")
    parser.add_argument("--holdout_size", type=int, default=800, help="Size of holdout")
    parser.add_argument("--pool_seed", type=int, default=515151, help="Seed for pool")
    parser.add_argument("--pool_size", type=int, default=60000, help="Size of pool")
    parser.add_argument("--out_dir", type=str, default="project_12/results/revalidate/data", help="Output directory")
    parser.add_argument("--manifest", type=str, default=None, help="Manifest JSON (if provided, override args)")
    
    args = parser.parse_args()
    
    # Override from manifest if provided
    if args.manifest:
        manifest = load_manifest(args.manifest)
        fixed_params = manifest.get("fixed_params", {})
        args.holdout_seed = fixed_params.get("holdout_seed", args.holdout_seed)
        args.holdout_size = fixed_params.get("holdout_size", args.holdout_size)
        args.pool_seed = fixed_params.get("pool_seed", args.pool_seed)
        args.pool_size = fixed_params.get("pool_size", args.pool_size)
        args.out_dir = manifest.get("output_dir", args.out_dir)
    
    out_dir = Path(args.out_dir)
    ensure_output_dir_safe(out_dir)
    
    print(f"🔨 Generating holdout ({args.holdout_size} points, seed={args.holdout_seed})...")
    holdout_points = generate_points(args.holdout_seed, args.holdout_size)
    
    print(f"🔨 Generating pool ({args.pool_size} points, seed={args.pool_seed})...")
    pool_points = generate_points(args.pool_seed, args.pool_size)
    
    # Write holdout
    holdout_path = out_dir / "holdout_points.json"
    holdout_data = {
        "points": holdout_points,
        "seed": args.holdout_seed,
        "size": args.holdout_size,
        "bounds": {
            "H": [H_MIN, H_MAX],
            "P": [P_MIN, P_MAX]
        }
    }
    write_json(holdout_path, holdout_data)
    print(f"✅ Holdout written: {holdout_path}")
    
    # Write pool
    pool_path = out_dir / "pool_points.json"
    pool_data = {
        "points": pool_points,
        "seed": args.pool_seed,
        "size": args.pool_size,
        "bounds": {
            "H": [H_MIN, H_MAX],
            "P": [P_MIN, P_MAX]
        }
    }
    write_json(pool_path, pool_data)
    print(f"✅ Pool written: {pool_path}")
    
    print(f"\n✅ Generation complete!")
    print(f"   Holdout: {len(holdout_points)} points in {holdout_path}")
    print(f"   Pool: {len(pool_points)} points in {pool_path}")

if __name__ == "__main__":
    main()
