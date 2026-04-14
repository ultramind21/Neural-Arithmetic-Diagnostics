"""
================================================================================
PROJECT 5 DECOMPOSITION BLOCKWISE V1
================================================================================

PURPOSE:
  First bounded decomposition experiment for Project 5.

CORE QUESTION:
  Does small-block decomposition with explicit carry interface improve
  structural robustness in neural arithmetic?

CURRENT DESIGN:
  - uses a local arithmetic oracle as a clean decomposition control
  - compares:
      1. full exact arithmetic reference
      2. blockwise arithmetic with explicit carry interface
      3. blockwise arithmetic with carry reset at chunk boundaries
  - evaluates on:
      * alternating carry
      * full propagation chain
      * block-boundary stress

IMPORTANT:
  This first experiment is intentionally clean and conservative.
  It does NOT yet use a learned local processor.
  It is designed to isolate the decomposition question before introducing
  learned local modules.

INTERPRETATION:
  This is a structural decomposition probe, not a final Project 5 claim.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np


# ============================================================================
# PATHS
# ============================================================================
PROJECT_5_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_5_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_5_decomposition_blockwise_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_5_decomposition_blockwise_v1_report.md"


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


def exact_match_accuracy(pred: np.ndarray, truth: np.ndarray) -> float:
    if pred.shape != truth.shape:
        raise ValueError(f"Shape mismatch: {pred.shape} vs {truth.shape}")
    return float(np.mean(np.all(pred == truth, axis=1))) if len(pred) > 0 else 0.0


# ============================================================================
# PATTERN GENERATORS
# ============================================================================

def make_alternating_carry(num_samples: int, length: int) -> Tuple[np.ndarray, np.ndarray]:
    a_row = [9 if i % 2 == 0 else 0 for i in range(length)]
    b_row = [1 if i % 2 == 0 else 0 for i in range(length)]
    a = np.tile(np.array(a_row, dtype=np.int64), (num_samples, 1))
    b = np.tile(np.array(b_row, dtype=np.int64), (num_samples, 1))
    return a, b


def make_full_propagation_chain(num_samples: int, length: int) -> Tuple[np.ndarray, np.ndarray]:
    a = np.full((num_samples, length), 9, dtype=np.int64)
    b = np.full((num_samples, length), 1, dtype=np.int64)
    return a, b


def make_block_boundary_stress(num_samples: int, length: int) -> Tuple[np.ndarray, np.ndarray]:
    a = np.zeros((num_samples, length), dtype=np.int64)
    b = np.zeros((num_samples, length), dtype=np.int64)

    blocks = np.array_split(np.arange(length), 4)
    if len(blocks) >= 4:
        for i in blocks[1]:
            a[:, i] = 9
        for i in blocks[2]:
            a[:, i] = 1
            b[:, i] = 8
    else:
        half = length // 2
        a[:, :half] = 9
        a[:, half:] = 1
        b[:, half:] = 8

    return a, b


# ============================================================================
# EXACT ARITHMETIC
# ============================================================================

def full_exact_addition(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Standard full carry-propagating addition.
    Returns [batch, length + 1]
    """
    batch, length = a.shape
    out = np.zeros((batch, length + 1), dtype=np.int64)
    carry = np.zeros(batch, dtype=np.int64)

    for pos in range(length - 1, -1, -1):
        s = a[:, pos] + b[:, pos] + carry
        out[:, pos + 1] = s % 10
        carry = s // 10

    out[:, 0] = carry
    return out


