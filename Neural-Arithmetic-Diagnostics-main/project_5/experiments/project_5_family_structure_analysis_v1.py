"""
================================================================================
PROJECT 5 FAMILY STRUCTURE ANALYSIS V1
================================================================================

PURPOSE:
  Analyze structural differences between the three core families:
    - alternating_carry
    - full_propagation_chain
    - block_boundary_stress

CORE QUESTION:
  If chunk size does not explain the residual family split, what structural
  property might?

THIS SCRIPT MEASURES:
  1. carry-pattern transitions
  2. local (a,b,carry_in) diversity
  3. local pair diversity
  4. periodicity / repetition structure
  5. family-level regularity vs heterogeneity

IMPORTANT:
  This is a structural analysis script.
  It does NOT by itself prove a causal mechanism.

================================================================================
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, List

import numpy as np


# ============================================================================
# PATHS
# ============================================================================
PROJECT_5_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_5_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_5_family_structure_analysis_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_5_family_structure_analysis_v1_report.md"


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
# EXACT CARRY PATTERN
# ============================================================================

def compute_carry_sequence(a_seq: List[int], b_seq: List[int]) -> List[int]:
    carry_seq = []
    carry = 0
    for pos in range(len(a_seq) - 1, -1, -1):
        total = a_seq[pos] + b_seq[pos] + carry
        carry = 1 if total >= 10 else 0
        carry_seq.append(carry)
    carry_seq.reverse()
    return carry_seq


# ============================================================================
# ANALYSIS
# ============================================================================

def count_transitions(seq: List[int]) -> int:
    if len(seq) <= 1:
        return 0
    return sum(1 for i in range(1, len(seq)) if seq[i] != seq[i - 1])


def analyze_family(name: str, a_arr: np.ndarray, b_arr: np.ndarray) -> Dict[str, Any]:
    a_first = a_arr[0].tolist()
    b_first = b_arr[0].tolist()
    carry_seq = compute_carry_sequence(a_first, b_first)

    local_pairs = [(int(a), int(b)) for a, b in zip(a_first, b_first)]
    local_triples = [(int(a), int(b), int(c)) for a, b, c in zip(a_first, b_first, carry_seq)]

    pair_counter = Counter(local_pairs)
    triple_counter = Counter(local_triples)

    pair_diversity = len(pair_counter)
    triple_diversity = len(triple_counter)

    carry_transitions = count_transitions(carry_seq)
    a_transitions = count_transitions(a_first)
    b_transitions = count_transitions(b_first)

    periodicity_hint = "unknown"
    if len(set(a_first)) == 1 and len(set(b_first)) == 1:
        periodicity_hint = "uniform"
    elif a_first[:2] * (len(a_first) // 2) == a_first[:2 * (len(a_first) // 2)]:
        periodicity_hint = "short_periodic"
    else:
        periodicity_hint = "block_or_mixed"

    return {
        "family": name,
        "a_first": a_first,
        "b_first": b_first,
        "carry_seq_first": carry_seq,
        "a_transitions": a_transitions,
        "b_transitions": b_transitions,
        "carry_transitions": carry_transitions,
        "pair_diversity": pair_diversity,
        "triple_diversity": triple_diversity,
        "most_common_pairs": pair_counter.most_common(10),
        "most_common_triples": triple_counter.most_common(10),
        "periodicity_hint": periodicity_hint,
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 5 FAMILY STRUCTURE ANALYSIS V1",
        "",
        "## Purpose",
        "This report compares the internal structural properties of the three Project 5 core families.",
        "",
    ]

    for family_name, result in artifact["results"].items():
        lines.extend([
            f"## {family_name}",
            f"- a_first: {result['a_first']}",
            f"- b_first: {result['b_first']}",
            f"- carry_seq_first: {result['carry_seq_first']}",
            f"- a_transitions: {result['a_transitions']}",
            f"- b_transitions: {result['b_transitions']}",
            f"- carry_transitions: {result['carry_transitions']}",
            f"- pair_diversity: {result['pair_diversity']}",
            f"- triple_diversity: {result['triple_diversity']}",
            f"- periodicity_hint: {result['periodicity_hint']}",
            f"- most_common_pairs: {result['most_common_pairs']}",
            f"- most_common_triples: {result['most_common_triples']}",
            "",
        ])

    lines.extend([
        "## Interpretation Boundary",
        "- This analysis identifies structural differences, not final causal proof.",
        "- Its role is to narrow the next mechanistic or representational hypothesis.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 5 FAMILY STRUCTURE ANALYSIS V1")

    length = 6
    num_samples = 16

    families = {
        "alternating_carry": make_alternating_carry(num_samples=num_samples, length=length),
        "full_propagation_chain": make_full_propagation_chain(num_samples=num_samples, length=length),
        "block_boundary_stress": make_block_boundary_stress(num_samples=num_samples, length=length),
    }

    results = {}
    for family_name, (a, b) in families.items():
        results[family_name] = analyze_family(family_name, a, b)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_5_family_structure_analysis_v1",
        "results": results,
        "notes": [
            "This analysis compares family structure after chunk-size sensitivity ruled out granularity as the primary explanation.",
            "Its purpose is to identify what structural differences remain plausible explanatory candidates.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
