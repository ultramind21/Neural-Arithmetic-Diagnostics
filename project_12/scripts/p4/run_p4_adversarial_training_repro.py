"""
================================================================================
PROJECT 4 ADVERSARIAL TRAINING
================================================================================

PURPOSE:
  MVP intervention runner for Project 4:
  test whether adversarial training improves genuine structural robustness.

ROLE:
  This script builds a bounded first intervention path that:
    - trains an MLP baseline with adversarial augmentation
    - evaluates on seen adversarial families
    - evaluates on unseen / held-out adversarial family
    - emits Project 4-style structured artifacts

IMPORTANT:
  This is the first MVP intervention implementation.
  It is intentionally bounded and explicit.
  It does NOT by itself settle all Project 4 conclusions.

CURRENT STRATEGY (v1.0):
  - Base model family: Phase 30 MLP
  - Seen adversarial families used in augmentation:
      * alternating_carry
      * full_propagation_chain
  - Held-out adversarial family for transfer test:
      * block_boundary_stress

INTERPRETIVE PRINCIPLE:
  Improvement on seen adversarial families alone may reflect pattern memorization.
  Stronger evidence of robustness requires improvement on the held-out family too.

================================================================================
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import torch

# Project 12 utilities
from project_12.scripts.p12_runlib import (
    load_manifest,
    ensure_output_dir_is_safe,
    build_p12_metadata,
    write_json,
)


# ============================================================================
# PATHS
# ============================================================================
PROJECT_4_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = PROJECT_4_ROOT.parent

PHASE30_FILE = PROJECT_ROOT / "src" / "train" / "phase_30_multidigit_learning.py"
OUTPUT_DIR = PROJECT_4_ROOT / "interventions" / "adversarial_training" / "results"

JSON_OUTPUT = OUTPUT_DIR / "project_4_adversarial_training_artifact.json"
MD_OUTPUT = OUTPUT_DIR / "project_4_adversarial_training_report.md"


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


def load_phase30_module():
    if not PHASE30_FILE.exists():
        raise FileNotFoundError(f"Phase 30 source file not found: {PHASE30_FILE}")

    spec = importlib.util.spec_from_file_location("phase_30_multidigit_learning", str(PHASE30_FILE))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for {PHASE30_FILE}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def random_digit_batch(num_samples: int, length: int, seed: int):
    rng = np.random.default_rng(seed)
    a = rng.integers(0, 10, size=(num_samples, length), dtype=np.int64)
    b = rng.integers(0, 10, size=(num_samples, length), dtype=np.int64)
    return a, b


def compute_phase30_targets(a: np.ndarray, b: np.ndarray):
    if a.shape != b.shape:
        raise ValueError("a and b must have same shape")

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


def exact_match_over_valid_positions(
    digit_pred: np.ndarray,
    carry_pred: np.ndarray,
    digit_true: np.ndarray,
    carry_true: np.ndarray,
    lengths: np.ndarray,
) -> float:
    batch = digit_pred.shape[0]
    exact = []

    for i in range(batch):
        L = int(lengths[i])
        ok = (
            np.all(digit_pred[i, :L] == digit_true[i, :L]) and
            np.all(carry_pred[i, :L] == carry_true[i, :L])
        )
        exact.append(ok)

    return float(np.mean(exact)) if exact else 0.0


# ============================================================================
# PROJECT 4 ADVERSARIAL PATTERNS (LOCAL COPY FOR TRAIN/AUGMENT CONTROL)
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
# MODEL / TRAINING
# ============================================================================

def build_mlp_model(module, max_length: int, device: torch.device):
    model = module.MLPSequenceArithmetic(max_length=max_length)
    return model.to(device)


def make_training_tensors(a: np.ndarray, b: np.ndarray, device: torch.device):
    digit_true_np, carry_true_np = compute_phase30_targets(a, b)

    a_t = torch.tensor(a, dtype=torch.long, device=device)
    b_t = torch.tensor(b, dtype=torch.long, device=device)
    digit_true_t = torch.tensor(digit_true_np, dtype=torch.long, device=device)
    carry_true_t = torch.tensor(carry_true_np, dtype=torch.long, device=device)

    return a_t, b_t, digit_true_t, carry_true_t


def train_mlp_with_adversarial_augmentation(module, device: torch.device, seed: int = 42):
    torch.manual_seed(seed)
    np.random.seed(seed)

    # Base random training data
    all_a = []
    all_b = []

    for length in [2, 3, 4, 5]:
        a_rand, b_rand = random_digit_batch(num_samples=200, length=length, seed=seed + length)
        all_a.append(a_rand)
        all_b.append(b_rand)

    # For v1.0 bounded intervention, train only at length 5 after padding-like simplification:
    # convert all to fixed max_length=5 by right-padding zeros
    max_length = 5

    def pad_to_5(x):
        out = np.zeros((x.shape[0], max_length), dtype=np.int64)
        out[:, -x.shape[1]:] = x
        return out

    base_a = np.concatenate([pad_to_5(x) for x in all_a], axis=0)
    base_b = np.concatenate([pad_to_5(x) for x in all_b], axis=0)

    # Seen adversarial augmentation
    adv_alt_a, adv_alt_b = make_alternating_carry(num_samples=200, length=max_length)
    adv_chain_a, adv_chain_b = make_full_propagation_chain(num_samples=200, length=max_length)

    train_a = np.concatenate([base_a, adv_alt_a, adv_chain_a], axis=0)
    train_b = np.concatenate([base_b, adv_alt_b, adv_chain_b], axis=0)

    a_t, b_t, digit_true_t, carry_true_t = make_training_tensors(train_a, train_b, device=device)

    dataset = torch.utils.data.TensorDataset(a_t, b_t, digit_true_t, carry_true_t)
    loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

    model = build_mlp_model(module, max_length=max_length, device=device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion_digit = torch.nn.CrossEntropyLoss()
    criterion_carry = torch.nn.CrossEntropyLoss()

    model.train()
    for epoch in range(30):
        for a_batch, b_batch, digit_batch, carry_batch in loader:
            optimizer.zero_grad()
            digit_logits, carry_logits = model(a_batch, b_batch)

            loss_digit = criterion_digit(digit_logits.view(-1, 10), digit_batch.view(-1))
            loss_carry = criterion_carry(carry_logits.view(-1, 2), carry_batch.view(-1))
            loss = loss_digit + loss_carry
            loss.backward()
            optimizer.step()

    return model


# ============================================================================
# EVALUATION
# ============================================================================

def evaluate_batch(model, a: np.ndarray, b: np.ndarray, device: torch.device) -> Dict[str, float]:
    digit_true_np, carry_true_np = compute_phase30_targets(a, b)
    lengths_np = np.full(shape=(a.shape[0],), fill_value=a.shape[1], dtype=np.int64)

    a_t = torch.tensor(a, dtype=torch.long, device=device)
    b_t = torch.tensor(b, dtype=torch.long, device=device)
    digit_true_t = torch.tensor(digit_true_np, dtype=torch.long, device=device)
    carry_true_t = torch.tensor(carry_true_np, dtype=torch.long, device=device)

    model.eval()
    with torch.no_grad():
        digit_logits, carry_logits = model(a_t, b_t)

        digit_pred = digit_logits.argmax(dim=2)
        carry_pred = carry_logits.argmax(dim=2)

        digit_correct = (digit_pred == digit_true_t).float()
        carry_correct = (carry_pred == carry_true_t).float()
        combined_correct = digit_correct * carry_correct

    digit_pred_np = digit_pred.detach().cpu().numpy()
    carry_pred_np = carry_pred.detach().cpu().numpy()
    digit_correct_np = digit_correct.detach().cpu().numpy()
    carry_correct_np = carry_correct.detach().cpu().numpy()
    combined_correct_np = combined_correct.detach().cpu().numpy()

    digit_acc_list = []
    carry_acc_list = []
    combined_acc_list = []

    for i in range(a.shape[0]):
        L = int(lengths_np[i])
        digit_acc_list.append(float(np.mean(digit_correct_np[i, :L])))
        carry_acc_list.append(float(np.mean(carry_correct_np[i, :L])))
        combined_acc_list.append(float(np.mean(combined_correct_np[i, :L])))

    exact_match = exact_match_over_valid_positions(
        digit_pred=digit_pred_np,
        carry_pred=carry_pred_np,
        digit_true=digit_true_np,
        carry_true=carry_true_np,
        lengths=lengths_np,
    )

    return {
        "digit_acc": float(np.mean(digit_acc_list)),
        "carry_acc": float(np.mean(carry_acc_list)),
        "combined_acc": float(np.mean(combined_acc_list)),
        "exact_match": exact_match,
    }


# ============================================================================
# MAIN
# ============================================================================

def render_report(artifact: Dict[str, Any]) -> str:
    lines = [
        "# PROJECT 4 ADVERSARIAL TRAINING REPORT",
        "",
        "## Status",
        "Bounded MVP adversarial training artifact generated.",
        "",
        "## Core Question",
        "Does adversarial training improve seen-family robustness only, or also transfer to held-out adversarial structure?",
        "",
        "## Seen Adversarial Families",
        f"- alternating_carry: {artifact['seen_results']['alternating_carry']}",
        f"- full_propagation_chain: {artifact['seen_results']['full_propagation_chain']}",
        "",
        "## Held-Out Adversarial Family",
        f"- block_boundary_stress: {artifact['heldout_results']['block_boundary_stress']}",
        "",
        "## Baseline Reference",
        f"- in_distribution: {artifact['baseline_reference']['in_distribution']}",
        f"- heldout_block_boundary_reference: {artifact['baseline_reference']['block_boundary_stress']}",
        "",
        "## Qualification",
        "- This is a bounded MVP intervention artifact.",
        "- Stronger robustness claims require repeated-run validation and later synthesis.",
        "",
    ]
    return "\n".join(lines)


def main():
    # PATCH B: Parse arguments and load manifest
    parser = argparse.ArgumentParser(
        description="Project 4 adversarial training with P12 artifact output"
    )
    parser.add_argument(
        "--manifest",
        type=str,
        required=True,
        help="Path to Project 12 manifest JSON",
    )
    args = parser.parse_args()
    
    # Load manifest to extract output directory, baseline artifact path, and seed
    manifest = load_manifest(args.manifest)
    output_dir_relative = manifest.get("output_dir", "project_12/results/repro_p4/adversarial")
    output_dir = Path(output_dir_relative)
    ensure_output_dir_is_safe(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract seed (default 42 if not in manifest)
    seed = manifest.get("seed", 42)
    
    # PATCH C: Extract baseline exact_match from manifest-specified baseline artifact
    baseline_exact_match = {}
    baseline_artifact_path = manifest.get("baseline_artifact_path")
    if baseline_artifact_path:
        baseline_path = Path(baseline_artifact_path)
        if not baseline_path.is_absolute():
            # Resolve relative to workspace root
            workspace_root = Path(__file__).resolve().parents[3]
            baseline_path = workspace_root / baseline_path
        
        if baseline_path.exists():
            baseline_data = json.loads(baseline_path.read_text(encoding="utf-8"))
            # Extract per-family exact_match from raw_metrics.adversarial
            adv_metrics = baseline_data.get("raw_metrics", {}).get("adversarial", {})
            for family, metrics in adv_metrics.items():
                baseline_exact_match[family] = metrics.get("exact_match", 0.0)
        else:
            print(f"⚠️  Baseline artifact not found: {baseline_path}")
            print("   Continuing with empty baseline_exact_match")
    
    print_header("PROJECT 4 ADVERSARIAL TRAINING")

    module = load_phase30_module()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = train_mlp_with_adversarial_augmentation(module, device=device, seed=seed)
    print("✓ Adversarially trained MLP model ready")

    # Baseline-like in-distribution evaluation
    a_id, b_id = random_digit_batch(num_samples=128, length=5, seed=42)
    id_metrics = evaluate_batch(model, a_id, b_id, device=device)

    # Seen adversarial families
    alt_a, alt_b = make_alternating_carry(num_samples=64, length=5)
    chain_a, chain_b = make_full_propagation_chain(num_samples=64, length=5)

    seen_results = {
        "alternating_carry": evaluate_batch(model, alt_a, alt_b, device=device),
        "full_propagation_chain": evaluate_batch(model, chain_a, chain_b, device=device),
    }

    # Held-out family
    block_a, block_b = make_block_boundary_stress(num_samples=64, length=5)
    heldout_results = {
        "block_boundary_stress": evaluate_batch(model, block_a, block_b, device=device),
    }

    artifact = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "framework_version": "1.0",
        "intervention_type": "adversarial_training",
        "base_model_family": "phase30_mlp",
        "seen_families": ["alternating_carry", "full_propagation_chain"],
        "heldout_family": ["block_boundary_stress"],
        "in_distribution": id_metrics,
        "seen_results": seen_results,
        "heldout_results": heldout_results,
        "baseline_reference": {
            "in_distribution": "compare against PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md",
            "block_boundary_stress": "compare against stable baseline matrix",
        },
        "notes": [
            "Seen-family gains alone do not establish robust transfer.",
            "Held-out-family behavior is the key Project 4 MVP discriminator.",
            "This artifact should be followed by validation reruns if retained.",
        ],
    }

    save_json(JSON_OUTPUT, artifact)
    save_text(MD_OUTPUT, render_report(artifact))

    print(f"✓ JSON artifact saved to: {JSON_OUTPUT}")
    print(f"✓ Markdown report saved to: {MD_OUTPUT}")
    
    # PATCH D: Compute gains and write P12-format artifact
    seen_families = manifest.get("seen_families", ["alternating_carry", "full_propagation_chain"])
    heldout_families = manifest.get("heldout_families", ["block_boundary_stress"])
    
    # Extract post-training exact_match
    post_exact_match = {}
    for family in seen_families:
        post_exact_match[family] = artifact["seen_results"][family]["exact_match"]
    for family in heldout_families:
        post_exact_match[family] = artifact["heldout_results"][family]["exact_match"]
    
    # Compute gains
    pre_seen_vals = [baseline_exact_match.get(f, 0.0) for f in seen_families]
    post_seen_vals = [post_exact_match.get(f, 0.0) for f in seen_families]
    pre_heldout_vals = [baseline_exact_match.get(f, 0.0) for f in heldout_families]
    post_heldout_vals = [post_exact_match.get(f, 0.0) for f in heldout_families]
    
    pre_seen_mean = float(np.mean(pre_seen_vals)) if pre_seen_vals else 0.0
    post_seen_mean = float(np.mean(post_seen_vals)) if post_seen_vals else 0.0
    pre_heldout_mean = float(np.mean(pre_heldout_vals)) if pre_heldout_vals else 0.0
    post_heldout_mean = float(np.mean(post_heldout_vals)) if post_heldout_vals else 0.0
    
    seen_gain = post_seen_mean - pre_seen_mean
    heldout_gain = post_heldout_mean - pre_heldout_mean
    gap = seen_gain - heldout_gain
    
    # Build repro_check-compatible artifact
    acceptance = manifest.get("acceptance", {"min_gap": 0.10, "require_ordering": True})
    
    artifact_repro = {
        "base_arch": manifest.get("base_arch", "mlp"),
        "seen_families": seen_families,
        "heldout_families": heldout_families,
        "pre_exact_match": baseline_exact_match,
        "post_exact_match": post_exact_match,
        "computed_gains": {
            "pre_seen_mean": pre_seen_mean,
            "post_seen_mean": post_seen_mean,
            "pre_heldout_mean": pre_heldout_mean,
            "post_heldout_mean": post_heldout_mean,
            "seen_gain": float(seen_gain),
            "heldout_gain": float(heldout_gain),
            "gap": float(gap),
        },
        "acceptance": acceptance,
        "p12_metadata": build_p12_metadata(
            manifest_path=args.manifest,
            entrypoint="run_p4_adversarial_training_repro.py",
            source_script_copied_from="project_4/interventions/adversarial_training/project_4_adversarial_training.py",
        ),
    }
    
    artifact_path_repro = output_dir / "artifact.json"
    write_json(artifact_path_repro, artifact_repro)
    print(f"✓ P12 repro artifact saved to: {artifact_path_repro}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
