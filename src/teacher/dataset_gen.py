"""
dataset_gen.py - Generate training data from teacher traces.
"""

import random
import torch
from torch.utils.data import Dataset
from typing import List, Tuple

from .teacher_add import teacher_trace
from ..env.soroban_env import SorobanEnv
from ..env.encode import encode_obs
from ..utils.config import SorobanConfig, DEFAULT_CONFIG


class SorobanBCDataset(Dataset):
    """
    Behavioral Cloning dataset.
    Each example = one decision point: (obs, correct_action)
    """

    def __init__(self, config: SorobanConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.observations: List[torch.Tensor] = []
        self.actions: List[int] = []

    def add_problem(self, a: int, b: int):
        """Add all steps from one teacher trace."""
        actions = teacher_trace(a, b, self.config)
        env = SorobanEnv(self.config)
        env.reset(a, b)

        for act in actions:
            obs = encode_obs(env)
            self.observations.append(obs)
            self.actions.append(act)

            # Advance env (except DONE terminates)
            _, _, done, _ = env.step(act)
            if done:
                break

    def add_problems(self, problems: List[Tuple[int, int]]):
        """Add multiple problems."""
        for a, b in problems:
            try:
                self.add_problem(a, b)
            except Exception as e:
                pass  # Skip problematic cases silently

    def __len__(self):
        return len(self.observations)

    def __getitem__(self, idx):
        return {
            "obs": self.observations[idx],
            "action": torch.tensor(self.actions[idx], dtype=torch.long),
        }


def generate_problems(
    n: int,
    max_digits: int = 6,
    min_digits: int = 1,
) -> List[Tuple[int, int]]:
    """Generate random addition problems."""
    problems = []
    for _ in range(n):
        nd = random.randint(min_digits, max_digits)
        a = random.randint(0, 10**nd - 1)
        b = random.randint(0, 10**nd - 1)
        problems.append((a, b))
    return problems


def generate_curriculum(
    per_stage: int = 5000,
    config: SorobanConfig = None,
) -> List[Tuple[int, int]]:
    """
    Curriculum: easy → hard problems.
    
    Stage 1: 1-digit
    Stage 2: 2-digit (no carry)
    Stage 3: 2-digit (with carry)
    Stage 4: 3-4 digit
    Stage 5: 5-6 digit
    Stage 6: carry-heavy (lots of 9s)
    """
    problems = []

    # Stage 1: 1-digit
    for _ in range(per_stage):
        problems.append((random.randint(0, 9), random.randint(0, 9)))

    # Stage 2: 2-digit no carry
    count = 0
    while count < per_stage:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        has_carry = any(
            (int(da) + int(db)) >= 10
            for da, db in zip(str(a).zfill(2), str(b).zfill(2))
        )
        if not has_carry:
            problems.append((a, b))
            count += 1

    # Stage 3: 2-digit general
    for _ in range(per_stage):
        problems.append((random.randint(10, 99), random.randint(10, 99)))

    # Stage 4: 3-4 digit
    for _ in range(per_stage):
        nd = random.choice([3, 4])
        problems.append((
            random.randint(0, 10**nd - 1),
            random.randint(0, 10**nd - 1),
        ))

    # Stage 5: 5-6 digit
    for _ in range(per_stage):
        nd = random.choice([5, 6])
        problems.append((
            random.randint(0, 10**nd - 1),
            random.randint(0, 10**nd - 1),
        ))

    # Stage 6: carry-heavy
    for _ in range(per_stage):
        # Numbers with lots of 9s
        nd = random.randint(2, 6)
        a = int('9' * nd) - random.randint(0, 10**(nd-1))
        b = random.randint(1, 10**nd)
        problems.append((max(0, a), b))

    random.shuffle(problems)
    return problems
