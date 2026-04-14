"""
encode.py - Encode observations for neural network.
"""

import torch
import numpy as np
from typing import List, Tuple

from .soroban_env import SorobanEnv


def encode_obs(env: SorobanEnv) -> torch.Tensor:
    """
    Encode env state as a tensor of shape (num_columns, F),
    where F is defined by the environment's _obs() implementation.

    This function intentionally does not assume a fixed feature count.
    """
    obs = env._obs()
    assert obs.ndim == 2, f"Expected 2D obs (W,F); got shape={obs.shape}"
    return torch.from_numpy(obs)


def encode_obs_from_array(obs: np.ndarray) -> torch.Tensor:
    """Convert numpy obs to tensor."""
    return torch.from_numpy(obs)
