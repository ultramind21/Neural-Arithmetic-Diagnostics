"""
================================================================================
RUN_P4_TRANSFORMER_BASELINE_REPRO.PY
================================================================================

PROJECT 12 BASELINE REPRODUCTION ENTRYPOINT — TRANSFORMER

PURPOSE:
  Reproduce Project 4 Transformer baseline evaluation in Project 12 using manifest-driven
  configuration. Read output_dir from manifest, execute baseline evaluation,
  add P12 metadata, and save artifact to project_12/results/.

PROCEDURE:
  1. Load manifest (JSON path from --manifest)
  2. Extract output_dir, optional device
  3. Safety check: ensure output_dir is within project_12/results/
  4. Copy Project 4 evaluation logic (digit/carry Phase 30 semantics)
  5. Build scorecard and regime guidance
  6. Create artifact with p12_metadata
  7. Save to output_dir/artifact.json

ALIGNMENT:
  - No changes to evaluation logic (scorecard, regime classification)
  - No changes to metric computation
  - Only patch: output path + manifest + p12_metadata

================================================================================
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import torch

# Setup paths - add scripts directory to sys.path FIRST
scripts_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(scripts_dir))

# NOW import p12_runlib to get find_repo_root
import p12_runlib
from p12_runlib import (
    load_manifest,
    ensure_output_dir_is_safe,
    build_p12_metadata,
    write_json,
    write_text,
    find_repo_root,
)

PROJECT_ROOT = find_repo_root()
sys.path.insert(0, str(PROJECT_ROOT))

# Import Project 4 baseline components
from project_4.baselines.project_4_baseline_runtime_adapter_phase30 import build_phase30_adapter
from project_4.diagnostics.benchmark_adversarial_patterns import generate_project4_adversarial_patterns
from project_4.diagnostics.diagnostic_scorecard import build_scorecard, scorecard_to_dict
from project_4.diagnostics.regime_classification import classify_regime


# ============================================================================
# PATHS (using find_repo_root for robust resolution)
# ============================================================================

PROJECT_4_ROOT = PROJECT_ROOT / "project_4"
SOURCE_SCRIPT = PROJECT_4_ROOT / "baselines" / "project_4_phase30_transformer_baseline_eval.py"
CHECKPOINT_PATH = PROJECT_4_ROOT / "checkpoints" / "phase30_transformer_project4_ready.pt"


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def random_digit_batch(num_samples: int, length: int, seed: int):
    rng = np.random.default_rng(seed)
    a = rng.integers(0, 10, size=(num_samples, length), dtype=np.int64)
    b = rng.integers(0, 10, size=(num_samples, length), dtype=np.int64)
    return a, b


def compute_phase30_targets(a: np.ndarray, b: np.ndarray):
    """
    Compute digit_true and carry_true consistent with Phase 30 semantics.
    """
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


def evaluate_batch_phase30_style(
    adapter,
    a: np.ndarray,
    b: np.ndarray,
) -> Dict[str, float]:
    """
    Use actual Phase 30-style digit/carry evaluation semantics.
    """
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


# ============================================================================
# EVALUATION FAMILIES
# ============================================================================

def evaluate_in_distribution(adapter, train_length: int, num_samples: int, seed: int) -> Dict[str, float]:
    a, b = random_digit_batch(num_samples=num_samples, length=train_length, seed=seed)
    return evaluate_batch_phase30_style(adapter, a, b)


def evaluate_adversarial(adapter, length: int, num_samples: int) -> Dict[str, Dict[str, float]]:
    patterns = generate_project4_adversarial_patterns(length=length, num_samples=num_samples)
    results = {}

    for name, pattern in patterns.items():
        results[name] = evaluate_batch_phase30_style(adapter, pattern.operand_a, pattern.operand_b)

    return results


def evaluate_lengths(adapter, lengths: List[int], num_samples: int, seed: int) -> Dict[int, Dict[str, float]]:
    results = {}
    for i, L in enumerate(lengths):
        a, b = random_digit_batch(num_samples=num_samples, length=L, seed=seed + 1000 + i)
        results[L] = evaluate_batch_phase30_style(adapter, a, b)
    return results


def evaluate_rounding_sensitivity_placeholder(
    in_distribution_metrics: Dict[str, float],
) -> Dict[str, Any]:
    return {
        "status": "placeholder",
        "with_rounding": in_distribution_metrics["exact_match"],
        "without_rounding": in_distribution_metrics["exact_match"],
        "sensitivity": 0.0,
        "qualification": "alternate decode path not yet implemented in aligned Phase 30 Project 4 path",
    }


def evaluate_carry_corruption_placeholder(
    baseline_exact_match: float,
    corruption_levels: List[float],
) -> Dict[str, Any]:
    return {
        "status": "placeholder",
        "levels": corruption_levels,
        "accuracies": {float(p): baseline_exact_match for p in corruption_levels},
        "qualification": "carry corruption intervention not yet directly wired into aligned Phase 30 Project 4 path",
    }


def validate_checkpoint(ckpt_path: Path, device: torch.device) -> Dict[str, Any]:
    """Validate and probe checkpoint loading."""
    result = {
        "checkpoint_path": str(ckpt_path),
        "checkpoint_exists": ckpt_path.exists(),
        "checkpoint_readable": False,
        "state_dict_num_keys": 0,
        "param_norm_estimate": 0.0,
    }

    assert ckpt_path.exists(), f"Checkpoint not found: {ckpt_path}"

    try:
        state_dict = torch.load(ckpt_path, map_location=device)
        if isinstance(state_dict, dict):
            result["state_dict_num_keys"] = len(state_dict)
            norms = []
            for key, val in state_dict.items():
                if isinstance(val, torch.Tensor):
                    norms.append(val.norm().item())
            if norms:
                result["param_norm_estimate"] = (sum(n**2 for n in norms)) ** 0.5
            result["checkpoint_readable"] = True
            print(f"  ✓ Checkpoint readable: {result['state_dict_num_keys']} keys, "
                  f"param norm={result['param_norm_estimate']:.6f}")
        else:
            raise ValueError(f"Unexpected checkpoint object type: {type(state_dict)}")
    except Exception as e:
        print(f"  ✗ Checkpoint load failed: {e}")
        raise AssertionError(f"Checkpoint loading failed for {ckpt_path}: {e}")

    return result


# ============================================================================
# MAIN
# ============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Project 12 Project 4 Transformer baseline reproduction"
    )
    parser.add_argument(
        "--manifest",
        type=str,
        required=True,
        help="Path to manifest JSON file",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="phase30_transformer_baseline",
        help="Model name for artifact",
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        default="",
        help="Checkpoint path. If empty, will attempt to load from adapter defaults.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device (cpu or cuda:N)",
    )
    parser.add_argument(
        "--train-length",
        type=int,
        default=5,
        help="Training digit length",
    )
    parser.add_argument(
        "--adversarial-length",
        type=int,
        default=5,
        help="Adversarial pattern length",
    )
    parser.add_argument(
        "--num-samples-id",
        type=int,
        default=128,
        help="Samples for in-distribution evaluation",
    )
    parser.add_argument(
        "--num-samples-adv",
        type=int,
        default=32,
        help="Samples for adversarial evaluation",
    )
    parser.add_argument(
        "--num-samples-extra",
        type=int,
        default=128,
        help="Samples for length evaluation",
    )
    parser.add_argument(
        "--lengths",
        type=int,
        nargs="+",
        default=[5],
        help="Lengths to test",
    )
    parser.add_argument(
        "--corruption-levels",
        type=float,
        nargs="+",
        default=[0.0, 0.1, 0.2, 0.5],
        help="Carry corruption levels",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )
    
    return parser.parse_args()


def main():
    args = parse_args()
    manifest = p12_runlib.load_manifest(args.manifest)

    print_header("PROJECT 12 — PROJECT 4 TRANSFORMER BASELINE REPRODUCTION")

    # Get output_dir from manifest
    output_dir = Path(manifest.get("output_dir"))
    
    # Safety check
    p12_runlib.ensure_output_dir_is_safe(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Output directory: {output_dir}")

    device = torch.device(args.device)

    # Validate checkpoint before building adapter
    print(f"Validating checkpoint...")
    ckpt_metadata = validate_checkpoint(CHECKPOINT_PATH, device)

    # Get checkpoint (if specified, use it; otherwise use default from adapter)
    checkpoint_path = args.checkpoint if args.checkpoint else str(CHECKPOINT_PATH)
    
    print(f"Building adapter (Transformer)...")
    adapter = build_phase30_adapter(
        model_type="transformer",
        checkpoint_path=checkpoint_path,
        device=device,
    )

    print(f"Evaluating in-distribution...")
    in_distribution_metrics = evaluate_in_distribution(
        adapter=adapter,
        train_length=args.train_length,
        num_samples=args.num_samples_id,
        seed=args.seed,
    )

    print(f"Evaluating adversarial patterns...")
    adversarial_metrics = evaluate_adversarial(
        adapter=adapter,
        length=args.adversarial_length,
        num_samples=args.num_samples_adv,
    )

    print(f"Evaluating lengths...")
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

    # For Project 4 scorecard projection
    pattern_breakdown = {
        name: metrics["exact_match"]
        for name, metrics in adversarial_metrics.items()
    }

    accuracy_by_length = {
        int(L): metrics["exact_match"]
        for L, metrics in length_metrics.items()
    }

    qualification_notes = [
        "PROJECT 12 BASELINE REPRODUCTION: This artifact was generated by re-running Project 4 baseline evaluation in Project 12.",
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
        tags=["project4", "phase30", "transformer", "aligned_eval_path", "p12_repro"],
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

    # Build P12 metadata
    p12_metadata = p12_runlib.build_p12_metadata(
        manifest_path=args.manifest,
        entrypoint="run_p4_transformer_baseline_repro.py",
        source_script_copied_from=str(SOURCE_SCRIPT.relative_to(PROJECT_ROOT)),
    )

    artifact = {
        "model_name": args.model_name,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "config": vars(args),
        "adapter_metadata": adapter.metadata(),
        "qualification_notes": qualification_notes,
        "raw_metrics": raw_metrics,
        "scorecard": scorecard_dict,
        "regime_guidance": regime_guidance,
        "checkpoint_metadata": ckpt_metadata,
        "p12_metadata": p12_metadata,
    }

    artifact_path = output_dir / "artifact.json"
    md_path = output_dir / "report.md"

    p12_runlib.write_json(artifact_path, artifact)
    
    report_text = f"""# PROJECT 12 — PROJECT 4 TRANSFORMER BASELINE REPRODUCTION REPORT

