"""
================================================================================
PROJECT 6 FAMILY-LEVEL CAUSAL LINKAGE V1
================================================================================

PURPOSE:
  Test whether digit-relevant and carry-relevant unit groups have different
  causal effects on higher-level arithmetic family behavior.

CORE QUESTION:
  Do the dissociated internal unit groups found in Project 6 contribute
  differently to:
    - alternating_carry
    - full_propagation_chain
    - block_boundary_stress

GOAL:
  Move from:
    internal dissociation
  to:
    family-level causal linkage

IMPORTANT:
  This is a stronger causal-style probe than previous Project 6 analyses.
  It still does not claim a full final circuit explanation.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, List

import numpy as np
import torch
import torch.nn as nn


# ============================================================================
# PATHS
# ============================================================================
PROJECT_6_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_6_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_6_family_level_causal_linkage_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_6_family_level_causal_linkage_v1_report.md"


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
# DATASET
# ============================================================================

def build_dataset():
    X_digits = []
    X_carry = []
    digit_y = []
    carry_y = []

    for a in range(10):
        for b in range(10):
            for carry_in in [0, 1]:
                X_digits.append([a, b])
                X_carry.append([carry_in])
                d, c = local_targets(a, b, carry_in)
                digit_y.append(d)
                carry_y.append(c)

    return (
        np.array(X_digits, dtype=np.float32),
        np.array(X_carry, dtype=np.float32),
        np.array(digit_y, dtype=np.int64),
        np.array(carry_y, dtype=np.int64),
    )


# ============================================================================
# MODEL
# ============================================================================

class CarryConditionedLocalNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.digit_net = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
        )

        self.carry_net = nn.Sequential(
            nn.Linear(1, 8),
            nn.ReLU(),
            nn.Linear(8, 8),
        )

        self.combined_net = nn.Sequential(
            nn.Linear(16 + 8, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
        )

        self.digit_head = nn.Linear(32, 10)
        self.carry_head = nn.Linear(32, 2)

    def forward(self, x_digits, x_carry):
        h_digits = self.digit_net(x_digits)
        h_carry = self.carry_net(x_carry)
        h_combined = torch.cat([h_digits, h_carry], dim=1)
        h = self.combined_net(h_combined)
        return self.digit_head(h), self.carry_head(h), h


# ============================================================================
# TRAIN
# ============================================================================

def train_model(device: torch.device):
    X_digits, X_carry, digit_y, carry_y = build_dataset()

    X_digits_t = torch.tensor(X_digits, dtype=torch.float32, device=device)
    X_carry_t = torch.tensor(X_carry, dtype=torch.float32, device=device)
    digit_t = torch.tensor(digit_y, dtype=torch.long, device=device)
    carry_t = torch.tensor(carry_y, dtype=torch.long, device=device)

    model = CarryConditionedLocalNet().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion_digit = nn.CrossEntropyLoss()
    criterion_carry = nn.CrossEntropyLoss()

    for _ in range(100):
        optimizer.zero_grad()
        digit_logits, carry_logits, _ = model(X_digits_t, X_carry_t)
        loss = criterion_digit(digit_logits, digit_t) + criterion_carry(carry_logits, carry_t)
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        digit_logits, carry_logits, hidden = model(X_digits_t, X_carry_t)
        digit_pred = digit_logits.argmax(dim=1).detach().cpu().numpy()
        carry_pred = carry_logits.argmax(dim=1).detach().cpu().numpy()
        hidden_np = hidden.detach().cpu().numpy()

    return model, digit_y, carry_y, digit_pred, carry_pred, hidden_np


# ============================================================================
# TOP UNIT IDENTIFICATION
# ============================================================================

def top_units_by_digit_success(digit_y, digit_pred, hidden_np, top_k=5):
    correct = (digit_pred == digit_y)
    success_hidden = hidden_np[correct]
    failure_hidden = hidden_np[~correct]

    success_mean = np.mean(success_hidden, axis=0)
    failure_mean = np.mean(failure_hidden, axis=0)
    diff = np.abs(success_mean - failure_mean)

    top_units = np.argsort(diff)[-top_k:][::-1]
    return [int(i) for i in top_units]


def top_units_by_carry_class(carry_y, hidden_np, top_k=5):
    carry0_hidden = hidden_np[carry_y == 0]
    carry1_hidden = hidden_np[carry_y == 1]

    mean0 = np.mean(carry0_hidden, axis=0)
    mean1 = np.mean(carry1_hidden, axis=0)
    std0 = np.std(carry0_hidden, axis=0)
    std1 = np.std(carry1_hidden, axis=0)

    separability = np.abs(mean1 - mean0) / (np.maximum(std0, std1) + 1e-6)
    top_units = np.argsort(separability)[-top_k:][::-1]
    return [int(i) for i in top_units]


# ============================================================================
# FAMILY-LEVEL PROCESSOR WITH ABLATION
# ============================================================================

class FamilyProcessor:
    def __init__(self, model: CarryConditionedLocalNet, device: torch.device, ablate_units: List[int] | None = None):
        self.model = model
        self.device = device
        self.ablate_units = ablate_units

    def predict_local(self, a_digit: np.ndarray, b_digit: np.ndarray, carry_in: np.ndarray):
        x_digits = np.stack([a_digit, b_digit], axis=1).astype(np.float32)
        x_carry = np.array(carry_in, dtype=np.float32).reshape(-1, 1)

        x_digits_t = torch.tensor(x_digits, dtype=torch.float32, device=self.device)
        x_carry_t = torch.tensor(x_carry, dtype=torch.float32, device=self.device)

        with torch.no_grad():
            digit_logits, carry_logits, hidden = self.model(x_digits_t, x_carry_t)

            if self.ablate_units:
                hidden = hidden.clone()
                hidden[:, self.ablate_units] = 0.0
                digit_logits = self.model.digit_head(hidden)
                carry_logits = self.model.carry_head(hidden)

            digit = digit_logits.argmax(dim=1).detach().cpu().numpy()
            carry = carry_logits.argmax(dim=1).detach().cpu().numpy()

        return digit.astype(np.int64), carry.astype(np.int64)


def blockwise_family_eval(
    processor: FamilyProcessor,
    a: np.ndarray,
    b: np.ndarray,
    chunk_size: int,
) -> float:
    batch, length = a.shape
    pred = np.zeros((batch, length + 1), dtype=np.int64)
    truth = full_exact_addition(a, b)

    carry_between_chunks = np.zeros(batch, dtype=np.int64)

    for chunk_end in range(length, 0, -chunk_size):
        chunk_start = max(0, chunk_end - chunk_size)
        carry = carry_between_chunks.copy()

        for pos in range(chunk_end - 1, chunk_start - 1, -1):
            digit, carry = processor.predict_local(a[:, pos], b[:, pos], carry)
            pred[:, pos + 1] = digit

        carry_between_chunks = carry

    pred[:, 0] = carry_between_chunks
    return exact_match_accuracy(pred, truth)


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 6 FAMILY-LEVEL CAUSAL LINKAGE V1",
        "",
        "## Digit-relevant Units",
        f"- {artifact['digit_units']}",
        "",
        "## Carry-relevant Units",
        f"- {artifact['carry_units']}",
        "",
        "## Family Metrics",
    ]

    for family, metrics in artifact["family_results"].items():
        lines.append(f"\n### {family}")
        lines.append(f"- baseline_exact_match: {metrics['baseline_exact_match']}")
        lines.append(f"- digit_unit_ablation_exact_match: {metrics['digit_unit_ablation_exact_match']}")
        lines.append(f"- carry_unit_ablation_exact_match: {metrics['carry_unit_ablation_exact_match']}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This probe asks whether digit-relevant and carry-relevant units affect higher-level family behavior differently.",
        "- It does not yet constitute a full final circuit explanation.",
        "",
    ])
    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 6 FAMILY-LEVEL CAUSAL LINKAGE V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, digit_y, carry_y, digit_pred, carry_pred, hidden_np = train_model(device=device)

    digit_units = top_units_by_digit_success(digit_y, digit_pred, hidden_np, top_k=5)
    carry_units = top_units_by_carry_class(carry_y, hidden_np, top_k=5)

    baseline_processor = FamilyProcessor(model, device=device, ablate_units=None)
    digit_ablation_processor = FamilyProcessor(model, device=device, ablate_units=digit_units)
    carry_ablation_processor = FamilyProcessor(model, device=device, ablate_units=carry_units)

    families = {
        "alternating_carry": make_alternating_carry(num_samples=64, length=6),
        "full_propagation_chain": make_full_propagation_chain(num_samples=64, length=6),
        "block_boundary_stress": make_block_boundary_stress(num_samples=64, length=6),
    }

    family_results = {}
    for family_name, (a, b) in families.items():
        family_results[family_name] = {
            "baseline_exact_match": blockwise_family_eval(baseline_processor, a, b, chunk_size=2),
            "digit_unit_ablation_exact_match": blockwise_family_eval(digit_ablation_processor, a, b, chunk_size=2),
            "carry_unit_ablation_exact_match": blockwise_family_eval(carry_ablation_processor, a, b, chunk_size=2),
        }

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_6_family_level_causal_linkage_v1",
        "digit_units": digit_units,
        "carry_units": carry_units,
        "family_results": family_results,
        "notes": [
            "This probe links unit-level dissociation to family-level causal effects.",
            "It compares family performance under digit-unit vs carry-unit ablation.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
