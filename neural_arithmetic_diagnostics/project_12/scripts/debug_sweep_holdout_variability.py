#!/usr/bin/env python3
"""
debug_sweep_holdout_variability.py

Check if 5 sample holdout files are actually different (not cached/identical).
Compares hashes and first data points.
"""

import json
import hashlib
from pathlib import Path

def hash_array(arr):
    """Compute SHA256 of JSON array."""
    return hashlib.sha256(json.dumps(arr, sort_keys=True).encode()).hexdigest()

def main():
    project_root = Path(__file__).parent.parent.parent
    sweep_dir = project_root / "project_12/results/sweep_c07_v1"
    
    # Check holdout files in temp
    tmp_holdouts_dir = sweep_dir / "tmp_holdouts"
    
    print("="*70)
    print("HOLDOUT VARIABILITY CHECK")
    print("="*70)
    
    if not tmp_holdouts_dir.exists():
        print("❌ tmp_holdouts directory not found!")
        print(f"   Expected: {tmp_holdouts_dir}")
        print("   Note: sweep may have keep_temporary_holdouts=false")
        return
    
    # Sample 5 seeds
    seeds = list(range(100001, 100006))  # 100001-100005
    
    results = []
    hashes = set()
    first_points = []
    
    for seed in seeds:
        holdout_path = tmp_holdouts_dir / f"seed_{seed}" / "holdout_points.json"
        
        if not holdout_path.exists():
            print(f"❌ Missing: seed_{seed}")
            continue
        
        with open(holdout_path, 'r') as f:
            data = json.load(f)
        
        points_array = data.get("points", [])
        points_hash = hash_array(points_array)
        hashes.add(points_hash)
        
        first_point = points_array[0] if points_array else None
        first_points.append((seed, first_point))
        
        results.append({
            "seed": seed,
            "points_count": len(points_array),
            "hash": points_hash[:16],  # Short hash
        })
        
        print(f"Seed {seed}:")
        print(f"  Points: {len(points_array)}")
        print(f"  Hash (first 16 chars): {points_hash[:16]}")
        print(f"  First point: {first_point}")
    
    print()
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Unique hashes: {len(hashes)}")
    print(f"Samples checked: {len(results)}")
    
    if len(hashes) > 1:
        print("✅ PASS: Holdouts are different (variability detected)")
    else:
        print("❌ FAIL: All holdouts are identical (no variability!)")
        print("   This suggests files were not regenerated or seed not used.")
    
    # Print table
    print()
    print("Details:")
    for r in results:
        print(f"  Seed {r['seed']}: {r['points_count']} points, hash {r['hash']}")

if __name__ == "__main__":
    main()
