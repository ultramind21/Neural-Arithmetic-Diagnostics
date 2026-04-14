#!/usr/bin/env python3
"""
Phase 2 Transformer Smoke Baseline — Tiny Policy Network for Soroban Addition.

Trains a minimal Transformer on (observation, action) pairs from the Soroban environment.
Outputs artifact.json (metrics + config) and report.md to project_12/results/phase2_transformer_smoke/.
"""

import argparse
import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

# Add repo root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.env.soroban_env import SorobanEnv
from src.teacher.teacher_add import teacher_trace
from src.utils.config import DEFAULT_CONFIG


class TinyTransformer(nn.Module):
    """Minimal Transformer policy for Soroban action prediction."""

    def __init__(self, obs_size, action_size, embed_dim=32, num_heads=2, num_layers=1):
        super().__init__()
        self.embed_dim = embed_dim
        self.obs_size = obs_size
        self.action_size = action_size

        # Embedding for flattened observations
        self.obs_embed = nn.Linear(obs_size, embed_dim)

        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=num_heads, dim_feedforward=64, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        # Action output head
        self.action_head = nn.Linear(embed_dim, action_size)

    def forward(self, obs):
        """obs: (batch, seq_len, obs_feat) -> action logits: (batch, action_size)
        Flattened version for simpler learning.
        """
        batch_size = obs.shape[0]
        obs_flat = obs.reshape(batch_size, -1)  # (batch, seq_len * obs_feat)
        x = self.obs_embed(obs_flat)  # (batch, embed_dim)
        x = x.unsqueeze(1)  # (batch, 1, embed_dim)
        x = self.transformer(x)  # (batch, 1, embed_dim)
        x = x.squeeze(1)  # (batch, embed_dim)
        logits = self.action_head(x)  # (batch, action_size)
        return logits


def generate_dataset(seed=0, train_size=2000, eval_size=500, problem_mode="iid"):
    """Generate (obs, action) pairs from teacher traces.
    
    problem_mode:
      - 'iid': uniform random (a, b)
      - 'no_carry': digit-wise sums always < 10
      - 'carry_heavy': digit-wise sums always >= 10
    """
    np.random.seed(seed)
    random.seed(seed)

    config = DEFAULT_CONFIG
    env = SorobanEnv(config)
    W = config.num_columns

    dataset = []
    num_pairs = 0
    while num_pairs < train_size + eval_size:
        # Generate (a, b) based on problem_mode
        if problem_mode == "no_carry":
            # Each digit of a and b sums to < 10
            a_digits = [np.random.randint(0, 5) for _ in range(W)]
            b_digits = [np.random.randint(0, min(5, 9 - a_digits[i])) for i in range(W)]
            num_a = sum(a_digits[i] * (10 ** i) for i in range(W))
            num_b = sum(b_digits[i] * (10 ** i) for i in range(W))
        elif problem_mode == "carry_heavy":
            # Fewer digits (2-3), each digit sum >= 10 to force carries
            num_digits = np.random.randint(2, 4)
            a_digits = [0] * W
            b_digits = [0] * W
            for i in range(num_digits):
                a_dig = np.random.randint(5, 10)
                b_dig = np.random.randint(5, 10)
                a_digits[i] = a_dig
                b_digits[i] = b_dig
            num_a = sum(a_digits[i] * (10 ** i) for i in range(W))
            num_b = sum(b_digits[i] * (10 ** i) for i in range(W))
        else:  # iid (default)
            num_a = np.random.randint(1, 100)
            num_b = np.random.randint(1, 100)
        
        # Get action sequence from teacher
        actions = teacher_trace(num_a, num_b, config)

        # Replay in environment to get observations
        obs = env.reset(num_a, num_b)
        
        for action in actions:
            # Record (obs, action) pair
            dataset.append((obs.copy(), action))
            num_pairs += 1
            if num_pairs >= train_size + eval_size:
                break
            
            # Step environment
            obs, _, done, _ = env.step(action)
            if done:
                break

    # Convert to arrays
    obs_list = np.array([d[0] for d in dataset[:train_size + eval_size]])
    action_list = np.array([d[1] for d in dataset[:train_size + eval_size]])

    # Split
    train_obs, train_actions = obs_list[:train_size], action_list[:train_size]
    eval_obs, eval_actions = obs_list[train_size : train_size + eval_size], action_list[
        train_size : train_size + eval_size
    ]

    return (train_obs, train_actions), (eval_obs, eval_actions)


