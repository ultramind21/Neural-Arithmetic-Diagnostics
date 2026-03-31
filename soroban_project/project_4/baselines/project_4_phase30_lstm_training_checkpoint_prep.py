"""
================================================================================
PROJECT 4 PHASE-30 LSTM TRAINING CHECKPOINT PREP
================================================================================

PURPOSE:
  Prepare a trained LSTM checkpoint from phase_30_multidigit_learning.py for use
  in Project 4 baseline evaluation.

ROLE:
  This script isolates the checkpoint-preparation step so that:
    - LSTM baseline evaluation is not run on untrained weights
    - Project 4 baseline artifacts are built from an actually trained model
    - the training-to-evaluation transition is explicit and reproducible

CURRENT SCOPE:
  - LSTMSequenceArithmetic only

OUTPUT:
  project_4/checkpoints/phase30_lstm_project4_ready.pt

================================================================================
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import torch


# ============================================================================
# PATHS
# ============================================================================
PROJECT_4_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[2]

TARGET_FILE = PROJECT_ROOT / "src" / "train" / "phase_30_multidigit_learning.py"
CHECKPOINT_DIR = PROJECT_4_ROOT / "checkpoints"
CHECKPOINT_PATH = CHECKPOINT_DIR / "phase30_lstm_project4_ready.pt"


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
    print_header("PROJECT 4 PHASE-30 LSTM TRAINING CHECKPOINT PREP")

    module = load_phase30_module()

    required = [
        "generate_multidigit_sequences",
        "pad_sequences",
        "sequences_to_tensors",
        "LSTMSequenceArithmetic",
        "train_model",
    ]

    for name in required:
        if not hasattr(module, name):
            raise AttributeError(f"Phase 30 module missing required object: {name}")

    print("✓ Phase 30 module imported successfully")
    print("✓ Required training objects found")

    device = module.DEVICE if hasattr(module, "DEVICE") else torch.device("cpu")
    print(f"Device: {device}")

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
    # 2) Pad training data
    # ------------------------------------------------------------------------
    print_header("2) PAD TRAINING DATA")

    max_length = max(len(x[0]) for x in train_sequences)
    padded_sequences = module.pad_sequences(train_sequences, max_length=max_length)

    print(f"✓ max_length from training data: {max_length}")
    print(f"✓ Padded {len(padded_sequences)} sequences to length {max_length}")

    # ------------------------------------------------------------------------
    # 3) Convert training data to tensors
    # ------------------------------------------------------------------------
    print_header("3) CONVERT TRAINING DATA TO TENSORS")

    converted = module.sequences_to_tensors(padded_sequences)

    if not isinstance(converted, tuple):
        raise TypeError("sequences_to_tensors did not return tuple as expected")

    if len(converted) != 5:
        raise ValueError(f"Expected 5 outputs from sequences_to_tensors, got {len(converted)}")

    a, b, digit_true, carry_true, lengths = converted

    a = a.to(device)
    b = b.to(device)
    digit_true = digit_true.to(device)
    carry_true = carry_true.to(device)
    lengths = lengths.to(device)

    print(f"✓ Converted to tensors and moved to device: {device}")
    print(f"  a shape:          {tuple(a.shape)}")
    print(f"  b shape:          {tuple(b.shape)}")
    print(f"  digit_true shape: {tuple(digit_true.shape)}")
    print(f"  carry_true shape: {tuple(carry_true.shape)}")
    print(f"  lengths shape:    {tuple(lengths.shape)}")

    # ------------------------------------------------------------------------
    # 4) Build LSTM model
    # ------------------------------------------------------------------------
    print_header("4) BUILD LSTM MODEL")

    print(f"✓ Building model with max_length={max_length}")
    model = module.LSTMSequenceArithmetic(max_length=max_length).to(device)
    print(f"✓ Built model: {model.__class__.__name__} on device {device}")

    # ------------------------------------------------------------------------
    # 5) Build train loader
    # ------------------------------------------------------------------------
    print_header("5) BUILD TRAIN LOADER")

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
            "model_type": "LSTMSequenceArithmetic",
            "max_length": max_length,
            "source_file": str(TARGET_FILE),
            "project4_role": "phase30_lstm_baseline_checkpoint",
        },
        CHECKPOINT_PATH,
    )

    print(f"✓ Saved checkpoint to: {CHECKPOINT_PATH}")

    print("\n" + "=" * 80)
    print("LSTM CHECKPOINT PREP COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
