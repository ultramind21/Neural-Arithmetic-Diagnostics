"""
================================================================================
PROJECT 4 PHASE-30 TRAINING CHECKPOINT PREP
================================================================================

PURPOSE:
  Prepare a trained MLP checkpoint from phase_30_multidigit_learning.py for use
  in Project 4 baseline evaluation.

ROLE:
  This script isolates the checkpoint-preparation step so that:
    - baseline evaluation is not run on untrained weights
    - Project 4 baseline artifacts are built from an actually trained model
    - the training-to-evaluation transition is explicit and reproducible

IMPORTANT:
  This script currently targets:
    - MLPSequenceArithmetic only

OUTPUT:
  A saved checkpoint file for later use by:
    project_4_phase30_mlp_baseline_eval.py

================================================================================
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import torch


# ============================================================================
# PATHS & DEVICE
# ============================================================================
PROJECT_4_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PROJECT_4_ROOT.parents[0]

TARGET_FILE = PROJECT_ROOT / "src" / "train" / "phase_30_multidigit_learning.py"
CHECKPOINT_DIR = PROJECT_4_ROOT / "checkpoints"
CHECKPOINT_PATH = CHECKPOINT_DIR / "phase30_mlp_project4_ready.pt"

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# ============================================================================
# HELPERS
# ============================================================================

def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def load_phase30_module():
    if not TARGET_FILE.exists():
        raise FileNotFoundError(f"Phase 30 source file not found: {TARGET_FILE}")

    spec = importlib.util.spec_from_file_location("phase_30_multidigit_learning", str(TARGET_FILE))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for {TARGET_FILE}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ============================================================================
# MAIN
# ============================================================================

def main():
    print_header("PROJECT 4 PHASE-30 TRAINING CHECKPOINT PREP")

    module = load_phase30_module()

    required = [
        "generate_multidigit_sequences",
        "pad_sequences",
        "sequences_to_tensors",
        "MLPSequenceArithmetic",
        "train_model",
    ]

    for name in required:
        if not hasattr(module, name):
            raise AttributeError(f"Phase 30 module missing required object: {name}")

    print("✓ Phase 30 module imported successfully")
    print("✓ Required training objects found")

    # ------------------------------------------------------------------------
    # 1) Generate training data
    # ------------------------------------------------------------------------
    print_header("1) GENERATE TRAINING DATA")

    train_sequences = module.generate_multidigit_sequences(
        lengths=[2, 3, 4, 5],
        num_samples_per_length=200,
        seed=42,
    )
    print(f"✓ Generated {len(train_sequences)} training sequences")

    # ------------------------------------------------------------------------
    # 2) Pad sequences to uniform length
    # ------------------------------------------------------------------------
    print_header("2) PAD TRAINING DATA")

    max_length = max(len(a) for a, _, _, _ in train_sequences)
    print(f"✓ max_length from training data: {max_length}")

    padded_sequences = module.pad_sequences(train_sequences, max_length)
    print(f"✓ Padded {len(padded_sequences)} sequences to length {max_length}")

    # ------------------------------------------------------------------------
    # 3) Convert to tensors
    # ------------------------------------------------------------------------
    print_header("3) CONVERT TRAINING DATA TO TENSORS")

    a, b, digit_true, carry_true, lengths = module.sequences_to_tensors(padded_sequences, max_length=max_length)

    # Move to device
    a = a.to(DEVICE)
    b = b.to(DEVICE)
    digit_true = digit_true.to(DEVICE)
    carry_true = carry_true.to(DEVICE)
    lengths = lengths.to(DEVICE)

    print(f"✓ Converted to tensors and moved to device: {DEVICE}")

    print(f"  a shape:          {tuple(a.shape)}")
    print(f"  b shape:          {tuple(b.shape)}")
    print(f"  digit_true shape: {tuple(digit_true.shape)}")
    print(f"  carry_true shape: {tuple(carry_true.shape)}")
    print(f"  lengths shape:    {tuple(lengths.shape)}")

    # ------------------------------------------------------------------------
    # 4) Build model
    # ------------------------------------------------------------------------
    print_header("4) BUILD MLP MODEL")

    print(f"✓ Building model with max_length={max_length}")

    model = module.MLPSequenceArithmetic(max_length=max_length)
    model = model.to(DEVICE)
    print(f"✓ Built model: {model.__class__.__name__} on device {DEVICE}")

    # ------------------------------------------------------------------------
    # 5) Build training loader
    # ------------------------------------------------------------------------
    print_header("5) BUILD TRAIN LOADER")

    # train_model() expects only 4 values: a, b, digit_true, carry_true
    dataset = torch.utils.data.TensorDataset(a, b, digit_true, carry_true)
    train_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

    print(f"✓ DataLoader built with {len(dataset)} samples")

    # ------------------------------------------------------------------------
    # 6) Train model
    # ------------------------------------------------------------------------
    print_header("6) TRAIN MODEL")

    module.train_model(model, train_loader, epochs=30, lr=0.001)
    print("✓ Training complete")

    # ------------------------------------------------------------------------
    # 7) Save checkpoint
    # ------------------------------------------------------------------------
    print_header("7) SAVE CHECKPOINT")

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "model_type": "MLPSequenceArithmetic",
            "max_length": max_length,
            "source_file": str(TARGET_FILE),
            "project4_role": "phase30_mlp_baseline_checkpoint",
        },
        CHECKPOINT_PATH,
    )

    print(f"✓ Saved checkpoint to: {CHECKPOINT_PATH}")

    print("\n" + "=" * 80)
    print("CHECKPOINT PREP COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
