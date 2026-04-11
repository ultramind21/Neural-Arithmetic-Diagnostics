"""
================================================================================
PHASE 30: COMPLETE LOCAL-STATE INTERROGATION (VALIDATED)
================================================================================

Using verified MLPSequenceArithmetic model from phase_30_multidigit_learning.py
Testing FULL (a,b,carry_in) local-state space: 10×10×2 = 200 cases

This is Step 2-3 COMPLETE version:
- All 100 cases with carry_in=0 ✓ (already tested)
- All 100 cases with carry_in=1 ✗ (NEW - required)
- Digit accuracy per case
- Carry accuracy per case
- Failure breakdown by type
- Ready for frequency masking analysis
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from torch.utils.data import DataLoader
from pathlib import Path
import sys

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {DEVICE}\n")


# ============================================================================
# MODEL DEFINITION (From phase_30_multidigit_learning.py)
# ============================================================================

class MLPSequenceArithmetic(nn.Module):
    """MLP baseline: process sequence with sequential carry propagation"""
    def __init__(self, max_length):
        super().__init__()
        self.max_length = max_length
        self.embed_a = nn.Embedding(10, 8)
        self.embed_b = nn.Embedding(10, 8)
        
        # Per-position model: (a_emb, b_emb, carry_in_emb) -> (digit, carry)
        self.fc1 = nn.Linear(8 + 8 + 2, 64)
        self.fc2 = nn.Linear(64, 32)
        self.digit_head = nn.Linear(32, 10)
        self.carry_head = nn.Linear(32, 2)
    
    def forward(self, a, b):
        # a, b: (batch, max_length)
        batch_size = a.shape[0]
        
        a_emb = self.embed_a(a)  # (batch, max_length, 8)
        b_emb = self.embed_b(b)  # (batch, max_length, 8)
        
        digit_logits = []
        carry_logits = []
        
        # Process sequentially with carry propagation
        carry_in = torch.zeros(batch_size, 2, device=a.device)  # (batch, 2)
        carry_in[:, 0] = 1  # Start with carry=0
        
        for i in range(self.max_length):
            # Combine input and carry
            combined = torch.cat([a_emb[:, i, :], b_emb[:, i, :], carry_in], dim=1)
            
            # Forward pass
            h = torch.relu(self.fc1(combined))
            h = torch.relu(self.fc2(h))
            
            digit_logit = self.digit_head(h)  # (batch, 10)
            carry_logit = self.carry_head(h)  # (batch, 2)
            
            digit_logits.append(digit_logit)
            carry_logits.append(carry_logit)
            
            # Extract carry for next iteration
            carry_in = torch.softmax(carry_logit, dim=1)  # (batch, 2)
        
        digit_logits = torch.stack(digit_logits, dim=1)  # (batch, max_length, 10)
        carry_logits = torch.stack(carry_logits, dim=1)  # (batch, max_length, 2)
        
        return digit_logits, carry_logits


# ============================================================================
# DATA GENERATION
# ============================================================================

def generate_multidigit_sequences(lengths, num_samples_per_length, seed=42):
    """Generate multi-digit addition sequences."""
    random.seed(seed)
    np.random.seed(seed)
    
    sequences = []
    
    for length in lengths:
        for _ in range(num_samples_per_length):
            a_seq = [random.randint(0, 9) for _ in range(length)]
            b_seq = [random.randint(0, 9) for _ in range(length)]
            
            # Compute ground truth (LSB to MSB)
            digit_out = []
            carry_out = []
            carry = 0
            
            for i in range(length):
                total = a_seq[i] + b_seq[i] + carry
                digit_out.append(total % 10)
                carry = 1 if total >= 10 else 0
                carry_out.append(carry)
            
            sequences.append((a_seq, b_seq, digit_out, carry_out))
    
    return sequences


def pad_sequences(sequences, max_length=5):
    """Pad sequences to fixed length."""
    padded = []
    for a, b, d, c in sequences:
        a_pad = a + [0] * (max_length - len(a))
        b_pad = b + [0] * (max_length - len(b))
        d_pad = d + [0] * (max_length - len(d))
        c_pad = c + [0] * (max_length - len(c))
        padded.append((a_pad, b_pad, d_pad, c_pad))
    return padded


# ============================================================================
# MODEL TRAINING
# ============================================================================

def train_model(model, train_dataloader, epochs=30):
    """Train the model."""
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion_digit = nn.CrossEntropyLoss()
    criterion_carry = nn.CrossEntropyLoss()
    
    model.train()
    for epoch in range(1, epochs + 1):
        total_loss = 0
        for a_batch, b_batch, d_batch, c_batch in train_dataloader:
            a_batch = a_batch.to(DEVICE)
            b_batch = b_batch.to(DEVICE)
            d_batch = d_batch.to(DEVICE)
            c_batch = c_batch.to(DEVICE)
            
            optimizer.zero_grad()
            digit_logits, carry_logits = model(a_batch, b_batch)
            
            loss_digit = criterion_digit(
                digit_logits.view(-1, 10),
                d_batch.view(-1)
            )
            loss_carry = criterion_carry(
                carry_logits.view(-1, 2),
                c_batch.view(-1)
            )
            
            loss = loss_digit + loss_carry
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        if epoch % 10 == 0:
            print(f"  Epoch {epoch}/{epochs}")
    
    print("✅ Model trained\n")


# ============================================================================
# LOCAL-STATE INTERROGATION (COMPLETE SPACE)
# ============================================================================

def interrogate_local_state_complete(model):
    """
    Test all (a, b, carry_in) combinations in local space.
    
    Returns:
    - results[0]: digit and carry accuracy for carry_in=0
    - results[1]: digit and carry accuracy for carry_in=1
    """
    model.eval()
    
    results = [[], []]  # results[0] for carry_in=0, results[1] for carry_in=1
    
    print("=" * 80)
    print("STEP 2-3: COMPLETE LOCAL-STATE TABLE")
    print("=" * 80)
    print()
    
    # Test both carry_in values
    for carry_in_value in [0, 1]:
        print(f"Testing with carry_in={carry_in_value}")
        print()
        
        # Create batch of all (a, b) pairs
        a_values = []
        b_values = []
        true_digits = []
        true_carries = []
        
        for a in range(10):
            for b in range(10):
                a_values.append(a)
                b_values.append(b)
                
                # Compute ground truth
                total = a + b + carry_in_value
                digit_true = total % 10
                carry_true = 1 if total >= 10 else 0
                
                true_digits.append(digit_true)
                true_carries.append(carry_true)
        
        # Convert to tensors (batch_size=100, max_length=5)
        # We're testing position 0, so we need sequences of length 5 with values at position 0
        a_batch = torch.zeros(100, 5, dtype=torch.long, device=DEVICE)
        b_batch = torch.zeros(100, 5, dtype=torch.long, device=DEVICE)
        d_batch = torch.zeros(100, 5, dtype=torch.long, device=DEVICE)
        c_batch = torch.zeros(100, 5, dtype=torch.long, device=DEVICE)
        
        # Fill position 0
        a_batch[:, 0] = torch.tensor(a_values, dtype=torch.long, device=DEVICE)
        b_batch[:, 0] = torch.tensor(b_values, dtype=torch.long, device=DEVICE)
        d_batch[:, 0] = torch.tensor(true_digits, dtype=torch.long, device=DEVICE)
        c_batch[:, 0] = torch.tensor(true_carries, dtype=torch.long, device=DEVICE)
        
        # Forward pass (but we need to inject carry_in manually)
        # Since the model always starts with carry=0, we test by:
        # - Testing position 1 with injected carry from position 0
        # This is complex. Alternative: test position 0 with custom carry_in
        
        # Actually, let's directly test with position 0 by extracting the embeddings
        # and running just that one position with the desired carry_in
        
        with torch.no_grad():
            a_emb = model.embed_a(a_batch[:, 0])  # (100, 8)
            b_emb = model.embed_b(b_batch[:, 0])  # (100, 8)
            
            # Create carry_in embedding
            carry_in_emb = torch.zeros(100, 2, device=DEVICE)
            if carry_in_value == 0:
                carry_in_emb[:, 0] = 1  # [1, 0] = carry=0
            else:
                carry_in_emb[:, 1] = 1  # [0, 1] = carry=1
            
            # Combine and forward
            combined = torch.cat([a_emb, b_emb, carry_in_emb], dim=1)
            h = torch.relu(model.fc1(combined))
            h = torch.relu(model.fc2(h))
            digit_logits = model.digit_head(h)  # (100, 10)
            carry_logits = model.carry_head(h)  # (100, 2)
            
            digit_preds = torch.argmax(digit_logits, dim=1).cpu().numpy()
            carry_preds = torch.argmax(carry_logits, dim=1).cpu().numpy()
        
        # Evaluate
        digit_correct = (digit_preds == np.array(true_digits)).astype(int)
        carry_correct = (carry_preds == np.array(true_carries)).astype(int)
        
        # Print full table
        print(f"| a | b | d_true | d_pred | d_ok | c_true | c_pred | c_ok |")
        print("-" * 65)
        
        failures = []
        for idx, (a, b) in enumerate(zip(a_values, b_values)):
            d_t = true_digits[idx]
            d_p = digit_preds[idx]
            c_t = true_carries[idx]
            c_p = carry_preds[idx]
            d_ok = "✓" if digit_correct[idx] else "✗"
            c_ok = "✓" if carry_correct[idx] else "✗"
            
            print(f"| {a} | {b} | {d_t} | {d_p} | {d_ok} | {c_t} | {c_p} | {c_ok} |")
            
            if not digit_correct[idx] or not carry_correct[idx]:
                failures.append({
                    'a': a, 'b': b, 'carry_in': carry_in_value,
                    'digit_true': d_t, 'digit_pred': d_p,
                    'carry_true': c_t, 'carry_pred': c_p,
                    'digit_ok': bool(digit_correct[idx]),
                    'carry_ok': bool(carry_correct[idx])
                })
        
        print("-" * 65)
        digit_accuracy = np.mean(digit_correct)
        carry_accuracy = np.mean(carry_correct)
        overall_accuracy = np.mean(digit_correct & carry_correct)
        
        print(f"Digit accuracy:   {digit_accuracy*100:.1f}% ({np.sum(digit_correct)}/100)")
        print(f"Carry accuracy:   {carry_accuracy*100:.1f}% ({np.sum(carry_correct)}/100)")
        print(f"Overall (both):   {overall_accuracy*100:.1f}% ({np.sum(digit_correct & carry_correct)}/100)")
        print()
        
        results[carry_in_value] = {
            'digit_accuracy': digit_accuracy,
            'carry_accuracy': carry_accuracy,
            'overall_accuracy': overall_accuracy,
            'failures': failures
        }
    
    return results


# ============================================================================
# FAILURE ANALYSIS
# ============================================================================

def analyze_failures(results):
    """Break down failures by type and location."""
    print("=" * 80)
    print("FAILURE BREAKDOWN BY SUBCASE")
    print("=" * 80)
    print()
    
    all_failures = []
    for carry_in_val in [0, 1]:
        all_failures.extend(results[carry_in_val]['failures'])
    
    if not all_failures:
        print("✅ NO FAILURES FOUND (perfect local accuracy)")
        print()
        return
    
    # Categorize
    digit_only = [f for f in all_failures if f['digit_ok'] == False and f['carry_ok'] == True]
    carry_only = [f for f in all_failures if f['digit_ok'] == True and f['carry_ok'] == False]
    both = [f for f in all_failures if f['digit_ok'] == False and f['carry_ok'] == False]
    
    print(f"Total failures: {len(all_failures)}")
    print(f"  - Digit-only: {len(digit_only)}")
    print(f"  - Carry-only: {len(carry_only)}")
    print(f"  - Both: {len(both)}")
    print()
    
    # Print detailed failures
    if all_failures:
        print("Detailed failure cases:")
        print()
        for f in all_failures:
            print(f"  ({f['a']}, {f['b']}, carry_in={f['carry_in']})")
            print(f"    Digit: {f['digit_true']} -> {f['digit_pred']} {'✓' if f['digit_ok'] else '✗'}")
            print(f"    Carry: {f['carry_true']} -> {f['carry_pred']} {'✓' if f['carry_ok'] else '✗'}")
            print()


# ============================================================================
# FREQUENCY MASKING PREVIEW
# ============================================================================

def preview_frequency_masking(results):
    """
    Preview: if these local failures occur at their frequencies in sequences,
    what global accuracy would we predict?
    """
    print("=" * 80)
    print("FREQUENCY MASKING PREVIEW (Not full analysis yet)")
    print("=" * 80)
    print()
    
    # Collect all failure locations
    all_failures = []
    for carry_in_val in [0, 1]:
        all_failures.extend(results[carry_in_val]['failures'])
    
    if not all_failures:
        print("No local failures → expect ~100% global accuracy")
        return
    
    # For a rough estimate: frequency of (a,b,carry_in) in random sequences
    # carry_in=0: ~50% of positions (except first)
    # carry_in=1: ~50% of positions (except first)
    
    failure_rate = len(all_failures) / 200  # 200 total cases
    print(f"Local failure frequency: {failure_rate*100:.1f}% ({len(all_failures)}/200)")
    print(f"Naive prediction: {(1-failure_rate)*100:.1f}% global accuracy")
    print()
    print("Note: This assumes uniform distribution. Actual depends on sequence patterns.")
    print()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 30 INTERROGATION: COMPLETE LOCAL-STATE ANALYSIS (VALIDATED)")
    print("=" * 80)
    print()
    
    # Create and train model
    print("Training MLPSequenceArithmetic (30 epochs)...")
    model = MLPSequenceArithmetic(max_length=5).to(DEVICE)
    
    # Generate training data
    train_sequences = generate_multidigit_sequences(
        lengths=[2, 3, 4, 5],
        num_samples_per_length=400,
        seed=42
    )
    train_sequences = pad_sequences(train_sequences)
    
    a_data = torch.tensor([s[0] for s in train_sequences], dtype=torch.long)
    b_data = torch.tensor([s[1] for s in train_sequences], dtype=torch.long)
    d_data = torch.tensor([s[2] for s in train_sequences], dtype=torch.long)
    c_data = torch.tensor([s[3] for s in train_sequences], dtype=torch.long)
    
    train_dataset = torch.utils.data.TensorDataset(a_data, b_data, d_data, c_data)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
    
    train_model(model, train_loader, epochs=30)
    
    # Interrogate
    results = interrogate_local_state_complete(model)
    
    # Analysis
    analyze_failures(results)
    preview_frequency_masking(results)
    
    # Summary
    print("=" * 80)
    print("STEP 2-3 STATUS")
    print("=" * 80)
    print(f"carry_in=0: {results[0]['digit_accuracy']*100:.1f}% digit, {results[0]['carry_accuracy']*100:.1f}% carry")
    print(f"carry_in=1: {results[1]['digit_accuracy']*100:.1f}% digit, {results[1]['carry_accuracy']*100:.1f}% carry")
    print()
    print("Ready for: Frequency masking analysis (Step 4)")
    print("=" * 80)
