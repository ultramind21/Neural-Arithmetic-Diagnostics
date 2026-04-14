"""
================================================================================
PROJECT 4 ADVERSARIAL PATTERN BENCHMARKS
================================================================================

PURPOSE:
  Official adversarial pattern generator for Project 4 framework v1.0.

PATTERN FAMILIES INCLUDED:
  1. alternating_carry
  2. full_propagation_chain
  3. block_boundary_stress

DESIGN GOAL:
  Provide a reproducible, inspectable, framework-level set of structured
  arithmetic stress patterns for diagnostic evaluation.

IMPORTANT:
  This module generates benchmark inputs.
  It does NOT evaluate model predictions by itself.

================================================================================
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import numpy as np


# ============================================================================
# DATA CLASS
# ============================================================================

@dataclass
class AdversarialPattern:
    name: str
    description: str
    length: int
    num_samples: int
    operand_a: np.ndarray
    operand_b: np.ndarray
    metadata: Dict[str, Any]


# ============================================================================
# HELPERS
# ============================================================================

def _repeat_rows(base_row: List[int], num_samples: int) -> np.ndarray:
    row = np.array(base_row, dtype=np.int64)
    return np.tile(row, (num_samples, 1))


def _block_ranges(length: int, n_blocks: int = 4):
    """
    Split sequence into roughly equal contiguous blocks.
    """
    indices = np.array_split(np.arange(length), n_blocks)
    return [list(idx_block) for idx_block in indices]


# ============================================================================
# PATTERN BUILDERS
# ============================================================================

def build_alternating_carry(length: int, num_samples: int) -> AdversarialPattern:
    """
    Alternating carry pattern:
      a = 9,0,9,0,...
      b = 1,0,1,0,...
    """
    a_row = [9 if i % 2 == 0 else 0 for i in range(length)]
    b_row = [1 if i % 2 == 0 else 0 for i in range(length)]

    return AdversarialPattern(
        name="alternating_carry",
        description="Alternating 9,0,9,0... + 1,0,1,0...",
        length=length,
        num_samples=num_samples,
        operand_a=_repeat_rows(a_row, num_samples),
        operand_b=_repeat_rows(b_row, num_samples),
        metadata={
            "family": "structured_adversarial",
            "pattern_type": "periodic",
            "intended_stress": "alternating carry structure",
        },
    )


def build_full_propagation_chain(length: int, num_samples: int) -> AdversarialPattern:
    """
    Full propagation chain:
      a = 9,9,9,9,...
      b = 1,1,1,1,...
    """
    a_row = [9 for _ in range(length)]
    b_row = [1 for _ in range(length)]

    return AdversarialPattern(
        name="full_propagation_chain",
        description="Full carry propagation chain: 999...9 + 111...1",
        length=length,
        num_samples=num_samples,
        operand_a=_repeat_rows(a_row, num_samples),
        operand_b=_repeat_rows(b_row, num_samples),
        metadata={
            "family": "structured_adversarial",
            "pattern_type": "long_dependency",
            "intended_stress": "long carry propagation",
        },
    )


def build_block_boundary_stress(length: int, num_samples: int) -> AdversarialPattern:
    """
    Block-boundary stress pattern:
    Construct blocks so carry-relevant transitions occur at or across block edges.

    v1.0 implementation:
      - first block mostly zeros
      - second block mostly 9s in a
      - third block mostly 1s in b
      - final block zeros
    """
    a_row = [0 for _ in range(length)]
    b_row = [0 for _ in range(length)]

    blocks = _block_ranges(length, n_blocks=4)

    if len(blocks) >= 4:
        # block 2: 9s in a
        for i in blocks[1]:
            a_row[i] = 9

        # block 3: 1s in a, 8s in b to create a structured stress region
        for i in blocks[2]:
            a_row[i] = 1
            b_row[i] = 8
    else:
        # fallback for very small lengths
        for i in range(length // 2):
            a_row[i] = 9
        for i in range(length // 2, length):
            a_row[i] = 1
            b_row[i] = 8

    return AdversarialPattern(
        name="block_boundary_stress",
        description="Block-boundary stress pattern with structured carry transitions",
        length=length,
        num_samples=num_samples,
        operand_a=_repeat_rows(a_row, num_samples),
        operand_b=_repeat_rows(b_row, num_samples),
        metadata={
            "family": "structured_adversarial",
            "pattern_type": "block_boundary",
            "intended_stress": "carry transitions across contiguous regions",
            "blocks": _block_ranges(length, n_blocks=4),
        },
    )


# ============================================================================
# PUBLIC API
# ============================================================================

def generate_project4_adversarial_patterns(length: int = 20, num_samples: int = 8) -> Dict[str, AdversarialPattern]:
    """
    Generate the full Project 4 v1.0 adversarial core.
    """
    patterns = {
        "alternating_carry": build_alternating_carry(length, num_samples),
        "full_propagation_chain": build_full_propagation_chain(length, num_samples),
        "block_boundary_stress": build_block_boundary_stress(length, num_samples),
    }
    return patterns


def patterns_to_dict(patterns: Dict[str, AdversarialPattern]) -> Dict[str, Dict[str, Any]]:
    return {name: asdict(pattern) for name, pattern in patterns.items()}


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    patterns = generate_project4_adversarial_patterns(length=20, num_samples=4)

    print("=" * 80)
    print("PROJECT 4 ADVERSARIAL PATTERN BENCHMARKS — DEMO")
    print("=" * 80)

    for name, pattern in patterns.items():
        print(f"\nPattern: {pattern.name}")
        print(f"Description: {pattern.description}")
        print(f"Length: {pattern.length}")
        print(f"Samples: {pattern.num_samples}")
        print(f"Metadata: {pattern.metadata}")
        print(f"operand_a shape: {pattern.operand_a.shape}")
        print(f"operand_b shape: {pattern.operand_b.shape}")
        print(f"first row a: {pattern.operand_a[0].tolist()}")
        print(f"first row b: {pattern.operand_b[0].tolist()}")
