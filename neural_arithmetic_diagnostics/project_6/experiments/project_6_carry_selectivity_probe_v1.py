"""
================================================================================
PROJECT 6 CARRY SELECTIVITY PROBE V1
================================================================================

PURPOSE:
  Investigate whether carry-related information is distinguishable in internal
  representations of local processor models from Project 5.

CORE HYPOTHESIS:
  If carry is central to learned local computation, then hidden activations
  should show measurable differences between carry_out = 0 and carry_out = 1 cases.

EXPERIMENT DESIGN:
  Extract hidden activations from local models when processing digit pairs
  with different carry outputs, and measure separability.

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
PROJECT_6_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_6_ROOT / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_6_carry_selectivity_probe_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_6_carry_selectivity_probe_v1_report.md"


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
# SIMPLE LOCAL MODEL (baseline for comparison)
# ============================================================================

class SimpleLocalNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden1 = nn.Linear(3, 32)
        self.hidden2 = nn.Linear(32, 32)
        self.digit_head = nn.Linear(32, 10)
        self.carry_head = nn.Linear(32, 2)

    def forward(self, x):
        h1 = torch.relu(self.hidden1(x))
        h2 = torch.relu(self.hidden2(h1))
        return self.digit_head(h2), self.carry_head(h2), h2


# ============================================================================
# CARRY-CONDITIONED LOCAL MODEL
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
# DATASET
# ============================================================================

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

                total = a + b + carry_in
                d = total % 10
                c = total // 10

                digit_y.append(d)
                carry_y.append(c)

    return (
        np.array(X_digits, dtype=np.float32),
        np.array(X_carry, dtype=np.float32),
        np.array(digit_y, dtype=np.int64),
        np.array(carry_y, dtype=np.int64),
    )


# ============================================================================
# TRAIN MODELS
# ============================================================================

def train_simple_model(device: torch.device):
    X_digits, X_carry, digit_y, carry_y = build_dataset()

    X_combined = np.concatenate([X_digits, X_carry], axis=1).astype(np.float32)
    X_t = torch.tensor(X_combined, dtype=torch.float32, device=device)
    digit_t = torch.tensor(digit_y, dtype=torch.long, device=device)
    carry_t = torch.tensor(carry_y, dtype=torch.long, device=device)

    model = SimpleLocalNet().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion_digit = nn.CrossEntropyLoss()
    criterion_carry = nn.CrossEntropyLoss()

    for _ in range(100):
        optimizer.zero_grad()
        digit_logits, carry_logits, _ = model(X_t)
        loss = criterion_digit(digit_logits, digit_t) + criterion_carry(carry_logits, carry_t)
        loss.backward()
        optimizer.step()

    return model, X_t, digit_y, carry_y


def train_carry_conditioned_model(device: torch.device):
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

    return model, (X_digits_t, X_carry_t), digit_y, carry_y


# ============================================================================
# ANALYSIS
# ============================================================================

def extract_and_analyze(model_name: str, model, X_data, digit_y, carry_y, device: torch.device):
    """
    Extract hidden activations and analyze carry selectivity.
    """

    # Forward pass to get hidden activations
    with torch.no_grad():
        if model_name == "simple":
            _, _, hiddens = model(X_data)
        else:  # carry-conditioned
            X_digits_t, X_carry_t = X_data
            _, _, hiddens = model(X_digits_t, X_carry_t)

    hiddens_np = hiddens.detach().cpu().numpy()

    # Separate by carry_out
    carry_0_hiddens = hiddens_np[carry_y == 0]
    carry_1_hiddens = hiddens_np[carry_y == 1]

    # Basic statistics
    mean_0 = np.mean(carry_0_hiddens, axis=0)
    mean_1 = np.mean(carry_1_hiddens, axis=0)
    std_0 = np.std(carry_0_hiddens, axis=0)
    std_1 = np.std(carry_1_hiddens, axis=0)

    # Compute simple separability: mean absolute difference scaled by std
    diffs = np.abs(mean_1 - mean_0)
    stds = np.maximum(std_0, std_1) + 1e-6

    separability = diffs / stds

    # Identify top carry-selective units
    top_unit_indices = np.argsort(separability)[-5:][::-1]
    top_separability_scores = separability[top_unit_indices]

    # Average separability
    avg_separability = np.mean(separability)

    return {
        "model_name": model_name,
        "num_units": hiddens_np.shape[1],
        "num_cases_carry0": len(carry_0_hiddens),
        "num_cases_carry1": len(carry_1_hiddens),
        "avg_separability": float(avg_separability),
        "top_unit_indices": [int(i) for i in top_unit_indices],
        "top_unit_separability": [float(s) for s in top_separability_scores],
        "overall_mean_0": [float(m) for m in mean_0[:5]],  # First 5 for brevity
        "overall_mean_1": [float(m) for m in mean_1[:5]],
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 6 CARRY SELECTIVITY PROBE V1 REPORT",
        "",
        "## Experiment Summary",
        "Extracted carry selectivity from two local processor architectures.",
        "",
        "## Results",
        "",
    ]

    for result in artifact["results"]:
        lines.extend([
            f"### {result['model_name'].upper()}",
            f"- Units: {result['num_units']}",
            f"- Cases (carry=0, carry=1): ({result['num_cases_carry0']}, {result['num_cases_carry1']})",
            f"- Average carry separability score: {result['avg_separability']:.6f}",
            f"- Top 5 carry-selective unit indices: {result['top_unit_indices']}",
            f"- Top 5 separability scores: {[f'{s:.4f}' for s in result['top_unit_separability']]}",
            "",
        ])

    lines.extend([
        "## Interpretation",
        "- Higher separability score indicates stronger carry-selective encoding.",
        "- Top unit indices show which hidden units best distinguish carry_out.",
        "- This is the first probe; full interpretability requires deeper analysis.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 6 CARRY SELECTIVITY PROBE V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Train models
    print("Training simple local model...")
    simple_model, simple_X, simple_digit_y, simple_carry_y = train_simple_model(device=device)
    print("✓ Simple model trained")

    print("Training carry-conditioned local model...")
    cc_model, cc_X, cc_digit_y, cc_carry_y = train_carry_conditioned_model(device=device)
    print("✓ Carry-conditioned model trained")

    # Analyze
    print("Analyzing carry selectivity...")

    simple_analysis = extract_and_analyze(
        "simple",
        simple_model,
        simple_X,
        simple_carry_y,
        simple_carry_y,
        device=device,
    )

    cc_analysis = extract_and_analyze(
        "carry_conditioned",
        cc_model,
        cc_X,
        cc_digit_y,
        cc_carry_y,
        device=device,
    )

    print("✓ Analysis complete")

    # Compile artifact
    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_6_carry_selectivity_probe_v1",
        "device": str(device),
        "results": [simple_analysis, cc_analysis],
        "notes": [
            "First interpretability experiment in Project 6.",
            "Compares two local processor architectures.",
            "Measures carry selectivity in hidden activations.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
