"""
================================================================================
PROJECT 7 STEPWISE COMPOSITION TRACE V1
================================================================================

PURPOSE:
  Trace step-by-step composition behavior to locate where local competence
  fails to scale into global success.

CORE QUESTION:
  At what point in the sequence does local arithmetic competence stop producing
  globally correct behavior?

GOAL:
  Produce a detailed stepwise trace for three key family types:
    - full_propagation_chain
    - alternating_carry
    - block_boundary_stress

IMPORTANT:
  This is the first bridge experiment in Project 7.
  It is designed to observe local-to-global breakdown directly.

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
PROJECT_7_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_7_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_7_stepwise_composition_trace_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_7_stepwise_composition_trace_v1_report.md"


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
# TRAIN LOCAL PROCESSOR
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
# TRACE
# ============================================================================

def run_stepwise_trace(model, a: np.ndarray, b: np.ndarray, device: torch.device) -> Dict[str, Any]:
    truth = full_exact_addition(a, b)[0].tolist()

    batch, length = a.shape
    assert batch == 1, "This v1 trace expects one example only"

    carry = 0
    pred_digits = []
    pred_carries = []
    trace = []

    prev_hidden = None

    for pos in range(length - 1, -1, -1):
        a_digit = int(a[0, pos])
        b_digit = int(b[0, pos])

        x_digits = torch.tensor([[a_digit, b_digit]], dtype=torch.float32, device=device)
        x_carry = torch.tensor([[carry]], dtype=torch.float32, device=device)

        with torch.no_grad():
            digit_logits, carry_logits, hidden = model(x_digits, x_carry)
            digit_pred = int(digit_logits.argmax(dim=1).item())
            carry_pred = int(carry_logits.argmax(dim=1).item())

        digit_true, carry_true = local_targets(a_digit, b_digit, carry)

        hidden_np = hidden.detach().cpu().numpy()[0]

        diff_from_prev = None
        if prev_hidden is not None:
            diff_from_prev = float(np.mean(np.abs(hidden_np - prev_hidden)))

        row = {
            "position": pos,
            "a_digit": a_digit,
            "b_digit": b_digit,
            "carry_in": carry,
            "digit_true": int(digit_true),
            "carry_true": int(carry_true),
            "digit_pred": digit_pred,
            "carry_pred": carry_pred,
            "digit_correct": digit_pred == int(digit_true),
            "carry_correct": carry_pred == int(carry_true),
            "hidden_first5": [float(x) for x in hidden_np[:5]],
            "hidden_diff_from_prev": diff_from_prev,
        }
        trace.append(row)

        pred_digits.append(digit_pred)
        pred_carries.append(carry_pred)
        carry = carry_pred
        prev_hidden = hidden_np.copy()

    # rebuild predicted full number
    pred_full = [carry] + list(reversed(pred_digits))
    exact_match = (pred_full == truth)

    return {
        "truth_full_sequence": truth,
        "predicted_full_sequence": pred_full,
        "exact_match": exact_match,
        "trace": trace,
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 7 STEPWISE COMPOSITION TRACE V1",
        "",
        "## Families",
    ]

    for family, result in artifact["family_results"].items():
        lines.append(f"\n### {family}")
        lines.append(f"- truth_full_sequence: {result['truth_full_sequence']}")
        lines.append(f"- predicted_full_sequence: {result['predicted_full_sequence']}")
        lines.append(f"- exact_match: {result['exact_match']}")
        lines.append("- step trace:")
        for step in result["trace"]:
            lines.append(f"  - {step}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This experiment traces where local competence first fails to produce globally correct behavior.",
        "- It is a bridge experiment, not a final full theory.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 7 STEPWISE COMPOSITION TRACE V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = train_model(device=device)
    model.eval()

    families = {
        "alternating_carry": make_alternating_carry(length=6),
        "full_propagation_chain": make_full_propagation_chain(length=6),
        "block_boundary_stress": make_block_boundary_stress(length=6),
    }

    family_results = {}
    for family_name, (a, b) in families.items():
        family_results[family_name] = run_stepwise_trace(model, a, b, device=device)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_7_stepwise_composition_trace_v1",
        "family_results": family_results,
        "notes": [
            "This is the first bridge experiment in Project 7.",
            "It traces where local competence fails to scale into global success.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