**Generated:** {p12_metadata['timestamp_utc']}  
**Git Hash:** {p12_metadata['git_hash']}  
**Manifest:** {args.manifest}

## Status
Aligned Phase 30 evaluation-path baseline artifact regenerated in Project 12.

## Raw Metrics
- in_distribution: {raw_metrics.get('in_distribution')}
- adversarial: {raw_metrics.get('adversarial')}
- lengths: {raw_metrics.get('lengths')}

## Scorecard Projection
- in_distribution_accuracy: {scorecard_dict.get('in_distribution_accuracy')}
- pattern_breakdown: {scorecard_dict.get('pattern_breakdown')}
- mean_adversarial_accuracy: {scorecard_dict.get('mean_adversarial_accuracy')}
- worst_case_pattern_accuracy: {scorecard_dict.get('worst_case_pattern_accuracy')}
- length_summary: {scorecard_dict.get('length_summary')}

## Regime Guidance
- tentative regime: {regime_guidance.get('tentative_regime')}
- rationale: {regime_guidance.get('rationale')}

## Qualification Notes
{chr(10).join(f'- {note}' for note in qualification_notes)}

## Artifact Path
- {artifact_path}
"""
    
    p12_runlib.write_text(md_path, report_text)

    print(f"\n✓ Artifact saved to: {artifact_path}")
    print(f"✓ Report saved to: {md_path}")
    print(f"✓ Model name: {args.model_name}")
    print(f"✓ In-distribution exact match: {in_distribution_metrics['exact_match']:.6f}")
    print(f"✓ Mean adversarial accuracy: {scorecard_dict.get('mean_adversarial_accuracy'):.6f}")
    print(f"✓ Regime: {regime_guidance.get('tentative_regime')}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
