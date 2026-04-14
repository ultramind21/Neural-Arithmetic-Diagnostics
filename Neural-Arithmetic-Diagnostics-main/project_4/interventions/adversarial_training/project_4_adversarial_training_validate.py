"""
================================================================================
PROJECT 4 ADVERSARIAL TRAINING VALIDATION RUNNER
================================================================================

PURPOSE:
  Run repeated Project 4 adversarial-training MVP executions and aggregate them
  into a validation payload suitable for validate_run_stability.py.

ROLE:
  This script:
    - reruns the bounded adversarial-training intervention
    - captures the produced artifacts
    - extracts run-level intervention metrics
    - saves a merged validation payload

IMPORTANT:
  This script does NOT decide scientific validity by itself.
  It prepares repeated-run evidence for stability checking.

================================================================================
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Dict, Any, List


# ============================================================================
# PATHS
# ============================================================================
PROJECT_4_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = PROJECT_4_ROOT.parent

INTERVENTION_FILE = PROJECT_4_ROOT / "interventions" / "adversarial_training" / "project_4_adversarial_training.py"
RESULTS_DIR = PROJECT_4_ROOT / "interventions" / "adversarial_training" / "results"
VALIDATION_OUTPUT = RESULTS_DIR / "project_4_adversarial_training_validation_runs.json"


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


def load_intervention_module():
    if not INTERVENTION_FILE.exists():
        raise FileNotFoundError(f"Intervention file not found: {INTERVENTION_FILE}")

    spec = importlib.util.spec_from_file_location(
        "project_4_adversarial_training",
        str(INTERVENTION_FILE)
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for {INTERVENTION_FILE}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 4 ADVERSARIAL TRAINING VALIDATION RUNNER")

    intervention_module = load_intervention_module()

    all_runs: List[Dict[str, Any]] = []

    for run_idx in range(3):
        print(f"\nRunning adversarial-training validation repeat {run_idx + 1}/3")

        try:
            intervention_module.main()
        except Exception as e:
            print(f"ERROR in adversarial-training run {run_idx}: {e}")
            raise RuntimeError(f"Adversarial-training run {run_idx} failed") from e

        artifact_path = RESULTS_DIR / "project_4_adversarial_training_artifact.json"
        if not artifact_path.exists():
            raise FileNotFoundError(f"Expected artifact not found: {artifact_path}")

        artifact = load_json(artifact_path)

        in_distribution = artifact.get("in_distribution", {})
        seen_results = artifact.get("seen_results", {})
        heldout_results = artifact.get("heldout_results", {})

        run_record = {
            "run_index": run_idx,
            "artifact_path": str(artifact_path),

            "in_distribution_accuracy": in_distribution.get("exact_match"),

            "pattern_breakdown": {
                "alternating_carry": seen_results.get("alternating_carry", {}).get("exact_match"),
                "full_propagation_chain": seen_results.get("full_propagation_chain", {}).get("exact_match"),
                "block_boundary_stress": heldout_results.get("block_boundary_stress", {}).get("exact_match"),
            },

            "accuracy_by_length": {},
            "accuracy_with_rounding": None,
            "accuracy_without_rounding": None,
            "accuracy_by_corruption": {},

            "notes": artifact.get("notes", []),
        }

        all_runs.append(run_record)
        print(f"✓ Run {run_idx + 1} complete")

    validation_payload = {
        "status": "project4_adversarial_training_validation_runs",
        "run_count": len(all_runs),
        "run_metrics": all_runs,
        "notes": [
            "This file is intended for validate_run_stability.py",
            "It aggregates repeated Project 4 adversarial-training MVP runs",
            "Strong intervention conclusions require validation review, not single-run interpretation alone",
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
