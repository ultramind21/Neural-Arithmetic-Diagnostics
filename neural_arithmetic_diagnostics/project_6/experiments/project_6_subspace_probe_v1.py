"""
================================================================================
PROJECT 6 SUBSPACE PROBE V1
================================================================================

PURPOSE:
  Test whether arithmetic-relevant signals are captured by low-dimensional
  directions/subspaces rather than only by individual units.

CORE QUESTION:
  Are carry-related and success-related distinctions visible as meaningful
  directions in hidden activation space?

THIS PROBE DOES:
  1. trains the carry-conditioned local model
  2. extracts hidden activations
  3. computes mean-difference directions for:
     - carry_out = 0 vs carry_out = 1
     - success vs failure
  4. projects activations onto those directions
  5. reports separability and directional overlap

IMPORTANT:
  This is a first subspace-level probe, not yet a full subspace intervention.

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

JSON_OUTPUT = OUTPUT_DIR / "project_6_subspace_probe_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_6_subspace_probe_v1_report.md"


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


def projection_stats(hidden: np.ndarray, direction: np.ndarray, labels: np.ndarray):
    """
    Return mean projection for label 0 and label 1, plus separation.
    """
    proj = hidden @ direction
    proj0 = proj[labels == 0]
    proj1 = proj[labels == 1]

    mean0 = float(np.mean(proj0))
    mean1 = float(np.mean(proj1))
    sep = abs(mean1 - mean0)

    return {
        "mean_label0": mean0,
        "mean_label1": mean1,
        "separation": sep,
    }


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

    return digit_y, carry_y, digit_pred, carry_pred, hidden_np


# ============================================================================
# SUBSPACE ANALYSIS
# ============================================================================

def run_subspace_probe(digit_y, carry_y, digit_pred, carry_pred, hidden_np):
    digit_correct = (digit_pred == digit_y)
    carry_correct = (carry_pred == carry_y)
    exact_correct = digit_correct & carry_correct

    # carry direction
    carry0_mean = np.mean(hidden_np[carry_y == 0], axis=0)
    carry1_mean = np.mean(hidden_np[carry_y == 1], axis=0)
    carry_direction = normalize(carry1_mean - carry0_mean)

    # success/failure direction
    success_mean = np.mean(hidden_np[exact_correct], axis=0)
    failure_mean = np.mean(hidden_np[~exact_correct], axis=0)
    success_failure_direction = normalize(success_mean - failure_mean)

    # overlap between directions
    direction_cosine = float(np.dot(carry_direction, success_failure_direction))

    carry_stats = projection_stats(hidden_np, carry_direction, carry_y)
    sf_labels = exact_correct.astype(np.int64)
    sf_stats = projection_stats(hidden_np, success_failure_direction, sf_labels)

    # cross-check projections
    carry_direction_on_success_failure = projection_stats(hidden_np, carry_direction, sf_labels)
    sf_direction_on_carry = projection_stats(hidden_np, success_failure_direction, carry_y)

    return {
        "carry_direction_first5": [float(x) for x in carry_direction[:5]],
        "success_failure_direction_first5": [float(x) for x in success_failure_direction[:5]],
        "direction_cosine": direction_cosine,
        "carry_projection_stats": carry_stats,
        "success_failure_projection_stats": sf_stats,
        "carry_direction_on_success_failure": carry_direction_on_success_failure,
        "success_failure_direction_on_carry": sf_direction_on_carry,
        "overall_digit_acc": float(np.mean(digit_correct)),
        "overall_carry_acc": float(np.mean(carry_correct)),
        "overall_exact_acc": float(np.mean(exact_correct)),
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    a = artifact["analysis"]

    lines = [
        "# PROJECT 6 SUBSPACE PROBE V1",
        "",
        "## Overall Local Metrics",
        f"- digit_acc: {a['overall_digit_acc']}",
        f"- carry_acc: {a['overall_carry_acc']}",
        f"- exact_acc: {a['overall_exact_acc']}",
        "",
        "## Direction Alignment",
        f"- carry vs success/failure cosine: {a['direction_cosine']}",
        "",
        "## Carry Direction Projection",
        f"- {a['carry_projection_stats']}",
        "",
        "## Success/Failure Direction Projection",
        f"- {a['success_failure_projection_stats']}",
        "",
        "## Cross Projections",
        f"- carry_direction on success/failure labels: {a['carry_direction_on_success_failure']}",
        f"- success/failure direction on carry labels: {a['success_failure_direction_on_carry']}",
        "",
        "## Interpretation Boundary",
        "- This probe asks whether carry and success/failure can be captured as meaningful directions in hidden space.",
        "- It does not yet intervene causally on the subspaces themselves.",
        "",
    ]
    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 6 SUBSPACE PROBE V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    digit_y, carry_y, digit_pred, carry_pred, hidden_np = train_model(device=device)

    analysis = run_subspace_probe(digit_y, carry_y, digit_pred, carry_pred, hidden_np)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_6_subspace_probe_v1",
        "analysis": analysis,
        "notes": [
            "This is the first subspace-level interpretability probe in Project 6.",
            "It tests whether arithmetic-relevant distinctions are visible as directions in hidden space.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
