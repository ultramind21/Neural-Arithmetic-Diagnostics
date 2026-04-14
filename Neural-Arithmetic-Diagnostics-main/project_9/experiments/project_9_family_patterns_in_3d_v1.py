"""
================================================================================
PROJECT 9 FAMILY PATTERNS IN 3D V1
================================================================================

PURPOSE:
  Introduce family-like structure into the 3D arithmetic sandbox and test
  whether family membership affects perturbation propagation.

CORE QUESTION:
  Does family identity inside a 3D compositional lattice shape local-to-global
  influence patterns?

GOAL:
  Extend the sandbox from pure topology-sensitive propagation to
  family-sensitive higher-dimensional composition.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, List

import numpy as np


# ============================================================================
# PATHS
# ============================================================================
PROJECT_9_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_9_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_9_family_patterns_in_3d_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_9_family_patterns_in_3d_v1_report.md"


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def save_json(path: Path, obj: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def save_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def neighbors_3d(x: int, y: int, z: int, shape: Tuple[int, int, int]):
    X, Y, Z = shape
    neigh = []
    for dx, dy, dz in [
        (-1, 0, 0), (1, 0, 0),
        (0, -1, 0), (0, 1, 0),
        (0, 0, -1), (0, 0, 1),
    ]:
        nx, ny, nz = x + dx, y + dy, z + dz
        if 0 <= nx < X and 0 <= ny < Y and 0 <= nz < Z:
            neigh.append((nx, ny, nz))
    return neigh


# ============================================================================
# SANDBOX
# ============================================================================

def build_lattice(shape=(3, 2, 2), seed=42):
    rng = np.random.default_rng(seed)
    return rng.integers(0, 10, size=shape, dtype=np.int64)


def build_family_map(shape=(3, 2, 2)):
    """
    Define three simple family types:
      0 = low
      1 = transition
      2 = high
    based on x-axis slices
    """
    family_map = np.zeros(shape, dtype=np.int64)
    X, Y, Z = shape

    for x in range(X):
        if x == 0:
            family_map[x, :, :] = 0
        elif x == 1:
            family_map[x, :, :] = 1
        else:
            family_map[x, :, :] = 2

    return family_map


def local_update_rule(lattice: np.ndarray, family_map: np.ndarray, position: Tuple[int, int, int]) -> Tuple[int, int]:
    """
    Arithmetic-like family-sensitive local update:
      total = local_digit + high_neighbor_count + family_bonus

    family_bonus:
      family 0 -> +0
      family 1 -> +1
      family 2 -> +2
    """
    x, y, z = position
    local_digit = int(lattice[x, y, z])
    local_family = int(family_map[x, y, z])

    neigh = neighbors_3d(x, y, z, lattice.shape)
    high_neighbor_count = sum(1 for (nx, ny, nz) in neigh if lattice[nx, ny, nz] >= 5)

    family_bonus = local_family
    total = local_digit + high_neighbor_count + family_bonus

    digit_out = total % 10
    carry_out = total // 10
    return digit_out, carry_out


def evaluate_lattice(lattice: np.ndarray, family_map: np.ndarray):
    outputs = {}
    carries = {}
    total_carry_count = 0

    for x in range(lattice.shape[0]):
        for y in range(lattice.shape[1]):
            for z in range(lattice.shape[2]):
                d, c = local_update_rule(lattice, family_map, (x, y, z))
                outputs[(x, y, z)] = d
                carries[(x, y, z)] = c
                total_carry_count += c

    return outputs, carries, total_carry_count


def compare_outputs(outputs_a: Dict, outputs_b: Dict):
    changed_positions = []
    for key in outputs_a:
        if outputs_a[key] != outputs_b[key]:
            changed_positions.append(key)

    return {
        "changed_count": len(changed_positions),
        "changed_positions": [list(pos) for pos in changed_positions],
    }


def perturb_cell(lattice: np.ndarray, position: Tuple[int, int, int], delta: int):
    perturbed = lattice.copy()
    perturbed[position] = (perturbed[position] + delta) % 10
    return perturbed


# ============================================================================
# MAIN
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 9 FAMILY PATTERNS IN 3D V1",
        "",
        "## Base Structure",
        f"- shape: {artifact['shape']}",
        f"- family_map: {artifact['family_map']}",
        f"- base_total_carry_count: {artifact['base_total_carry_count']}",
        "",
        "## Perturbation Results",
    ]

    for row in artifact["position_results"]:
        lines.append(
            f"- pos={row['position']} | family={row['family_type']} | "
            f"changed_count={row['changed_count']} | carry {row['carry_count_before']}→{row['carry_count_after']}"
        )

    lines.extend([
        "",
        "## Family Aggregates",
    ])

    for family, agg in artifact["family_aggregates"].items():
        lines.append(f"- family {family}: {agg}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This experiment tests whether family identity affects perturbation propagation in the 3D sandbox.",
        "- It extends Project 9 from topology-sensitive to family-sensitive higher-dimensional structure.",
        "",
    ])

    return "\n".join(lines)


def main():
    print_header("PROJECT 9 FAMILY PATTERNS IN 3D V1")

    shape = (3, 2, 2)
    lattice = build_lattice(shape=shape, seed=42)
    family_map = build_family_map(shape=shape)

    base_outputs, base_carries, base_total_carry_count = evaluate_lattice(lattice, family_map)

    position_results: List[Dict[str, Any]] = []

    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                pos = (x, y, z)
                old_value = int(lattice[pos])
                family_type = int(family_map[pos])

                new_lattice = perturb_cell(lattice, pos, delta=5)

                new_outputs, new_carries, new_total_carry_count = evaluate_lattice(new_lattice, family_map)
                diff = compare_outputs(base_outputs, new_outputs)

                position_results.append({
                    "position": list(pos),
                    "family_type": family_type,
                    "old_value": old_value,
                    "new_value": int(new_lattice[pos]),
                    "changed_count": diff["changed_count"],
                    "changed_positions": diff["changed_positions"],
                    "carry_count_before": base_total_carry_count,
                    "carry_count_after": new_total_carry_count,
                })

    # Aggregate by family type
    family_aggregates = {}
    for family_type in [0, 1, 2]:
        family_rows = [row for row in position_results if row["family_type"] == family_type]
        family_aggregates[str(family_type)] = {
            "mean_changed_count": float(np.mean([r["changed_count"] for r in family_rows])),
            "mean_carry_after": float(np.mean([r["carry_count_after"] for r in family_rows])),
            "positions": [r["position"] for r in family_rows],
        }

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_9_family_patterns_in_3d_v1",
        "shape": list(shape),
        "base_lattice": lattice.tolist(),
        "family_map": family_map.tolist(),
        "base_total_carry_count": base_total_carry_count,
        "position_results": position_results,
        "family_aggregates": family_aggregates,
        "notes": [
            "This is the first family-sensitive 3D sandbox experiment in Project 9.",
            "It tests whether family identity shapes perturbation propagation in a higher-dimensional compositional world.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