def local_block_addition(
    a_block: np.ndarray,
    b_block: np.ndarray,
    carry_in: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Exact local block addition with explicit carry-in.
    Returns:
      block_output_digits [batch, block_len]
      carry_out [batch]
    """
    batch, block_len = a_block.shape
    digits = np.zeros((batch, block_len), dtype=np.int64)
    carry = carry_in.copy()

    for local_pos in range(block_len - 1, -1, -1):
        s = a_block[:, local_pos] + b_block[:, local_pos] + carry
        digits[:, local_pos] = s % 10
        carry = s // 10

    return digits, carry


# ============================================================================
# DECOMPOSITION VARIANTS
# ============================================================================

def blockwise_with_carry_interface(a: np.ndarray, b: np.ndarray, chunk_size: int) -> np.ndarray:
    """
    Full carry is passed across chunk boundaries.
    """
    batch, length = a.shape
    out = np.zeros((batch, length + 1), dtype=np.int64)

    carry_between_chunks = np.zeros(batch, dtype=np.int64)

    for chunk_end in range(length, 0, -chunk_size):
        chunk_start = max(0, chunk_end - chunk_size)

        a_block = a[:, chunk_start:chunk_end]
        b_block = b[:, chunk_start:chunk_end]

        block_digits, carry_between_chunks = local_block_addition(
            a_block, b_block, carry_between_chunks
        )

        out[:, chunk_start + 1:chunk_end + 1] = block_digits

    out[:, 0] = carry_between_chunks
    return out


def blockwise_carry_reset(a: np.ndarray, b: np.ndarray, chunk_size: int) -> np.ndarray:
    """
    Carry is reset at each chunk boundary.
    This acts as a decomposition stress control.
    """
    batch, length = a.shape
    out = np.zeros((batch, length + 1), dtype=np.int64)

    for chunk_end in range(length, 0, -chunk_size):
        chunk_start = max(0, chunk_end - chunk_size)

        a_block = a[:, chunk_start:chunk_end]
        b_block = b[:, chunk_start:chunk_end]

        carry_in = np.zeros(batch, dtype=np.int64)
        block_digits, block_carry = local_block_addition(a_block, b_block, carry_in)

        out[:, chunk_start + 1:chunk_end + 1] = block_digits

        # carry is intentionally not propagated across blocks
        if chunk_start == 0:
            out[:, 0] = block_carry

    return out


# ============================================================================
# EVALUATION
# ============================================================================

def evaluate_family(a: np.ndarray, b: np.ndarray, chunk_size: int) -> Dict[str, float]:
    truth = full_exact_addition(a, b)

    pred_full = full_exact_addition(a, b)
    pred_interface = blockwise_with_carry_interface(a, b, chunk_size=chunk_size)
    pred_reset = blockwise_carry_reset(a, b, chunk_size=chunk_size)

    return {
        "full_exact_reference": exact_match_accuracy(pred_full, truth),
        "blockwise_with_carry_interface": exact_match_accuracy(pred_interface, truth),
        "blockwise_carry_reset": exact_match_accuracy(pred_reset, truth),
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 5 DECOMPOSITION BLOCKWISE V1 RESULTS",
        "",
        "## Status",
        "First bounded decomposition experiment completed.",
        "",
        "## Experiment Type",
        "Small-block decomposition with explicit carry interface",
        "",
        f"## Chunk Size\n- {artifact['chunk_size']}",
        "",
        "## Family Results",
    ]

    for family, result in artifact["results"].items():
        lines.append(f"\n### {family}")
        for k, v in result.items():
            lines.append(f"- {k}: {v}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This is a clean decomposition control experiment using exact local arithmetic.",
        "- It does not yet use a learned local processor.",
        "- Its role is to test whether decomposition itself is structurally favorable before learned local decomposition is attempted.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 5 DECOMPOSITION BLOCKWISE V1")

    chunk_size = 2
    length = 6
    num_samples = 64

    families = {
        "alternating_carry": make_alternating_carry(num_samples=num_samples, length=length),
        "full_propagation_chain": make_full_propagation_chain(num_samples=num_samples, length=length),
        "block_boundary_stress": make_block_boundary_stress(num_samples=num_samples, length=length),
    }

    results: Dict[str, Dict[str, float]] = {}

    for family_name, (a, b) in families.items():
        results[family_name] = evaluate_family(a, b, chunk_size=chunk_size)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_5_decomposition_blockwise_v1",
        "chunk_size": chunk_size,
        "length": length,
        "num_samples": num_samples,
        "results": results,
        "notes": [
            "This is the first clean Project 5 decomposition experiment.",
            "It uses exact local arithmetic rather than a learned local processor.",
            "Its purpose is to isolate the structural effect of decomposition and chunk-boundary carry handling.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
