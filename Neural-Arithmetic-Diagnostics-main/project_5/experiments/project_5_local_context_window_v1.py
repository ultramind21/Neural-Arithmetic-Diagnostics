"""
================================================================================
PROJECT 5 LOCAL CONTEXT WINDOW V1
================================================================================

PURPOSE:
  Test whether adding a small local context window improves the learned local
  decomposition behavior.

CORE HYPOTHESIS:
  The local processor may need more than (a_i, b_i, carry_in). A small local
  neighborhood may help disambiguate higher-variation pattern families.

CURRENT DESIGN:
  Input at position i includes:
    - previous digit pair
    - current digit pair
    - next digit pair
    - carry_in

This yields a richer local representation while preserving decomposition spirit.

QUESTIONS:
  1. Does local digit accuracy improve?
  2. Does carry-conditioned digit behavior improve?
  3. Does composed exact-match improve on alternating/block-boundary families?

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

JSON_OUTPUT = OUTPUT_DIR / "project_5_local_context_window_v1_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_5_local_context_window_v1_report.md"


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


def local_targets(a_digit: int, b_digit: int, carry_in: int):
    total = a_digit + b_digit + carry_in
    return total % 10, total // 10


# ============================================================================
# CONTEXT DATASET
# ============================================================================

def build_context_dataset():
    X = []
    digit_y = []
    carry_y = []

    digits = list(range(10))

    for prev_a in digits:
        for prev_b in digits:
            for a in digits:
                for b in digits:
                    for next_a in digits:
                        for next_b in digits:
                            for carry_in in [0, 1]:
                                X.append([prev_a, prev_b, a, b, next_a, next_b, carry_in])
                                d, c = local_targets(a, b, carry_in)
                                digit_y.append(d)
                                carry_y.append(c)

    X = np.array(X, dtype=np.float32)
    digit_y = np.array(digit_y, dtype=np.int64)
    carry_y = np.array(carry_y, dtype=np.int64)
    return X, digit_y, carry_y


# ============================================================================
# MODEL
# ============================================================================

class ContextWindowLocalNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(7, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
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

def train_model(device: torch.device):
    X, digit_y, carry_y = build_context_dataset()

    X_t = torch.tensor(X, dtype=torch.float32, device=device)
    digit_t = torch.tensor(digit_y, dtype=torch.long, device=device)
    carry_t = torch.tensor(carry_y, dtype=torch.long, device=device)

    model = ContextWindowLocalNet().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion_digit = nn.CrossEntropyLoss()
    criterion_carry = nn.CrossEntropyLoss()

    for _ in range(200):
        optimizer.zero_grad()
        digit_logits, carry_logits = model(X_t)
        loss = criterion_digit(digit_logits, digit_t) + criterion_carry(carry_logits, carry_t)
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        digit_logits, carry_logits = model(X_t)
        digit_pred = digit_logits.argmax(dim=1).detach().cpu().numpy()
        carry_pred = carry_logits.argmax(dim=1).detach().cpu().numpy()

    return model, X, digit_y, carry_y, digit_pred, carry_pred


# ============================================================================
# ANALYSIS
# ============================================================================

def analyze_local_behavior(digit_y, carry_y, digit_pred, carry_pred):
    digit_correct = (digit_pred == digit_y)
    carry_correct = (carry_pred == carry_y)
    exact_correct = digit_correct & carry_correct

    overall = {
        "digit_acc": float(np.mean(digit_correct)),
        "carry_acc": float(np.mean(carry_correct)),
        "exact_acc": float(np.mean(exact_correct)),
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

    return {
        "overall": overall,
        "by_carry_out": by_carry_out,
    }


# ============================================================================
# LOCAL PROCESSOR
# ============================================================================

class ContextWindowProcessor:
    def __init__(self, model: ContextWindowLocalNet, device: torch.device):
        self.model = model
        self.device = device

    def predict_local(
        self,
        prev_a: np.ndarray,
        prev_b: np.ndarray,
        a: np.ndarray,
        b: np.ndarray,
        next_a: np.ndarray,
        next_b: np.ndarray,
        carry_in: np.ndarray,
    ):
        x = np.stack([prev_a, prev_b, a, b, next_a, next_b, carry_in], axis=1).astype(np.float32)
        x_t = torch.tensor(x, dtype=torch.float32, device=self.device)

        with torch.no_grad():
            digit_logits, carry_logits = self.model(x_t)
            digit = digit_logits.argmax(dim=1).detach().cpu().numpy()
            carry = carry_logits.argmax(dim=1).detach().cpu().numpy()

        return digit.astype(np.int64), carry.astype(np.int64)


# ============================================================================
# BLOCKWISE COMPOSITION
# ============================================================================

def get_context(arr: np.ndarray, pos: int):
    prev_ = arr[:, pos - 1] if pos - 1 >= 0 else np.zeros(arr.shape[0], dtype=np.int64)
    curr_ = arr[:, pos]
    next_ = arr[:, pos + 1] if pos + 1 < arr.shape[1] else np.zeros(arr.shape[0], dtype=np.int64)
    return prev_, curr_, next_


def blockwise_with_context_window(
    processor: ContextWindowProcessor,
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
            prev_a, curr_a, next_a = get_context(a, pos)
            prev_b, curr_b, next_b = get_context(b, pos)

            digit, carry = processor.predict_local(
                prev_a, prev_b, curr_a, curr_b, next_a, next_b, carry
            )
            out[:, pos + 1] = digit

        carry_between_chunks = carry

    out[:, 0] = carry_between_chunks
    return out


# ============================================================================
# EVALUATION
# ============================================================================

def evaluate_family(
    processor: ContextWindowProcessor,
    a: np.ndarray,
    b: np.ndarray,
    chunk_size: int,
) -> Dict[str, float]:
    truth = full_exact_addition(a, b)
    pred = blockwise_with_context_window(processor, a, b, chunk_size=chunk_size)
    return {
        "exact_match": exact_match_accuracy(pred, truth),
    }


# ============================================================================
# REPORT
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    overall = artifact["local_analysis"]["overall"]
    by_carry_out = artifact["local_analysis"]["by_carry_out"]

    lines = [
        "# PROJECT 5 LOCAL CONTEXT WINDOW V1 RESULTS",
        "",
        "## Overall Local Metrics",
        f"- digit_acc: {overall['digit_acc']}",
        f"- carry_acc: {overall['carry_acc']}",
        f"- exact_acc: {overall['exact_acc']}",
        "",
        "## Local Digit Accuracy by carry_out",
        f"- carry_out = 0: {by_carry_out['0']}",
        f"- carry_out = 1: {by_carry_out['1']}",
        "",
        "## Composed Family Results",
    ]

    for family, result in artifact["results"].items():
        lines.append(f"- {family}: {result}")

    lines.extend([
        "",
        "## Interpretation Boundary",
        "- This experiment tests whether a richer local context window improves decomposition performance.",
        "- It does not yet establish final Project 5 closure.",
        "",
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 5 LOCAL CONTEXT WINDOW V1")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    chunk_size = 2
    length = 6
    num_samples = 64

    model, X, digit_y, carry_y, digit_pred, carry_pred = train_model(device=device)
    processor = ContextWindowProcessor(model=model, device=device)

    print("✓ Context-window local processor trained")

    local_analysis = analyze_local_behavior(digit_y, carry_y, digit_pred, carry_pred)

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
        "experiment": "project_5_local_context_window_v1",
        "chunk_size": chunk_size,
        "length": length,
        "num_samples": num_samples,
        "local_analysis": local_analysis,
        "results": results,
        "notes": [
            "This experiment tests whether richer local context improves learned decomposition.",
            "Its purpose is to see whether local neighborhood information helps the unrecovered families.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
