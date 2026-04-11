"""
Project 12 minimal support library for manifest loading, metadata capture, and safety checks.
Zero experimental logic — only I/O and environment utilities.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def load_manifest(path: str) -> dict:
    """Load manifest JSON from disk."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256_file(p: Path) -> str:
    """Compute SHA256 of file."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def sha256_text(s: str) -> str:
    """Compute SHA256 of text."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def get_git_hash() -> str:
    """Get current git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).resolve().parents[2],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else "UNKNOWN"
    except Exception:
        return "UNKNOWN"


def utc_now_iso() -> str:
    """Return current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def get_env_info() -> dict:
    """Capture Python, PyTorch, platform, and CUDA info."""
    import sys
    try:
        import torch
        torch_version = torch.__version__
        cuda_available = torch.cuda.is_available()
    except ImportError:
        torch_version = "NOT_INSTALLED"
        cuda_available = False

    return {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "torch_version": torch_version,
        "cuda_available": cuda_available,
        "platform": platform.platform(),
    }


def ensure_output_dir_is_safe(output_dir: Path) -> None:
    """
    Verify that output_dir is:
    - Within project_12/results
    - NOT within project_11/results
    
    Raises ValueError if path is unsafe.
    """
    output_dir = output_dir.resolve()
    root = Path(__file__).resolve().parents[2]  # neural_arithmetic_diagnostics
    
    project_12_results = root / "project_12" / "results"
    project_11_results = root / "project_11" / "results"
    
    # Check if output_dir is under project_12/results
    try:
        output_dir.relative_to(project_12_results)
    except ValueError:
        raise ValueError(
            f"Output directory {output_dir} is NOT under project_12/results. "
            f"Expected base: {project_12_results}"
        )
    
    # Check if output_dir is under project_11/results (forbidden)
    try:
        output_dir.relative_to(project_11_results)
        raise ValueError(
            f"Output directory {output_dir} is under project_11/results. "
            f"This is forbidden. Use project_12/results instead."
        )
    except ValueError as e:
        if "is under project_11/results" in str(e):
            raise
        # If relative_to fails, it's safe (not under project_11)


def write_json(path: Path, obj: dict) -> None:
    """Write dict to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    """Write text to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def check_leakage(holdout_points: list, pool_points: list, tolerance: float = 1e-10) -> None:
    """
    Verify that holdout and pool are disjoint (no data leakage).
    
    Points are rounded to 'tolerance' precision for comparison.
    Raises AssertionError if any overlap detected.
    """
    def make_key(h: float, p: float) -> tuple:
        """Create hashable key for point."""
        decimals = 10
        return (round(h, decimals), round(p, decimals))
    
    holdout_keys = set(make_key(pt[0], pt[1]) for pt in holdout_points)
    pool_keys = set(make_key(pt[0], pt[1]) for pt in pool_points)
    
    overlap = holdout_keys & pool_keys
    if overlap:
        raise AssertionError(
            f"❌ Data leakage detected! {len(overlap)} points in both holdout and pool.\n"
            f"First overlap: {list(overlap)[0]}"
        )
    
    print(f"✅ Leakage check PASS: {len(holdout_keys)} holdout points ∩ {len(pool_keys)} pool points = ∅")


def build_p12_metadata(
    manifest_path: str,
    entrypoint: str,
    source_script_copied_from: str,
) -> dict:
    """
    Build P12 standard metadata dictionary for inclusion in artifacts.
    
    Parameters:
    - manifest_path: Path to the manifest JSON used for this run
    - entrypoint: Name of the entry point script (e.g. "run_p4_mlp_baseline_repro.py")
    - source_script_copied_from: Path to original Project 4 source script (e.g. "project_4/baselines/...")
    
    Returns dict with:
    - git_hash: Current git commit
    - timestamp_utc: ISO 8601 UTC timestamp
    - env: Python, PyTorch, platform, CUDA info
    - manifest_path (resolved)
    - manifest_sha256
    - entrypoint
    - source_script_copied_from
    """
    manifest_path_resolved = Path(manifest_path).resolve()
    manifest_sha256 = sha256_file(manifest_path_resolved)
    
    return {
        "git_hash": get_git_hash(),
        "timestamp_utc": utc_now_iso(),
        "env": get_env_info(),
        "manifest_path": str(manifest_path_resolved),
        "manifest_sha256": manifest_sha256,
        "entrypoint": entrypoint,
        "source_script_copied_from": source_script_copied_from,
    }
