"""
================================================================================
PROJECT 6 SUBSPACE INTERVENTION V1
================================================================================

PURPOSE:
  Test whether the carry-related direction identified in hidden space is
  causally important for local arithmetic behavior.

CORE QUESTION:
  What happens if we remove or suppress the hidden-state component aligned with
  the carry direction?

INTERVENTION:
  Project hidden activations onto the carry direction and subtract that
  component before decoding the output heads.

GOAL:
  Move from:
    subspace observation
  to:
    subspace-level causal intervention

IMPORTANT:
  This is the first direct subspace intervention in Project 6.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import numpy as np
import torch
import torch.nn as nn


# ============================================================================
# PATHS
# ============================================================================
PROJECT_6_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_6_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_6_subspace_intervention_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_6_subspace_intervention_v1_report.md"


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


def normalize(v: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(v)
    if norm < 1e-12:
        return v.copy()
    return v / norm


# ============================================================================
# DATA
# ============================================================================

def local_targets(a_digit: int, b_digit: int, carry_in: int):
    total = a_digit + b_digit + carry_in
    return total % 10, total // 10


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

    model.eval()
    with torch.no_grad():
        digit_logits, carry_logits, hidden = model(X_digits_t, X_carry_t)
        digit_pred = digit_logits.argmax(dim=1).detach().cpu().numpy()
        carry_pred = carry_logits.argmax(dim=1).detach().cpu().numpy()
        hidden_np = hidden.detach().cpu().numpy()

    return X_digits_t, X_carry_t, digit_y, carry_y, digit_pred, carry_pred, hidden_np, model


# ============================================================================
# DIRECTION EXTRACTION
# ============================================================================

def compute_carry_direction(carry_y, hidden_np):
    carry0_mean = np.mean(hidden_np[carry_y == 0], axis=0)
    carry1_mean = np.mean(hidden_np[carry_y == 1], axis=0)
    return normalize(carry1_mean - carry0_mean)


# ============================================================================
# INTERVENTION
# ============================================================================

def evaluate_with_optional_subspace_removal(model, X_digits_t, X_carry_t, digit_y, carry_y, carry_direction=None):
    with torch.no_grad():
        digit_logits, carry_logits, hidden = model(X_digits_t, X_carry_t)

        if carry_direction is not None:
            direction_t = torch.tensor(carry_direction, dtype=hidden.dtype, device=hidden.device).view(1, -1)
            projection = (hidden * direction_t).sum(dim=1, keepdim=True) * direction_t
            hidden = hidden - projection
            digit_logits = model.digit_head(hidden)
            carry_logits = model.carry_head(hidden)

        digit_pred = digit_logits.argmax(dim=1).detach().cpu().numpy()
        carry_pred = carry_logits.argmax(dim=1).detach().cpu().numpy()

    digit_correct = (digit_pred == digit_y)
    carry_correct = (carry_pred == carry_y)
    exact_correct = digit_correct & carry_correct

    return {
        "digit_acc": float(np.mean(digit_correct)),
        "carry_acc": float(np.mean(carry_correct)),
        "exact_acc": float(np.mean(exact_correct)),
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 6 SUBSPACE INTERVENTION V1",
        "",
        "## Carry Direction Information",
        f"- first 5 dims: {artifact['carry_direction_first5']}",
        "",
        "## Metrics",
        f"- baseline: {artifact['baseline_metrics']}",
        f"- carry_direction_removed: {artifact['carry_direction_removed_metrics']}",
        "",
        "## Interpretation Boundary",
        "- This probe tests whether the carry-related direction is causally important under direct subspace removal.",
        "- It does not yet establish a full geometric theory of arithmetic computation.",
        "",
    ]
    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 6 SUBSPACE INTERVENTION V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    X_digits_t, X_carry_t, digit_y, carry_y, digit_pred, carry_pred, hidden_np, model = train_model(device=device)

    carry_direction = compute_carry_direction(carry_y, hidden_np)

    baseline_metrics = evaluate_with_optional_subspace_removal(
        model, X_digits_t, X_carry_t, digit_y, carry_y, carry_direction=None
    )

    carry_removed_metrics = evaluate_with_optional_subspace_removal(
        model, X_digits_t, X_carry_t, digit_y, carry_y, carry_direction=carry_direction
    )

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_6_subspace_intervention_v1",
        "carry_direction_first5": [float(x) for x in carry_direction[:5]],
        "baseline_metrics": baseline_metrics,
        "carry_direction_removed_metrics": carry_removed_metrics,
        "notes": [
            "This is the first direct subspace intervention in Project 6.",
            "It removes the carry-related direction before output decoding.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
