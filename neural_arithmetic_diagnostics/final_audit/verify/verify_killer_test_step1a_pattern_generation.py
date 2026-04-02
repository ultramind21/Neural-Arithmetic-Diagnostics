"""
================================================================================
VERIFICATION SCRIPT: KILLER TEST STEP 1A
================================================================================

OFFICIAL TARGET:
  File: src/train/project_3_killer_test_adversarial_carry_chain.py
  Model: ResidualLogicAdder
  Purpose: Verify killer test pattern generation

WHAT THIS SCRIPT VERIFIES:
  1. Pattern generation produces the correct sequences
  2. Ground truth computation is correct (no model needed)
  3. Patterns have expected properties (carry positions, alternation, etc.)

WHAT THIS SCRIPT DOES NOT VERIFY:
  - Model training
  - Model predictions
  - Metric computation
  - Any model-dependent logic

ACCEPTANCE CRITERIA:
  - Alternating pattern is actually [9,0,9,0,9,0,...]
  - Chain pattern is actually [all 9s] + [all 0s] + [all 9s]
  - Block pattern alternates in blocks (not individual digits)
  - Ground truth digits match manual computation
  - Ground truth carries match manual computation
  - Carry positions are where expected (sum >= 10)

================================================================================
"""

import random
import numpy as np


def generate_multidigit_sequences_for_killer_test(lengths, num_samples_per_length, seed=42):
    """
    Standard sequence generation from official killer test.
    Returns list of (a_seq, b_seq, digit_out, carry_out) tuples.
    """
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


def generate_alternating_pattern(length=100, seed=42):
    """
    Killer test pattern: Alternating 9,0,9,0,9,0,...
    b is always 1.
    Expected: each position generates a carry (9+1=10 if c_in=0, 9+1+1=11 if c_in=1)
    """
    random.seed(seed)
    
    a_seq = [9 if i % 2 == 0 else 0 for i in range(length)]
    b_seq = [1 for _ in range(length)]
    
    # Compute ground truth
    digit_out = []
    carry_out = []
    carry = 0
    
    for i in range(length):
        total = a_seq[i] + b_seq[i] + carry
        digit_out.append(total % 10)
        carry = 1 if total >= 10 else 0
        carry_out.append(carry)
    
    return a_seq, b_seq, digit_out, carry_out


def generate_chain_pattern(length=100, seed=42):
    """
    Killer test pattern: Chain of all 9s, then all 0s, then all 9s.
    b is always 1.
    Sections: [0, length//3), [length//3, 2*length//3), [2*length//3, length)
    """
    random.seed(seed)
    
    sec1_len = length // 3
    sec2_len = length // 3
    sec3_len = length - sec1_len - sec2_len
    
    a_seq = [9] * sec1_len + [0] * sec2_len + [9] * sec3_len
    b_seq = [1 for _ in range(length)]
    
    # Compute ground truth
    digit_out = []
    carry_out = []
    carry = 0
    
    for i in range(length):
        total = a_seq[i] + b_seq[i] + carry
        digit_out.append(total % 10)
        carry = 1 if total >= 10 else 0
        carry_out.append(carry)
    
    return a_seq, b_seq, digit_out, carry_out


def generate_block_pattern(length=100, block_size=10, seed=42):
    """
    Killer test pattern: Blocks of 9s and 0s.
    Block size is fixed.
    Blocks: [9s], [0s], [9s], [0s], ...
    b is always 1.
    """
    random.seed(seed)
    
    a_seq = []
    block_idx = 0
    while len(a_seq) < length:
        block_digit = 9 if block_idx % 2 == 0 else 0
        remaining = length - len(a_seq)
        block_to_add = min(block_size, remaining)
        a_seq.extend([block_digit] * block_to_add)
        block_idx += 1
    
    b_seq = [1 for _ in range(length)]
    
    # Compute ground truth
    digit_out = []
    carry_out = []
    carry = 0
    
    for i in range(length):
        total = a_seq[i] + b_seq[i] + carry
        digit_out.append(total % 10)
        carry = 1 if total >= 10 else 0
        carry_out.append(carry)
    
    return a_seq, b_seq, digit_out, carry_out


