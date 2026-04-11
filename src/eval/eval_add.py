"""
eval_add.py - Evaluation

Measures:
- accuracy (exact match)
- avg_steps
- p95_steps
- loop_rate (timeout)
- generalization to longer numbers
- ADD1 abuse detection
"""

import random
import torch
from typing import Dict, List, Tuple

from ..env.soroban_env import SorobanEnv
from ..env.encode import encode_obs
from ..env.action_space import action_add1, decode_action
from ..models.policy_net import SorobanPolicy
from ..utils.config import SorobanConfig, DEFAULT_CONFIG


def evaluate_model(
    model: SorobanPolicy,
    config: SorobanConfig = None,
    device: torch.device = None,
    verbose: bool = True,
    num_per_digit: int = 200,
) -> Dict:
    """
    Full evaluation across digit lengths.
    Returns dict: {num_digits: {accuracy, avg_steps, ...}}
    """
    if config is None:
        config = DEFAULT_CONFIG
    if device is None:
        device = torch.device("cpu")

    model.eval()
    results = {}

    W = config.num_columns
    add1_id = action_add1(W)

    for nd in range(1, config.test_max_digits + 1):
        correct = 0
        total = 0
        total_steps = 0
        loops = 0
        step_list = []
        add1_counts = []
        errors = []

        for _ in range(num_per_digit):
            a = random.randint(0, 10**nd - 1)
            b = random.randint(0, 10**nd - 1)

            if a + b >= 10**W:
                continue

            env = SorobanEnv(config)
            env.reset(a, b)
            total += 1

            episode_add1 = 0

            for step in range(config.max_steps):
                obs = encode_obs(env).unsqueeze(0).to(device)
                with torch.no_grad():
                    logits = model(obs)
                    action = logits.argmax(-1).item()

                if action == add1_id:
                    episode_add1 += 1

                _, _, done, info = env.step(action)

                if done:
                    if info.get("correct", False):
                        correct += 1
                        total_steps += step + 1
                        step_list.append(step + 1)
                        add1_counts.append(episode_add1)
                    elif info.get("timeout", False):
                        loops += 1
                    else:
                        errors.append({
                            "a": a, "b": b,
                            "expected": a + b,
                            "got": env.get_result(),
                        })
                    break

        accuracy = correct / max(total, 1)
        avg_steps = total_steps / max(correct, 1)
        p95_steps = sorted(step_list)[int(0.95 * len(step_list))] if step_list else 0
        avg_add1 = sum(add1_counts) / max(len(add1_counts), 1)
        loop_rate = loops / max(total, 1)

        ood = nd > config.train_max_digits
        tag = "✅" if accuracy >= 0.99 else "⚠️" if accuracy >= 0.8 else "❌"
        ood_str = " [OOD]" if ood else ""

        results[nd] = {
            "accuracy": accuracy,
            "correct": correct,
            "total": total,
            "avg_steps": avg_steps,
            "p95_steps": p95_steps,
            "avg_add1": avg_add1,
            "loop_rate": loop_rate,
            "errors": errors[:5],
        }

        if verbose:
            print(
                f"  {tag} {nd}-digit{ood_str}: "
                f"{accuracy:.1%} ({correct}/{total}) "
                f"steps={avg_steps:.1f} "
                f"p95={p95_steps} "
                f"add1/ep={avg_add1:.1f} "
                f"loops={loop_rate:.1%}"
            )
            if errors and nd <= config.train_max_digits:
                for e in errors[:3]:
                    print(f"      ❌ {e['a']}+{e['b']}={e['expected']} got {e['got']}")

    return results


if __name__ == "__main__":
    print("Evaluation requires a trained model. Run train_bc.py first.")
