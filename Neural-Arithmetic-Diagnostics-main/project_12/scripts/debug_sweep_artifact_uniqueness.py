#!/usr/bin/env python3
"""
debug_sweep_artifact_uniqueness.py

Check if Phase D artifacts per seed are actually different or all identical.
Compares true_dist, metrics, timestamps.
"""

import json
from pathlib import Path
from collections import Counter

def main():
    project_root = Path(__file__).parent.parent.parent
    sweep_dir = project_root / "project_12/results/sweep_c07_v1/phase_d"
    
    print("="*70)
    print("ARTIFACT UNIQUENESS CHECK")
    print("="*70)
    
    if not sweep_dir.exists():
        print(f"❌ Sweep phase_d directory not found: {sweep_dir}")
        return
    
    # Collect artifacts
    artifacts = {}
    for seed_dir in sorted(sweep_dir.glob("seed_*")):
        seed = int(seed_dir.name.split("_")[1])
        artifact_path = seed_dir / "RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json"
        
        if not artifact_path.exists():
            print(f"⚠️  Missing artifact for seed {seed}")
            continue
        
        with open(artifact_path, 'r') as f:
            artifact = json.load(f)
        
        # Extract key metrics
        true_dist = artifact.get("true_dist", {})
        true_dist_tuple = tuple(sorted(true_dist.items()))  # Make hashable
        
        try:
            v3_boundary = artifact["rules"]["V3"]["boundary"]["macro_f1_present"]
            v31_boundary = artifact["rules"]["V3.1"]["boundary"]["macro_f1_present"]
            nn81_boundary = artifact["nn"]["NN81"]["boundary"]["macro_f1_present"]
        except (KeyError, TypeError) as e:
            print(f"❌ Error extracting metrics from seed {seed}: {e}")
            continue
        
        metadata = artifact.get("p12_metadata", {})
        timestamp = metadata.get("generated_at", "N/A")
        
        artifacts[seed] = {
            "true_dist": true_dist_tuple,
            "true_dist_str": str(true_dist),
            "v3_boundary": v3_boundary,
            "v31_boundary": v31_boundary,
            "nn81_boundary": nn81_boundary,
            "timestamp": timestamp[:10] if timestamp else "N/A",
        }
    
    # Analyze uniqueness
    print(f"\nArtifacts found: {len(artifacts)}")
    print()
    
    # true_dist uniqueness
    true_dists = [a["true_dist"] for a in artifacts.values()]
    unique_true_dists = set(true_dists)
    print(f"Unique true_dist values: {len(unique_true_dists)}")
    print(f"  Sample: {artifacts[list(artifacts.keys())[0]]['true_dist_str']}")
    
    # V3.1 boundary uniqueness
    v31_bounds = [a["v31_boundary"] for a in artifacts.values()]
    unique_v31_bounds = set(round(x, 6) for x in v31_bounds)
    print(f"Unique V3.1_boundary values: {len(unique_v31_bounds)}")
    print(f"  Sample: {v31_bounds[0]:.6f}")
    
    # Timestamps
    timestamps = [a["timestamp"] for a in artifacts.values()]
    unique_timestamps = set(timestamps)
    print(f"Unique timestamps: {len(unique_timestamps)}")
    
    print()
    print("="*70)
    print("SUMMARY")
    print("="*70)
    
    if len(unique_true_dists) > 1:
        print("✅ true_dist varies (good: holdouts are different)")
    else:
        print("❌ true_dist identical (BAD: holdouts likely identical or not used)")
    
    if len(unique_v31_bounds) > 1:
        print("✅ V3.1_boundary varies (good: phase D computations differ)")
    else:
        print("❌ V3.1_boundary identical (BAD: phase D results identical)")
    
    # Detailed table (first 5 seeds)
    print()
    print("Per-seed details (first 5):")
    print("| Seed | true_dist | V3.1_boundary | Timestamp |")
    print("|------|-----------|---------------|-----------|")
    for seed in list(artifacts.keys())[:5]:
        a = artifacts[seed]
        print(f"| {seed} | {str(a['true_dist']).replace(',', ' ')} | {a['v31_boundary']:.6f} | {a['timestamp']} |")

if __name__ == "__main__":
    main()
