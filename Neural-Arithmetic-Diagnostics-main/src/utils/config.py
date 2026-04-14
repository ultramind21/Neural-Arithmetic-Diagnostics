"""
config.py - Central configuration

All magic numbers in one place.
Change here, affects everything.
"""

from dataclasses import dataclass


@dataclass
class SorobanConfig:
    # Board
    num_columns: int = 13        # W: Increased to 13 to handle overflow carry from 12d dense problems
    
    # Training
    train_max_digits: int = 6    # Train on up to 6-digit numbers
    test_max_digits: int = 8     # Test generalization to 8 digits
    
    # Environment
    max_steps: int = 250         # Training: allow student to explore; eval can be stricter
    step_penalty: float = -0.01  # Small penalty per step
    correct_reward: float = 1.0  # Reward for correct DONE
    wrong_penalty: float = -5.0  # Penalty for wrong DONE
    
    # Model
    hidden_dim: int = 128
    num_heads: int = 4
    num_layers: int = 3
    dropout: float = 0.1
    
    # Training hyperparams
    batch_size: int = 256
    learning_rate: float = 3e-4
    weight_decay: float = 0.01
    bc_epochs: int = 80
    dagger_rounds: int = 10
    dagger_episodes_per_round: int = 2000
    patience: int = 10
    
    # Data
    bc_problems_per_stage: int = 5000
    
    # Evaluation
    eval_problems: int = 1000
    
    # Derived
    @property
    def num_actions(self) -> int:
        return self.num_columns + 3  # GOTO_0..GOTO_(W-1) + ADD1 + ADD5 + DONE


DEFAULT_CONFIG = SorobanConfig()