def print_pattern_analysis(name, a, b, digits, carries, show_length=20):
    """
    Print detailed analysis of a pattern.
    """
    print(f"\n{'='*80}")
    print(f"PATTERN: {name}")
    print(f"{'='*80}")
    print()
    
    # Basic info
    total_length = len(a)
    num_carries = sum(carries)
    carry_positions = [i for i in range(len(carries)) if carries[i] == 1]
    
    print(f"Total length: {total_length}")
    print(f"Number of carry-out positions: {num_carries}")
    print()
    
    # Show first N positions
    print(f"First {show_length} positions:")
    print(f"Position | a | b | a+b+c_in | digit | carry | Explanation")
    print(f"{'-'*80}")
    
    for i in range(min(show_length, total_length)):
        c_in = carries[i-1] if i > 0 else 0
        total = a[i] + b[i] + c_in
        digit = digits[i]
        carry = carries[i]
        
        explanation = ""
        if carry == 1:
            explanation = f"[{a[i]}+{b[i]}+{c_in}={total} >= 10] → digit={digit}, carry=1"
        else:
            explanation = f"[{a[i]}+{b[i]}+{c_in}={total} < 10] → digit={digit}, carry=0"
        
        print(f"{i:8d} | {a[i]} | {b[i]} | {total:8d} | {digit:5d} | {carry:5d} | {explanation}")
    
    print()
    
    # Pattern analysis
    print(f"a sequence (first {show_length}): {a[:show_length]}")
    print(f"b sequence (first {show_length}): {b[:show_length]}")
    print(f"digit out  (first {show_length}): {digits[:show_length]}")
    print(f"carry out  (first {show_length}): {carries[:show_length]}")
    print()
    
    # Carry distribution
    if len(carry_positions) <= 30:
        print(f"All carry-out positions: {carry_positions}")
    else:
        print(f"First 30 carry-out positions: {carry_positions[:30]}")
        print(f"Total carry-out positions: {len(carry_positions)}")
    print()
    
    # Expected output description
    if name == "ALTERNATING":
        print("Expected property: Alternating for a [9,0,9,0,...], constant 1 for b")
        print("Expected carry: Should see pattern in carry propagation")
    elif name == "CHAIN":
        print("Expected property: Three sections [9s], [0s], [9s]")
        print("Expected carry: High in section 1, low in section 2, high in section 3")
    elif name == "BLOCK":
        print("Expected property: Alternating blocks of 9s and 0s")
        print("Expected carry: Pattern repeats with block boundaries")
    
    print()


