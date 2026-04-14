#!/usr/bin/env python3
"""
PROJECT 5 SELECTIVE FAILURE DIAGNOSTIC

Objective:
After Result 6, we identified that failures concentrate on predicting digit=0 
in certain families:

- alternating_carry: Fails specifically at position 5 (digit_true=0)
- block_boundary_stress: Fails at positions 0,1,5 (all digit_true=0)
- full_propagation_chain: Succeeds everywhere including position 5 (digit_true=0)

HYPOTHESIS: The failure is NOT about zero-prediction per se, but about
the CARRY_IN state when digit_true=0 is encountered.

This script will examine the carry_in context at each failure point to see
if there's a systematic difference between:
  - "Success at digit=0" cases (full_propagation_chain position 5)
  - "Failure at digit=0" cases (alternating_carry position 5, block edges)

Expected finding: Zero-prediction failure happens specifically when
carry_in=1 (different from full_propagation where it's carry_in=0 at end)
"""

import os
import json
import numpy as np
import torch
import torch.nn as nn
from datetime import datetime

# ============================================================================
# CORE: Reproduce explicit carry representation model
# ============================================================================

class ExplicitCarryLocalProcessor(nn.Module):
    """Model architecture from Result 5 that achieved breakthrough."""
    
    def __init__(self, hidden_digit=16, hidden_carry=8, shared_hidden=32):
        super().__init__()
        
        self.digit_pair_net = nn.Sequential(
            nn.Linear(2, hidden_digit),
            nn.ReLU(),
            nn.Linear(hidden_digit, hidden_digit),
            nn.ReLU()
        )
        
        self.carry_net = nn.Sequential(
            nn.Linear(1, hidden_carry),
            nn.ReLU(),
            nn.Linear(hidden_carry, hidden_carry),
            nn.ReLU()
        )
        
        combined_dim = hidden_digit + hidden_carry
        
        self.combined_net = nn.Sequential(
            nn.Linear(combined_dim, shared_hidden),
            nn.ReLU(),
            nn.Linear(shared_hidden, shared_hidden),
            nn.ReLU()
        )
        
        self.digit_head = nn.Linear(shared_hidden, 10)
        self.carry_head = nn.Linear(shared_hidden, 2)
    
    def forward(self, x_digits, x_carry):
        digit_h = self.digit_pair_net(x_digits)
        carry_h = self.carry_net(x_carry)
        combined_h = torch.cat([digit_h, carry_h], dim=-1)
        combined = self.combined_net(combined_h)
        digit_out = self.digit_head(combined)
        carry_out = self.carry_head(combined)
        return digit_out, carry_out

# ============================================================================
# Train model from scratch (Result 5 architecture)
# ============================================================================

