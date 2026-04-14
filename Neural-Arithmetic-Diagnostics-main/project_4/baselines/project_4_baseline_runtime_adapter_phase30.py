"""
================================================================================
PROJECT 4 BASELINE RUNTIME ADAPTER: PHASE 30
================================================================================

PURPOSE:
  Provide a runtime adapter layer between Project 4 diagnostic tooling and
  the Phase 30 multidigit learning source file.

TARGET:
  src/train/phase_30_multidigit_learning.py

ROLE:
  This module:
    - imports Phase 30 model classes
    - exposes a uniform adapter interface
    - allows Project 4 baseline tools to instantiate target models safely
    - keeps adapter assumptions explicit

IMPORTANT:
  This module does NOT by itself prove scientific validity of the wrapped model.
  It is a runtime bridge for Project 4 baseline execution.

SUPPORTED MODEL TYPES:
  - mlp
  - lstm
  - transformer

================================================================================
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Optional

import torch


# ============================================================================
# PATHS
# ============================================================================
PROJECT_4_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PROJECT_4_ROOT.parents[0]
TARGET_FILE = PROJECT_ROOT / "src" / "train" / "phase_30_multidigit_learning.py"


# ============================================================================
# DATA CLASS
# ============================================================================

@dataclass
class Phase30AdapterMetadata:
    source_file: str
    model_type: str
    device: str
    import_successful: bool
    adapter_scope: str
    notes: list


# ============================================================================
# HELPERS
# ============================================================================

def load_phase30_module():
    if not TARGET_FILE.exists():
        raise FileNotFoundError(f"Phase 30 source file not found: {TARGET_FILE}")

    spec = importlib.util.spec_from_file_location("phase_30_multidigit_learning", str(TARGET_FILE))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for: {TARGET_FILE}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ============================================================================
# ADAPTER
# ============================================================================

class Phase30ModelAdapter:
    """
    Runtime adapter for one of the model classes defined in phase_30_multidigit_learning.py

    This adapter currently provides:
      - model construction
      - checkpoint loading
      - metadata exposure

    It does NOT yet define a complete Project 4 evaluation path by itself.
    """

    def __init__(
        self,
        model_type: str,
        checkpoint_path: Optional[str] = None,
        device: Optional[torch.device] = None,
    ):
        self.model_type = model_type.lower().strip()
        self.checkpoint_path = checkpoint_path
        self.device = device or torch.device("cpu")

        self.module = load_phase30_module()
        self.model = self._build_model()
        self.model = self.model.to(self.device)

        if self.checkpoint_path:
            self._load_checkpoint(self.checkpoint_path)

        self.model.eval()

    def _build_model(self):
        max_length = 5  # Default training length from Phase 30
        
        if self.model_type == "mlp":
            if not hasattr(self.module, "MLPSequenceArithmetic"):
                raise AttributeError("Phase 30 module missing MLPSequenceArithmetic")
            return self.module.MLPSequenceArithmetic(max_length=max_length)

        if self.model_type == "lstm":
            if not hasattr(self.module, "LSTMSequenceArithmetic"):
                raise AttributeError("Phase 30 module missing LSTMSequenceArithmetic")
            return self.module.LSTMSequenceArithmetic(max_length=max_length)

        if self.model_type == "transformer":
            if not hasattr(self.module, "TransformerSequenceArithmetic"):
                raise AttributeError("Phase 30 module missing TransformerSequenceArithmetic")
            return self.module.TransformerSequenceArithmetic(max_length=max_length)

        raise ValueError(
            f"Unsupported model_type={self.model_type}. "
            f"Expected one of: mlp, lstm, transformer"
        )

    def _load_checkpoint(self, checkpoint_path: str):
        ckpt = torch.load(checkpoint_path, map_location=self.device)

        if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
            self.model.load_state_dict(ckpt["model_state_dict"])
        elif isinstance(ckpt, dict):
            # direct state_dict format
            self.model.load_state_dict(ckpt)
        else:
            raise ValueError("Unsupported checkpoint format")

    def metadata(self) -> Dict[str, Any]:
        meta = Phase30AdapterMetadata(
            source_file=str(TARGET_FILE),
            model_type=self.model_type,
            device=str(self.device),
            import_successful=True,
            adapter_scope="runtime_construction_only",
            notes=[
                "This adapter wraps phase_30_multidigit_learning.py model classes.",
                "It supports model instantiation and optional checkpoint loading.",
                "It does not by itself establish a complete Project 4 evaluation path.",
                "Project 4 runtime/evaluation logic must still be defined at baseline-runner level.",
            ],
        )
        return asdict(meta)

    def get_model(self):
        return self.model

    def get_module(self):
        return self.module


# ============================================================================
# PUBLIC API
# ============================================================================

def build_phase30_adapter(
    model_type: str,
    checkpoint_path: Optional[str] = None,
    device: Optional[torch.device] = None,
) -> Phase30ModelAdapter:
    return Phase30ModelAdapter(
        model_type=model_type,
        checkpoint_path=checkpoint_path,
        device=device,
    )


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PROJECT 4 PHASE-30 RUNTIME ADAPTER DEMO")
    print("=" * 80)

    for model_type in ["mlp", "lstm", "transformer"]:
        try:
            adapter = build_phase30_adapter(
                model_type=model_type,
                checkpoint_path=None,
                device=torch.device("cpu"),
            )
            print(f"\n✓ Built adapter for: {model_type}")
            print(f"  model class: {adapter.get_model().__class__.__name__}")
            print(f"  metadata: {adapter.metadata()}")
        except Exception as e:
            print(f"\n✗ Failed to build adapter for: {model_type}")
            print(f"  error: {e}")
