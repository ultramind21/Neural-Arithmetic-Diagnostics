"""
PROJECT 3: KILLER TEST - ADVERSARIAL CARRY-CHAIN SUITE
================================================================================
PURPOSE: Final verification that 99.6% is genuine algorithm or lucky approximation
METHOD:  Force maximum sequential carry dependencies with adversarial patterns
GOAL:    If > 95% on all patterns → 99.6% is real algorithm
         If < 85% on any pattern → 99.6% is approximation with blind spots
================================================================================
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import sys
import os
from pathlib import Path
from torch.utils.data import DataLoader
from tqdm import tqdm

# Set seeds
torch.manual_seed(42)
np.random.seed(42)

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.residual_logic_adder import ResidualLogicAdder

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}\n")


def create_fresh_model():
    """Create fresh V2 model and train for 100 epochs"""
    import torch.optim as optim
    from torch.utils.data import DataLoader
    import random
    from tqdm import tqdm
    
    print("Creating fresh V2 model and training for 100 epochs...")
    
    # Generate training data
    def generate_multidigit_sequences(lengths, num_samples_per_length, seed=42):
        random.seed(seed)
        np.random.seed(seed)
        
        sequences = []
        for length in lengths:
            for _ in range(num_samples_per_length):
                a_seq = [random.randint(0, 9) for _ in range(length)]
                b_seq = [random.randint(0, 9) for _ in range(length)]
                
                sum_out = []
                carry = 0
                
                for i in range(length):
                    total = a_seq[i] + b_seq[i] + carry
                    sum_out.append(total)
                    carry = 1 if total >= 10 else 0
                
                sequences.append((a_seq, b_seq, sum_out))
        
        return sequences
    
    def collate_sequences(batch):
        max_len = max(len(a) for a, b, s in batch)
        
        a_list, b_list, s_list = [], [], []
        
        for a, b, s in batch:
            a_pad = a + [0] * (max_len - len(a))
            b_pad = b + [0] * (max_len - len(b))
            s_pad = s + [0] * (max_len - len(s))
            
            a_list.append(a_pad)
            b_list.append(b_pad)
            s_list.append(s_pad)
        
        a_tensor = torch.LongTensor(a_list).to(device)
        b_tensor = torch.LongTensor(b_list).to(device)
        s_tensor = torch.LongTensor(s_list).to(device)
        
        return a_tensor, b_tensor, s_tensor
    
    # Create model
    model = ResidualLogicAdder().to(device)
    
    # Training data
    train_sequences = generate_multidigit_sequences(
        lengths=[2, 3, 4, 5],
        num_samples_per_length=500,
        seed=42
    )
    
    train_loader = DataLoader(
        train_sequences,
        batch_size=32,
        shuffle=True,
        collate_fn=collate_sequences
    )
    
    # Train
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)
    mse_criterion = nn.MSELoss()
    
    for epoch in range(100):
        model.train()
        total_loss = 0.0
        total_samples = 0
        
        for a, b, s in tqdm(train_loader, desc=f"Training epoch {epoch+1}/100", leave=False):
            batch_size = a.size(0)
            max_len = a.size(1)
            
            carry_in = torch.zeros(batch_size, dtype=torch.float32, device=device)
            
            total_mse = 0.0
            
            for pos in range(max_len):
                a_pos = a[:, pos]
                b_pos = b[:, pos]
                s_pos = s[:, pos]
                
                sum_pred = model(a_pos, b_pos, carry_in)
                
                s_float = s_pos.float()
                mse_loss = mse_criterion(sum_pred, s_float)
                total_mse += mse_loss
                
                sum_int = torch.round(sum_pred).clamp(0, 19).long()
                carry_in = (sum_int // 10).float()
            
            loss = total_mse / max_len
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item() * batch_size
            total_samples += batch_size
        
        avg_loss = total_loss / total_samples
        scheduler.step()
        
        if (epoch + 1) % 20 == 0:
            print(f"  Epoch {epoch+1}: Loss = {avg_loss:.4f}")
    
    print("✅ Model trained\n")
    return model


def generate_test_patterns(length=100, num_samples=100):
    """Generate 5 adversarial carry-chain patterns"""
    
    patterns = {}
    
    # Pattern 1: Maximum carry (999...9 + 0...0)
    a_pat1 = np.array([[9] * length for _ in range(num_samples)])
    b_pat1 = np.array([[0] * length for _ in range(num_samples)])
    patterns['max_carry_leading'] = (a_pat1, b_pat1, "999...9 + 0...0")
    
    # Pattern 2: Full carry chain (999...9 + 111...1)
    a_pat2 = np.array([[9] * length for _ in range(num_samples)])
    b_pat2 = np.array([[1] * length for _ in range(num_samples)])
    patterns['full_carry_chain'] = (a_pat2, b_pat2, "999...9 + 111...1 (max carry propagation)")
    
    # Pattern 3: Single carry propagating (5000...0 + 5000...0)
    a_pat3 = np.array([[5] + [0] * (length - 1) for _ in range(num_samples)])
    b_pat3 = np.array([[5] + [0] * (length - 1) for _ in range(num_samples)])
    patterns['single_carry_start'] = (a_pat3, b_pat3, "5000...0 + 5000...0 (single carry at position 0)")
    
    # Pattern 4: Alternating (090909... + 010101...)
    a_pat4 = np.array([([9, 0] * (length // 2))[:length] for _ in range(num_samples)])
    b_pat4 = np.array([([1, 0] * (length // 2))[:length] for _ in range(num_samples)])
    patterns['alternating'] = (a_pat4, b_pat4, "Alternating 9,0,9,0... + 1,0,1,0...")
    
    # Pattern 5: Block pattern (000...999...000...)
    block_size = length // 4
    a_pat5 = np.array([[0]*block_size + [9]*block_size + [1]*block_size + [0]*block_size 
                       for _ in range(num_samples)])[:, :length]
    b_pat5 = np.array([[0]*block_size + [0]*block_size + [8]*block_size + [0]*block_size 
                       for _ in range(num_samples)])[:, :length]
    patterns['block_pattern'] = (a_pat5, b_pat5, "Blocks: 000...999...888...000")
    
    return patterns


def evaluate_pattern(model, a, b, pattern_name, pattern_desc):
    """Evaluate model on a specific pattern"""
    
    model.eval()
    
    digit_correct = 0
    carry_correct = 0
    exact_correct = 0
    total = 0
    errors = []
    
    with torch.no_grad():
        for sample_idx in range(len(a)):
            carry = 0
            
            for i in range(len(a[sample_idx])):
                a_val = torch.LongTensor([a[sample_idx][i]]).to(device)
                b_val = torch.LongTensor([b[sample_idx][i]]).to(device)
                carry_in = torch.FloatTensor([carry]).to(device)
                
                # Use forward_with_logic to get digit and carry output
                _, _, digit_pred, carry_out = model.forward_with_logic(a_val, b_val, carry_in)
                
                # Compute ground truth
                total_sum = a[sample_idx][i] + b[sample_idx][i] + carry
                digit_true = total_sum % 10
                carry_true = 1 if total_sum >= 10 else 0
                
                if digit_pred.item() == digit_true:
                    digit_correct += 1
                if carry_out.item() == carry_true:
                    carry_correct += 1
                if digit_pred.item() == digit_true and carry_out.item() == carry_true:
                    exact_correct += 1
                
                errors.append(total_sum - total_sum if digit_pred == digit_true else 1.0)
                total += 1
                carry = carry_out.item()
    
    digit_acc = digit_correct / total if total > 0 else 0.0
    carry_acc = carry_correct / total if total > 0 else 0.0
    exact_acc = exact_correct / total if total > 0 else 0.0
    error_mean = np.mean(errors) if errors else 0.0
    error_std = np.std(errors) if errors else 0.0
    large_errors = np.sum(np.abs(np.array(errors)) > 0.5) / len(errors) * 100 if errors else 0.0
    
    return {
        'pattern': pattern_name,
        'description': pattern_desc,
        'digit_acc': digit_acc * 100,
        'carry_acc': carry_acc * 100,
        'exact_acc': exact_acc * 100,
        'error_mean': error_mean,
        'error_std': error_std,
        'large_errors_pct': large_errors,
    }


def main():
    print("=" * 80)
    print("PROJECT 3: KILLER TEST - ADVERSARIAL CARRY-CHAIN SUITE")
    print("=" * 80)
    print()
    
    # Create and train fresh model
    model = create_fresh_model()
    
    # Generate adversarial patterns
    patterns = generate_test_patterns(length=100, num_samples=100)
    
    print("RUNNING 5 ADVERSARIAL CARRY-CHAIN PATTERNS")
    print("-" * 80)
    print()
    
    results = []
    
    for pattern_key, (a, b, desc) in patterns.items():
        print(f"Testing: {desc}")
        result = evaluate_pattern(model, a, b, pattern_key, desc)
        results.append(result)
        
        print(f"  Digit Accuracy:  {result['digit_acc']:6.2f}%")
        print(f"  Carry Accuracy:  {result['carry_acc']:6.2f}%")
        print(f"  Exact Match:     {result['exact_acc']:6.2f}%")
        print(f"  Error Mean:      {result['error_mean']:7.4f}")
        print(f"  Error Std:       {result['error_std']:7.4f}")
        print(f"  Large Errors:    {result['large_errors_pct']:6.2f}%")
        print()
    
    # Summary
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    print()
    
    digit_accs = [r['digit_acc'] for r in results]
    min_digit_acc = min(digit_accs)
    mean_digit_acc = np.mean(digit_accs)
    
    print(f"Minimum digit accuracy: {min_digit_acc:.2f}%")
    print(f"Mean digit accuracy:    {mean_digit_acc:.2f}%")
    print()
    
    if min_digit_acc > 95:
        print("✅ VERDICT: GENUINE ALGORITHM")
        print("   All adversarial patterns maintained > 95% accuracy")
        print("   99.6% is real, not a lucky approximation")
        verdict_score = +2
    elif min_digit_acc > 85:
        print("⚠️  VERDICT: MIXED EVIDENCE")
        print(f"   Some patterns degrade to {min_digit_acc:.2f}%")
        print("   Suggests algorithm with edge case weakness")
        verdict_score = 0
    else:
        print("❌ VERDICT: APPROXIMATION WITH BLIND SPOTS")
        print(f"   Adversarial patterns collapse < 85% ({min_digit_acc:.2f}%)")
        print("   99.6% is local approximation, not general algorithm")
        verdict_score = -2
    
    print()
    print("=" * 80)
    
    # Save results
    results_file = Path(__file__).parent.parent.parent / "Papers" / "killer_test_results.txt"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        f.write("PROJECT 3: KILLER TEST RESULTS\n")
        f.write("=" * 80 + "\n\n")
        for r in results:
            f.write(f"Pattern: {r['pattern']}\n")
            f.write(f"Description: {r['description']}\n")
            f.write(f"  Digit Accuracy:  {r['digit_acc']:.2f}%\n")
            f.write(f"  Carry Accuracy:  {r['carry_acc']:.2f}%\n")
            f.write(f"  Exact Match:     {r['exact_acc']:.2f}%\n")
            f.write(f"  Error Mean:      {r['error_mean']:.4f}\n")
            f.write(f"  Error Std:       {r['error_std']:.4f}\n")
            f.write(f"  Large Errors:    {r['large_errors_pct']:.2f}%\n\n")
        
        f.write("=" * 80 + "\n")
        f.write(f"Minimum digit accuracy: {min_digit_acc:.2f}%\n")
        f.write(f"Mean digit accuracy:    {mean_digit_acc:.2f}%\n")
        f.write(f"Verdict score: {verdict_score}\n")
    
    print(f"\n✅ Results saved to {results_file}")


if __name__ == "__main__":
    main()
