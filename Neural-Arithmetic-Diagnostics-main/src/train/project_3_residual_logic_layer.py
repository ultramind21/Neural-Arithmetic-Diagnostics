"""
================================================================================
PROJECT 3: RESIDUAL + LOGIC LAYER TRAINING (V2: REGRESSION SUM)
================================================================================

Training the ResidualLogicAdder model on Phase 30 protocol.

KEY DIFFERENCE FROM V1:
- V1: Classification on sum (20 classes) → discrete jumps → high error
- V2: Regression on sum (continuous float) → smooth structure → lower error

Why regression works:
- Physical structure: sum=9 and sum=10 are close (differ by 1)
- Classification breaks this: class 9 ≠ class 10 (completely different)
- Regression preserves continuity: 9.2 → 9.8 → 10.1 (smooth)
- MSE loss allows gradient to flow smoothly
- Rounding at inference preserves integer semantics

Protocol:
- Train: lengths 2-5
- Test in-distribution: 2-5
- Test OOD compositional: 6, 8, 10, 15, 20
- Test OOD stress: 30, 50, 100 (Phase 30b)

================================================================================
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.residual_logic_adder import ResidualLogicAdder

# ============================================================================
# SETUP
# ============================================================================

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {DEVICE}\n")

# ============================================================================
# DATA GENERATION
# ============================================================================

def generate_multidigit_sequences(lengths, num_samples_per_length, seed=42):
    """
    Generate multi-digit addition sequences.
    
    Returns:
        sequences: list of (a_seq, b_seq, sum_out)
        where sum_out[i] = a_seq[i] + b_seq[i] + carry_in[i] ∈ [0..19]
    """
    random.seed(seed)
    np.random.seed(seed)
    
    sequences = []
    
    for length in lengths:
        for _ in range(num_samples_per_length):
            a_seq = [random.randint(0, 9) for _ in range(length)]
            b_seq = [random.randint(0, 9) for _ in range(length)]
            
            # Compute sum sequence (a + b + carry_in)
            sum_out = []
            carry = 0
            
            for i in range(length):
                total = a_seq[i] + b_seq[i] + carry
                sum_out.append(total)
                carry = 1 if total >= 10 else 0
            
            sequences.append((a_seq, b_seq, sum_out))
    
    return sequences


def pad_sequences(sequences, max_length):
    """Pad sequences to max_length."""
    padded = []
    for a, b, s in sequences:
        a_pad = a + [0] * (max_length - len(a))
        b_pad = b + [0] * (max_length - len(b))
        s_pad = s + [0] * (max_length - len(s))
        padded.append((a_pad, b_pad, s_pad))
    return padded


def collate_sequences(batch):
    """Convert batch to tensors, handling variable lengths."""
    max_len = max(len(a) for a, b, s in batch)
    
    a_list = []
    b_list = []
    s_list = []
    lengths = []
    
    for a, b, s in batch:
        length = len(a)
        a_pad = a + [0] * (max_len - len(a))
        b_pad = b + [0] * (max_len - len(b))
        s_pad = s + [0] * (max_len - len(s))
        
        a_list.append(a_pad)
        b_list.append(b_pad)
        s_list.append(s_pad)
        lengths.append(length)
    
    a_tensor = torch.LongTensor(a_list).to(DEVICE)
    b_tensor = torch.LongTensor(b_list).to(DEVICE)
    s_tensor = torch.LongTensor(s_list).to(DEVICE)
    
    return a_tensor, b_tensor, s_tensor, torch.LongTensor(lengths)


# ============================================================================
# TRAINING
# ============================================================================

def train_model(model, train_loader, num_epochs=50, lr=0.001):
    """Train the model with MSE regression loss."""
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0.0
        
        for a, b, s, lengths in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}"):
            # Initialize carry_in (all zeros at sequence start)
            carry_in = torch.zeros_like(a, dtype=torch.float32)
            
            # Forward pass: regression sum
            sum_pred = model(a, b, carry_in)  # (batch, seq_len)
            
            # Target: floating point sum
            s_float = s.float()
            
            # Loss: MSE (regression)
            loss = criterion(sum_pred, s_float)
            
            # Optional: small constraint to keep predictions close to integers
            loss += 0.05 * torch.mean((sum_pred - torch.round(sum_pred))**2)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item() * a.size(0)
        
        avg_loss = total_loss / len(train_loader.dataset)
        print(f"Epoch {epoch+1}/{num_epochs}: Loss = {avg_loss:.4f}\n")
    
    return model


# ============================================================================
# EVALUATION
# ============================================================================

def evaluate_model(model, test_sequences):
    """
    Evaluate model on test sequences.
    
    Returns:
        digit_acc: accuracy of digit predictions
        carry_acc: accuracy of carry predictions
        exact_match: accuracy of exact digit+carry matching
    """
    model.eval()
    
    digit_correct = 0
    carry_correct = 0
    exact_correct = 0
    total = 0
    
    with torch.no_grad():
        for a_seq, b_seq, s_seq in test_sequences:
            length = len(a_seq)
            
            # Initialize carry
            carry = 0
            
            for i in range(length):
                a = torch.LongTensor([a_seq[i]]).to(DEVICE)
                b = torch.LongTensor([b_seq[i]]).to(DEVICE)
                carry_in = torch.FloatTensor([carry]).to(DEVICE)
                
                # Forward with logic layer
                sum_pred, sum_int, digit_pred, carry_out = model.forward_with_logic(a, b, carry_in)
                
                # Ground truth
                total_sum = a_seq[i] + b_seq[i] + carry
                digit_true = total_sum % 10
                carry_true = 1 if total_sum >= 10 else 0
                
                # Check predictions
                if digit_pred.item() == digit_true:
                    digit_correct += 1
                if carry_out.item() == carry_true:
                    carry_correct += 1
                if digit_pred.item() == digit_true and carry_out.item() == carry_true:
                    exact_correct += 1
                
                total += 1
                carry = carry_out.item()
    
    digit_acc = digit_correct / total if total > 0 else 0.0
    carry_acc = carry_correct / total if total > 0 else 0.0
    exact_acc = exact_correct / total if total > 0 else 0.0
    
    return digit_acc, carry_acc, exact_acc


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PROJECT 3: RESIDUAL + LOGIC LAYER")
    print("=" * 80)
    print()
    
    # Generate training data (lengths 2-5)
    print("Generating training data (lengths 2-5)...")
    train_sequences = generate_multidigit_sequences(
        lengths=[2, 3, 4, 5],
        num_samples_per_length=500,
        seed=42
    )
    print(f"  Total training sequences: {len(train_sequences)}")
    
    # Create DataLoader
    train_loader = DataLoader(
        train_sequences,
        batch_size=32,
        shuffle=True,
        collate_fn=collate_sequences
    )
    
    # Initialize model
    print("\nInitializing ResidualLogicAdder...")
    model = ResidualLogicAdder(embedding_dim=8, hidden_dim=64).to(DEVICE)
    print(f"  Model parameters: {sum(p.numel() for p in model.parameters())}")
    print()
    
    # Train
    print("Training...")
    model = train_model(model, train_loader, num_epochs=50, lr=0.001)
    print("\n✅ Training complete!\n")
    
    # Save model checkpoint
    checkpoint_path = os.path.join(os.path.dirname(__file__), '..', '..', 'checkpoints', 'residual_logic_adder.pt')
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    torch.save(model.state_dict(), checkpoint_path)
    print(f"Model saved to: {checkpoint_path}\n")
    
    # Evaluation: In-distribution
    print("=" * 80)
    print("EVALUATION: IN-DISTRIBUTION (lengths 2-5)")
    print("=" * 80)
    
    indist_sequences = generate_multidigit_sequences(
        lengths=[2, 3, 4, 5],
        num_samples_per_length=100,
        seed=999
    )
    
    digit_acc, carry_acc, exact_acc = evaluate_model(model, indist_sequences)
    print(f"Digit Accuracy:  {digit_acc*100:.2f}%")
    print(f"Carry Accuracy:  {carry_acc*100:.2f}%")
    print(f"Exact Match:     {exact_acc*100:.2f}%\n")
    
    # Evaluation: OOD Compositional (lengths 6, 8, 10, 15, 20)
    print("=" * 80)
    print("EVALUATION: OOD COMPOSITIONAL (lengths 6, 8, 10, 15, 20)")
    print("=" * 80)
    
    for length in [6, 8, 10, 15, 20]:
        ood_sequences = generate_multidigit_sequences(
            lengths=[length],
            num_samples_per_length=100,
            seed=999 + length
        )
        
        digit_acc, carry_acc, exact_acc = evaluate_model(model, ood_sequences)
        print(f"Length {length:2d}: Digit={digit_acc*100:5.1f}% | Carry={carry_acc*100:5.1f}% | Exact={exact_acc*100:5.1f}%")
    
    print()
    
    # Evaluation: Stress test (Phase 30b)
    print("=" * 80)
    print("EVALUATION: STRESS TEST (lengths 30, 50, 100)")
    print("=" * 80)
    
    for length in [30, 50, 100]:
        stress_sequences = generate_multidigit_sequences(
            lengths=[length],
            num_samples_per_length=50,
            seed=999 + length
        )
        
        digit_acc, carry_acc, exact_acc = evaluate_model(model, stress_sequences)
        print(f"Length {length:3d}: Digit={digit_acc*100:5.1f}% | Carry={carry_acc*100:5.1f}% | Exact={exact_acc*100:5.1f}%")
    
    print("\n" + "=" * 80)
    print("✅ EVALUATION COMPLETE")
    print("=" * 80)
