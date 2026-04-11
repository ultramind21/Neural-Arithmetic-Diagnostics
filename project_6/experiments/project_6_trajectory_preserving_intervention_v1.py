"""
================================================================================
PROJECT 6 TRAJECTORY-PRESERVING INTERVENTION V1
================================================================================

PURPOSE:
  Test whether selective hidden-state smoothing improves family-level behavior
  more safely than naive global damping.

CORE QUESTION:
  Can we reduce harmful oscillatory jumps without destroying useful internal
  dynamics in families that already succeed?

INTERVENTION:
  At each step, compare the current hidden state with the previous one.
  Only if the difference exceeds a threshold, apply partial smoothing:

      if diff > threshold:
          h_new = alpha * h_current + (1 - alpha) * h_prev
      else:
          h_new = h_current

This differs from the previous damping probe because it is selective rather
than uniformly applied.

TARGET:
  - alternating_carry
  - full_propagation_chain
  - block_boundary_stress

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np
import torch
import torch.nn as nn


# ============================================================================
# PATHS
# ============================================================================
PROJECT_6_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_6_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_6_trajectory_preserving_intervention_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_6_trajectory_preserving_intervention_v1_report.md"


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

    return model


# ============================================================================
# PROCESSOR
# ============================================================================

class SelectiveSmoothingProcessor:
    def __init__(self, model: CarryConditionedLocalNet, device: torch.device, alpha: float, threshold: float):
        self.model = model
        self.device = device
        self.alpha = alpha
        self.threshold = threshold

    def predict_local(self, a_digit: np.ndarray, b_digit: np.ndarray, carry_in: np.ndarray, prev_hidden: torch.Tensor | None):
        x_digits = np.stack([a_digit, b_digit], axis=1).astype(np.float32)
        x_carry = np.array(carry_in, dtype=np.float32).reshape(-1, 1)

        x_digits_t = torch.tensor(x_digits, dtype=torch.float32, device=self.device)
        x_carry_t = torch.tensor(x_carry, dtype=torch.float32, device=self.device)

        with torch.no_grad():
            digit_logits, carry_logits, hidden = self.model(x_digits_t, x_carry_t)

            applied_smoothing = False
            diff_value = 0.0

            if prev_hidden is not None:
                diff_value = torch.mean(torch.abs(hidden - prev_hidden)).item()
                if diff_value > self.threshold:
                    hidden = self.alpha * hidden + (1.0 - self.alpha) * prev_hidden
                    digit_logits = self.model.digit_head(hidden)
                    carry_logits = self.model.carry_head(hidden)
                    applied_smoothing = True

            digit = digit_logits.argmax(dim=1).detach().cpu().numpy()
            carry = carry_logits.argmax(dim=1).detach().cpu().numpy()

        return digit.astype(np.int64), carry.astype(np.int64), hidden, diff_value, applied_smoothing


# ============================================================================
# EVALUATION
# ============================================================================

def evaluate_family(
    processor: SelectiveSmoothingProcessor,
    a: np.ndarray,
    b: np.ndarray,
) -> Dict[str, Any]:
    batch, length = a.shape
    pred = np.zeros((batch, length + 1), dtype=np.int64)
    truth = full_exact_addition(a, b)

    carry = np.zeros(batch, dtype=np.int64)
    prev_hidden = None

    diff_sequence = []
    smoothing_count = 0

    for pos in range(length - 1, -1, -1):
        digit, carry, hidden, diff_value, applied = processor.predict_local(
            a[:, pos], b[:, pos], carry, prev_hidden
        )

        pred[:, pos + 1] = digit
        if prev_hidden is not None:
            diff_sequence.append(float(diff_value))
        if applied:
            smoothing_count += 1

        prev_hidden = hidden

    pred[:, 0] = carry

    return {
        "exact_match": exact_match_accuracy(pred, truth),
        "trajectory_diff_mean": float(np.mean(diff_sequence)) if diff_sequence else 0.0,
        "trajectory_diff_sequence": diff_sequence,
        "smoothing_count": smoothing_count,
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 6 TRAJECTORY-PRESERVING INTERVENTION V1",
        "",
        f"## Parameters\n- alpha: {artifact['alpha']}\n- threshold: {artifact['threshold']}",
        "",
        "## Family Results",
    ]

    for family, result in artifact["family_results"].items():
        lines.append(f"\n### {family}")
        lines.append(f"- exact_match: {result['exact_match']}")
        lines.append(f"- trajectory_diff_mean: {result['trajectory_diff_mean']}")
        lines.append(f"- trajectory_diff_sequence: {result['trajectory_diff_sequence']}")
        lines.append(f"- smoothing_count: {result['smoothing_count']}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This probe tests selective trajectory smoothing rather than uniform damping.",
        "- It asks whether harmful jumps can be reduced without destroying useful dynamics.",
        "",
    ])
    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 6 TRAJECTORY-PRESERVING INTERVENTION V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    alpha = 0.5
    threshold = 5.0

    model = train_model(device=device)
    processor = SelectiveSmoothingProcessor(model, device=device, alpha=alpha, threshold=threshold)

    families = {
        "alternating_carry": make_alternating_carry(num_samples=64, length=6),
        "full_propagation_chain": make_full_propagation_chain(num_samples=64, length=6),
        "block_boundary_stress": make_block_boundary_stress(num_samples=64, length=6),
    }

    family_results = {}
    for family_name, (a, b) in families.items():
        family_results[family_name] = evaluate_family(processor, a, b)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_6_trajectory_preserving_intervention_v1",
        "alpha": alpha,
        "threshold": threshold,
        "family_results": family_results,
        "notes": [
            "This is the first selective trajectory smoothing intervention in Project 6.",
            "It tests whether large hidden jumps can be reduced without destroying useful family-level dynamics.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
