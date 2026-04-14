"""
================================================================================
PROJECT 7 CONTEXT-TRIGGER INTERVENTION V1
================================================================================

PURPOSE:
  Test whether correcting only the known recurring local trigger contexts
  rescues family-level behavior.

CORE QUESTION:
  Are the observed local trigger failures causally central enough that fixing
  only those positions substantially improves the failing family?

INTERVENTION:
  If a known trigger context is detected during stepwise composition,
  replace the model prediction at that step with the exact local oracle output.
  All other positions remain model-driven.

TARGET:
  - alternating_carry
  - block_boundary_stress
  - full_propagation_chain (control)

IMPORTANT:
  This is a surgical causal probe.
  It asks whether a small number of recurring local failures drives
  the larger family-level failure.

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
PROJECT_7_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_7_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_7_context_trigger_intervention_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_7_context_trigger_intervention_v1_report.md"


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
# INTERVENTION LOGIC
# ============================================================================

class TriggerInterventionProcessor:
    def __init__(self, model: CarryConditionedLocalNet, device: torch.device):
        self.model = model
        self.device = device

    def predict_local(self, a_digit: int, b_digit: int, carry_in: int):
        x_digits = torch.tensor([[a_digit, b_digit]], dtype=torch.float32, device=self.device)
        x_carry = torch.tensor([[carry_in]], dtype=torch.float32, device=self.device)

        with torch.no_grad():
            digit_logits, carry_logits, _ = self.model(x_digits, x_carry)
            digit_pred = int(digit_logits.argmax(dim=1).item())
            carry_pred = int(carry_logits.argmax(dim=1).item())

        return digit_pred, carry_pred

    def maybe_intervene(self, a_digit: int, b_digit: int, carry_in: int, digit_pred: int, carry_pred: int):
        """
        Apply surgical correction only on the known trigger context:
          (a=0, b=0, carry_in=0) -> wrong digit=1 instead of 0
        """
        applied = False

        if a_digit == 0 and b_digit == 0 and carry_in == 0 and digit_pred == 1:
            digit_true, carry_true = local_targets(a_digit, b_digit, carry_in)
            digit_pred = digit_true
            carry_pred = carry_true
            applied = True

        return digit_pred, carry_pred, applied


# ============================================================================
# STEPWISE EVAL
# ============================================================================

def run_family_with_intervention(processor: TriggerInterventionProcessor, a: np.ndarray, b: np.ndarray):
    truth = full_exact_addition(a, b)[0].tolist()
    batch, length = a.shape
    assert batch == 1

    carry = 0
    pred_digits = []
    intervention_count = 0
    trace = []

    for pos in range(length - 1, -1, -1):
        a_digit = int(a[0, pos])
        b_digit = int(b[0, pos])

        digit_pred, carry_pred = processor.predict_local(a_digit, b_digit, carry)
        digit_true, carry_true = local_targets(a_digit, b_digit, carry)

        digit_pred_new, carry_pred_new, applied = processor.maybe_intervene(
            a_digit, b_digit, carry, digit_pred, carry_pred
        )

        if applied:
            intervention_count += 1

        row = {
            "position": pos,
            "a_digit": a_digit,
            "b_digit": b_digit,
            "carry_in": carry,
            "digit_true": digit_true,
            "carry_true": carry_true,
            "digit_pred_before": digit_pred,
            "carry_pred_before": carry_pred,
            "digit_pred_after": digit_pred_new,
            "carry_pred_after": carry_pred_new,
            "intervention_applied": applied,
        }
        trace.append(row)

        pred_digits.append(digit_pred_new)
        carry = carry_pred_new

    pred_full = [carry] + list(reversed(pred_digits))
    exact_match = (pred_full == truth)

    return {
        "truth_full_sequence": truth,
        "predicted_full_sequence": pred_full,
        "exact_match": exact_match,
        "intervention_count": intervention_count,
        "trace": trace,
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 7 CONTEXT-TRIGGER INTERVENTION V1",
        "",
        "## Family Results",
    ]

    for family, result in artifact["family_results"].items():
        lines.append(f"\n### {family}")
        lines.append(f"- truth_full_sequence: {result['truth_full_sequence']}")
        lines.append(f"- predicted_full_sequence: {result['predicted_full_sequence']}")
        lines.append(f"- exact_match: {result['exact_match']}")
        lines.append(f"- intervention_count: {result['intervention_count']}")
        lines.append("- trace:")
        for step in result["trace"]:
            lines.append(f"  - {step}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This is a surgical trigger intervention on a specific recurring local failure context.",
        "- It tests whether correcting that trigger is enough to rescue family-level behavior.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 7 CONTEXT-TRIGGER INTERVENTION V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = train_model(device=device)
    processor = TriggerInterventionProcessor(model=model, device=device)

    families = {
        "alternating_carry": make_alternating_carry(length=6),
        "full_propagation_chain": make_full_propagation_chain(length=6),
        "block_boundary_stress": make_block_boundary_stress(length=6),
    }

    family_results = {}
    for family_name, (a, b) in families.items():
        family_results[family_name] = run_family_with_intervention(processor, a, b)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_7_context_trigger_intervention_v1",
        "family_results": family_results,
        "notes": [
            "This is the first surgical local trigger intervention in Project 7.",
            "It tests whether correcting a known recurring local failure context rescues family-level behavior.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
