"""
================================================================================
PROBE_PROJECT4_CHECKPOINTS.PY
================================================================================

PURPOSE:
  Verify that Project 4 baseline checkpoints exist, are readable, and can be
  loaded successfully.

SCOPE:
  - Check MLP, LSTM, Transformer checkpoints
  - Verify file existence and size
  - Attempt torch.load() 
  - Report state_dict structure

================================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Any

# Add paths before any imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "project_12" / "scripts"))

try:
    from p12_runlib import find_repo_root
except ImportError:
    # Fallback if import fails
    def find_repo_root() -> Path:
        current = Path(__file__).resolve().parents[2]
        for parent in [current] + list(current.parents):
            if (parent / ".git").exists():
                if parent.name == "neural_arithmetic_diagnostics":
                    return parent
                if (parent / "neural_arithmetic_diagnostics").exists():
                    return parent / "neural_arithmetic_diagnostics"
                return parent
            if parent.name == "neural_arithmetic_diagnostics":
                return parent
        raise ValueError("Could not find repository root")

import torch


def probe_checkpoint(ckpt_path: Path) -> Dict[str, Any]:
    """Probe a single checkpoint for readability and structure."""
    result = {
        "path": str(ckpt_path),
        "exists": ckpt_path.exists(),
        "size_bytes": 0,
        "torch_load_success": False,
        "error": None,
        "state_dict_keys": 0,
        "param_norm_l2": 0.0,
    }

    if not ckpt_path.exists():
        result["error"] = "File not found"
        return result

    # Get size
    try:
        result["size_bytes"] = ckpt_path.stat().st_size
    except Exception as e:
        result["error"] = f"Could not stat file: {e}"
        return result

    # Try to load
    try:
        ckpt_obj = torch.load(ckpt_path, map_location="cpu")
        result["torch_load_success"] = True

        # If it's a state_dict directly
        if isinstance(ckpt_obj, dict) and all(isinstance(k, str) for k in ckpt_obj.keys()):
            result["state_dict_keys"] = len(ckpt_obj)

            # Estimate param norm
            norms = []
            for key, val in ckpt_obj.items():
                if isinstance(val, torch.Tensor):
                    norms.append(val.norm().item())
            if norms:
                result["param_norm_l2"] = sum(n**2 for n in norms) ** 0.5
        else:
            result["state_dict_keys"] = 0
            result["torch_load_success"] = True  # Loaded but structure unclear
            result["error"] = f"Checkpoint structure not recognized (type={type(ckpt_obj).__name__})"

    except Exception as e:
        result["torch_load_success"] = False
        result["error"] = f"torch.load failed: {type(e).__name__}: {e}"

    return result


def main():
    """Main probe."""
    print("\n" + "=" * 80)
    print("PROBE PROJECT 4 CHECKPOINTS")
    print("=" * 80)

    try:
        ROOT = find_repo_root()
        print(f"✓ Repository root: {ROOT}")
    except ValueError as e:
        print(f"✗ Could not find repo root: {e}")
        return 1

    PROJECT_4_ROOT = ROOT / "project_4"
    CHECKPOINTS_DIR = PROJECT_4_ROOT / "checkpoints"

    # Standard checkpoint paths (correct names from project_4/checkpoints/)
    checkpoints = {
        "mlp": CHECKPOINTS_DIR / "phase30_mlp_project4_ready.pt",
        "lstm": CHECKPOINTS_DIR / "phase30_lstm_project4_ready.pt",
        "transformer": CHECKPOINTS_DIR / "phase30_transformer_project4_ready.pt",
    }

    print(f"\nChecking {len(checkpoints)} checkpoint(s)...\n")

    all_good = True
    for arch, ckpt_path in checkpoints.items():
        print(f"[{arch.upper()}]")
        result = probe_checkpoint(ckpt_path)

        print(f"  Path: {result['path']}")
        print(f"  Exists: {'✅' if result['exists'] else '❌'}")

        if result["exists"]:
            print(f"  Size: {result['size_bytes']:,} bytes")
            print(f"  Torch load: {'✅' if result['torch_load_success'] else '❌'}")
            if result["state_dict_keys"] > 0:
                print(f"  State dict keys: {result['state_dict_keys']}")
                print(f"  Param norm (L2): {result['param_norm_l2']:.6f}")
            if result["error"]:
                print(f"  Error: {result['error']}")
                all_good = False
        else:
            print(f"  Error: {result['error']}")
            all_good = False

        print()

    print("=" * 80)
    if all_good:
        print("✅ All checkpoints OK")
        print("=" * 80 + "\n")
        return 0
    else:
        print("❌ Some checkpoints have issues")
        print("=" * 80 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
