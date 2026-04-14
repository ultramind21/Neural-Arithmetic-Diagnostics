"""
================================================================================
PROJECT 6 DIGIT VS CARRY DISSOCIATION V1
================================================================================

PURPOSE:
  Test whether digit-relevant and carry-relevant internal units are separable.

CORE QUESTION:
  Are the units most diagnostic for digit behavior distinct from the units
  most diagnostic for carry behavior, or do the same internal units support both?

GOAL:
  Move from "carry-selective units exist" and "success-related units exist"
  to a sharper dissociation question:
  - is there internal functional specialization?

IMPORTANT:
  This is still a bounded interpretability probe, not a final circuit claim.

================================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import torch
import torch.nn as nn


# ============================================================================
# PATHS
# ============================================================================
PROJECT_6_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_6_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_6_digit_vs_carry_dissociation_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_6_digit_vs_carry_dissociation_v1_report.md"


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
# ANALYSIS
# ============================================================================

def top_units_by_digit_success(digit_y, digit_pred, hidden_np, top_k=5):
    correct = (digit_pred == digit_y)
    success_hidden = hidden_np[correct]
    failure_hidden = hidden_np[~correct]

    success_mean = np.mean(success_hidden, axis=0)
    failure_mean = np.mean(failure_hidden, axis=0)
    diff = np.abs(success_mean - failure_mean)

    top_units = np.argsort(diff)[-top_k:][::-1]
    top_scores = diff[top_units]
    return [int(i) for i in top_units], [float(s) for s in top_scores]


def top_units_by_carry_class(carry_y, hidden_np, top_k=5):
    carry0_hidden = hidden_np[carry_y == 0]
    carry1_hidden = hidden_np[carry_y == 1]

    mean0 = np.mean(carry0_hidden, axis=0)
    mean1 = np.mean(carry1_hidden, axis=0)
    std0 = np.std(carry0_hidden, axis=0)
    std1 = np.std(carry1_hidden, axis=0)

    separability = np.abs(mean1 - mean0) / (np.maximum(std0, std1) + 1e-6)

    top_units = np.argsort(separability)[-top_k:][::-1]
    top_scores = separability[top_units]
    return [int(i) for i in top_units], [float(s) for s in top_scores]


def overlap_stats(units_a: List[int], units_b: List[int]) -> Dict[str, Any]:
    set_a = set(units_a)
    set_b = set(units_b)
    overlap = sorted(list(set_a & set_b))

    return {
        "units_a": units_a,
        "units_b": units_b,
        "overlap_units": overlap,
        "overlap_count": len(overlap),
        "overlap_ratio": len(overlap) / max(1, min(len(units_a), len(units_b))),
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 6 DIGIT VS CARRY DISSOCIATION V1",
        "",
        "## Top Units for Digit Success",
        f"- units: {artifact['digit_units']['units']}",
        f"- scores: {artifact['digit_units']['scores']}",
        "",
        "## Top Units for Carry Selectivity",
        f"- units: {artifact['carry_units']['units']}",
        f"- scores: {artifact['carry_units']['scores']}",
        "",
        "## Overlap",
        f"- overlap_units: {artifact['overlap']['overlap_units']}",
        f"- overlap_count: {artifact['overlap']['overlap_count']}",
        f"- overlap_ratio: {artifact['overlap']['overlap_ratio']}",
        "",
        "## Interpretation Boundary",
        "- This probe asks whether digit-relevant and carry-relevant internal units are shared or dissociable.",
        "- It does not yet provide a full circuit decomposition.",
        "",
    ]
    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 6 DIGIT VS CARRY DISSOCIATION V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    digit_y, carry_y, digit_pred, carry_pred, hidden_np = train_model(device=device)
    print("✓ Carry-conditioned local model trained")

    digit_units, digit_scores = top_units_by_digit_success(digit_y, digit_pred, hidden_np, top_k=5)
    carry_units, carry_scores = top_units_by_carry_class(carry_y, hidden_np, top_k=5)
    overlap = overlap_stats(digit_units, carry_units)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_6_digit_vs_carry_dissociation_v1",
        "digit_units": {
            "units": digit_units,
            "scores": digit_scores,
        },
        "carry_units": {
            "units": carry_units,
            "scores": carry_scores,
        },
        "overlap": overlap,
        "notes": [
            "This probe compares top units for digit-related and carry-related internal distinctions.",
            "Its goal is to test whether the model uses dissociable or overlapping internal substructures.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
