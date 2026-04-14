"""
================================================================================
PROJECT 4 RUN STABILITY VALIDATOR
================================================================================

PURPOSE:
  Validation utility for repeated-run result stability in Project 4.

ROLE:
  This script evaluates whether multiple runs of the same experimental
  configuration are stable enough for use in Project 4 reporting.

IMPORTANT:
  This is a validation support tool.
  It does NOT replace scientific judgment.
  It provides:
    - summary statistics
    - spread analysis
    - consistency flags
    - stability verdict

SUPPORTED INPUT:
  JSON file containing repeated-run outputs for a single configuration.

EXPECTED JSON SHAPE (minimum):
{
  "run_metrics": [
    {
      "in_distribution_accuracy": ...,
      "pattern_breakdown": {...},
      "accuracy_by_length": {...},
      "accuracy_with_rounding": ...,
      "accuracy_without_rounding": ...,
      "accuracy_by_corruption": {...}
    },
    ...
  ]
}

================================================================================
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional
import statistics


# ============================================================================
# CONSTANTS
# ============================================================================

DEFAULT_MIN_RUNS = 3
DEFAULT_RANGE_THRESHOLD = 0.15
DEFAULT_STD_THRESHOLD = 0.08
FLOAT_TOL = 1e-8


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize(values: List[float]) -> Dict[str, Any]:
    if not values:
        return {"mean": None, "std": None, "min": None, "max": None, "range": None, "run_count": 0}

    if len(values) == 1:
        return {
            "mean": values[0],
            "std": 0.0,
            "min": values[0],
            "max": values[0],
            "range": 0.0,
            "run_count": 1,
        }

    vmin = min(values)
    vmax = max(values)
    return {
        "mean": statistics.mean(values),
        "std": statistics.stdev(values),
        "min": vmin,
        "max": vmax,
        "range": vmax - vmin,
        "run_count": len(values),
    }


def format_float(x: Optional[float]) -> str:
    if x is None:
        return "N/A"
    return f"{x:.6f}"


def collect_scalar(run_metrics: List[Dict[str, Any]], key: str) -> List[float]:
    vals = []
    for rm in run_metrics:
        v = rm.get(key)
        if isinstance(v, (int, float)):
            vals.append(float(v))
    return vals


def collect_nested_scalar(run_metrics: List[Dict[str, Any]], parent_key: str) -> Dict[str, List[float]]:
    bucket: Dict[str, List[float]] = {}
    for rm in run_metrics:
        d = rm.get(parent_key, {})
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, (int, float)):
                    bucket.setdefault(str(k), []).append(float(v))
    return bucket


def summarize_nested_scalars(run_metrics: List[Dict[str, Any]], parent_key: str) -> Dict[str, Dict[str, Any]]:
    grouped = collect_nested_scalar(run_metrics, parent_key)
    return {k: summarize(vs) for k, vs in grouped.items()}


def judge_summary(summary: Dict[str, Any], range_threshold: float, std_threshold: float) -> str:
    std = summary.get("std")
    rng = summary.get("range")

    if summary.get("run_count", 0) < DEFAULT_MIN_RUNS:
        return "insufficient_runs"

    if std is None or rng is None:
        return "unknown"

    if rng > range_threshold or std > std_threshold:
        return "unstable"

    return "stable"


# ============================================================================
# CORE VALIDATION
# ============================================================================

def validate_run_metrics(
    run_metrics: List[Dict[str, Any]],
    range_threshold: float,
    std_threshold: float,
    min_runs: int,
) -> Dict[str, Any]:
    results: Dict[str, Any] = {}

    scalar_keys = [
        "in_distribution_accuracy",
        "accuracy_with_rounding",
        "accuracy_without_rounding",
    ]

    scalar_summary = {}
    scalar_verdicts = {}

    for key in scalar_keys:
        vals = collect_scalar(run_metrics, key)
        summary = summarize(vals)
        scalar_summary[key] = summary
        scalar_verdicts[key] = judge_summary(summary, range_threshold, std_threshold)

    pattern_summary = summarize_nested_scalars(run_metrics, "pattern_breakdown")
    pattern_verdicts = {
        k: judge_summary(v, range_threshold, std_threshold)
        for k, v in pattern_summary.items()
    }

    length_summary = summarize_nested_scalars(run_metrics, "accuracy_by_length")
    length_verdicts = {
        k: judge_summary(v, range_threshold, std_threshold)
        for k, v in length_summary.items()
    }

    corruption_summary = summarize_nested_scalars(run_metrics, "accuracy_by_corruption")
    corruption_verdicts = {
        k: judge_summary(v, range_threshold, std_threshold)
        for k, v in corruption_summary.items()
    }

    # Overall verdict
    all_verdicts = (
        list(scalar_verdicts.values()) +
        list(pattern_verdicts.values()) +
        list(length_verdicts.values()) +
        list(corruption_verdicts.values())
    )

    if len(run_metrics) < min_runs:
        overall = "INSUFFICIENT_RUNS"
    elif any(v == "unstable" for v in all_verdicts):
        overall = "UNSTABLE"
    elif any(v == "insufficient_runs" for v in all_verdicts):
        overall = "PARTIAL"
    else:
        overall = "STABLE"

    results["run_count"] = len(run_metrics)
    results["thresholds"] = {
        "min_runs": min_runs,
        "range_threshold": range_threshold,
        "std_threshold": std_threshold,
    }
    results["scalars"] = scalar_summary
    results["scalar_verdicts"] = scalar_verdicts
    results["patterns"] = pattern_summary
    results["pattern_verdicts"] = pattern_verdicts
    results["lengths"] = length_summary
    results["length_verdicts"] = length_verdicts
    results["corruption"] = corruption_summary
    results["corruption_verdicts"] = corruption_verdicts
    results["overall_verdict"] = overall

    return results


# ============================================================================
# REPORTING
# ============================================================================

def print_summary_block(title: str, summaries: Dict[str, Dict[str, Any]], verdicts: Dict[str, str]):
    print_header(title)
    if not summaries:
        print("(none found)")
        return

    for key, summary in summaries.items():
        verdict = verdicts.get(key, "unknown")
        print(f"{key}:")
        print(f"  mean   = {format_float(summary.get('mean'))}")
        print(f"  std    = {format_float(summary.get('std'))}")
        print(f"  min    = {format_float(summary.get('min'))}")
        print(f"  max    = {format_float(summary.get('max'))}")
        print(f"  range  = {format_float(summary.get('range'))}")
        print(f"  runs   = {summary.get('run_count')}")
        print(f"  verdict= {verdict}")
        print()


# ============================================================================
# MAIN
# ============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Project 4 run stability validator")
    parser.add_argument("--input-json", type=str, required=True, help="Path to repeated-run artifact JSON")
    parser.add_argument("--range-threshold", type=float, default=DEFAULT_RANGE_THRESHOLD)
    parser.add_argument("--std-threshold", type=float, default=DEFAULT_STD_THRESHOLD)
    parser.add_argument("--min-runs", type=int, default=DEFAULT_MIN_RUNS)
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input_json)

    print_header("PROJECT 4 RUN STABILITY VALIDATOR")

    if not input_path.exists():
        raise FileNotFoundError(f"Input JSON not found: {input_path}")

    payload = load_json(input_path)
    run_metrics = payload.get("run_metrics", [])

    if not isinstance(run_metrics, list):
        raise ValueError("Input JSON field 'run_metrics' must be a list")

    result = validate_run_metrics(
        run_metrics=run_metrics,
        range_threshold=args.range_threshold,
        std_threshold=args.std_threshold,
        min_runs=args.min_runs,
    )

    print_header("OVERALL VALIDATION STATUS")
    print(f"Run count: {result['run_count']}")
    print(f"Overall verdict: {result['overall_verdict']}")
    print(f"Thresholds: {result['thresholds']}")

    print_summary_block("SCALAR METRICS", result["scalars"], result["scalar_verdicts"])
    print_summary_block("PATTERN METRICS", result["patterns"], result["pattern_verdicts"])
    print_summary_block("LENGTH METRICS", result["lengths"], result["length_verdicts"])
    print_summary_block("CARRY-CORRUPTION METRICS", result["corruption"], result["corruption_verdicts"])

    print_header("FINAL NOTE")
    print("This tool supports Project 4 validation discipline.")
    print("It does NOT by itself replace scientific interpretation or regime judgment.")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
