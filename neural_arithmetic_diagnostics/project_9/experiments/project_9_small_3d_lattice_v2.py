"""
================================================================================
PROJECT 9 SMALL 3D LATTICE V2
================================================================================

PURPOSE:
  Extend the first 3D sandbox from 2×2×2 to 3×2×2 in order to test whether
  perturbation symmetry breaks in a slightly larger higher-dimensional structure.

CORE QUESTION:
  Does a larger lattice reveal non-uniform perturbation influence across positions?

GOAL:
  Detect whether:
    - changed-count symmetry breaks
    - carry-dynamic asymmetry becomes richer
    - different structural roles (edge/interior-like positions) begin to emerge

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

JSON_OUTPUT = OUTPUT_DIR / "project_9_small_3d_lattice_v2_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_9_small_3d_lattice_v2_report.md"


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


def local_update_rule(lattice: np.ndarray, position: Tuple[int, int, int]) -> Tuple[int, int]:
    x, y, z = position
    local_digit = int(lattice[x, y, z])
    neigh = neighbors_3d(x, y, z, lattice.shape)

    high_neighbor_count = sum(1 for (nx, ny, nz) in neigh if lattice[nx, ny, nz] >= 5)

    total = local_digit + high_neighbor_count
    digit_out = total % 10
    carry_out = total // 10
    return digit_out, carry_out


def evaluate_lattice(lattice: np.ndarray):
    outputs = {}
    carries = {}
    total_carry_count = 0

    for x in range(lattice.shape[0]):
        for y in range(lattice.shape[1]):
            for z in range(lattice.shape[2]):
                d, c = local_update_rule(lattice, (x, y, z))
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


def classify_position_type(position: Tuple[int, int, int], shape: Tuple[int, int, int]) -> str:
    x, y, z = position
    X, Y, Z = shape

    boundary_count = 0
    if x == 0 or x == X - 1:
        boundary_count += 1
    if y == 0 or y == Y - 1:
        boundary_count += 1
    if z == 0 or z == Z - 1:
        boundary_count += 1

    if boundary_count == 3:
        return "corner_like"
    elif boundary_count == 2:
        return "edge_like"
    elif boundary_count == 1:
        return "face_like"
    else:
        return "interior_like"


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 9 SMALL 3D LATTICE V2",
        "",
        "## Base Lattice",
        f"- shape: {artifact['shape']}",
        f"- base_total_carry_count: {artifact['base_total_carry_count']}",
        "",
        "## Position Sensitivity Map",
    ]

    for row in artifact["position_results"]:
        lines.append(
            f"- pos={row['position']} ({row['position_type']}) | "
            f"old={row['old_value']} -> new={row['new_value']} | "
            f"changed_count={row['changed_count']} | "
            f"carry_before={row['carry_count_before']} | "
            f"carry_after={row['carry_count_after']}"
        )

    lines.extend([
        "",
        "## Ranked Influence",
    ])

    for row in artifact["ranked_by_influence"]:
        lines.append(
            f"- pos={row['position']} ({row['position_type']}) | "
            f"changed_count={row['changed_count']} | "
            f"carry_before={row['carry_count_before']} | carry_after={row['carry_count_after']}"
        )

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This experiment tests whether a larger 3D lattice breaks the perturbation symmetry of v1.",
        "- It is the first scale-up result in Project 9.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 9 SMALL 3D LATTICE V2")

    shape = (3, 2, 2)
    lattice = build_lattice(shape=shape, seed=42)

    base_outputs, base_carries, base_total_carry_count = evaluate_lattice(lattice)

    position_results: List[Dict[str, Any]] = []

    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                pos = (x, y, z)
                old_value = int(lattice[pos])

                new_lattice = perturb_cell(lattice, pos, delta=5)

                new_outputs, new_carries, new_total_carry_count = evaluate_lattice(new_lattice)
                diff = compare_outputs(base_outputs, new_outputs)

                position_results.append({
                    "position": list(pos),
                    "position_type": classify_position_type(pos, shape),
                    "old_value": old_value,
                    "new_value": int(new_lattice[pos]),
                    "changed_count": diff["changed_count"],
                    "changed_positions": diff["changed_positions"],
                    "carry_count_before": base_total_carry_count,
                    "carry_count_after": new_total_carry_count,
                })

    ranked = sorted(position_results, key=lambda row: row["changed_count"], reverse=True)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_9_small_3d_lattice_v2",
        "shape": list(shape),
        "base_lattice": lattice.tolist(),
        "base_total_carry_count": base_total_carry_count,
        "position_results": position_results,
        "ranked_by_influence": ranked,
        "notes": [
            "This is the first scale-up of the 3D compositional sandbox.",
            "It tests whether a slightly larger lattice reveals non-uniform perturbation influence.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
