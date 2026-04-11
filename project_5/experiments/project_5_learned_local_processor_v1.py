"""
================================================================================
PROJECT 5 LEARNED LOCAL PROCESSOR V1
================================================================================

PURPOSE:
  Test whether a learned local processor can support decomposition with an
  explicit carry interface.

CORE QUESTION:
  Can a small learned digitwise module approximate:
    (a_digit, b_digit, carry_in) -> (digit_out, carry_out)
  well enough to preserve structural robustness when composed blockwise?

CURRENT DESIGN:
  1. Train a small local processor on exact local digit-addition examples
  2. Evaluate its local accuracy
  3. Insert it into blockwise-with-carry-interface composition
  4. Test the composed system on:
       - alternating_carry
       - full_propagation_chain
       - block_boundary_stress

IMPORTANT:
  This is the first learned-interface experiment in Project 5.
  It tests local learnability plus compositional use, not final project closure.

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

JSON_OUTPUT = OUTPUT_DIR / "project_5_learned_local_processor_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_5_learned_local_processor_v1_report.md"


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
# EXACT ARITHMETIC
# ============================================================================

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


def local_oracle(a_digit: np.ndarray, b_digit: np.ndarray, carry_in: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    s = a_digit + b_digit + carry_in
    digit = s % 10
    carry = s // 10
    return digit.astype(np.int64), carry.astype(np.int64)


# ============================================================================
# LOCAL DATASET
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
# TRAINING
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
        digit_pred = digit_logits.argmax(dim=1)
        carry_pred = carry_logits.argmax(dim=1)

        digit_acc = (digit_pred == digit_t).float().mean().item()
        carry_acc = (carry_pred == carry_t).float().mean().item()
        local_exact = ((digit_pred == digit_t) & (carry_pred == carry_t)).float().mean().item()

    return model, {
        "local_digit_acc": digit_acc,
        "local_carry_acc": carry_acc,
        "local_exact_acc": local_exact,
    }


# ============================================================================
# LEARNED LOCAL PROCESSOR
# ============================================================================

class LearnedLocalProcessor:
    def __init__(self, model: LocalCarryNet, device: torch.device):
        self.model = model
        self.device = device

    def predict_local(self, a_digit: np.ndarray, b_digit: np.ndarray, carry_in: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        x = np.stack([a_digit, b_digit, carry_in], axis=1).astype(np.float32)
        x_t = torch.tensor(x, dtype=torch.float32, device=self.device)

        with torch.no_grad():
            digit_logits, carry_logits = self.model(x_t)
            digit = digit_logits.argmax(dim=1).detach().cpu().numpy()
            carry = carry_logits.argmax(dim=1).detach().cpu().numpy()

        return digit.astype(np.int64), carry.astype(np.int64)


# ============================================================================
# BLOCKWISE COMPOSITION
# ============================================================================

def blockwise_with_learned_interface(
    processor: LearnedLocalProcessor,
    a: np.ndarray,
    b: np.ndarray,
    chunk_size: int,
) -> np.ndarray:
    batch, length = a.shape
    out = np.zeros((batch, length + 1), dtype=np.int64)

    carry_between_chunks = np.zeros(batch, dtype=np.int64)

    for chunk_end in range(length, 0, -chunk_size):
        chunk_start = max(0, chunk_end - chunk_size)

        carry = carry_between_chunks.copy()
        for pos in range(chunk_end - 1, chunk_start - 1, -1):
            digit, carry = processor.predict_local(a[:, pos], b[:, pos], carry)
            out[:, pos + 1] = digit

        carry_between_chunks = carry

    out[:, 0] = carry_between_chunks
    return out


# ============================================================================
# EVALUATION
# ============================================================================

def evaluate_family(
    processor: LearnedLocalProcessor,
    a: np.ndarray,
    b: np.ndarray,
    chunk_size: int,
) -> Dict[str, float]:
    truth = full_exact_addition(a, b)
    pred = blockwise_with_learned_interface(processor, a, b, chunk_size=chunk_size)

    return {
        "exact_match": exact_match_accuracy(pred, truth),
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 5 LEARNED LOCAL PROCESSOR V1 RESULTS",
        "",
        "## Status",
        "First learned local decomposition experiment completed.",
        "",
        "## Local Processor Training",
        f"- local_digit_acc: {artifact['local_training_metrics']['local_digit_acc']}",
        f"- local_carry_acc: {artifact['local_training_metrics']['local_carry_acc']}",
        f"- local_exact_acc: {artifact['local_training_metrics']['local_exact_acc']}",
        "",
        "## Family Results",
    ]

    for family, result in artifact["results"].items():
        lines.append(f"- {family}: {result}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This experiment tests whether a learned local processor can support decomposition with explicit carry passing.",
        "- It does not yet establish broad Project 5 closure.",
        "- It is the first empirical step after the structural-oracle decomposition result.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 5 LEARNED LOCAL PROCESSOR V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    chunk_size = 2
    length = 6
    num_samples = 64

    model, local_metrics = train_local_model(device=device)
    processor = LearnedLocalProcessor(model=model, device=device)

    print("✓ Local processor trained")
    print(local_metrics)

    families = {
        "alternating_carry": make_alternating_carry(num_samples=num_samples, length=length),
        "full_propagation_chain": make_full_propagation_chain(num_samples=num_samples, length=length),
        "block_boundary_stress": make_block_boundary_stress(num_samples=num_samples, length=length),
    }

    results: Dict[str, Dict[str, float]] = {}

    for family_name, (a, b) in families.items():
        results[family_name] = evaluate_family(processor, a, b, chunk_size=chunk_size)

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "experiment": "project_5_learned_local_processor_v1",
        "chunk_size": chunk_size,
        "length": length,
        "num_samples": num_samples,
        "local_training_metrics": local_metrics,
        "results": results,
        "notes": [
            "This is the first learned local processor experiment in Project 5.",
            "It follows the structural-oracle decomposition result.",
            "Its purpose is to test whether learned carry-interface support can preserve blockwise robustness.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