def build_local_dataset():
    """Generate local digit-carry pairs."""
    pairs = []
    for a in range(10):
        for b in range(10):
            for c_in in [0, 1]:
                pairs.append([a, b, c_in])
    
    X_digits = np.array([[p[0], p[1]] for p in pairs], dtype=np.float32)
    X_carry = np.array([[p[2]] for p in pairs], dtype=np.float32)
    
    digit_y = np.array([(p[0] + p[1] + p[2]) % 10 for p in pairs], dtype=np.int64)
    carry_y = np.array([(p[0] + p[1] + p[2]) // 10 for p in pairs], dtype=np.int64)
    
    return X_digits, X_carry, digit_y, carry_y

device = torch.device("cpu")
X_digits, X_carry, digit_y, carry_y = build_local_dataset()

X_digits_t = torch.tensor(X_digits, dtype=torch.float32, device=device)
X_carry_t = torch.tensor(X_carry, dtype=torch.float32, device=device)
digit_t = torch.tensor(digit_y, dtype=torch.long, device=device)
carry_t = torch.tensor(carry_y, dtype=torch.long, device=device)

model = ExplicitCarryLocalProcessor().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion_digit = nn.CrossEntropyLoss()
criterion_carry = nn.CrossEntropyLoss()

print("Training model from Result 5 architecture...")
for epoch in range(300):
    optimizer.zero_grad()
    digit_logits, carry_logits = model(X_digits_t, X_carry_t)
    loss = criterion_digit(digit_logits, digit_t) + criterion_carry(carry_logits, carry_t)
    loss.backward()
    optimizer.step()

model.eval()
print("✓ Model trained from Result 5 architecture")

# ============================================================================
# Generate test families with full diagnostic information
# ============================================================================

def generate_test_sequences(family_name, num_sequences=100, seq_length=6):
    """Generate test sequences with full per-position diagnostic info."""
    sequences = []
    
    if family_name == "alternating_carry":
        # Pattern: alternating 9,0 to stress alternating carry behavior
        # From Result 5: a=[9,0,9,0,9,0], b=[1,0,1,0,1,0]
        for _ in range(num_sequences):
            a = np.array([9, 0, 9, 0, 9, 0])
            b = np.array([1, 0, 1, 0, 1, 0])  # FIXED: was [0,0,0,...], should match pattern
            sequences.append((a, b))
    
    elif family_name == "full_propagation_chain":
        # Pattern: all 9s to test full carry propagation
        # From Result 5: a=[9,9,9,9,9,9], b=[1,1,1,1,1,1]
        for _ in range(num_sequences):
            a = np.array([9, 9, 9, 9, 9, 9])
            b = np.array([1, 1, 1, 1, 1, 1])  # FIXED: was [0,0,0,...], should match pattern
            sequences.append((a, b))
    
    elif family_name == "block_boundary_stress":
        # Pattern: alternates 0/9 blocks with complementary b
        # From Result 5: a[even]={0,1,2}, a[odd]={9,8,7}, b=[0,0,0,0,0,0]
        for _ in range(num_sequences):
            a = np.array([0, 9, 1, 8, 2, 7])
            b = np.array([0, 0, 0, 0, 0, 0])
            sequences.append((a, b))
    
    return sequences

# ============================================================================
# Execute blockwise decomposition and trace per-position context
# ============================================================================

def blockwise_decomposition_with_diagnostics(a_digits, b_digits, model, block_size=3):
    """
    Execute blockwise composition and record:
    - True/predicted digit at each position
    - True/predicted carry at each position
    - Carry_in state at each position
    - Failure status at each position
    """
    
    n = len(a_digits)
    num_blocks = (n + block_size - 1) // block_size
    
    diagnostics = {
        "position_data": [],  # List of {pos, digit_in_a, digit_in_b, carry_in, digit_true, carry_true, digit_pred, carry_pred, digit_correct}
        "failures": []  # List of failure positions with context
    }
    
    carry = torch.tensor([[0.0]], device=device)  # Initial carry = 0
    
    for pos in range(n):
        # Prepare input
        digit_pair = np.array([float(a_digits[pos]), float(b_digits[pos])], dtype=np.float32)
        x_digits = torch.tensor([digit_pair], dtype=torch.float32, device=device)
        x_carry = torch.tensor([[float(carry.item())]], dtype=torch.float32, device=device)
        
        # True output
        digit_true = (a_digits[pos] + b_digits[pos] + int(carry.item())) % 10
        carry_true_int = (a_digits[pos] + b_digits[pos] + int(carry.item())) // 10
        carry_true = torch.tensor([[carry_true_int]], device=device)
        
        # Forward pass
        with torch.no_grad():
            digit_logits, carry_logits = model(x_digits, x_carry)
        
        digit_pred_idx = digit_logits.argmax(dim=1).item()
        carry_pred_idx = carry_logits.argmax(dim=1).item()
        
        # Record diagnostic
        pos_data = {
            "position": pos,
            "digit_a": int(a_digits[pos]),
            "digit_b": int(b_digits[pos]),
            "carry_in": int(carry.item()),
            "digit_true": int(digit_true),
            "carry_true": int(carry_true.item()),
            "digit_pred": digit_pred_idx,
            "carry_pred": carry_pred_idx,
            "digit_correct": digit_pred_idx == int(digit_true),
            "carry_correct": carry_pred_idx == int(carry_true.item())
        }
        diagnostics["position_data"].append(pos_data)
        
        # Track failures
        if digit_pred_idx != int(digit_true):
            diagnostics["failures"].append({
                "position": pos,
                "carry_in": int(carry.item()),
                "digit_a": int(a_digits[pos]),
                "digit_b": int(b_digits[pos]),
                "digit_true": int(digit_true),
                "digit_pred": digit_pred_idx,
                "carry_true": int(carry_true.item())
            })
        
        # Update carry for next position
        carry = carry_true.clone()
    
    return diagnostics

# ============================================================================
# RUN DIAGNOSTIC ANALYSIS
# ============================================================================

all_results = {}

for family_name in ["alternating_carry", "full_propagation_chain", "block_boundary_stress"]:
    print(f"\n{'='*70}")
    print(f"FAMILY: {family_name}")
    print('='*70)
    
    sequences = generate_test_sequences(family_name, num_sequences=100)
    
    family_failures = []  # All failures across sequences
    
    for seq_idx, (a_digits, b_digits) in enumerate(sequences):
        diag = blockwise_decomposition_with_diagnostics(a_digits, b_digits, model)
        family_failures.extend(diag["failures"])
    
    # Analyze failure patterns
    print(f"\nTotal failures: {len(family_failures)} / {len(sequences) * 6}")
    
    if family_failures:
        print("\nFailure Context Analysis:")
        print("-" * 70)
        
        # Group by carry_in state
        failures_by_carry = {"carry_in_0": [], "carry_in_1": []}
        for failure in family_failures:
            key = f"carry_in_{failure['carry_in']}"
            failures_by_carry[key].append(failure)
        
        for carry_state, failures_list in failures_by_carry.items():
            if failures_list:
                print(f"\n{carry_state}: {len(failures_list)} failures")
                # Show first few
                for i, f in enumerate(failures_list[:3]):
                    print(f"  Position {f['position']}: a={f['digit_a']}, b={f['digit_b']}, "
                          f"digit_true={f['digit_true']}, digit_pred={f['digit_pred']}")
        
        # Aggregate statistics
        zero_failures = [f for f in family_failures if f['digit_true'] == 0]
        nonzero_failures = [f for f in family_failures if f['digit_true'] != 0]
        
        print(f"\nFailures on digit_true=0: {len(zero_failures)}")
        print(f"Failures on digit_true≠0: {len(nonzero_failures)}")
        
        if zero_failures:
            carry_in_0_count = sum(1 for f in zero_failures if f['carry_in'] == 0)
            carry_in_1_count = sum(1 for f in zero_failures if f['carry_in'] == 1)
            print(f"  Within digit=0 failures:")
            print(f"    carry_in=0: {carry_in_0_count}")
            print(f"    carry_in=1: {carry_in_1_count}")
    
    all_results[family_name] = {
        "total_failures": len(family_failures),
        "failures": family_failures
    }

# ============================================================================
# HYPOTHESIS TEST
# ============================================================================

print("\n" + "="*70)
print("HYPOTHESIS TEST: Zero-prediction failures by carry_in context")
print("="*70)

for family_name in ["alternating_carry", "full_propagation_chain", "block_boundary_stress"]:
    failures = all_results[family_name]["failures"]
    
    if not failures:
        print(f"\n{family_name}: NO FAILURES (carries context not applicable)")
        continue
    
    zero_failures = [f for f in failures if f['digit_true'] == 0]
    
    if not zero_failures:
        print(f"\n{family_name}: NO ZERO-PREDICTION FAILURES")
        continue
    
    print(f"\n{family_name}:")
    print(f"  Zero-prediction failures: {len(zero_failures)}")
    
    for f in zero_failures:
        print(f"  Position {f['position']}: a={f['digit_a']}, b={f['digit_b']}, "
              f"carry_in={f['carry_in']}, predicted={f['digit_pred']}")

# ============================================================================
# SAVE RESULTS
# ============================================================================

result_artifact = {
    "timestamp_utc": datetime.utcnow().isoformat() + "Z",
    "experiment": "project_5_selective_failure_diagnostic",
    "hypothesis": "Zero-prediction failures correlate with carry_in=1 context",
    "analysis": all_results
}

artifact_path = "d:\\Music\\Project 03 Abacus\\neural_arithmetic_diagnostics\\project_5\\results\\project_5_selective_failure_diagnostic_artifact.json"
with open(artifact_path, "w") as f:
    json.dump(result_artifact, f, indent=2)

print(f"\n✓ Artifact saved to: {artifact_path}")
print("\nDIAGNOSTIC COMPLETE")