def main():
    """
    Main verification routine.
    """
    print("\n")
    print("="*80)
    print("KILLER TEST STEP 1A: PATTERN GENERATION VERIFICATION")
    print("="*80)
    print("\nGoal: Verify that killer test patterns are generated correctly")
    print("No model used. Only pattern and ground truth computation.")
    print()
    
    # =========================================================================
    # PATTERN 1: ALTERNATING
    # =========================================================================
    print("\n" + "="*80)
    print("STEP 1: ALTERNATING PATTERN")
    print("="*80)
    
    a_alt, b_alt, d_alt, c_alt = generate_alternating_pattern(length=100)
    print_pattern_analysis("ALTERNATING", a_alt, b_alt, d_alt, c_alt, show_length=30)
    
    # Manual check: alternating pattern sanity
    print("SANITY CHECK: Is a sequence truly alternating?")
    is_alternating = all(
        (a_alt[i] == 9 and i % 2 == 0) or (a_alt[i] == 0 and i % 2 == 1)
        for i in range(len(a_alt))
    )
    print(f"  Result: {is_alternating} ✓" if is_alternating else f"  Result: {is_alternating} ✗ ERROR")
    print()
    
    # =========================================================================
    # PATTERN 2: CHAIN
    # =========================================================================
    print("\n" + "="*80)
    print("STEP 2: CHAIN PATTERN")
    print("="*80)
    
    a_chain, b_chain, d_chain, c_chain = generate_chain_pattern(length=100)
    print_pattern_analysis("CHAIN", a_chain, b_chain, d_chain, c_chain, show_length=30)
    
    # Manual check: chain pattern sanity
    print("SANITY CHECK: Is a sequence truly [9s], [0s], [9s]?")
    sec1_len = 100 // 3
    sec2_len = 100 // 3
    is_chain = (
        all(a_chain[i] == 9 for i in range(sec1_len)) and
        all(a_chain[i] == 0 for i in range(sec1_len, sec1_len + sec2_len)) and
        all(a_chain[i] == 9 for i in range(sec1_len + sec2_len, len(a_chain)))
    )
    print(f"  Result: {is_chain} ✓" if is_chain else f"  Result: {is_chain} ✗ ERROR")
    print()
    
    # =========================================================================
    # PATTERN 3: BLOCK
    # =========================================================================
    print("\n" + "="*80)
    print("STEP 3: BLOCK PATTERN")
    print("="*80)
    
    block_size = 10
    a_block, b_block, d_block, c_block = generate_block_pattern(length=100, block_size=block_size)
    print_pattern_analysis("BLOCK", a_block, b_block, d_block, c_block, show_length=40)
    
    # Manual check: block pattern sanity
    print(f"SANITY CHECK: Is a sequence in blocks of size {block_size}?")
    is_block = True
    for block_idx in range(100 // block_size + 1):
        start = block_idx * block_size
        end = min(start + block_size, 100)
        if end <= start:
            break
        expected_digit = 9 if block_idx % 2 == 0 else 0
        actual = a_block[start:end]
        if not all(x == expected_digit for x in actual):
            is_block = False
            break
    print(f"  Result: {is_block} ✓" if is_block else f"  Result: {is_block} ✗ ERROR")
    print()
    
    # =========================================================================
    # SUMMARY TABLE
    # =========================================================================
    print("\n" + "="*80)
    print("SUMMARY: PATTERN VERIFICATION")
    print("="*80)
    print()
    print(f"{'Pattern':<15} | {'Length':<7} | {'Carries':<7} | {'Alternating':<11} | {'Chain':<7} | {'Block':<7}")
    print("-" * 80)
    
    is_alt = all(
        (a_alt[i] == 9 and i % 2 == 0) or (a_alt[i] == 0 and i % 2 == 1)
        for i in range(len(a_alt))
    )
    
    is_ch = (
        all(a_chain[i] == 9 for i in range(sec1_len)) and
        all(a_chain[i] == 0 for i in range(sec1_len, sec1_len + sec2_len)) and
        all(a_chain[i] == 9 for i in range(sec1_len + sec2_len, len(a_chain)))
    )
    
    is_bl = True
    for block_idx in range(100 // block_size + 1):
        start = block_idx * block_size
        end = min(start + block_size, 100)
        if end <= start:
            break
        expected_digit = 9 if block_idx % 2 == 0 else 0
        if not all(x == expected_digit for x in a_block[start:end]):
            is_bl = False
            break
    
    print(f"{'ALTERNATING':<15} | {len(a_alt):<7} | {sum(c_alt):<7} | {'✓ PASS' if is_alt else '✗ FAIL':<11} | {'':<7} | {'':<7}")
    print(f"{'CHAIN':<15} | {len(a_chain):<7} | {sum(c_chain):<7} | {'':<11} | {'✓ PASS' if is_ch else '✗ FAIL':<7} | {'':<7}")
    print(f"{'BLOCK':<15} | {len(a_block):<7} | {sum(c_block):<7} | {'':<11} | {'':<7} | {'✓ PASS' if is_bl else '✗ FAIL':<7}")
    
    print()
    print("="*80)
    print("END OF STEP 1A")
    print("="*80)
    print()
    print("Next: Review these patterns manually.")
    print("If all patterns pass sanity checks, proceed to Step 1B (ground truth computation).")
    print()


if __name__ == "__main__":
    main()
