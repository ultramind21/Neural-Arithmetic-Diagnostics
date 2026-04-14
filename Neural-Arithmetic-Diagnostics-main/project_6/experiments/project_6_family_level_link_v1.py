"""
================================================================================
PROJECT 6 FAMILY-LEVEL LINK V1
================================================================================

PURPOSE:
  Test whether the top diagnostic units identified locally are also informative
  for explaining family-level success vs failure patterns.

CORE QUESTION:
  Do the same units that matter for local success/failure also show systematically
  different activation behavior across the Project 5 family types?

TARGET FAMILIES:
  - alternating_carry
  - full_propagation_chain
  - block_boundary_stress

IMPORTANT:
  This is an interpretability bridge between Project 5 and Project 6.
  It does NOT yet prove a full circuit explanation.
  It asks whether family-level differences are reflected in the same key units.

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

JSON_OUTPUT = OUTPUT_DIR / "project_6_family_level_link_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_6_family_level_link_v1_report.md"


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
# PATTERN GENERATORS
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
# TARGETS
# ============================================================================

def local_targets(a_digit: int, b_digit: int, carry_in: int):
    total = a_digit + b_digit + carry_in
    return total % 10, total // 10


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
# FAMILY-LEVEL ACTIVATION EXTRACTION
# ============================================================================

TOP_UNITS = [7, 19, 11, 0, 28]


def collect_family_hidden_statistics(model, a: np.ndarray, b: np.ndarray, device: torch.device) -> Dict[str, Any]:
    """
    Run the local model position-by-position over a family and collect hidden
    activations for the known diagnostic units.
    """
    batch, length = a.shape

    activations_by_unit = {u: [] for u in TOP_UNITS}
    carry_inputs = []
    local_cases = []

    carry = np.zeros(batch, dtype=np.int64)

    with torch.no_grad():
        for pos in range(length - 1, -1, -1):
            a_digit = a[:, pos]
            b_digit = b[:, pos]

            x_digits = torch.tensor(
                np.stack([a_digit, b_digit], axis=1).astype(np.float32),
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
            carry_pred = carry_logits.argmax(dim=1).detach().cpu().numpy().astype(np.int64)

            for u in TOP_UNITS:
                activations_by_unit[u].extend(hidden_np[:, u].tolist())

            carry_inputs.extend(carry.tolist())

            for i in range(batch):
                local_cases.append({
                    "position": pos,
                    "a": int(a_digit[i]),
                    "b": int(b_digit[i]),
                    "carry_in": int(carry[i]),
                    "predicted_carry_out": int(carry_pred[i]),
                })

            carry = carry_pred

    unit_summary = {}
    for u, values in activations_by_unit.items():
        unit_summary[str(u)] = {
            "mean": float(np.mean(values)),
            "std": float(np.std(values)),
            "min": float(np.min(values)),
            "max": float(np.max(values)),
        }

    return {
        "unit_summary": unit_summary,
        "carry_in_mean": float(np.mean(carry_inputs)) if carry_inputs else None,
        "sample_local_cases": local_cases[:20],
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 6 FAMILY-LEVEL LINK V1",
        "",
        "## Top Diagnostic Units",
        f"- {artifact['top_units']}",
        "",
        "## Family-Level Activation Summary",
    ]

    for family, info in artifact["families"].items():
        lines.append(f"\n### {family}")
        lines.append(f"- carry_in_mean: {info['carry_in_mean']}")
        lines.append(f"- unit_summary: {info['unit_summary']}")
        lines.append(f"- sample_local_cases: {info['sample_local_cases']}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This probe asks whether the units identified locally also track family-level differences.",
        "- It does not yet prove a complete family-level causal mechanism.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 6 FAMILY-LEVEL LINK V1")

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
        family_results[family_name] = collect_family_hidden_statistics(model, a, b, device=device)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_6_family_level_link_v1",
        "top_units": TOP_UNITS,
        "families": family_results,
        "notes": [
            "This probe links top local diagnostic units to family-level structure.",
            "It asks whether family differences are reflected in the same internal units identified earlier.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
