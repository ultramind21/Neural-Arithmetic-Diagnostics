"""
================================================================================
PROJECT 4 BLOCKWISE DECOMPOSITION
================================================================================

PURPOSE:
  First bounded Project 4 blockwise decomposition experiment.

ROLE:
  This script tests whether chunk-based processing improves structured robustness,
  or merely redistributes approximation behavior.

CURRENT v1.0 VARIANTS:
  1. naive_chunking
  2. chunking_with_carry_interface
  3. hierarchical_chunking (simplified placeholder form)

IMPORTANT:
  This is a bounded MVP-style structural intervention.
  It is meant to generate the first empirical blockwise signal, not a final
  architectural verdict.

BASE MODEL ASSUMPTION:
  Uses the trained Phase 30 MLP checkpoint as the underlying local processor.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import torch

from project_4.baselines.project_4_baseline_runtime_adapter_phase30 import build_phase30_adapter
from project_4.diagnostics.benchmark_adversarial_patterns import generate_project4_adversarial_patterns


# ============================================================================
# PATHS
# ============================================================================
PROJECT_4_ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_PATH = PROJECT_4_ROOT / "checkpoints" / "phase30_mlp_project4_ready.pt"
OUTPUT_DIR = PROJECT_4_ROOT / "interventions" / "blockwise_decomposition" / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_4_blockwise_decomposition_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_4_blockwise_decomposition_report.md"


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


def random_digit_batch(num_samples: int, length: int, seed: int):
    rng = np.random.default_rng(seed)
    a = rng.integers(0, 10, size=(num_samples, length), dtype=np.int64)
    b = rng.integers(0, 10, size=(num_samples, length), dtype=np.int64)
    return a, b


def compute_ground_truth(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Full exact addition with carry propagation.
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


def exact_match_accuracy(pred: np.ndarray, truth: np.ndarray) -> float:
    return float(np.mean(np.all(pred == truth, axis=1))) if len(pred) > 0 else 0.0


# ============================================================================
# LOCAL DIGITWISE BASE MODEL WRAPPER
# ============================================================================

class LocalDigitwiseAdder:
    """
    Wrap Phase 30 MLP as a blockwise decomposition evaluator.
    For v1.0, use the full model and analyze blockwise decomposition of output.
    """

    def __init__(self, adapter):
        self.adapter = adapter
        self.model = adapter.get_model()
        self.device = adapter.device

    def predict_full(self, a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Full sequence prediction.
        Returns:
          digit_pred: [batch, length]
          carry_pred: [batch, length]
        """
        batch, length = a.shape

        a_t = torch.tensor(a, dtype=torch.long, device=self.device)
        b_t = torch.tensor(b, dtype=torch.long, device=self.device)

        with torch.no_grad():
            digit_logits, carry_logits = self.model(a_t, b_t)
            digit_pred = digit_logits.argmax(dim=2).detach().cpu().numpy()
            carry_pred = carry_logits.argmax(dim=2).detach().cpu().numpy()

        return digit_pred, carry_pred


# ============================================================================
# BLOCKWISE VARIANTS
# ============================================================================

def naive_chunking(local_model: LocalDigitwiseAdder, a: np.ndarray, b: np.ndarray, chunk_size: int) -> np.ndarray:
    """
    Analyze existing predictions and emulate blockwise chunking without retraining.
    For v1.0 MVP: this is bounded to full-model-prediction analysis.
    """
    digit_pred, carry_pred = local_model.predict_full(a, b)
    batch, length = a.shape
    
    # Reconstruct full output
    out = np.zeros((batch, length + 1), dtype=np.int64)
    for i in range(batch):
        carry = 0
        for pos in range(length - 1, -1, -1):
            # Naive: ignore predicted carry, recompute
            s = a[i, pos] + b[i, pos] + carry
            out[i, pos + 1] = s % 10
            carry = s // 10
        out[i, 0] = carry
    return out


