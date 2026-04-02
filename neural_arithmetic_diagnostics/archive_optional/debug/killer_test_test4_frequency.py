"""
================================================================================
KILLER TEST: TEST 4 & FREQUENCY ANALYSIS
================================================================================

CRITICAL FOLLOW-UP:
1. Is failure ONLY at (0,0)? Or broader?
2. How often does (0,0,carry=1) appear in different distributions?

This bridges mechanism with distribution.
================================================================================
"""

import torch
import numpy as np
import random
import sys
import os
from pathlib import Path
from torch.utils.data import DataLoader

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from models.residual_logic_adder import ResidualLogicAdder

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def create_killer_test_model(seed=42):
    """Create model with killer test parameters"""
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    
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
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)
    mse_criterion = torch.nn.MSELoss()
    
    for epoch in range(100):
        model.train()
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
        
        scheduler.step()
    
    print("✅ Model trained\n")
    return model


# ================================================================================
# TEST 4: ADJACENT CASES
# ================================================================================

def test_4_adjacent_cases(model):
    """
    Test cases SIMILAR to (0,0,c=1) to see if failure is isolated or broader.
    
    Test pairs:
    - (0,0,1) ← the known failure
    - (0,1,0) ← b has signal
    - (1,0,0) ← a has signal
    - (0,2,0) ← stronger signal
    - (1,1,0) ← equal signal
    """
    
    print("\n" + "="*80)
    print("TEST 4: ADJACENT CASES (Is failure ONLY at (0,0)?)")
    print("="*80)
    print()
    
    test_cases = [
        (0, 0, 1, "carry-only (KNOWN FAILURE)"),
        (0, 0, 0, "zero everywhere"),
        (0, 1, 0, "b has signal, no carry"),
        (1, 0, 0, "a has signal, no carry"),
        (0, 1, 1, "b + carry, a=0"),
        (1, 0, 1, "a + carry, b=0"),
        (0, 2, 0, "stronger b signal"),
        (1, 1, 0, "equal a,b signal"),
    ]
    
    model.eval()
    results = []
    
    with torch.no_grad():
        for a, b, c, desc in test_cases:
            a_t = torch.LongTensor([a]).to(device)
            b_t = torch.LongTensor([b]).to(device)
            c_t = torch.FloatTensor([c]).to(device)
            
            sum_pred, sum_int, digit_pred, carry_pred = model.forward_with_logic(a_t, b_t, c_t)
            
            true_sum = a + b + c
            digit_true = true_sum % 10
            carry_true = 1 if true_sum >= 10 else 0
            
            digit_ok = digit_pred.item() == digit_true
            carry_ok = carry_pred.item() == carry_true
            
            results.append({
                'a': a, 'b': b, 'c': c, 'desc': desc,
                'sum_true': true_sum,
                'sum_pred': sum_pred.item(),
                'digit_true': digit_true,
                'digit_pred': int(digit_pred.item()),
                'carry_true': carry_true,
                'carry_pred': int(carry_pred.item()),
                'digit_ok': digit_ok,
                'carry_ok': carry_ok,
            })
    
    print("| a | b | c | Description              | sum_true | sum_pred | d_true | d_pred | d_ok | c_true | c_pred | c_ok")
    print("-" * 120)
    
    for r in results:
        print(f"| {r['a']} | {r['b']} | {r['c']} | {r['desc']:24s} | {r['sum_true']:8d} | {r['sum_pred']:8.4f} | {r['digit_true']:6d} | {r['digit_pred']:6d} | {'✓' if r['digit_ok'] else '✗':4s} | {r['carry_true']:6d} | {r['carry_pred']:6d} | {'✓' if r['carry_ok'] else '✗':4s}")
    
    # Summary
    digit_fails = [r for r in results if not r['digit_ok']]
    carry_fails = [r for r in results if not r['carry_ok']]
    
    print("\n" + "-" * 80)
    print(f"\nDigit failures: {len(digit_fails)}/{len(results)}")
    for r in digit_fails:
        print(f"  ({r['a']},{r['b']},{r['c']}): predicted digit {r['digit_pred']} instead of {r['digit_true']}")
    
    print(f"\nCarry failures: {len(carry_fails)}/{len(results)}")
    for r in carry_fails:
        print(f"  ({r['a']},{r['b']},{r['c']}): predicted carry {r['carry_pred']} instead of {r['carry_true']}")
    
    return results


# ================================================================================
# FREQUENCY ANALYSIS
# ================================================================================

