"""
================================================================================
KILLER TEST: CARRY SENSITIVITY FOLLOW-UP INVESTIGATION
================================================================================

OBJECTIVE:
Determine precisely how the model uses carry_in signal across different conditions.
Three mechanistic tests to distinguish between:
  A) Carry nearly ignored
  B) Carry weakly/inconsistently used
  C) Carry locally encoded but structurally fragile

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

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from models.residual_logic_adder import ResidualLogicAdder

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}\n")


def create_killer_test_model(seed=42):
    """
    Create and train model using EXACT same procedure as killer test.
    This ensures we're testing the SAME model, not a different one.
    """
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    
    print("Creating model with killer test parameters...")
    
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
    
    model = ResidualLogicAdder().to(device)
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
    
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)
    mse_criterion = nn.MSELoss()
    
    for epoch in range(100):
        model.train()
        total_loss = 0.0
        total_samples = 0
        
        for a, b, s in train_loader:
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
        
        scheduler.step()
    
    print("✅ Model trained\n")
    return model


# ================================================================================
# TEST 1: CARRY MINIMAL-PAIR INTERVENTION
# ================================================================================

def test_1_minimal_pair_intervention(model):
    """
    Fix (a,b) and vary carry_in between 0 and 1.
    Measure how much the prediction changes.
    
    If delta ≈ 0: carry ignored
    If delta ≈ 1: carry properly integrated
    If delta weak/inconsistent: carry weakly used
    """
    
    print("\n" + "="*80)
    print("TEST 1: CARRY MINIMAL-PAIR INTERVENTION")
    print("="*80)
    print("\nTesting: Fix (a,b) and vary carry_in ∈ {0,1}\n")
    
    test_pairs = [
        (0, 0, "no sum, sum = 0"),
        (1, 1, "low sum, sum = 2"),
        (4, 5, "mid sum, sum = 9"),
        (8, 1, "boundary, sum = 9"),
        (9, 0, "near boundary, sum = 9"),
        (9, 1, "boundary, sum = 10"),
        (9, 9, "high sum, sum = 18"),
    ]
    
    model.eval()
    results = []
    
    with torch.no_grad():
        for a, b, desc in test_pairs:
            a_t = torch.LongTensor([a]).to(device)
            b_t = torch.LongTensor([b]).to(device)
            
            # Carry = 0
            carry_0 = torch.FloatTensor([0]).to(device)
            sum_pred_0, sum_int_0, digit_0, carry_out_0 = model.forward_with_logic(a_t, b_t, carry_0)
            
            # Carry = 1
            carry_1 = torch.FloatTensor([1]).to(device)
            sum_pred_1, sum_int_1, digit_1, carry_out_1 = model.forward_with_logic(a_t, b_t, carry_1)
            
            delta = sum_pred_1.item() - sum_pred_0.item()
            
            results.append({
                'a': a, 'b': b, 'desc': desc,
                'sum_pred_0': sum_pred_0.item(),
                'sum_int_0': sum_int_0.item(),
                'digit_0': digit_0.item(),
                'carry_out_0': carry_out_0.item(),
                'sum_pred_1': sum_pred_1.item(),
                'sum_int_1': sum_int_1.item(),
                'digit_1': digit_1.item(),
                'carry_out_1': carry_out_1.item(),
                'delta_sum': delta,
                'digit_changed': digit_0.item() != digit_1.item(),
                'carry_changed': carry_out_0.item() != carry_out_1.item(),
            })
    
    # Print results
    print("a | b | Description        | sum_pred(c=0) | sum_pred(c=1) | delta | digit_c0 | digit_c1 | diff | carry_c0 | carry_c1 | diff")
    print("-" * 140)
    
    for r in results:
        print(f"{r['a']} | {r['b']} | {r['desc']:18s} | {r['sum_pred_0']:13.4f} | {r['sum_pred_1']:13.4f} | {r['delta_sum']:5.4f} | {int(r['digit_0']):8d} | {int(r['digit_1']):8d} | {str(r['digit_changed']):4s} | {int(r['carry_out_0']):8d} | {int(r['carry_out_1']):8d} | {str(r['carry_changed']):4s}")
    
    # Summary
    print("\n" + "-" * 80)
    deltas = [r['delta_sum'] for r in results]
    print(f"\nDelta Summary (carry effect on sum_pred):")
    print(f"  Mean delta:      {np.mean(deltas):.4f}")
    print(f"  Std delta:       {np.std(deltas):.4f}")
    print(f"  Min delta:       {np.min(deltas):.4f}")
    print(f"  Max delta:       {np.max(deltas):.4f}")
    
    count_strong = sum(1 for d in deltas if 0.8 <= d <= 1.2)
    count_weak = sum(1 for d in deltas if abs(d) < 0.3)
    print(f"\n  Strong carry effect (0.8 ≤ delta ≤ 1.2): {count_strong}/{len(deltas)}")
    print(f"  Weak carry effect (|delta| < 0.3):       {count_weak}/{len(deltas)}")
    
    digit_changes = sum(1 for r in results if r['digit_changed'])
    print(f"\n  Digit changed by carry:  {digit_changes}/{len(results)}")
    
    return results


# ================================================================================
# TEST 2: FULL CARRY SENSITIVITY SWEEP
# ================================================================================

def test_2_full_carry_sensitivity(model):
    """
    For all a,b ∈ {0..9}, compute delta_carry = sum_pred(a,b,c=1) - sum_pred(a,b,c=0)
    
    Provide full statistical breakdown and group by sum range.
    """
    
    print("\n" + "="*80)
    print("TEST 2: FULL CARRY SENSITIVITY SWEEP")
    print("="*80)
    print("\nComputing carry sensitivity for all (a,b) pairs...\n")
    
    model.eval()
    deltas_all = []
    
    # Group by sum range
    deltas_by_sum = {
        'low': [],      # a+b <= 8
        'boundary': [], # a+b = 9 or 10
        'high': [],     # a+b >= 11
    }
    
    with torch.no_grad():
        for a in range(10):
            for b in range(10):
                a_t = torch.LongTensor([a]).to(device)
                b_t = torch.LongTensor([b]).to(device)
                
                carry_0 = torch.FloatTensor([0]).to(device)
                sum_pred_0, _, _, _ = model.forward_with_logic(a_t, b_t, carry_0)
                
                carry_1 = torch.FloatTensor([1]).to(device)
                sum_pred_1, _, _, _ = model.forward_with_logic(a_t, b_t, carry_1)
                
                delta = sum_pred_1.item() - sum_pred_0.item()
                deltas_all.append(delta)
                
                # Categorize by sum
                s = a + b
                if s <= 8:
                    deltas_by_sum['low'].append(delta)
                elif s in [9, 10]:
                    deltas_by_sum['boundary'].append(delta)
                else:
                    deltas_by_sum['high'].append(delta)
    
    # Print summary
    print("OVERALL STATISTICS:")
    print(f"  Mean delta:          {np.mean(deltas_all):.4f}")
    print(f"  Std delta:           {np.std(deltas_all):.4f}")
    print(f"  Min delta:           {np.min(deltas_all):.4f}")
    print(f"  Max delta:           {np.max(deltas_all):.4f}")
    print(f"  95th percentile:     {np.percentile(deltas_all, 95):.4f}")
    
    # Distribution buckets
    print("\nDELTA DISTRIBUTION:")
    bucket_ranges = [
        (0, 0.2, "delta < 0.2 (minimal carry effect)"),
        (0.2, 0.5, "0.2 ≤ delta < 0.5 (weak)"),
        (0.5, 0.8, "0.5 ≤ delta < 0.8 (moderate)"),
        (0.8, 1.2, "0.8 ≤ delta ≤ 1.2 (strong)"),
        (1.2, 2.0, "delta > 1.2 (very strong)"),
    ]
    
    for min_d, max_d, label in bucket_ranges:
        count = sum(1 for d in deltas_all if min_d <= d <= max_d)
        pct = 100 * count / len(deltas_all)
        print(f"  {label:40s}: {count:3d} pairs ({pct:5.1f}%)")
    
    # By sum range
    print("\nBY SUM RANGE:")
    for range_name in ['low', 'boundary', 'high']:
        if deltas_by_sum[range_name]:
            ds = deltas_by_sum[range_name]
            print(f"\n  {range_name.upper()}:")
            print(f"    Mean:   {np.mean(ds):.4f}")
            print(f"    Std:    {np.std(ds):.4f}")
            print(f"    Min:    {np.min(ds):.4f}")
            print(f"    Max:    {np.max(ds):.4f}")
    
    return deltas_all, deltas_by_sum


# ================================================================================
# TEST 3: ALTERNATING FAILURE STRUCTURE ANALYSIS
# ================================================================================

def test_3_alternating_failure_structure(model):
    """
    Detailed position-by-position analysis of alternating pattern failure.
    Track both digit and carry separately.
    """
    
    print("\n" + "="*80)
    print("TEST 3: ALTERNATING FAILURE STRUCTURE ANALYSIS")
    print("="*80)
    print("\nDetailed trace of alternating pattern (a=[9,0,9,0,...], b=[1,0,1,0,...])\n")
    
    length = 100
    a = [9 if i % 2 == 0 else 0 for i in range(length)]
    b = [1 if i % 2 == 0 else 0 for i in range(length)]
    
    model.eval()
    carry = 0
    
    digit_correct_even = 0
    digit_correct_odd = 0
    digit_count_even = 0
    digit_count_odd = 0
    
    carry_correct_even = 0
    carry_correct_odd = 0
    carry_count_even = 0
    carry_count_odd = 0
    
    trace_data = []
    
    with torch.no_grad():
        for i in range(length):
            a_t = torch.LongTensor([a[i]]).to(device)
            b_t = torch.LongTensor([b[i]]).to(device)
            carry_t = torch.FloatTensor([carry]).to(device)
            
            sum_pred, sum_int, digit_pred, carry_out = model.forward_with_logic(a_t, b_t, carry_t)
            
            total_sum = a[i] + b[i] + carry
            digit_true = total_sum % 10
            carry_true = 1 if total_sum >= 10 else 0
            
            digit_match = digit_pred.item() == digit_true
            carry_match = carry_out.item() == carry_true
            
            trace_data.append({
                'pos': i,
                'a': a[i],
                'b': b[i],
                'carry_in': int(carry),
                'sum_true': total_sum,
                'sum_pred': sum_pred.item(),
                'sum_int': int(sum_int.item()),
                'digit_pred': int(digit_pred.item()),
                'digit_true': digit_true,
                'carry_pred': int(carry_out.item()),
                'carry_true': carry_true,
                'digit_correct': digit_match,
                'carry_correct': carry_match,
            })
            
            # Track by position parity
            if i % 2 == 0:  # Even positions
                digit_count_even += 1
                carry_count_even += 1
                if digit_match:
                    digit_correct_even += 1
                if carry_match:
                    carry_correct_even += 1
            else:  # Odd positions
                digit_count_odd += 1
                carry_count_odd += 1
                if digit_match:
                    digit_correct_odd += 1
                if carry_match:
                    carry_correct_odd += 1
            
            carry = carry_out.item()
    
    # Print first 30 positions
    print("First 30 positions trace:")
    print("pos | a | b | c_in | sum_true | sum_pred | s_int | d_pred | d_true | d_ok | c_pred | c_true | c_ok")
    print("-" * 110)
    
    for row in trace_data[:30]:
        print(f"{row['pos']:3d} | {row['a']} | {row['b']} |  {row['carry_in']}   |    {row['sum_true']:2d}    |  {row['sum_pred']:6.3f}  |  {row['sum_int']:2d}   |   {row['digit_pred']}    |   {row['digit_true']}     | {'✓' if row['digit_correct'] else '✗'} |   {row['carry_pred']}    |   {row['carry_true']}     | {'✓' if row['carry_correct'] else '✗'}")
    
    # Summary
    print("\n" + "-" * 80)
    print("\nACCURACY BY POSITION PARITY:")
    
    digit_acc_even = 100 * digit_correct_even / digit_count_even if digit_count_even > 0 else 0
    digit_acc_odd = 100 * digit_correct_odd / digit_count_odd if digit_count_odd > 0 else 0
    
    carry_acc_even = 100 * carry_correct_even / carry_count_even if carry_count_even > 0 else 0
    carry_acc_odd = 100 * carry_correct_odd / carry_count_odd if carry_count_odd > 0 else 0
    
    print(f"  Digit Accuracy (even positions [0,2,4,...]):  {digit_acc_even:6.2f}%")
    print(f"  Digit Accuracy (odd positions  [1,3,5,...]):  {digit_acc_odd:6.2f}%")
    print(f"  Carry Accuracy (even positions [0,2,4,...]):  {carry_acc_even:6.2f}%")
    print(f"  Carry Accuracy (odd positions  [1,3,5,...]):  {carry_acc_odd:6.2f}%")
    
    total_digit_correct = digit_correct_even + digit_correct_odd
    total_digit_count = digit_count_even + digit_count_odd
    print(f"\n  Overall Digit Accuracy: {100 * total_digit_correct / total_digit_count:.2f}%")
    
    total_carry_correct = carry_correct_even + carry_correct_odd
    total_carry_count = carry_count_even + carry_count_odd
    print(f"  Overall Carry Accuracy: {100 * total_carry_correct / total_carry_count:.2f}%")
    
    # Carry-only positions analysis
    carry_only_positions = [i for i in range(length) if a[i] == 0 and b[i] == 0]
    if carry_only_positions:
        carry_only_correct = sum(1 for i in carry_only_positions if trace_data[i]['digit_correct'])
        print(f"\n  Digit accuracy on CARRY-ONLY positions (a=0,b=0): {100 * carry_only_correct / len(carry_only_positions):.2f}%")
    
    return trace_data


# ================================================================================
# MAIN
# ================================================================================

def main():
    print("="*80)
    print("KILLER TEST: CARRY SENSITIVITY FOLLOW-UP INVESTIGATION")
    print("="*80)
    print()
    
    # Create model with killer test parameters
    model = create_killer_test_model(seed=42)
    
    # Run tests
    test_1_results = test_1_minimal_pair_intervention(model)
    test_2_deltas, test_2_by_sum = test_2_full_carry_sensitivity(model)
    test_3_trace = test_3_alternating_failure_structure(model)
    
    # Save results
    results_file = Path(__file__).parent.parent / "KILLER_TEST_FOLLOWUP_RESULTS.txt"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("KILLER TEST: CARRY SENSITIVITY FOLLOW-UP INVESTIGATION\n")
        f.write("="*80 + "\n\n")
        
        f.write("TEST 1: MINIMAL-PAIR RESULTS\n")
        f.write("-"*80 + "\n")
        for r in test_1_results:
            f.write(f"(a,b) = ({r['a']},{r['b']}) | {r['desc']}\n")
            f.write(f"  carry=0: sum={r['sum_pred_0']:.4f} digit={int(r['digit_0'])} carry={int(r['carry_out_0'])}\n")
            f.write(f"  carry=1: sum={r['sum_pred_1']:.4f} digit={int(r['digit_1'])} carry={int(r['carry_out_1'])}\n")
            f.write(f"  delta={r['delta_sum']:.4f} digit_changed={r['digit_changed']} carry_changed={r['carry_changed']}\n\n")
        
        f.write("\nTEST 2: FULL CARRY SWEEP RESULTS\n")
        f.write("-"*80 + "\n")
        f.write(f"Mean delta: {np.mean(test_2_deltas):.4f}\n")
        f.write(f"Std delta:  {np.std(test_2_deltas):.4f}\n")
        f.write(f"Min delta:  {np.min(test_2_deltas):.4f}\n")
        f.write(f"Max delta:  {np.max(test_2_deltas):.4f}\n")
    
    print(f"\n✅ Results saved to {results_file}")


if __name__ == "__main__":
    main()
