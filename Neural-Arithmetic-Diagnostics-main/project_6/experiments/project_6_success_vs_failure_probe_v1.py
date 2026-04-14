"""
================================================================================
PROJECT 6 SUCCESS VS FAILURE PROBE V1
================================================================================

PURPOSE:
  Link internal representation differences to behavioral success and failure.

CORE QUESTION:
  Do successful and failing local arithmetic cases show distinguishable internal
  activation structure?

FOCUS:
  - compare successful vs failing local cases
  - inspect carry-conditioned model only
  - ask whether error cases have a consistent hidden signature

IMPORTANT:
  This is the second interpretability probe in Project 6.
  It is still exploratory, but tighter than the first probe because it links
  internal structure directly to behavioral correctness.

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

JSON_OUTPUT = OUTPUT_DIR / "project_6_success_vs_failure_probe_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_6_success_vs_failure_probe_v1_report.md"


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

    model.eval()
    with torch.no_grad():
        digit_logits, carry_logits, hidden = model(X_digits_t, X_carry_t)
        digit_pred = digit_logits.argmax(dim=1).detach().cpu().numpy()
        carry_pred = carry_logits.argmax(dim=1).detach().cpu().numpy()
        hidden_np = hidden.detach().cpu().numpy()

    return X_digits, X_carry, digit_y, carry_y, digit_pred, carry_pred, hidden_np


# ============================================================================
# ANALYSIS
# ============================================================================

def analyze_success_failure(X_digits, X_carry, digit_y, carry_y, digit_pred, carry_pred, hidden_np):
    digit_correct = (digit_pred == digit_y)
    carry_correct = (carry_pred == carry_y)
    exact_correct = digit_correct & carry_correct

    success_hidden = hidden_np[exact_correct]
    failure_hidden = hidden_np[~exact_correct]

    success_mean = np.mean(success_hidden, axis=0) if len(success_hidden) > 0 else np.zeros(hidden_np.shape[1])
    failure_mean = np.mean(failure_hidden, axis=0) if len(failure_hidden) > 0 else np.zeros(hidden_np.shape[1])

    diff = np.abs(success_mean - failure_mean)
    top_units = np.argsort(diff)[-5:][::-1]
    top_scores = diff[top_units]

    # Failure subgroup structure
    failure_cases = []
    for i in range(len(X_digits)):
        if not exact_correct[i]:
            failure_cases.append({
                "a": int(X_digits[i][0]),
                "b": int(X_digits[i][1]),
                "carry_in": int(X_carry[i][0]),
                "digit_true": int(digit_y[i]),
                "digit_pred": int(digit_pred[i]),
                "carry_true": int(carry_y[i]),
                "carry_pred": int(carry_pred[i]),
            })

    return {
        "overall": {
            "digit_acc": float(np.mean(digit_correct)),
            "carry_acc": float(np.mean(carry_correct)),
            "exact_acc": float(np.mean(exact_correct)),
            "success_count": int(np.sum(exact_correct)),
            "failure_count": int(np.sum(~exact_correct)),
        },
        "top_success_failure_units": [int(i) for i in top_units],
        "top_success_failure_scores": [float(s) for s in top_scores],
        "success_hidden_mean_first5": [float(x) for x in success_mean[:5]],
        "failure_hidden_mean_first5": [float(x) for x in failure_mean[:5]],
        "failure_cases": failure_cases[:20],  # sample for readability
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    overall = artifact["analysis"]["overall"]

    lines = [
        "# PROJECT 6 SUCCESS VS FAILURE PROBE V1",
        "",
        "## Overall",
        f"- digit_acc: {overall['digit_acc']}",
        f"- carry_acc: {overall['carry_acc']}",
        f"- exact_acc: {overall['exact_acc']}",
        f"- success_count: {overall['success_count']}",
        f"- failure_count: {overall['failure_count']}",
        "",
        "## Top Units Distinguishing Success vs Failure",
        f"- unit indices: {artifact['analysis']['top_success_failure_units']}",
        f"- scores: {artifact['analysis']['top_success_failure_scores']}",
        "",
        "## Hidden Means (First 5 dims)",
        f"- success mean: {artifact['analysis']['success_hidden_mean_first5']}",
        f"- failure mean: {artifact['analysis']['failure_hidden_mean_first5']}",
        "",
        "## Sample Failure Cases",
    ]

    for row in artifact["analysis"]["failure_cases"]:
        lines.append(f"- {row}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This probe asks whether failure is behaviorally and internally distinguishable.",
        "- It is still exploratory and does not yet establish a full mechanistic circuit claim.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 6 SUCCESS VS FAILURE PROBE V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    X_digits, X_carry, digit_y, carry_y, digit_pred, carry_pred, hidden_np = train_model(device=device)
    print("✓ Carry-conditioned local model trained and activations extracted")

    analysis = analyze_success_failure(
        X_digits, X_carry, digit_y, carry_y, digit_pred, carry_pred, hidden_np
    )

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_6_success_vs_failure_probe_v1",
        "analysis": analysis,
        "notes": [
            "This probe compares hidden activations for successful vs failing local cases.",
            "Its goal is to link internal structure to behavioral correctness.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
