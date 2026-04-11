"""
================================================================================
PROJECT 4 PHASE-30 MLP EVAL-PATH AUDIT
================================================================================

PURPOSE:
  Audit the evaluation path assumptions currently used in
  project_4_phase30_mlp_baseline_eval.py against the actual logic exposed by
  src/train/phase_30_multidigit_learning.py.

ROLE:
  This script checks:
    1. What MLPSequenceArithmetic.forward() actually returns
    2. What shape/type the outputs have
    3. How evaluate_model() in Phase 30 expects predictions/targets
    4. Whether the current Project 4 reconstruction path is aligned or misaligned
    5. Whether the very low observed Project 4 baseline result is likely due to
       evaluation-path mismatch rather than genuine model weakness

IMPORTANT:
  This is an audit of evaluation semantics, not a new baseline result.

================================================================================
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from typing import Any, Dict

import numpy as np
import torch


# ============================================================================
# PATHS
# ============================================================================
PROJECT_4_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PROJECT_4_ROOT.parents[0]
TARGET_FILE = PROJECT_ROOT / "src" / "train" / "phase_30_multidigit_learning.py"
CHECKPOINT_PATH = PROJECT_4_ROOT / "checkpoints" / "phase30_mlp_project4_ready.pt"


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def load_phase30_module():
    if not TARGET_FILE.exists():
        raise FileNotFoundError(f"Target file not found: {TARGET_FILE}")

    spec = importlib.util.spec_from_file_location("phase_30_multidigit_learning", str(TARGET_FILE))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for: {TARGET_FILE}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def preview_tensor(name: str, x: torch.Tensor):
    print(f"{name}:")
    print(f"  shape = {tuple(x.shape)}")
    print(f"  dtype = {x.dtype}")
    print(f"  device = {x.device}")
    flat_preview = x.detach().cpu().reshape(-1)[:12].tolist()
    print(f"  preview = {flat_preview}")


def preview_obj(name: str, x: Any):
    print(f"{name}: type={type(x)}")
    if hasattr(x, "shape"):
        print(f"  shape={tuple(x.shape)}")
    if isinstance(x, (list, tuple)):
        print(f"  len={len(x)}")
    print(f"  repr={repr(x)[:200]}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 4 PHASE-30 MLP EVAL-PATH AUDIT")

    module = load_phase30_module()
    print("✓ Phase 30 module import successful")

    required = [
        "generate_multidigit_sequences",
        "pad_sequences",
        "sequences_to_tensors",
        "MLPSequenceArithmetic",
        "evaluate_model",
    ]
    for name in required:
        if not hasattr(module, name):
            raise AttributeError(f"Missing required object in phase_30 module: {name}")
    print("✓ Required objects found")

    print_header("1) FUNCTION SIGNATURES")

    print(f"MLPSequenceArithmetic: {module.MLPSequenceArithmetic}")
    print(f"evaluate_model signature: {inspect.signature(module.evaluate_model)}")

    # ------------------------------------------------------------------------
    # Build a trained model from saved checkpoint
    # ------------------------------------------------------------------------
    print_header("2) MODEL BUILD + CHECKPOINT LOAD")

    model = module.MLPSequenceArithmetic(max_length=5)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    if not CHECKPOINT_PATH.exists():
        raise FileNotFoundError(f"Checkpoint not found: {CHECKPOINT_PATH}")

    ckpt = torch.load(CHECKPOINT_PATH, map_location=device)
    if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
        model.load_state_dict(ckpt["model_state_dict"])
    elif isinstance(ckpt, dict):
        model.load_state_dict(ckpt)
    else:
        raise ValueError("Unsupported checkpoint format")

    model.eval()
    print(f"✓ Model loaded on device: {device}")

    # ------------------------------------------------------------------------
    # Generate a tiny sample through official data path
    # ------------------------------------------------------------------------
    print_header("3) OFFICIAL DATA-PATH SAMPLE")

    examples = module.generate_multidigit_sequences(lengths=[5], num_samples_per_length=2, seed=42)
    print(f"✓ Generated {len(examples)} raw examples")

    padded = module.pad_sequences(examples, max_length=5)
    print("✓ pad_sequences succeeded")
    preview_obj("padded", padded)

    tensors = module.sequences_to_tensors(padded)
    print("✓ sequences_to_tensors succeeded")
    preview_obj("tensors", tensors)

    if not isinstance(tensors, tuple):
        raise TypeError("sequences_to_tensors did not return tuple")

    print("\nTuple parts:")
    for i, part in enumerate(tensors):
        preview_obj(f"  part[{i}]", part)

    if len(tensors) != 5:
        raise ValueError(f"Expected 5 outputs from sequences_to_tensors, got {len(tensors)}")

    a, b, digit_true, carry_true, lengths = tensors
    a = a.to(device)
    b = b.to(device)
    digit_true = digit_true.to(device)
    carry_true = carry_true.to(device)

    # ------------------------------------------------------------------------
    # Inspect forward output
    # ------------------------------------------------------------------------
    print_header("4) FORWARD OUTPUT AUDIT")

    with torch.no_grad():
        output = model(a, b)

    preview_obj("raw model output", output)

    if not isinstance(output, tuple):
        print("⚠ Forward output is not tuple-like; Project 4 eval path assumption is likely broken")
        return

    if len(output) != 2:
        print(f"⚠ Forward output tuple len={len(output)} (expected 2 in current Project 4 path)")
        return

    digit_pred, carry_pred = output

    preview_tensor("digit_pred", digit_pred)
    preview_tensor("carry_pred", carry_pred)
    preview_tensor("digit_true", digit_true)
    preview_tensor("carry_true", carry_true)

    # ------------------------------------------------------------------------
    # Check shape compatibility with current Project 4 path
    # ------------------------------------------------------------------------
    print_header("5) SHAPE-COMPATIBILITY CHECK")

    print("Current Project 4 baseline path assumes:")
    print("  - digit_pred has class dimension suitable for argmax over digits")
    print("  - carry_pred has class dimension suitable for argmax over carry")
    print("  - exact-match can be computed from reconstructed digit sequence body")

    shape_ok = True

    if digit_pred.ndim < 2:
        shape_ok = False
        print("✗ digit_pred rank too small for expected class-based decoding")
    else:
        print("✓ digit_pred rank is at least 2")

    if carry_pred.ndim < 2:
        shape_ok = False
        print("✗ carry_pred rank too small for expected class-based decoding")
    else:
        print("✓ carry_pred rank is at least 2")

    # Compare trailing dimensions with truth
    print(f"digit_pred shape: {tuple(digit_pred.shape)}")
    print(f"carry_pred shape: {tuple(carry_pred.shape)}")
    print(f"digit_true shape: {tuple(digit_true.shape)}")
    print(f"carry_true shape: {tuple(carry_true.shape)}")

    # ------------------------------------------------------------------------
    # Audit evaluate_model source intent
    # ------------------------------------------------------------------------
    print_header("6) EVALUATE_MODEL SOURCE INTENT")

    eval_src = inspect.getsource(module.evaluate_model)
    print(eval_src[:4000])

    # ------------------------------------------------------------------------
    # Final judgment
    # ------------------------------------------------------------------------
    print_header("7) EVAL-PATH AUDIT DECISION")

    print("This audit should answer one question:")
    print("  Does the current Project 4 MLP evaluation path reflect the real")
    print("  decoding/evaluation semantics of phase_30_multidigit_learning.py ?")
    print()

    if shape_ok:
        print("⚠ PARTIAL")
        print()
        print("Finding:")
        print("  Basic output structure is compatible enough for further inspection,")
        print("  but source-intent review is still required to confirm whether the")
        print("  current Project 4 evaluation reconstruction is semantically valid.")
    else:
        print("✗ FAIL")
        print()
        print("Finding:")
        print("  The current Project 4 baseline evaluation path is not aligned with")
        print("  the observed output structure of the Phase 30 MLP.")
        print()
        print("Interpretation:")
        print("  The previously observed low baseline accuracy is likely not yet")
        print("  scientifically interpretable as a real model result.")
        print("  The evaluation path must be revised before baseline reporting continues.")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
