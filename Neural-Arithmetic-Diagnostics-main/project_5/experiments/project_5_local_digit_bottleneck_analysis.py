"""
================================================================================
PROJECT 5 LOCAL DIGIT BOTTLENECK ANALYSIS
================================================================================

PURPOSE:
  Analyze why the learned local processor achieves weak digit accuracy despite
  perfect carry accuracy.

CORE QUESTION:
  Where exactly does local digit prediction fail?

THIS SCRIPT CHECKS:
  1. overall local digit/carry/exact accuracy
  2. accuracy broken down by carry_in
  3. accuracy broken down by whether the case produces carry_out
  4. accuracy at the exact (a, b, carry_in) triple level
  5. most common digit-confusion cases

IMPORTANT:
  This is a diagnostic follow-up to Project 5 learned-local-processor v1.

================================================================================
"""

from __future__ import annotations

import json
from collections import defaultdict, Counter
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

JSON_OUTPUT = OUTPUT_DIR / "project_5_local_digit_bottleneck_analysis_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_5_local_digit_bottleneck_analysis_report.md"


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
# DATASET
# ============================================================================

def build_local_dataset():
    X = []
    digit_y = []
    carry_y = []

    for a in range(10):
        for b in range(10):
            for c in range(2):
                total = a + b + c
                X.append([a, b, c])
                digit_y.append(total % 10)
                carry_y.append(1 if total >= 10 else 0)

    X = np.array(X, dtype=np.float32)
    digit_y = np.array(digit_y, dtype=np.int64)
    carry_y = np.array(carry_y, dtype=np.int64)
    return X, digit_y, carry_y


# ============================================================================
# MODEL
# ============================================================================

class LocalCarryNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
        )
        self.digit_head = nn.Linear(32, 10)
        self.carry_head = nn.Linear(32, 2)

    def forward(self, x):
        h = self.net(x)
        return self.digit_head(h), self.carry_head(h)


# ============================================================================
# TRAIN
# ============================================================================

def train_local_model(device: torch.device):
    X, digit_y, carry_y = build_local_dataset()

    X_t = torch.tensor(X, dtype=torch.float32, device=device)
    digit_t = torch.tensor(digit_y, dtype=torch.long, device=device)
    carry_t = torch.tensor(carry_y, dtype=torch.long, device=device)

    model = LocalCarryNet().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion_digit = nn.CrossEntropyLoss()
    criterion_carry = nn.CrossEntropyLoss()

    for _ in range(300):
        optimizer.zero_grad()
        digit_logits, carry_logits = model(X_t)
        loss = criterion_digit(digit_logits, digit_t) + criterion_carry(carry_logits, carry_t)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        digit_logits, carry_logits = model(X_t)
        digit_pred = digit_logits.argmax(dim=1).detach().cpu().numpy()
        carry_pred = carry_logits.argmax(dim=1).detach().cpu().numpy()

    return model, X, digit_y, carry_y, digit_pred, carry_pred


# ============================================================================
# ANALYSIS
# ============================================================================

def analyze_cases(X, digit_y, carry_y, digit_pred, carry_pred):
    total_cases = len(X)

    digit_correct = (digit_pred == digit_y)
    carry_correct = (carry_pred == carry_y)
    exact_correct = digit_correct & carry_correct

    overall = {
        "digit_acc": float(np.mean(digit_correct)),
        "carry_acc": float(np.mean(carry_correct)),
        "exact_acc": float(np.mean(exact_correct)),
    }

    by_carry_in = {}
    for c in [0, 1]:
        idx = X[:, 2] == c
        by_carry_in[str(c)] = {
            "count": int(np.sum(idx)),
            "digit_acc": float(np.mean(digit_correct[idx])),
            "carry_acc": float(np.mean(carry_correct[idx])),
            "exact_acc": float(np.mean(exact_correct[idx])),
        }

    by_carry_out = {}
    for c_out in [0, 1]:
        idx = carry_y == c_out
        by_carry_out[str(c_out)] = {
            "count": int(np.sum(idx)),
            "digit_acc": float(np.mean(digit_correct[idx])),
            "carry_acc": float(np.mean(carry_correct[idx])),
            "exact_acc": float(np.mean(exact_correct[idx])),
        }

    triple_level = []
    confusion_counter = Counter()

    for i in range(total_cases):
        a, b, c_in = map(int, X[i].tolist())
        row = {
            "a": a,
            "b": b,
            "carry_in": c_in,
            "digit_true": int(digit_y[i]),
            "digit_pred": int(digit_pred[i]),
            "carry_true": int(carry_y[i]),
            "carry_pred": int(carry_pred[i]),
            "digit_ok": bool(digit_correct[i]),
            "carry_ok": bool(carry_correct[i]),
            "exact_ok": bool(exact_correct[i]),
        }
        triple_level.append(row)

        if not digit_correct[i]:
            confusion_counter[(int(digit_y[i]), int(digit_pred[i]))] += 1

    worst_cases = [
        row for row in triple_level if not row["digit_ok"]
    ]

    most_common_confusions = [
        {"true_digit": t, "pred_digit": p, "count": c}
        for (t, p), c in confusion_counter.most_common(15)
    ]

    return {
        "overall": overall,
        "by_carry_in": by_carry_in,
        "by_carry_out": by_carry_out,
        "most_common_confusions": most_common_confusions,
        "worst_cases": worst_cases,
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    overall = artifact["analysis"]["overall"]
    by_carry_in = artifact["analysis"]["by_carry_in"]
    by_carry_out = artifact["analysis"]["by_carry_out"]

    lines = [
        "# PROJECT 5 LOCAL DIGIT BOTTLENECK ANALYSIS",
        "",
        "## Overall",
        f"- digit_acc: {overall['digit_acc']}",
        f"- carry_acc: {overall['carry_acc']}",
        f"- exact_acc: {overall['exact_acc']}",
        "",
        "## By carry_in",
        f"- carry_in = 0: {by_carry_in['0']}",
        f"- carry_in = 1: {by_carry_in['1']}",
        "",
        "## By carry_out",
        f"- carry_out = 0: {by_carry_out['0']}",
        f"- carry_out = 1: {by_carry_out['1']}",
        "",
        "## Most Common Digit Confusions",
    ]

    for row in artifact["analysis"]["most_common_confusions"]:
        lines.append(f"- true {row['true_digit']} -> pred {row['pred_digit']}: {row['count']}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This analysis is about local digit/carry learnability only.",
        "- It does not yet explain the full Project 5 decomposition behavior mechanistically.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 5 LOCAL DIGIT BOTTLENECK ANALYSIS")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model, X, digit_y, carry_y, digit_pred, carry_pred = train_local_model(device=device)
    print("✓ Local processor trained")

    analysis = analyze_cases(X, digit_y, carry_y, digit_pred, carry_pred)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_5_local_digit_bottleneck_analysis",
        "analysis": analysis,
        "notes": [
            "This analysis follows the first learned local processor result.",
            "Its purpose is to identify where local digit prediction fails.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
