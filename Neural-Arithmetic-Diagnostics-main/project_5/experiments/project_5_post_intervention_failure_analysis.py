"""
================================================================================
PROJECT 5 POST-INTERVENTION FAILURE ANALYSIS
================================================================================

PURPOSE:
  Analyze why explicit carry-conditioned representation rescues
  full_propagation_chain but still fails on alternating_carry and
  block_boundary_stress.

CORE QUESTION:
  What structural difference remains between the rescued family and the
  still-failing families?

THIS SCRIPT CHECKS:
  1. position-wise digit accuracy by family
  2. position-wise carry accuracy by family
  3. position-wise exact-match consistency
  4. family carry-pattern structure
  5. whether errors cluster around alternation or boundary transitions

IMPORTANT:
  This is a post-intervention analysis, not a new intervention itself.

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
PROJECT_5_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_5_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_5_post_intervention_failure_analysis_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_5_post_intervention_failure_analysis_report.md"


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
# EXACT TARGETS
# ============================================================================

def compute_digit_carry_targets(a: np.ndarray, b: np.ndarray):
    batch, length = a.shape
    digit_true = np.zeros((batch, length), dtype=np.int64)
    carry_true = np.zeros((batch, length), dtype=np.int64)

    carry = np.zeros(batch, dtype=np.int64)

    for pos in range(length - 1, -1, -1):
        total = a[:, pos] + b[:, pos] + carry
        digit_true[:, pos] = total % 10
        carry = total // 10
        carry_true[:, pos] = carry

    return digit_true, carry_true


# ============================================================================
# MODEL
# ============================================================================

class ExplicitCarryLocalNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.digit_pair_net = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
        )

        self.carry_net = nn.Sequential(
            nn.Linear(1, 8),
            nn.ReLU(),
            nn.Linear(8, 8),
            nn.ReLU(),
        )

        self.combined_net = nn.Sequential(
            nn.Linear(24, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
        )

        self.digit_head = nn.Linear(32, 10)
        self.carry_head = nn.Linear(32, 2)

    def forward(self, x_digits, x_carry):
        h_digits = self.digit_pair_net(x_digits)
        h_carry = self.carry_net(x_carry)
        h = torch.cat([h_digits, h_carry], dim=1)
        h = self.combined_net(h)
        return self.digit_head(h), self.carry_head(h)


def build_local_dataset():
    X_digits = []
    X_carry = []
    digit_y = []
    carry_y = []

    for a in range(10):
        for b in range(10):
            for c in range(2):
                total = a + b + c
                X_digits.append([a, b])
                X_carry.append([c])
                digit_y.append(total % 10)
                carry_y.append(1 if total >= 10 else 0)

    return (
        np.array(X_digits, dtype=np.float32),
        np.array(X_carry, dtype=np.float32),
        np.array(digit_y, dtype=np.int64),
        np.array(carry_y, dtype=np.int64),
    )


def train_model(device: torch.device):
    X_digits, X_carry, digit_y, carry_y = build_local_dataset()

    X_digits_t = torch.tensor(X_digits, dtype=torch.float32, device=device)
    X_carry_t = torch.tensor(X_carry, dtype=torch.float32, device=device)
    digit_t = torch.tensor(digit_y, dtype=torch.long, device=device)
    carry_t = torch.tensor(carry_y, dtype=torch.long, device=device)

    model = ExplicitCarryLocalNet().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion_digit = nn.CrossEntropyLoss()
    criterion_carry = nn.CrossEntropyLoss()

    for _ in range(300):
        optimizer.zero_grad()
        digit_logits, carry_logits = model(X_digits_t, X_carry_t)
        loss = criterion_digit(digit_logits, digit_t) + criterion_carry(carry_logits, carry_t)
        loss.backward()
        optimizer.step()

    return model


# ============================================================================
# PROCESSOR
# ============================================================================

class LearnedLocalProcessor:
    def __init__(self, model: ExplicitCarryLocalNet, device: torch.device):
        self.model = model
        self.device = device

    def predict_local(self, a_digit: np.ndarray, b_digit: np.ndarray, carry_in: np.ndarray):
        x_digits = np.stack([a_digit, b_digit], axis=1).astype(np.float32)
        x_carry = np.array(carry_in, dtype=np.float32).reshape(-1, 1)

        x_digits_t = torch.tensor(x_digits, dtype=torch.float32, device=self.device)
        x_carry_t = torch.tensor(x_carry, dtype=torch.float32, device=self.device)

        with torch.no_grad():
            digit_logits, carry_logits = self.model(x_digits_t, x_carry_t)
            digit = digit_logits.argmax(dim=1).detach().cpu().numpy()
            carry = carry_logits.argmax(dim=1).detach().cpu().numpy()

        return digit.astype(np.int64), carry.astype(np.int64)


# ============================================================================
# COMPOSED EVALUATION
# ============================================================================

def evaluate_family_detailed(processor: LearnedLocalProcessor, a: np.ndarray, b: np.ndarray, chunk_size: int):
    batch, length = a.shape
    digit_true, carry_true = compute_digit_carry_targets(a, b)

    digit_pred = np.zeros((batch, length), dtype=np.int64)
    carry_pred = np.zeros((batch, length), dtype=np.int64)

    carry_between_chunks = np.zeros(batch, dtype=np.int64)

    for chunk_end in range(length, 0, -chunk_size):
        chunk_start = max(0, chunk_end - chunk_size)

        carry = carry_between_chunks.copy()
        for pos in range(chunk_end - 1, chunk_start - 1, -1):
            d, c = processor.predict_local(a[:, pos], b[:, pos], carry)
            digit_pred[:, pos] = d
            carry_pred[:, pos] = c
            carry = c

        carry_between_chunks = carry

    digit_correct = (digit_pred == digit_true)
    carry_correct = (carry_pred == carry_true)
    exact_correct = digit_correct & carry_correct

    position_digit_acc = [float(np.mean(digit_correct[:, pos])) for pos in range(length)]
    position_carry_acc = [float(np.mean(carry_correct[:, pos])) for pos in range(length)]
    position_exact_acc = [float(np.mean(exact_correct[:, pos])) for pos in range(length)]

    return {
        "digit_acc": float(np.mean(digit_correct)),
        "carry_acc": float(np.mean(carry_correct)),
        "exact_acc": float(np.mean(exact_correct)),
        "position_digit_acc": position_digit_acc,
        "position_carry_acc": position_carry_acc,
        "position_exact_acc": position_exact_acc,
        "digit_true_first": digit_true[0].tolist(),
        "carry_true_first": carry_true[0].tolist(),
        "digit_pred_first": digit_pred[0].tolist(),
        "carry_pred_first": carry_pred[0].tolist(),
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 5 POST-INTERVENTION FAILURE ANALYSIS",
        "",
        "## Family-by-Family Summary",
    ]

    for family, result in artifact["results"].items():
        lines.append(f"\n### {family}")
        lines.append(f"- digit_acc: {result['digit_acc']}")
        lines.append(f"- carry_acc: {result['carry_acc']}")
        lines.append(f"- exact_acc: {result['exact_acc']}")
        lines.append(f"- position_digit_acc: {result['position_digit_acc']}")
        lines.append(f"- position_carry_acc: {result['position_carry_acc']}")
        lines.append(f"- position_exact_acc: {result['position_exact_acc']}")
        lines.append(f"- first true digit: {result['digit_true_first']}")
        lines.append(f"- first pred digit: {result['digit_pred_first']}")
        lines.append(f"- first true carry: {result['carry_true_first']}")
        lines.append(f"- first pred carry: {result['carry_pred_first']}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This analysis compares the rescued family and still-failing families after explicit carry-conditioned representation.",
        "- It aims to identify where structured failure remains concentrated.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 5 POST-INTERVENTION FAILURE ANALYSIS")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    chunk_size = 2
    length = 6
    num_samples = 64

    model = train_model(device=device)
    processor = LearnedLocalProcessor(model=model, device=device)

    families = {
        "alternating_carry": make_alternating_carry(num_samples=num_samples, length=length),
        "full_propagation_chain": make_full_propagation_chain(num_samples=num_samples, length=length),
        "block_boundary_stress": make_block_boundary_stress(num_samples=num_samples, length=length),
    }

    results = {}
    for family_name, (a, b) in families.items():
        results[family_name] = evaluate_family_detailed(processor, a, b, chunk_size=chunk_size)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_5_post_intervention_failure_analysis",
        "results": results,
        "notes": [
            "This analysis follows the explicit carry representation result.",
            "Its goal is to compare the rescued and still-failing families position by position.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