def frequency_analysis():
    """
    Count frequency of (a=0, b=0, carry=1) in different distributions.
    
    This explains why random data reaches 99.6% but alternating hits 50%.
    """
    
    print("\n" + "="*80)
    print("FREQUENCY ANALYSIS: How often does (0,0,carry=1) appear?")
    print("="*80)
    print()
    
    # =========================================================================
    # 1. TRAINING DATA (random)
    # =========================================================================
    print("1. TRAINING DATA (multidigit random sequences)")
    print("-" * 80)
    
    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)
    
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
    
    train_sequences = generate_multidigit_sequences(
        lengths=[2, 3, 4, 5],
        num_samples_per_length=500,
        seed=42
    )
    
    train_count_zero_zero_carry = 0
    train_total = 0
    
    for a_seq, b_seq, sum_seq in train_sequences:
        carry = 0
        for i in range(len(a_seq)):
            if a_seq[i] == 0 and b_seq[i] == 0 and carry == 1:
                train_count_zero_zero_carry += 1
            train_total += 1
            total = a_seq[i] + b_seq[i] + carry
            carry = 1 if total >= 10 else 0
    
    train_freq = 100 * train_count_zero_zero_carry / train_total if train_total > 0 else 0
    print(f"Total digit positions: {train_total}")
    print(f"Positions with (a=0, b=0, carry=1): {train_count_zero_zero_carry}")
    print(f"Frequency: {train_freq:.4f}%")
    
    # =========================================================================
    # 2. RANDOM TEST DATA
    # =========================================================================
    print("\n2. RANDOM TEST DATA (pure random, no sequential dependency)")
    print("-" * 80)
    
    # Pure random: sample (a,b,carry) independently
    num_random_samples = 100000
    random_count_zero_zero_carry = 0
    
    for _ in range(num_random_samples):
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        carry = random.randint(0, 1)
        
        if a == 0 and b == 0 and carry == 1:
            random_count_zero_zero_carry += 1
    
    random_freq = 100 * random_count_zero_zero_carry / num_random_samples
    print(f"Total samples: {num_random_samples}")
    print(f"Samples with (a=0, b=0, carry=1): {random_count_zero_zero_carry}")
    print(f"Frequency: {random_freq:.4f}%")
    print(f"Expected (theoretical): (1/10) * (1/10) * (1/2) = 0.5%")
    
    # =========================================================================
    # 3. ALTERNATING PATTERN
    # =========================================================================
    print("\n3. ALTERNATING PATTERN")
    print("-" * 80)
    
    length = 100
    a_alt = [9 if i % 2 == 0 else 0 for i in range(length)]
    b_alt = [1 if i % 2 == 0 else 0 for i in range(length)]
    
    alt_count_zero_zero_carry = 0
    alt_total = 0
    
    carry = 0
    for i in range(length):
        if a_alt[i] == 0 and b_alt[i] == 0 and carry == 1:
            alt_count_zero_zero_carry += 1
        alt_total += 1
        total = a_alt[i] + b_alt[i] + carry
        carry = 1 if total >= 10 else 0
    
    alt_freq = 100 * alt_count_zero_zero_carry / alt_total if alt_total > 0 else 0
    print(f"Total positions: {alt_total}")
    print(f"Positions with (a=0, b=0, carry=1): {alt_count_zero_zero_carry}")
    print(f"Frequency: {alt_freq:.4f}%")
    print(f"Expected (given pattern): 50% (every odd position)")
    
    # =========================================================================
    # 4. COMPARATIVE SUMMARY
    # =========================================================================
    print("\n" + "="*80)
    print("FREQUENCY COMPARISON")
    print("="*80)
    
    print(f"\nCase (a=0, b=0, carry=1) frequency:")
    print(f"  Training data (multidigit):  {train_freq:7.4f}%")
    print(f"  Random test data:             {random_freq:7.4f}%")
    print(f"  Alternating pattern:          {alt_freq:7.4f}%")
    
    print(f"\nRatio (alternating / random): {alt_freq / random_freq:.1f}x")
    
    print(f"\n📊 INTERPRETATION:")
    print(f"  → Random data has ~{random_freq:.2f}% of positions that should fail")
    print(f"  → Alternating pattern has ~{alt_freq:.2f}% of positions that should fail")
    print(f"  → If these failures affect digit accuracy proportionally...")
    print(f"     Expected digit accuracy on random:     ~{100 - random_freq:.1f}%")
    print(f"     Expected digit accuracy on alternating: ~{100 - alt_freq:.1f}%")
    print(f"  → Actual observed: 99.6% random, 50% alternating")
    print(f"     Ratio explained: ({alt_freq:.1f}% / {random_freq:.4f}%) ≈ {alt_freq / random_freq:.0f}x difference")


# ================================================================================
# MAIN
# ================================================================================

def main():
    print("="*80)
    print("KILLER TEST: TEST 4 & FREQUENCY ANALYSIS")
    print("="*80)
    print()
    
    # Create model
    model = create_killer_test_model(seed=42)
    
    # Test 4
    test_4_results = test_4_adjacent_cases(model)
    
    # Frequency analysis
    frequency_analysis()
    
    # Save results
    results_file = Path(__file__).parent.parent / "KILLER_TEST_TEST4_FREQUENCY_RESULTS.txt"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("KILLER TEST: TEST 4 & FREQUENCY ANALYSIS RESULTS\n")
        f.write("="*80 + "\n\n")
        
        f.write("TEST 4 RESULTS:\n")
        f.write("-"*80 + "\n")
        for r in test_4_results:
            f.write(f"({r['a']},{r['b']},{r['c']}) - {r['desc']}\n")
            f.write(f"  sum: true={r['sum_true']}, pred={r['sum_pred']:.4f}\n")
            f.write(f"  digit: true={r['digit_true']}, pred={r['digit_pred']}, ok={r['digit_ok']}\n")
            f.write(f"  carry: true={r['carry_true']}, pred={r['carry_pred']}, ok={r['carry_ok']}\n\n")
    
    print(f"\n✅ Results saved to {results_file}")


if __name__ == "__main__":
    main()
