"""
================================================================================
PHASE 30 INTERROGATION: LOCAL ERROR STRUCTURE ANALYSIS
================================================================================

Focused interrogation protocol:
STEP 1: Reproduce official result (quick)
STEP 2: Extract local error structure by (a,b,carry_in) triples
STEP 3: Build local error table
STEP 4: Frequency masking analysis
STEP 5: Compare observed vs frequency-predicted accuracy
STEP 6: Adjacent-case interrogation for failure modes
STEP 7: Careful interpretation and classification

This script prioritizes rapid local error analysis over full training cycles.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from torch.utils.data import DataLoader, TensorDataset
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))
from models.residual_logic_adder import ResidualLogicAdder

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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


def create_residual_logic_model(seed=42):
    """Create and briefly train ResidualLogicAdder model."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    
    # Generate data
    train_sequences = generate_multidigit_sequences(
        lengths=[2, 3, 4, 5],
        num_samples_per_length=500,
        seed=seed
    )
    
    # Prepare for training
    def pad_sequences(sequences, max_length=5):
        padded = []
        for a, b, d, c in sequences:
            a_pad = a + [0] * (max_length - len(a))
            b_pad = b + [0] * (max_length - len(b))
            d_pad = d + [0] * (max_length - len(d))
            c_pad = c + [0] * (max_length - len(c))
            padded.append((a_pad, b_pad, d_pad, c_pad, len(a)))
        return padded
    
    padded_seqs = pad_sequences(train_sequences)
    
    # Create model
    model = ResidualLogicAdder().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.MSELoss()
    
    # Quick training: just 30 epochs (not 100)
    print("Training ResidualLogicAdder (30 epochs, quick pass)...")
    for epoch in range(30):
        model.train()
        total_loss = 0.0
        batch_size = 32
        
        for i in range(0, len(padded_seqs), batch_size):
            batch = padded_seqs[i:i+batch_size]
            batch_size_actual = len(batch)
            
            # Extract components
            a_list = [b[0] for b in batch]
            b_list = [b[1] for b in batch]
            d_list = [b[2] for b in batch]
            c_list = [b[3] for b in batch]
            lengths = [b[4] for b in batch]
            
            for pos in range(5):  # max_length
                a_pos = torch.LongTensor([a[pos] for a in a_list]).to(DEVICE)
                b_pos = torch.LongTensor([b[pos] for b in b_list]).to(DEVICE)
                d_true = torch.LongTensor([d[pos] for d in d_list]).float().to(DEVICE)
                c_in = torch.FloatTensor([c[pos] for c in c_list]).to(DEVICE)
                
                # Forward pass
                sum_pred = model(a_pos, b_pos, c_in)
                loss = criterion(sum_pred, d_true)
                
                total_loss += loss.item()
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1}/30")
    
    print("✅ Model trained\n")
    return model


def extract_local_error_structure(model, num_samples=10000, seed=42):
    """
    STEP 2-3: Extract local errors by (a,b,carry_in) triple.
    
    Build a dictionary where:
    key = (a, b, carry_in)
    value = {count, digit_acc, carry_pred_acc, sum_pred_stats}
    """
    
    print("\n" + "="*80)
    print("STEP 2-3: EXTRACT LOCAL ERROR STRUCTURE")
    print("="*80)
    
    model.eval()
    
    # Collect all local (a,b,c) triples and their outcomes
    local_results = {}  # key = (a,b,c), value = [outcomes]
    
    with torch.no_grad():
        for a in range(10):
            for b in range(10):
                for c in [0, 1]:
                    a_t = torch.LongTensor([a]).to(DEVICE)
                    b_t = torch.LongTensor([b]).to(DEVICE)
                    c_t = torch.FloatTensor([c]).to(DEVICE)
                    
                    # Forward pass
                    sum_pred = model(a_t, b_t, c_t).item()
                    
                    # Ground truth
                    sum_true = a + b + c
                    digit_true = sum_true % 10
                    carry_true = 1 if sum_true >= 10 else 0
                    
                    # Predictions (rounded)
                    digit_pred = int(round(sum_pred)) % 10
                    carry_pred = 1 if int(round(sum_pred)) >= 10 else 0
                    
                    # Store results
                    key = (a, b, c)
                    if key not in local_results:
                        local_results[key] = []
                    
                    local_results[key].append({
                        'sum_true': sum_true,
                        'sum_pred': sum_pred,
                        'digit_true': digit_true,
                        'digit_pred': digit_pred,
                        'digit_ok': digit_pred == digit_true,
                        'carry_true': carry_true,
                        'carry_pred': carry_pred,
                        'carry_ok': carry_pred == carry_true,
                    })
    
    return local_results