def train_epoch(model, train_obs, train_actions, optimizer, criterion, device):
    """Train for one epoch."""
    model.train()
    total_loss = 0
    batch_size = 64

    for i in range(0, len(train_obs), batch_size):
        obs_batch = torch.FloatTensor(train_obs[i : i + batch_size]).to(device)
        action_batch = torch.LongTensor(train_actions[i : i + batch_size]).to(device)

        # Flatten obs if needed
        if obs_batch.dim() > 2:
            obs_batch = obs_batch.reshape(obs_batch.shape[0], -1)

        optimizer.zero_grad()
        logits = model(obs_batch)  # (batch, action_size)
        loss = criterion(logits, action_batch)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / (len(train_obs) // batch_size + 1)


def eval_accuracy(model, eval_obs, eval_actions, device):
    """Compute action accuracy on eval set."""
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for i in range(len(eval_obs)):
            obs = torch.FloatTensor(eval_obs[i]).to(device)
            if obs.dim() > 1:
                obs = obs.reshape(-1)  # (obs_size,)
            obs = obs.unsqueeze(0)  # (1, obs_size)
            logits = model(obs)  # (1, action_size)
            pred = logits.argmax(dim=1).item()
            if pred == eval_actions[i]:
                correct += 1
            total += 1

    return correct / total if total > 0 else 0.0


def main():
    parser = argparse.ArgumentParser(description="Phase 2 Transformer Smoke Run")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--train-size", type=int, default=2000)
    parser.add_argument("--eval-size", type=int, default=500)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--out-dir", type=str, default="project_12/results/phase2_transformer_smoke")
    parser.add_argument("--problem-mode", type=str, default="iid", choices=["iid", "no_carry", "carry_heavy"])
    args = parser.parse_args()

    # Setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating dataset (train={args.train_size}, eval={args.eval_size}, mode={args.problem_mode})...")
    (train_obs, train_actions), (eval_obs, eval_actions) = generate_dataset(
        seed=args.seed, train_size=args.train_size, eval_size=args.eval_size, problem_mode=args.problem_mode
    )

    obs_size = train_obs[0].size if hasattr(train_obs[0], 'size') else train_obs[0].shape[0]
    if len(train_obs[0].shape) > 1:
        obs_size = int(np.prod(train_obs[0].shape))
    action_size = int(np.max(train_actions)) + 1

    print(f"Obs shape: {train_obs[0].shape}, Flattened size: {obs_size}, Action size: {action_size}")

    # Model
    model = TinyTransformer(obs_size=obs_size, action_size=action_size).to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    # Training
    print(f"Training for {args.epochs} epochs...")
    train_losses = []
    eval_accs = []

    for epoch in range(args.epochs):
        loss = train_epoch(model, train_obs, train_actions, optimizer, criterion, device)
        acc = eval_accuracy(model, eval_obs, eval_actions, device)
        train_losses.append(loss)
        eval_accs.append(acc)
        print(f"Epoch {epoch+1}/{args.epochs}: loss={loss:.4f}, eval_acc={acc:.4f}")

    # Save artifact
    artifact = {
        "git_commit": os.popen("git rev-parse HEAD").read().strip(),
        "seed": args.seed,
        "train_size": args.train_size,
        "eval_size": args.eval_size,
        "epochs": args.epochs,
        "problem_mode": args.problem_mode,
        "obs_size": obs_size,
        "action_size": action_size,
        "metrics": {
            "final_train_loss": float(train_losses[-1]) if train_losses else None,
            "final_eval_accuracy": float(eval_accs[-1]) if eval_accs else None,
            "all_train_losses": [float(x) for x in train_losses],
            "all_eval_accuracies": [float(x) for x in eval_accs],
        },
        "device": str(device),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    artifact_path = output_dir / "artifact.json"
    with open(artifact_path, "w") as f:
        json.dump(artifact, f, indent=2)
    print(f"Artifact saved to {artifact_path}")

    # Save report
    report_md = f"""# Phase 2 Transformer Smoke — Evaluation Report

## Configuration

| Key | Value |
|-----|-------|
| Seed | {args.seed} |
| Train Size | {args.train_size} |
| Eval Size | {args.eval_size} |
| Epochs | {args.epochs} |
| Obs Size | {obs_size} |
| Action Size | {action_size} |
| Device | {device} |

## Results

| Metric | Value |
|--------|-------|
| Final Train Loss | {train_losses[-1]:.6f} |
| Final Eval Accuracy | {eval_accs[-1]:.4f} |

## Training History

"""
    for i, (loss, acc) in enumerate(zip(train_losses, eval_accs)):
        report_md += f"- Epoch {i+1}: loss={loss:.6f}, eval_acc={acc:.4f}\n"

    report_md += f"\nGit Commit: `{artifact['git_commit']}`\n"
    report_md += f"Timestamp: {artifact['timestamp']}\n"

    report_path = output_dir / "report.md"
    with open(report_path, "w") as f:
        f.write(report_md)
    print(f"Report saved to {report_path}")

    print("Phase 2 smoke run complete!")


if __name__ == "__main__":
    main()
