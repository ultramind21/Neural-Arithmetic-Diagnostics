"""
================================================================================
PROJECT 8 MINIMAL COMPOSITION ARCHITECTURE V2
================================================================================

PURPOSE:
  Redesign the first Project 8 architecture experiment so that local errors
  exist and interface/controller mechanisms have a real chance to matter.

CORE QUESTION:
  When controlled local errors are injected, which architecture variant best
  prevents local failure from becoming global family-level breakdown?

VARIANTS:
  1. baseline_composition
  2. interface_only
  3. controller_only
  4. interface_plus_controller

REDESIGN PRINCIPLE:
  Controlled local error injection creates a genuinely discriminative regime.

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
PROJECT_8_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_8_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_8_minimal_composition_architecture_v2_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_8_minimal_composition_architecture_v2_report.md"


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
# PATTERNS
# ============================================================================

def make_alternating_carry(length: int) -> Tuple[np.ndarray, np.ndarray]:
    a = np.array([9 if i % 2 == 0 else 0 for i in range(length)], dtype=np.int64).reshape(1, length)
    b = np.array([1 if i % 2 == 0 else 0 for i in range(length)], dtype=np.int64).reshape(1, length)
    return a, b


def make_full_propagation_chain(length: int) -> Tuple[np.ndarray, np.ndarray]:
    a = np.full((1, length), 9, dtype=np.int64)
    b = np.full((1, length), 1, dtype=np.int64)
    return a, b


def make_block_boundary_stress(length: int) -> Tuple[np.ndarray, np.ndarray]:
    a = np.zeros((1, length), dtype=np.int64)
    b = np.zeros((1, length), dtype=np.int64)

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
# TARGETS
# ============================================================================

def local_targets(a_digit: int, b_digit: int, carry_in: int):
    total = a_digit + b_digit + carry_in
    return total % 10, total // 10


def full_exact_addition(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    batch, length = a.shape
    out = np.zeros((batch, length + 1), dtype=np.int64)
    carry = np.zeros(batch, dtype=np.int64)

    for pos in range(length - 1, -1, -1):
        s = a[:, pos] + b[:, pos] + carry
        out[:, pos + 1] = s % 10
        carry = s // 10

    out[:, 0] = carry
    return out


# ============================================================================
# CONTROLLED LOCAL ERROR MODEL
# ============================================================================

def imperfect_local_predict(a_digit: int, b_digit: int, carry_in: int) -> Tuple[int, int]:
    """
    Controlled local predictor:
    - mostly correct
    - but intentionally fails on selected trigger contexts
    """
    digit_true, carry_true = local_targets(a_digit, b_digit, carry_in)

    # Inject controlled local failure on selected contexts
    if a_digit == 0 and b_digit == 0 and carry_in == 0:
        return 1, carry_true  # wrong digit
    if a_digit == 9 and b_digit == 1 and carry_in == 1:
        return 0, carry_true  # wrong digit for carry-heavy case

    return digit_true, carry_true


# ============================================================================
# VARIANT LOGIC
# ============================================================================

def maybe_interface_fix(a_digit: int, b_digit: int, carry_in: int, digit_pred: int, carry_pred: int):
    """
    Interface rule: fix known trigger contexts explicitly.
    """
    applied = False

    if a_digit == 0 and b_digit == 0 and carry_in == 0 and digit_pred == 1:
        digit_true, carry_true = local_targets(a_digit, b_digit, carry_in)
        digit_pred, carry_pred = digit_true, carry_true
        applied = True

    return digit_pred, carry_pred, applied


def maybe_controller_fix(prev_outputs: list, a_digit: int, b_digit: int, carry_in: int, digit_pred: int, carry_pred: int):
    """
    Controller rule:
    simple sequence-level override under suspicious recurrence.
    """
    applied = False

    if len(prev_outputs) >= 1:
        last = prev_outputs[-1]
        if (
            a_digit == 9 and b_digit == 1 and carry_in == 1
            and last["digit_pred"] in [0, 1]
        ):
            digit_true, carry_true = local_targets(a_digit, b_digit, carry_in)
            digit_pred, carry_pred = digit_true, carry_true
            applied = True

    return digit_pred, carry_pred, applied


# ============================================================================
# RUN VARIANT
# ============================================================================

def run_variant(a: np.ndarray, b: np.ndarray, variant_name: str) -> Dict[str, Any]:
    truth = full_exact_addition(a, b)[0].tolist()
    batch, length = a.shape
    assert batch == 1

    carry = 0
    pred_digits = []
    trace = []
    prev_outputs = []
    interface_count = 0
    controller_count = 0

    for pos in range(length - 1, -1, -1):
        a_digit = int(a[0, pos])
        b_digit = int(b[0, pos])

        digit_pred, carry_pred = imperfect_local_predict(a_digit, b_digit, carry)
        interface_applied = False
        controller_applied = False

        if variant_name in ["interface_only", "interface_plus_controller"]:
            digit_pred, carry_pred, interface_applied = maybe_interface_fix(
                a_digit, b_digit, carry, digit_pred, carry_pred
            )
            if interface_applied:
                interface_count += 1

        if variant_name in ["controller_only", "interface_plus_controller"]:
            digit_pred, carry_pred, controller_applied = maybe_controller_fix(
                prev_outputs, a_digit, b_digit, carry, digit_pred, carry_pred
            )
            if controller_applied:
                controller_count += 1

        row = {
            "position": pos,
            "a_digit": a_digit,
            "b_digit": b_digit,
            "carry_in": carry,
            "digit_pred": digit_pred,
            "carry_pred": carry_pred,
            "interface_applied": interface_applied,
            "controller_applied": controller_applied,
        }
        trace.append(row)
        prev_outputs.append(row)

        pred_digits.append(digit_pred)
        carry = carry_pred

    pred_full = [carry] + list(reversed(pred_digits))
    exact_match = (pred_full == truth)

    return {
        "truth_full_sequence": truth,
        "predicted_full_sequence": pred_full,
        "exact_match": exact_match,
        "interface_count": interface_count,
        "controller_count": controller_count,
        "trace": trace,
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 8 MINIMAL COMPOSITION ARCHITECTURE V2",
        "",
        "## Family-by-Variant Results",
    ]

    for family, variants in artifact["results"].items():
        lines.append(f"\n### {family}")
        for variant, result in variants.items():
            lines.append(f"- {variant}: exact_match={result['exact_match']}, "
                         f"interface_count={result['interface_count']}, "
                         f"controller_count={result['controller_count']}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This v2 experiment uses controlled local error injection to make variant comparison meaningful.",
        "- It tests whether interface or controller structure can prevent local failure from becoming global breakdown.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 8 MINIMAL COMPOSITION ARCHITECTURE V2")

    families = {
        "alternating_carry": make_alternating_carry(length=6),
        "full_propagation_chain": make_full_propagation_chain(length=6),
        "block_boundary_stress": make_block_boundary_stress(length=6),
    }

    variants = [
        "baseline_composition",
        "interface_only",
        "controller_only",
        "interface_plus_controller",
    ]

    results = {}
    for family_name, (a, b) in families.items():
        results[family_name] = {}
        for variant in variants:
            results[family_name][variant] = run_variant(a, b, variant)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_8_minimal_composition_architecture_v2",
        "results": results,
        "notes": [
            "This is the first discriminative architecture experiment in Project 8.",
            "It uses controlled local error injection so interface/controller effects can become visible.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