def build_local_error_table(local_results):
    """STEP 3: Build comprehensive local error table."""
    
    print("\n" + "="*80)
    print("STEP 3: LOCAL ERROR TABLE")
    print("="*80 + "\n")
    
    print("| a | b | c_in | sum_true | sum_pred | digit_ok | carry_ok | status")
    print("-" * 80)
    
    digit_failures = []
    carry_failures = []
    digit_success = 0
    
    for (a, b, c), outcomes in sorted(local_results.items()):
        outcome = outcomes[0]  # Single outcome per triple
        
        status = ""
        if not outcome['digit_ok']:
            status = "DIGIT FAIL"
            digit_failures.append((a, b, c, outcome))
        if not outcome['carry_ok']:
            status += " CARRY FAIL"
            carry_failures.append((a, b, c, outcome))
        if outcome['digit_ok'] and outcome['carry_ok']:
            status = "✓"
            digit_success += 1
        
        print(f"| {a} | {b} | {c:4d} | {outcome['sum_true']:8d} | {outcome['sum_pred']:8.4f} | {'✓' if outcome['digit_ok'] else '✗':8s} | {'✓' if outcome['carry_ok'] else '✗':8s} | {status}")
    
    print("\n" + "-"*80)
    print(f"Summary:")
    print(f"  Total local triples: {len(local_results)}")
    print(f"  Digit success: {digit_success}/200")
    print(f"  Digit failures: {len(digit_failures)}/200")
    print(f"  Carry failures: {len(carry_failures)}/200")
    
    return digit_failures, carry_failures


def frequency_masking_analysis(digit_failures):
    """STEP 4: Frequency analysis for each failure case."""
    
    print("\n" + "="*80)
    print("STEP 4: FREQUENCY MASKING ANALYSIS")
    print("="*80 + "\n")
    
    # For each failure case, count frequency in random data
    total_positions = 100000
    counted = 0
    
    for (a, b, c, outcome) in digit_failures:
        # Probability in random data: P(a) * P(b) * P(c)
        # a,b: uniform in [0,9] → 1/10 each
        # c: uniform in [0,1] → 1/2
        theoretical_prob = (1/10) * (1/10) * (1/2)  # = 0.005 = 0.5%
        expected_count = total_positions * theoretical_prob
        
        print(f"Failure case: (a={a}, b={b}, c={c})")
        print(f"  sum_true={outcome['sum_true']}, sum_pred={outcome['sum_pred']:.4f}")
        print(f"  Theoretical frequency: {theoretical_prob*100:.2f}% (expected {expected_count:.0f} positions in {total_positions})")
        print()
        counted += expected_count
    
    print(f"Total theoretical failure positions: {counted:.0f}/{total_positions}")
    print(f"Overall frequency: {(counted/total_positions)*100:.2f}%")
    print(f"Expected accuracy: {100 - (counted/total_positions)*100:.2f}%")
    
    return counted / total_positions


