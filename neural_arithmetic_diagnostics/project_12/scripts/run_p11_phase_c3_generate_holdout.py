"""
Phase C3 Holdout Generator (copied from Project 11, adapted for Project 12 manifests)

Generates holdout_points.json using Project 11's exact procedure:
- 400 uniform points sampled from H/P ranges
- 400 boundary-optimized points selected from 90k pool using v3_boundary_score

This script is **procedure-preserving**: no changes to sampling logic or thresholds.
Only adaptations: manifest-driven paths, seed from manifest, metadata capture.
"""

from __future__ import annotations

import json
import hashlib
import random
import argparse
from pathlib import Path
from datetime import datetime


def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def sha256_text(text: str) -> str:
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def sample_uniform(rng: random.Random, h_min: float, h_max: float, p_min: float, p_max: float):
    return rng.uniform(h_min, h_max), rng.uniform(p_min, p_max)


def v3_boundary_score(H: float, P: float, sfs: list[float]) -> float:
    """Project 11 Phase C3 boundary scoring (unchanged)."""
    deltas = [0.80 * H + (0.30 - P) * sf for sf in sfs]
    gap_est = sum(deltas) / len(deltas)
    d_gap_fam = abs(gap_est - 0.005)
    d_gap_uni = abs(gap_est + 0.003)
    d_delta_fam = min(abs(d - 0.005) for d in deltas)
    d_delta_uni = min(abs(d + 0.005) for d in deltas)
    return min(d_gap_fam, d_gap_uni, d_delta_fam, d_delta_uni)


def main():
    parser = argparse.ArgumentParser(
        description="Phase C3 Holdout Generator (Project 11 procedure, Project 12 manifest-driven)"
    )
    parser.add_argument(
        "--manifest",
        type=str,
        required=True,
        help="Path to manifest JSON (specifies seed, output_dir, etc)"
    )
    args = parser.parse_args()

    # Load manifest
    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    # Extract parameters
    fixed_params = manifest.get("fixed_params", {})
    seed = fixed_params.get("holdout_seed", 223311)
    n_total = fixed_params.get("holdout_size", 800)
    n_uniform = n_total // 2
    n_boundary = n_total - n_uniform

    h_min = fixed_params.get("h_min", 0.0010)
    h_max = fixed_params.get("h_max", 0.0200)
    p_min = fixed_params.get("p_min", 0.2600)
    p_max = fixed_params.get("p_max", 0.4200)
    boundary_pool_size = fixed_params.get("boundary_pool", 90000)

    output_dir = Path(manifest.get("output_dir", "project_12/results/revalidate_p11proc/data/"))
    output_dir.mkdir(parents=True, exist_ok=True)

    holdout_path = output_dir / "holdout_points.json"
    metadata_path = output_dir / "holdout_metadata.json"

    # Project 11 hardcoded SFS values (unchanged)
    sfs = [0.72, 0.65, 0.30, 0.28]

    # Generate holdout
    rng = random.Random(seed)
    used = set()
    points = []

    # Uniform sampling
    while len(points) < n_uniform:
        H, P = sample_uniform(rng, h_min, h_max, p_min, p_max)
        Hr, Pr = round(H, 6), round(P, 6)
        key = (Hr, Pr)
        if key in used:
            continue
        used.add(key)
        points.append({"id": f"c3_u{len(points)+1:04d}", "H": Hr, "P": Pr, "kind": "uniform"})

    # Boundary pool selection
    pool = []
    for _ in range(boundary_pool_size):
        H, P = sample_uniform(rng, h_min, h_max, p_min, p_max)
        Hr, Pr = round(H, 6), round(P, 6)
        bs = v3_boundary_score(Hr, Pr, sfs)
        pool.append((bs, Hr, Pr))
    pool.sort(key=lambda x: x[0])

    b_count = 0
    for bs, Hr, Pr in pool:
        if b_count >= n_boundary:
            break
        key = (Hr, Pr)
        if key in used:
            continue
        used.add(key)
        b_count += 1
        points.append({"id": f"c3_b{b_count:04d}", "H": Hr, "P": Pr, "kind": "boundary"})

    if b_count != n_boundary:
        raise SystemExit(f"FAIL: boundary pool insufficient. got={b_count}, expected={n_boundary}")

    holdout = {
        "test": "phase_c3_sat_margin",
        "created_date": datetime.utcnow().isoformat() + "Z",
        "seed": seed,
        "n_total": len(points),
        "n_uniform": sum(1 for p in points if p["kind"] == "uniform"),
        "n_boundary": sum(1 for p in points if p["kind"] == "boundary"),
        "ranges": {"H": [h_min, h_max], "P": [p_min, p_max]},
        "points": points
    }

    save_json(holdout_path, holdout)

    # Compute holdout hash
    holdout_hash = sha256_file(holdout_path)

    # Metadata
    metadata = {
        "script": "run_p11_phase_c3_generate_holdout.py",
        "procedure": "Project 11 Phase C3 (procedure-preserving)",
        "manifest": str(manifest_path),
        "output_path": str(holdout_path),
        "sha256": holdout_hash,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "parameters": {
            "seed": seed,
            "n_total": len(points),
            "n_uniform": holdout["n_uniform"],
            "n_boundary": holdout["n_boundary"],
            "h_range": [h_min, h_max],
            "p_range": [p_min, p_max],
            "boundary_pool_size": boundary_pool_size
        }
    }

    save_json(metadata_path, metadata)

    print("\n" + "="*60)
    print("PHASE C3 HOLDOUT GENERATED (Project 11 Procedure)")
    print("="*60)
    print(f"seed:           {seed}")
    print(f"total points:   {len(points)}")
    print(f"  uniform:      {holdout['n_uniform']}")
    print(f"  boundary:     {holdout['n_boundary']}")
    print(f"H range:        {[h_min, h_max]}")
    print(f"P range:        {[p_min, p_max]}")
    print(f"holdout hash:   {holdout_hash}")
    print(f"saved to:       {holdout_path}")
    print(f"metadata:       {metadata_path}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
