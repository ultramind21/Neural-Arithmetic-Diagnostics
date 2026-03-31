"""
================================================================================
PROJECT 4 PHASE-30 LSTM BASELINE VALIDATION RUNNER
================================================================================

PURPOSE:
  Run repeated Phase-30 LSTM baseline evaluations under Project 4 and aggregate
  them into a single validation artifact suitable for stability checking.

ROLE:
  This script:
    - reuses the trained LSTM checkpoint
    - runs the aligned baseline evaluation multiple times with different seeds
    - collects the resulting artifacts
    - saves a merged validation JSON
    - prepares the input expected by validate_run_stability.py

IMPORTANT:
  This file does NOT itself decide scientific validity.
  It prepares repeated-run evidence for validation review.

================================================================================
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List


# ============================================================================
# PATHS
# ============================================================================
PROJECT_4_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PROJECT_4_ROOT.parents[1]

BASELINE_EVAL_MODULE = "project_4.baselines.project_4_phase30_lstm_baseline_eval"

RESULTS_DIR = PROJECT_4_ROOT / "results" / "baseline_runs"
VALIDATION_OUTPUT = RESULTS_DIR / "phase30_lstm_validation_runs.json"

PYTHON = sys.executable


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


# ============================================================================
# MAIN
# ============================================================================

def parse_args():
    parser = argparse.ArgumentParser(description="Project 4 Phase-30 LSTM baseline validation runner")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--base-seed", type=int, default=42)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--train-length", type=int, default=5)
    parser.add_argument("--adversarial-length", type=int, default=5)
    parser.add_argument("--num-samples-id", type=int, default=128)
    parser.add_argument("--num-samples-adv", type=int, default=32)
    parser.add_argument("--num-samples-extra", type=int, default=128)
    parser.add_argument("--lengths", type=int, nargs="+", default=[5])
    parser.add_argument("--corruption-levels", type=float, nargs="+", default=[0.0, 0.1, 0.2, 0.5])
    return parser.parse_args()


def main():
    args = parse_args()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print_header("PROJECT 4 PHASE-30 LSTM BASELINE VALIDATION RUNNER")

    all_runs: List[Dict[str, Any]] = []
    run_artifact_paths: List[str] = []

    for run_idx in range(args.runs):
        run_seed = args.base_seed + run_idx
        model_name = f"phase30_lstm_baseline_run{run_idx}"

        import sys
        sys.argv = [
            "project_4_phase30_lstm_baseline_eval",
            "--model-name", model_name,
            "--checkpoint", args.checkpoint,
            "--device", args.device,
            "--train-length", str(args.train_length),
            "--adversarial-length", str(args.adversarial_length),
            "--num-samples-id", str(args.num_samples_id),
            "--num-samples-adv", str(args.num_samples_adv),
            "--num-samples-extra", str(args.num_samples_extra),
            "--seed", str(run_seed),
        ]

        for L in args.lengths:
            sys.argv.extend(["--lengths", str(L)])

        for p in args.corruption_levels:
            sys.argv.extend(["--corruption-levels", str(p)])

        print(f"\nRunning validation repeat {run_idx + 1}/{args.runs}")
        print("Model name:", model_name)
        print("Seed:", run_seed)

        try:
            from project_4.baselines.project_4_phase30_lstm_baseline_eval import main as baseline_main
            baseline_main()
        except Exception as e:
            print(f"Error running validation repeat {run_idx}:")
            print(str(e))
            raise RuntimeError(f"Validation run {run_idx} failed") from e

        artifact_path = RESULTS_DIR / f"{model_name}_artifact.json"
        if not artifact_path.exists():
            raise FileNotFoundError(f"Expected artifact not found: {artifact_path}")

        artifact = load_json(artifact_path)

        scorecard = artifact.get("scorecard", {})
        raw_metrics = artifact.get("raw_metrics", {})

        run_record = {
            "run_index": run_idx,
            "run_seed": run_seed,
            "artifact_path": str(artifact_path),
            "in_distribution_accuracy": scorecard.get("in_distribution_accuracy"),
            "pattern_breakdown": scorecard.get("pattern_breakdown", {}),
            "accuracy_by_length": {
                int(k): v.get("exact_match", v) if isinstance(v, dict) else v
                for k, v in raw_metrics.get("lengths", {}).items()
            },
            "accuracy_with_rounding": raw_metrics.get("rounding", {}).get("with_rounding"),
            "accuracy_without_rounding": raw_metrics.get("rounding", {}).get("without_rounding"),
            "accuracy_by_corruption": raw_metrics.get("carry_corruption", {}).get("accuracies", {}),
            "notes": artifact.get("qualification_notes", []),
        }

        all_runs.append(run_record)
        run_artifact_paths.append(str(artifact_path))

    validation_payload = {
        "status": "project4_phase30_lstm_validation_runs",
        "checkpoint": args.checkpoint,
        "run_count": args.runs,
        "base_seed": args.base_seed,
        "device": args.device,
        "run_artifact_paths": run_artifact_paths,
        "run_metrics": all_runs,
        "notes": [
            "This file is intended for validate_run_stability.py",
            "It aggregates repeated aligned Phase 30 LSTM Project 4 baseline runs",
            "Final scientific interpretation still requires validation review",
        ],
    }

    save_json(VALIDATION_OUTPUT, validation_payload)

    print_header("VALIDATION PAYLOAD SAVED")
    print(f"Saved to: {VALIDATION_OUTPUT}")
    print("\nNext step:")
    print("  Run validate_run_stability.py on this JSON payload")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