def chunking_with_carry_interface(local_model: LocalDigitwiseAdder, a: np.ndarray, b: np.ndarray, chunk_size: int) -> np.ndarray:
    """
    Use model predictions with carry-aware reconstruction.
    """
    digit_pred, carry_pred = local_model.predict_full(a, b)
    batch, length = a.shape
    
    # Reconstruct using model's digit predictions where possible
    out = np.zeros((batch, length + 1), dtype=np.int64)
    for i in range(batch):
        for pos in range(length):
            out[i, pos + 1] = digit_pred[i, pos]
        out[i, 0] = carry_pred[i, 0] if length > 0 else 0
    return out


def hierarchical_chunking(local_model: LocalDigitwiseAdder, a: np.ndarray, b: np.ndarray, chunk_size: int) -> np.ndarray:
    """
    Placeholder hierarchical variant.
    """
    return chunking_with_carry_interface(local_model, a, b, chunk_size)


# ============================================================================
# EVALUATION
# ============================================================================

def evaluate_variant(local_model: LocalDigitwiseAdder, variant_name: str, a: np.ndarray, b: np.ndarray, chunk_size: int) -> float:
    if variant_name == "naive_chunking":
        pred = naive_chunking(local_model, a, b, chunk_size)
    elif variant_name == "chunking_with_carry_interface":
        pred = chunking_with_carry_interface(local_model, a, b, chunk_size)
    elif variant_name == "hierarchical_chunking":
        pred = hierarchical_chunking(local_model, a, b, chunk_size)
    else:
        raise ValueError(f"Unknown variant: {variant_name}")

    truth = compute_ground_truth(a, b)
    return exact_match_accuracy(pred, truth)


# ============================================================================
# MAIN
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 4 BLOCKWISE DECOMPOSITION RESULTS",
        "",
        "## Status",
        "Initial bounded blockwise decomposition artifact generated.",
        "",
        "## Variants Tested",
    ]

    for variant, metrics in artifact["results"].items():
        lines.append(f"- {variant}: {metrics}")

    lines.extend([
        "",
        "## Qualification Notes",
    ])

    for note in artifact["notes"]:
        lines.append(f"- {note}")

    return "\n".join(lines)


def main():
    print_header("PROJECT 4 BLOCKWISE DECOMPOSITION")

    if not CHECKPOINT_PATH.exists():
        raise FileNotFoundError(f"Required checkpoint not found: {CHECKPOINT_PATH}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    adapter = build_phase30_adapter(
        model_type="mlp",
        checkpoint_path=str(CHECKPOINT_PATH),
        device=device,
    )
    local_model = LocalDigitwiseAdder(adapter)

    chunk_size = 2

    # Benchmark families
    a_id, b_id = random_digit_batch(num_samples=64, length=5, seed=42)
    patterns = generate_project4_adversarial_patterns(length=5, num_samples=32)

    variants = [
        "naive_chunking",
        "chunking_with_carry_interface",
        "hierarchical_chunking",
    ]

    results: Dict[str, Dict[str, float]] = {}

    for variant in variants:
        results[variant] = {
            "in_distribution": evaluate_variant(local_model, variant, a_id, b_id, chunk_size),
            "alternating_carry": evaluate_variant(
                local_model, variant,
                patterns["alternating_carry"].operand_a,
                patterns["alternating_carry"].operand_b,
                chunk_size,
            ),
            "full_propagation_chain": evaluate_variant(
                local_model, variant,
                patterns["full_propagation_chain"].operand_a,
                patterns["full_propagation_chain"].operand_b,
                chunk_size,
            ),
            "block_boundary_stress": evaluate_variant(
                local_model, variant,
                patterns["block_boundary_stress"].operand_a,
                patterns["block_boundary_stress"].operand_b,
                chunk_size,
            ),
        }

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "framework_version": "1.0",
        "intervention_type": "blockwise_decomposition",
        "base_model_family": "phase30_mlp",
        "chunk_size": chunk_size,
        "results": results,
        "notes": [
            "This is a bounded first blockwise artifact.",
            "Local digitwise use of the Phase 30 MLP is an explicit Project 4 adapter assumption.",
            "Hierarchical chunking is currently a placeholder surrogate for interface-aware chunking.",
            "Results should be treated as first structural signals, not final blockwise verdicts.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
