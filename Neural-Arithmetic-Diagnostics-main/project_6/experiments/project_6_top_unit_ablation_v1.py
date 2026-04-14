"""
================================================================================
PROJECT 6 TOP UNIT ABLATION V1
================================================================================

PURPOSE:
  Test whether the most diagnostic hidden units identified in the success-vs-failure
  probe have causal importance for local arithmetic performance.

CORE QUESTION:
  If we ablate the top success-vs-failure diagnostic units, does local arithmetic
  performance degrade significantly?

INTERPRETATION:
  - If performance drops clearly, the units are not just correlated with behavior;
    they are functionally important under this intervention.
  - If performance barely changes, the earlier probes may reflect distributed or
    redundant structure.

IMPORTANT:
  This is a first causal-style intervention, not a full causal proof.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import torch
import torch.nn as nn


# ============================================================================
# PATHS
# ============================================================================
PROJECT_6_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_6_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_6_top_unit_ablation_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_6_top_unit_ablation_v1_report.md"


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

    digits = list(range(10))

    for a in digits:
        for b in digits:
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

    return model, X_digits_t, X_carry_t, digit_y, carry_y, digit_pred, carry_pred, hidden_np


# ============================================================================
# ANALYSIS
# ============================================================================

def find_top_success_failure_units(digit_y, carry_y, digit_pred, carry_pred, hidden_np, top_k=5):
    digit_correct = (digit_pred == digit_y)
    carry_correct = (carry_pred == carry_y)
    exact_correct = digit_correct & carry_correct

    success_hidden = hidden_np[exact_correct]
    failure_hidden = hidden_np[~exact_correct]

    success_mean = np.mean(success_hidden, axis=0)
    failure_mean = np.mean(failure_hidden, axis=0)

    diff = np.abs(success_mean - failure_mean)
    top_units = np.argsort(diff)[-top_k:][::-1]
    top_scores = diff[top_units]

    return [int(i) for i in top_units], [float(s) for s in top_scores]


def evaluate_model(model, X_digits_t, X_carry_t, digit_y, carry_y, ablate_units: List[int] | None = None):
    with torch.no_grad():
        digit_logits, carry_logits, hidden = model(X_digits_t, X_carry_t)

        if ablate_units:
            hidden = hidden.clone()
            hidden[:, ablate_units] = 0.0

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
        "# PROJECT 6 TOP UNIT ABLATION V1",
        "",
        "## Top Units",
        f"- top_units: {artifact['top_units']}",
        f"- top_scores: {artifact['top_scores']}",
        "",
        "## Performance Comparison",
        f"- baseline: {artifact['baseline_metrics']}",
        f"- ablated: {artifact['ablated_metrics']}",
        "",
        "## Interpretation Boundary",
        "- This is a first causal-style perturbation on top diagnostic units.",
        "- It does not yet prove a full circuit, but it tests whether the identified units matter functionally.",
        "",
    ]
    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 6 TOP UNIT ABLATION V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model, X_digits_t, X_carry_t, digit_y, carry_y, digit_pred, carry_pred, hidden_np = train_model(device=device)
    print("✓ Carry-conditioned local model trained")

    top_units, top_scores = find_top_success_failure_units(
        digit_y, carry_y, digit_pred, carry_pred, hidden_np, top_k=5
    )
    print(f"✓ Top units identified: {top_units}")

    baseline_metrics = evaluate_model(model, X_digits_t, X_carry_t, digit_y, carry_y, ablate_units=None)
    ablated_metrics = evaluate_model(model, X_digits_t, X_carry_t, digit_y, carry_y, ablate_units=top_units)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_6_top_unit_ablation_v1",
        "top_units": top_units,
        "top_scores": top_scores,
        "baseline_metrics": baseline_metrics,
        "ablated_metrics": ablated_metrics,
        "notes": [
            "This is the first top-unit ablation test in Project 6.",
            "It evaluates whether the units identified by the success-vs-failure probe are functionally important.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
