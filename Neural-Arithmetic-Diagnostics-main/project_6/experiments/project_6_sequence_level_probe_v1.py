"""
================================================================================
PROJECT 6 SEQUENCE-LEVEL PROBE V1
================================================================================

PURPOSE:
  Test whether internal state trajectories differ across family types at the
  sequence level.

CORE QUESTION:
  How do internal state trajectories and error accumulation patterns differ
  between:
    - full_propagation_chain
    - alternating_carry
    - block_boundary_stress

GOAL:
  Move beyond local probes and test whether there is a sequence-level internal
  signature that distinguishes rescued and failing family behavior.

IMPORTANT:
  This is an extended Project 6 branch.
  It does not replace the closed core results, but builds on them.

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

JSON_OUTPUT = OUTPUT_DIR / "project_6_sequence_level_probe_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_6_sequence_level_probe_v1_report.md"


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
# TRAJECTORY EXTRACTION
# ============================================================================

def run_family_trajectory(model, a: np.ndarray, b: np.ndarray, device: torch.device) -> Dict[str, Any]:
    """
    Extract sequence-level hidden-state trajectories for one family.
    """
    batch, length = a.shape
    carry = np.zeros(batch, dtype=np.int64)

    hidden_traces = []
    digit_preds = []
    carry_preds = []

    with torch.no_grad():
        for pos in range(length - 1, -1, -1):
            x_digits = torch.tensor(
                np.stack([a[:, pos], b[:, pos]], axis=1).astype(np.float32),
                dtype=torch.float32,
                device=device,
            )
            x_carry = torch.tensor(
                carry.reshape(-1, 1).astype(np.float32),
                dtype=torch.float32,
                device=device,
            )

            digit_logits, carry_logits, hidden = model(x_digits, x_carry)

            hidden_np = hidden.detach().cpu().numpy()
            digit_pred = digit_logits.argmax(dim=1).detach().cpu().numpy()
            carry_pred = carry_logits.argmax(dim=1).detach().cpu().numpy()

            hidden_traces.append(hidden_np)
            digit_preds.append(digit_pred)
            carry_preds.append(carry_pred)

            carry = carry_pred

    # shape: list[length] of [batch, hidden_dim]
    # summarize mean hidden activity per position
    mean_hidden_by_pos = [np.mean(h, axis=0) for h in hidden_traces]

    # summarize trajectory roughness = mean abs diff between successive mean hidden states
    trajectory_diffs = []
    for i in range(len(mean_hidden_by_pos) - 1):
        diff = np.mean(np.abs(mean_hidden_by_pos[i+1] - mean_hidden_by_pos[i]))
        trajectory_diffs.append(float(diff))

    return {
        "mean_hidden_by_pos_first5dims": [
            [float(x) for x in vec[:5]] for vec in mean_hidden_by_pos
        ],
        "trajectory_diff_sequence": trajectory_diffs,
        "trajectory_diff_mean": float(np.mean(trajectory_diffs)) if trajectory_diffs else 0.0,
        "digit_preds_first_case": [int(arr[0]) for arr in digit_preds],
        "carry_preds_first_case": [int(arr[0]) for arr in carry_preds],
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 6 SEQUENCE-LEVEL PROBE V1",
        "",
        "## Family Trajectory Summaries",
    ]

    for family, result in artifact["family_results"].items():
        lines.append(f"\n### {family}")
        lines.append(f"- trajectory_diff_mean: {result['trajectory_diff_mean']}")
        lines.append(f"- trajectory_diff_sequence: {result['trajectory_diff_sequence']}")
        lines.append(f"- digit_preds_first_case: {result['digit_preds_first_case']}")
        lines.append(f"- carry_preds_first_case: {result['carry_preds_first_case']}")
        lines.append(f"- mean_hidden_by_pos_first5dims: {result['mean_hidden_by_pos_first5dims']}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This probe compares sequence-level hidden-state trajectories across families.",
        "- It is intended to reveal whether rescued and failing families differ in trajectory stability or transition dynamics.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 6 SEQUENCE-LEVEL PROBE V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = train_model(device=device)
    model.eval()

    families = {
        "alternating_carry": make_alternating_carry(num_samples=64, length=6),
        "full_propagation_chain": make_full_propagation_chain(num_samples=64, length=6),
        "block_boundary_stress": make_block_boundary_stress(num_samples=64, length=6),
    }

    family_results = {}
    for family_name, (a, b) in families.items():
        family_results[family_name] = run_family_trajectory(model, a, b, device=device)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_6_sequence_level_probe_v1",
        "family_results": family_results,
        "notes": [
            "This is the first sequence-level interpretability probe in Project 6.",
            "It compares hidden-state trajectories across rescued and failing families.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