def adjacent_case_interrogation(model, digit_failures):
    """STEP 6: Test adjacent cases for each failure."""
    
    print("\n" + "="*80)
    print("STEP 6: ADJACENT-CASE INTERROGATION")
    print("="*80 + "\n")
    
    model.eval()
    
    for (fail_a, fail_b, fail_c, fail_outcome) in digit_failures[:3]:  # Check first 3 failures
        print(f"\nFailure case: (a={fail_a}, b={fail_b}, c={fail_c})")
        print(f"  Generates: sum_true={fail_outcome['sum_true']}, sum_pred={fail_outcome['sum_pred']:.4f}")
        print(f"  -> digit_pred={fail_outcome['digit_pred']} (should be {fail_outcome['digit_true']})")
        
        # Test adjacent cases
        print(f"\nAdjacent cases:")
        print("  | case        | sum_true | sum_pred | digit_ok |")
        print("  " + "-" * 46)
        
        adjacent_successes = 0
        adjacent_tests = 0
        
        # Generate nearby cases
        for da in [-1, 0, 1]:
            for db in [-1, 0, 1]:
                if da == 0 and db == 0:
                    continue  # Skip the failure case itself
                
                a = fail_a + da
                b = fail_b + db
                if a < 0 or a > 9 or b < 0 or b > 9:
                    continue
                
                adjacent_tests += 1
                
                with torch.no_grad():
                    a_t = torch.LongTensor([a]).to(DEVICE)
                    b_t = torch.LongTensor([b]).to(DEVICE)
                    c_t = torch.FloatTensor([fail_c]).to(DEVICE)
                    
                    sum_pred = model(a_t, b_t, c_t).item()
                    
                    sum_true = a + b + fail_c
                    digit_true = sum_true % 10
                    digit_pred = int(round(sum_pred)) % 10
                    digit_ok = digit_pred == digit_true
                    
                    if digit_ok:
                        adjacent_successes += 1
                    
                    print(f"  | ({a},{b},{fail_c})    | {sum_true:8d} | {sum_pred:8.4f} | {'✓' if digit_ok else '✗':8s} |")
        
        if adjacent_tests > 0:
            print(f"\n  Adjacent success rate: {adjacent_successes}/{adjacent_tests} = {100*adjacent_successes/adjacent_tests:.0f}%")


def main():
    print("\n" + "="*80)
    print("PHASE 30 INTERROGATION: LOCAL ERROR STRUCTURE ANALYSIS")
    print("="*80 + "\n")
    
    # STEP 0: Already completed (hypotheses in PHASE_30_INTERROGATION_STEP0.md)
    
    # STEP 1: Create and train model
    print("STEP 1: REPRODUCE OFFICIAL RESULT")
    print("-" * 80)
    model = create_residual_logic_model(seed=42)
    
    # STEP 2-3: Extract local error structure
    local_results = extract_local_error_structure(model)
    digit_failures, carry_failures = build_local_error_table(local_results)
    
    # STEP 4: Frequency masking analysis
    failure_freq = frequency_masking_analysis(digit_failures)
    
    # STEP 5: Compare observed vs frequency-predicted
    print("\n" + "="*80)
    print("STEP 5: FREQUENCY-PREDICTED vs OBSERVED ACCURACY")
    print("="*80)
    print(f"\nIf digits fail at frequency {failure_freq*100:.2f}%:")
    print(f"  Expected digit accuracy: {(1-failure_freq)*100:.2f}%")
    print(f"  Official Phase 30 (random sequences): 99.6%")
    print(f"  Match: {'✓ YES' if abs((1-failure_freq)*100 - 99.6) < 1 else '⚠ CHECK'}")
    
    # STEP 6: Adjacent-case interrogation
    if digit_failures:
        adjacent_case_interrogation(model, digit_failures)
    
    # STEP 7: Interpretation
    print("\n" + "="*80)
    print("STEP 7: INTERPRETATION")
    print("="*80)
    
    if len(digit_failures) == 0:
        print("\n✓ No local failures found in (a,b,carry_in) space")
        print("  This suggests failure modes are position-specific or sequence-specific,")
        print("  not local digit-pair specific.")
    else:
        print(f"\n✓ Found {len(digit_failures)} failing local cases")
        print(f"  These failures explain ~{failure_freq*100:.2f}% of overall error")
        print(f"  Consistent with {(1-failure_freq)*100:.1f}% expected accuracy")
        print(f"  Observed accuracy: 99.6%")
        
        if len(digit_failures) <= 5:
            print(f"\n  Failure mode: ISOLATED (similar to killer test with (0,0,1))")
        else:
            print(f"\n  Failure mode: DISTRIBUTED (multiple failure points)")


if __name__ == '__main__':
    main()
