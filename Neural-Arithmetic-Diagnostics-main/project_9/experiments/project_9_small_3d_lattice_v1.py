"""
================================================================================
PROJECT 9 SMALL 3D LATTICE V1
================================================================================

PURPOSE:
  Implement the first small 3D arithmetic-like sandbox for Project 9.

DESIGN:
  - small 3D lattice (2 x 2 x 2)
  - each cell holds a local digit-like state
  - local propagation rule includes a carry-like transfer from neighbors
  - evaluate whether local perturbation creates global inconsistency

GOAL:
  Create the minimal higher-dimensional compositional world that:
    - is interpretable
    - has nontrivial local-to-global effects
    - can support later diagnosis and intervention

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np


# ============================================================================
# PATHS
# ============================================================================
PROJECT_9_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_9_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_9_small_3d_lattice_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_9_small_3d_lattice_v1_report.md"


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

def build_lattice(shape=(2, 2, 2), seed=42):
    rng = np.random.default_rng(seed)
    digits = rng.integers(0, 10, size=shape, dtype=np.int64)
    return digits


def local_update_rule(lattice: np.ndarray, position: Tuple[int, int, int]) -> Tuple[int, int]:
    """
    Local arithmetic-like update:
      total = local digit + number of neighbors with digit >= 5
      digit_out = total % 10
      carry_out = total // 10

    This is not ordinary arithmetic; it is a controlled arithmetic-like
    compositional sandbox rule designed to create local-to-global dependency.
    """
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


def perturb_cell(lattice: np.ndarray, position: Tuple[int, int, int], new_value: int):
    perturbed = lattice.copy()
    perturbed[position] = new_value
    return perturbed


def compare_outputs(outputs_a: Dict, outputs_b: Dict) -> Dict[str, Any]:
    changed_positions = []
    for key in outputs_a:
        if outputs_a[key] != outputs_b[key]:
            changed_positions.append(key)

    return {
        "changed_count": len(changed_positions),
        "changed_positions": [list(pos) for pos in changed_positions],
    }


# ============================================================================
# MAIN
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 9 SMALL 3D LATTICE V1",
        "",
        "## Base Lattice",
        f"- shape: {artifact['shape']}",
        f"- base_lattice: {artifact['base_lattice']}",
        "",
        "## Base Evaluation",
        f"- outputs: {artifact['base_outputs']}",
        f"- carries: {artifact['base_carries']}",
        f"- total_carry_count: {artifact['base_total_carry_count']}",
        "",
        "## Perturbation Test",
        f"- perturbed_position: {artifact['perturbation']['position']}",
        f"- old_value: {artifact['perturbation']['old_value']}",
        f"- new_value: {artifact['perturbation']['new_value']}",
        f"- output_changes: {artifact['perturbation']['output_changes']}",
        f"- carry_count_before: {artifact['perturbation']['carry_count_before']}",
        f"- carry_count_after: {artifact['perturbation']['carry_count_after']}",
        "",
        "## Interpretation Boundary",
        "- This first sandbox establishes whether local perturbation creates nontrivial global effects.",
        "- It is a minimal higher-dimensional arithmetic-like composition environment.",
        "",
    ]
    return "\n".join(lines)


def main():
    print_header("PROJECT 9 SMALL 3D LATTICE V1")

    shape = (2, 2, 2)
    lattice = build_lattice(shape=shape, seed=42)

    base_outputs, base_carries, base_total_carry_count = evaluate_lattice(lattice)

    # Choose one cell perturbation for first proof-of-concept
    perturb_position = (0, 0, 0)
    old_value = int(lattice[perturb_position])
    new_value = (old_value + 5) % 10

    perturbed = perturb_cell(lattice, perturb_position, new_value)
    pert_outputs, pert_carries, pert_total_carry_count = evaluate_lattice(perturbed)

    diff = compare_outputs(base_outputs, pert_outputs)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_9_small_3d_lattice_v1",
        "shape": list(shape),
        "base_lattice": lattice.tolist(),
        "base_outputs": {str(k): v for k, v in base_outputs.items()},
        "base_carries": {str(k): v for k, v in base_carries.items()},
        "base_total_carry_count": base_total_carry_count,
        "perturbation": {
            "position": list(perturb_position),
            "old_value": old_value,
            "new_value": new_value,
            "output_changes": diff,
            "carry_count_before": base_total_carry_count,
            "carry_count_after": pert_total_carry_count,
        },
        "notes": [
            "This is the first higher-dimensional compositional sandbox in Project 9.",
            "Its purpose is to test whether local perturbation produces nontrivial global effects.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
