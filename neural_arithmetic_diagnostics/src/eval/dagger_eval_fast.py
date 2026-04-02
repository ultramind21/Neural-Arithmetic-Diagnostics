#!/usr/bin/env python3
"""Fast DAgger evaluation - detects loops to prevent hanging"""

import torch
import random
from src.env.soroban_env import SorobanEnv  
from src.env.encode import encode_obs
from src.models.policy_net import SorobanPolicy
from src.utils.config import DEFAULT_CONFIG


def dagger_eval_fast(model, config, device, verbose=False):
    """Evaluate model quickly with loop detection (for DAgger)"""
    model.eval()
    
    # Only test 1-6 digits (not OOD)
    results = {}
    for nd in [6]:  # DAgger primarily cares about 6-digit accuracy
        correct = 0
        total = 0
        
        for _ in range(100):  # 100 trials per digit
            a = random.randint(0, 10**nd - 1)
            b = random.randint(0, 10**nd - 1)
            
            if a + b >= 10**config.num_columns:
                continue
            
            env = SorobanEnv(config)
            env.reset(a, b)
            
            state_history = []
            for step in range(100):  # Max 100 steps (vs 250)
                board_tuple = tuple(tuple(col) for col in env.board)
                state_history.append(board_tuple)
                
                # Loop detection: board unchanged for 3 steps
                if len(state_history) >= 3 and state_history[-1] == state_history[-2] == state_history[-3]:
                    break
                
                obs = encode_obs(env).unsqueeze(0).to(device)
                with torch.no_grad():
                    logits = model(obs)
                    action = logits.argmax(-1).item()
                
                _, _, done, info = env.step(action)
                if done:
                    if info.get("correct"):
                        correct += 1
                    break
            
            total += 1
        
        accuracy = correct / max(total, 1) if total > 0 else 0
        results[nd] = {"accuracy": accuracy, "correct": correct, "total": total}
        
        if verbose:
            print(f"  {nd}-digit: {accuracy:.1%} ({correct}/{total})")
    
    return results
