"""
================================================================================
DIAGNOSTIC SCRIPT: PHASE 26C TIMEOUT INVESTIGATION
================================================================================

PURPOSE:
  Check if phase_26c_failure_audit.py is hanging or just slow.
  Run a SINGLE simplified trial to measure runtime.

WHAT THIS DOES:
  1. Imports torch
  2. Tests GPU/CPU availability
  3. Runs ONE trial locally (not via subprocess)
  4. Measures total time
  5. Reports findings

================================================================================
"""

import time
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from pathlib import Path
from torch.utils.data import DataLoader, TensorDataset


def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def check_device():
    print_header("DEVICE CHECK")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    if device.type == "cuda":
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    return device


def create_train_data(train_pairs):
    """Create expanded training data (50k samples)"""
    data = []
    labels = []
    for a, b in train_pairs:
        for carry_in in range(2):
            sum_val = a + b + carry_in
            result = sum_val % 10
            carry_out = 1 if sum_val >= 10 else 0
            data.append([a, b, carry_in])
            labels.append([result, carry_out])
    
    base_size = len(data)
    repetitions = (50000 // base_size) + 1
    data = data * repetitions
    labels = labels * repetitions
    data = data[:50000]
    labels = labels[:50000]
    
    return torch.FloatTensor(data), torch.LongTensor(labels)


def create_test_data_simple(test_pairs):
    """Create SIMPLE test data: only 30 pairs × 2 carry states = 60 samples"""
    data = []
    labels = []
    for a, b in test_pairs:
        for carry_in in range(2):
            sum_val = a + b + carry_in
            result = sum_val % 10
            carry_out = 1 if sum_val >= 10 else 0
            data.append([a, b, carry_in])
            labels.append([result, carry_out])
    
    return torch.FloatTensor(data), torch.LongTensor(labels)


class SimpleMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 15),
        )
        self.digit_head = nn.Linear(15, 10)
        self.carry_head = nn.Linear(15, 1)

    def forward(self, x):
        hidden = self.net(x)
        digit_logits = self.digit_head(hidden)
        carry_logits = self.carry_head(hidden)
        return digit_logits, carry_logits


def run_single_trial(device, trial_num=0):
    """Run a SINGLE trial and measure time"""
    
    print_header(f"RUNNING TRIAL {trial_num}")
    
    torch.manual_seed(42)
    np.random.seed(42)
    
    start_time = time.time()
    
    # Step 1: Setup
    print("Step 1: Setting up pair space...")
    all_pairs = [(a, b) for a in range(10) for b in range(10)]
    print(f"  Total pairs: {len(all_pairs)}")
    
    # Step 2: Split
    print("\nStep 2: Splitting data...")
    import random
    random.seed(trial_num)
    random.shuffle(all_pairs)
    train_pairs = all_pairs[:70]
    test_pairs = all_pairs[70:]
    print(f"  Train pairs: {len(train_pairs)}")
    print(f"  Test pairs: {len(test_pairs)}")
    
    # Step 3: Create data
    print("\nStep 3: Creating training data...")
    data_start = time.time()
    X_train, y_train = create_train_data(train_pairs)
    data_time = time.time() - data_start
    print(f"  Training data shape: {X_train.shape}")
    print(f"  Time: {data_time:.2f}s")
    
    # Step 4: Create loader
    print("\nStep 4: Creating DataLoader...")
    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=256,
        shuffle=True
    )
    print(f"  Batches: {len(train_loader)}")
    
    # Step 5: Create model
    print("\nStep 5: Creating model...")
    model = SimpleMLP().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    digit_criterion = nn.CrossEntropyLoss()
    carry_criterion = nn.BCEWithLogitsLoss()
    print(f"  Model on: {device}")
    
    # Step 6: Training
    print("\nStep 6: Training (50 epochs)...")
    train_start = time.time()
    for epoch in range(50):
        model.train()
        total_loss = 0
        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)
            optimizer.zero_grad()
            digit_logits, carry_logits = model(batch_x)
            digit_loss = digit_criterion(digit_logits, batch_y[:, 0])
            carry_loss = carry_criterion(carry_logits.squeeze(), batch_y[:, 1].float())
            (digit_loss + carry_loss).backward()
            optimizer.step()
            total_loss += (digit_loss + carry_loss).item()
        
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1}/50 - Loss: {total_loss:.4f}")
    
    train_time = time.time() - train_start
    print(f"  Training time: {train_time:.2f}s")
    
    # Step 7: Test data
    print("\nStep 7: Creating test data...")
    test_start = time.time()
    X_test, y_test = create_test_data_simple(test_pairs)
    test_time = time.time() - test_start
    print(f"  Test data shape: {X_test.shape}")
    print(f"  Time: {test_time:.2f}s")
    
    # Step 8: Evaluation
    print("\nStep 8: Evaluating...")
    X_test = X_test.to(device)
    y_test = y_test.to(device)
    
    model.eval()
    with torch.no_grad():
        digit_logits, carry_logits = model(X_test)
        digit_pred = digit_logits.argmax(dim=1)
        carry_pred = (carry_logits > 0).long().squeeze()
        both_correct = (digit_pred == y_test[:, 0]) & (carry_pred == y_test[:, 1])
    
    accuracy = both_correct.float().mean().item() * 100
    print(f"  Accuracy: {accuracy:.1f}%")
    
    total_time = time.time() - start_time
    
    return total_time, accuracy


def main():
    print_header("PHASE 26C: TIMEOUT DIAGNOSTIC")
    
    device = check_device()
    
    print_header("RUNNING SINGLE TRIAL")
    print("This trial should take 60-300 seconds depending on device")
    print("(CPU: slow, GPU: faster)")
    print()
    
    try:
        total_time, accuracy = run_single_trial(device, trial_num=0)
        
        print_header("RESULTS")
        print(f"Single trial time: {total_time:.2f} seconds")
        print(f"Single trial accuracy: {accuracy:.1f}%")
        print()
        print("Extrapolation for full 30 trials:")
        print(f"  Estimated total time: {total_time * 30:.0f} seconds = {total_time * 30 / 60:.1f} minutes")
        print()
        
        if total_time > 120:
            print("⚠️  WARNING: Single trial takes > 2 minutes")
            print("   Full 30 trials may take > 1 hour")
        elif total_time > 30:
            print("⚠️  Single trial is moderate speed")
            print("   Full 30 trials may take 15-30 minutes")
        else:
            print("✓ Single trial is fast enough")
            print("  Full 30 trials should complete in < 15 minutes")
        
        print()
        print("Status: ✓ DIAGNOSTIC SUCCESSFUL")
        print("The hanging issue is likely due to slow runtime, not a code bug.")
        
    except Exception as e:
        print_header("ERROR DURING EXECUTION")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("Status: ✗ DIAGNOSTIC FAILED")
        print("There IS a code issue that needs investigation.")


if __name__ == "__main__":
    main()
