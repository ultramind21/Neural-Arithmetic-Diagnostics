"""
encode.py - Encode observations for neural network.
"""

import torch
import numpy as np
from typing import List, Tuple

from .soroban_env import SorobanEnv


def encode_obs(env: SorobanEnv) -> torch.Tensor:
    """
    Encode env state as tensor (num_columns, 4).
    Features per column: [upper, lower, is_cursor, b_digit]
    """
    obs = env._obs()  # numpy (W, 4)
    return torch.from_numpy(obs)


def encode_obs_from_array(obs: np.ndarray) -> torch.Tensor:
    """Convert numpy obs to tensor."""
    return torch.from_numpy(obs)
