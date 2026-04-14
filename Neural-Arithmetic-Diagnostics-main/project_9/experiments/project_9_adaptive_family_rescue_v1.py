"""
================================================================================
PROJECT 9 ADAPTIVE FAMILY RESCUE V1
================================================================================

PURPOSE:
  Test whether family-sensitive adaptive rescue policies outperform fixed
  rescue rules in the 3D compositional sandbox.

CORE QUESTION:
  If rescue is made explicitly family-aware, can we reduce harmful
  cross-family interference while preserving or improving local-to-global behavior?

RATIONALE:
  Project 9 already established that:
  - family identity matters
  - rescue behavior is family-sensitive
  - cross-family rescue can be harmful

  The next logical step is to replace one-size-fits-all rescue rules with
  adaptive family-specific rescue policies.

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

JSON_OUTPUT = OUTPUT_DIR / "project_9_adaptive_family_rescue_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_9_adaptive_family_rescue_v1_report.md"


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
# RESCUE POLICIES
# ============================================================================

def rescue_same_family(lattice: np.ndarray, family_map: np.ndarray, target_position: Tuple[int, int, int]):
    rescued = lattice.copy()
    x, y, z = target_position
    target_family = int(family_map[target_position])

    for nx, ny, nz in neighbors_3d(x, y, z, lattice.shape):
        if int(family_map[nx, ny, nz]) == target_family:
            rescued[nx, ny, nz] = (rescued[nx, ny, nz] + 1) % 10

    return rescued


def rescue_other_family(lattice: np.ndarray, family_map: np.ndarray, target_position: Tuple[int, int, int]):
    rescued = lattice.copy()
    x, y, z = target_position
    target_family = int(family_map[target_position])

    for nx, ny, nz in neighbors_3d(x, y, z, lattice.shape):
        if int(family_map[nx, ny, nz]) != target_family:
            rescued[nx, ny, nz] = (rescued[nx, ny, nz] + 1) % 10

    return rescued


def rescue_adaptive(lattice: np.ndarray, family_map: np.ndarray, target_position: Tuple[int, int, int]):
    """
    Family-specific adaptive rescue policy:
    - Family 0: use same-family rescue
    - Family 1: no local family rewrite, use mild no-op / preserve state
    - Family 2: use same-family rescue
    """
    target_family = int(family_map[target_position])

    if target_family in [0, 2]:
        return rescue_same_family(lattice, family_map, target_position)

    # Family 1: keep unchanged in v1 (acts as "do no additional harm")
    return lattice.copy()


# ============================================================================
# MAIN
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 9 ADAPTIVE FAMILY RESCUE V1",
        "",
        "## Rescue Results",
    ]

    for row in artifact["rescue_results"]:
        lines.append(
            f"- pos={row['target_position']} family={row['target_family']} | "
            f"base={row['base_changed_count']} | "
            f"same_family={row['same_family_changed_count']} | "
            f"other_family={row['other_family_changed_count']} | "
            f"adaptive={row['adaptive_changed_count']}"
        )

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This is the first adaptive rescue experiment in Project 9.",
        "- It asks whether family-sensitive rescue policies outperform fixed same/other-family rules.",
        "",
    ])
    return "\n".join(lines)


def main():
    print_header("PROJECT 9 ADAPTIVE FAMILY RESCUE V1")

    shape = (3, 2, 2)
    lattice = build_lattice(shape=shape, seed=42)
    family_map = build_family_map(shape=shape)

    base_outputs, _, base_total_carry_count = evaluate_lattice(lattice, family_map)

    representative_positions = [
        (0, 0, 0),  # family 0
        (1, 0, 0),  # family 1
        (2, 0, 0),  # family 2
    ]

    rescue_results: List[Dict[str, Any]] = []

    for pos in representative_positions:
        target_family = int(family_map[pos])

        perturbed = perturb_cell(lattice, pos, delta=5)
        pert_outputs, _, pert_carry = evaluate_lattice(perturbed, family_map)
        base_diff = compare_outputs(base_outputs, pert_outputs)

        same_lattice = rescue_same_family(perturbed, family_map, pos)
        same_outputs, _, same_carry = evaluate_lattice(same_lattice, family_map)
        same_diff = compare_outputs(base_outputs, same_outputs)

        other_lattice = rescue_other_family(perturbed, family_map, pos)
        other_outputs, _, other_carry = evaluate_lattice(other_lattice, family_map)
        other_diff = compare_outputs(base_outputs, other_outputs)

        adaptive_lattice = rescue_adaptive(perturbed, family_map, pos)
        adaptive_outputs, _, adaptive_carry = evaluate_lattice(adaptive_lattice, family_map)
        adaptive_diff = compare_outputs(base_outputs, adaptive_outputs)

        rescue_results.append({
            "target_position": list(pos),
            "target_family": target_family,
            "base_changed_count": base_diff["changed_count"],
            "same_family_changed_count": same_diff["changed_count"],
            "other_family_changed_count": other_diff["changed_count"],
            "adaptive_changed_count": adaptive_diff["changed_count"],
            "base_carry_count": pert_carry,
            "same_family_carry_count": same_carry,
            "other_family_carry_count": other_carry,
            "adaptive_carry_count": adaptive_carry,
        })

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_9_adaptive_family_rescue_v1",
        "shape": list(shape),
        "family_map": family_map.tolist(),
        "rescue_results": rescue_results,
        "notes": [
            "This is the first adaptive rescue experiment in Project 9.",
            "It compares same-family, cross-family, and family-aware adaptive rescue policies.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
