"""
================================================================================
PROJECT 4 PHASE-30 TRANSFORMER BASELINE EVALUATION
================================================================================

PURPOSE:
  Execute the Phase 30 Transformer baseline evaluation path under Project 4 using
  Phase-30-aligned digit/carry evaluation semantics.

ALIGNMENT PRINCIPLE:
  This file follows the actual Phase 30 evaluation structure:
    - digit predictions decoded by argmax over digit logits
    - carry predictions decoded by argmax over carry logits
    - metrics computed over valid sequence positions only
    - exact match requires both digit and carry correctness across the sequence

IMPORTANT:
  This file provides a bounded baseline artifact for Project 4.
  Final regime assignment remains human-reviewed.

================================================================================
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import torch

from project_4.baselines.project_4_baseline_runtime_adapter_phase30 import build_phase30_adapter
from project_4.diagnostics.benchmark_adversarial_patterns import generate_project4_adversarial_patterns
from project_4.diagnostics.diagnostic_scorecard import build_scorecard, scorecard_to_dict
from project_4.diagnostics.regime_classification import classify_regime


# ============================================================================
# PATHS
# ============================================================================
PROJECT_4_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_4_ROOT / "results" / "baseline_runs"


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


def evaluate_batch_phase30_style(adapter, a: np.ndarray, b: np.ndarray) -> Dict[str, float]:
    model = adapter.get_model()
    device = adapter.device

    digit_true_np, carry_true_np = compute_phase30_targets(a, b)
    lengths_np = np.full(shape=(a.shape[0],), fill_value=a.shape[1], dtype=np.int64)

    a_t = torch.tensor(a, dtype=torch.long, device=device)
    b_t = torch.tensor(b, dtype=torch.long, device=device)
    digit_true_t = torch.tensor(digit_true_np, dtype=torch.long, device=device)
    carry_true_t = torch.tensor(carry_true_np, dtype=torch.long, device=device)

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


def evaluate_in_distribution(adapter, train_length: int, num_samples: int, seed: int) -> Dict[str, float]:
    a, b = random_digit_batch(num_samples=num_samples, length=train_length, seed=seed)
    return evaluate_batch_phase30_style(adapter, a, b)


def evaluate_adversarial(adapter, length: int, num_samples: int) -> Dict[str, Dict[str, float]]:
    patterns = generate_project4_adversarial_patterns(length=length, num_samples=num_samples)
    return {
        name: evaluate_batch_phase30_style(adapter, pattern.operand_a, pattern.operand_b)
        for name, pattern in patterns.items()
    }


def evaluate_lengths(adapter, lengths: List[int], num_samples: int, seed: int) -> Dict[int, Dict[str, float]]:
    results = {}
    for i, L in enumerate(lengths):
        a, b = random_digit_batch(num_samples=num_samples, length=L, seed=seed + 1000 + i)
        results[L] = evaluate_batch_phase30_style(adapter, a, b)
    return results


def evaluate_rounding_sensitivity_placeholder(in_distribution_metrics: Dict[str, float]) -> Dict[str, Any]:
    return {
        "status": "placeholder",
        "with_rounding": in_distribution_metrics["exact_match"],
        "without_rounding": in_distribution_metrics["exact_match"],
        "sensitivity": 0.0,
        "qualification": "alternate decode path not yet implemented in aligned Phase 30 Project 4 path",
    }


def evaluate_carry_corruption_placeholder(baseline_exact_match: float, corruption_levels: List[float]) -> Dict[str, Any]:
    return {
        "status": "placeholder",
        "levels": corruption_levels,
        "accuracies": {float(p): baseline_exact_match for p in corruption_levels},
        "qualification": "carry corruption intervention not yet directly wired into aligned Phase 30 Project 4 path",
    }


def render_report(
    model_name: str,
    scorecard: Dict[str, Any],
    regime_guidance: Dict[str, Any],
    adapter_metadata: Dict[str, Any],
    qualification_notes: List[str],
    artifact_path: str,
    raw_metrics: Dict[str, Any],
) -> str:
    lines = [
        f"# PROJECT 4 BASELINE REPORT — {model_name}",
        "",
        "## Status",
        "Aligned Phase 30 evaluation-path baseline artifact generated.",
        "",
        "## Raw Metrics",
        f"- in_distribution: {raw_metrics.get('in_distribution')}",
        f"- adversarial: {raw_metrics.get('adversarial')}",
        f"- lengths: {raw_metrics.get('lengths')}",
        "",
        "## Scorecard Projection",
        f"- in_distribution_accuracy: {scorecard.get('in_distribution_accuracy')}",
        f"- pattern_breakdown: {scorecard.get('pattern_breakdown')}",
        f"- mean_adversarial_accuracy: {scorecard.get('mean_adversarial_accuracy')}",
        f"- worst_case_pattern_accuracy: {scorecard.get('worst_case_pattern_accuracy')}",
        f"- length_summary: {scorecard.get('length_summary')}",
        f"- rounding_sensitivity: {scorecard.get('rounding_sensitivity')}",
        f"- carry_corruption_summary: {scorecard.get('carry_corruption_summary')}",
        "",
        "## Regime Guidance",
        f"- tentative regime: {regime_guidance.get('tentative_regime')}",
        f"- rationale: {regime_guidance.get('rationale')}",
        f"- cautions: {regime_guidance.get('cautions')}",
        "",
        "## Adapter Metadata",
        f"- adapter metadata: {adapter_metadata}",
        "",
        "## Qualification Notes",
    ]

    for note in qualification_notes:
        lines.append(f"- {note}")

    lines.extend([
        "",
        "## Artifact Path",
        f"- {artifact_path}",
        "",
    ])

    return "\n".join(lines)


def parse_args():
    parser = argparse.ArgumentParser(description="Project 4 Phase30 Transformer baseline evaluation")
    parser.add_argument("--model-name", type=str, default="phase30_transformer_baseline")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--train-length", type=int, default=5)
    parser.add_argument("--adversarial-length", type=int, default=5)
    parser.add_argument("--num-samples-id", type=int, default=128)
    parser.add_argument("--num-samples-adv", type=int, default=32)
    parser.add_argument("--num-samples-extra", type=int, default=128)
    parser.add_argument("--lengths", type=int, nargs="+", default=[5])
    parser.add_argument("--corruption-levels", type=float, nargs="+", default=[0.0, 0.1, 0.2, 0.5])
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print_header("PROJECT 4 PHASE-30 TRANSFORMER BASELINE EVALUATION (ALIGNED PATH)")

    device = torch.device(args.device)
    adapter = build_phase30_adapter(
        model_type="transformer",
        checkpoint_path=args.checkpoint,
        device=device,
    )

    in_distribution_metrics = evaluate_in_distribution(
        adapter=adapter,
        train_length=args.train_length,
        num_samples=args.num_samples_id,
        seed=args.seed,
    )

    adversarial_metrics = evaluate_adversarial(
        adapter=adapter,
        length=args.adversarial_length,
        num_samples=args.num_samples_adv,
    )

    length_metrics = evaluate_lengths(
        adapter=adapter,
        lengths=args.lengths,
        num_samples=args.num_samples_extra,
        seed=args.seed,
    )

    rounding_info = evaluate_rounding_sensitivity_placeholder(in_distribution_metrics)
    corruption_info = evaluate_carry_corruption_placeholder(
        baseline_exact_match=in_distribution_metrics["exact_match"],
        corruption_levels=args.corruption_levels,
    )

    pattern_breakdown = {
        name: metrics["exact_match"]
        for name, metrics in adversarial_metrics.items()
    }

    accuracy_by_length = {
        int(L): metrics["exact_match"]
        for L, metrics in length_metrics.items()
    }

    qualification_notes = [
        "This baseline artifact uses the actual Phase 30 digit/carry evaluation semantics.",
        "Project 4 scorecard projection currently maps in-distribution and adversarial values using exact_match as the closest aligned scalar.",
        "Rounding sensitivity remains placeholder until an alternate aligned decode path is explicitly defined.",
        "Carry corruption remains placeholder until direct aligned intervention wiring is implemented.",
        "Final regime assignment must remain human-reviewed.",
    ]

    scorecard = build_scorecard(
        model_name=args.model_name,
        in_distribution_accuracy=in_distribution_metrics["exact_match"],
        pattern_breakdown=pattern_breakdown,
        training_max_length=args.train_length,
        accuracy_by_length=accuracy_by_length,
        accuracy_with_rounding=rounding_info["with_rounding"],
        accuracy_without_rounding=rounding_info["without_rounding"],
        accuracy_by_corruption=corruption_info["accuracies"],
        notes=qualification_notes,
        tags=["project4", "phase30", "transformer", "aligned_eval_path"],
    )

    scorecard_dict = scorecard_to_dict(scorecard)
    regime_guidance = classify_regime(scorecard_dict)

    raw_metrics = {
        "in_distribution": in_distribution_metrics,
        "adversarial": adversarial_metrics,
        "lengths": length_metrics,
        "rounding": rounding_info,
        "carry_corruption": corruption_info,
    }

    artifact = {
        "model_name": args.model_name,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "config": vars(args),
        "adapter_metadata": adapter.metadata(),
        "qualification_notes": qualification_notes,
        "raw_metrics": raw_metrics,
        "scorecard": scorecard_dict,
        "regime_guidance": regime_guidance,
    }

    json_path = RESULTS_DIR / f"{args.model_name}_artifact.json"
    md_path = RESULTS_DIR / f"{args.model_name}_report.md"

    save_json(json_path, artifact)
    save_text(
        md_path,
        render_report(
            model_name=args.model_name,
            scorecard=scorecard_dict,
            regime_guidance=regime_guidance,
            adapter_metadata=adapter.metadata(),
            qualification_notes=qualification_notes,
            artifact_path=str(json_path),
            raw_metrics=raw_metrics,
        ),
    )

    print(f"✓ JSON artifact saved to: {json_path}")
    print(f"✓ Markdown report saved to: {md_path}")
    print(f"✓ Tentative regime: {regime_guidance.get('tentative_regime')}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
