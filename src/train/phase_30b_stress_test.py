"""
================================================================================
PHASE 30b: STRESS TEST — LONG-RANGE COMPOSITIONAL GENERALIZATION
================================================================================

Question: Does strong compositional generalization (Phase 30) sustain beyond 20 digits?

Protocol:
- Train: lengths 2-5 (same as Phase 30)
- Test OOD: 30, 50, 100 digits
- Models: MLP, LSTM only (Transformer excluded after Phase 30)
- Trials: 3 (validation, not full benchmark)
- Metrics: digit_acc, carry_acc, exact_match

Goal: Determine if generalization holds, and where ceiling appears (if at all).

================================================================================
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from torch.utils.data import DataLoader, TensorDataset

# ============================================================================
# SETUP
# ============================================================================

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {DEVICE}\n")

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


def pad_sequences(sequences, max_length):
    """Pad sequences to max_length."""
    padded = []
    for a, b, d, c in sequences:
        a_pad = a + [0] * (max_length - len(a))
        b_pad = b + [0] * (max_length - len(b))
        d_pad = d + [0] * (max_length - len(d))
        c_pad = c + [0] * (max_length - len(c))
        padded.append((a_pad, b_pad, d_pad, c_pad, len(a)))
    
    return padded


def sequences_to_tensors(sequences, max_length=None):
    """Convert sequences to PyTorch tensors."""
    if max_length is None:
        max_length = max(len(a) for a, _, _, _, _ in sequences)
    
    a_tensor = torch.tensor([a for a, _, _, _, _ in sequences], dtype=torch.long)
    b_tensor = torch.tensor([b for _, b, _, _, _ in sequences], dtype=torch.long)
    d_tensor = torch.tensor([d for _, _, d, _, _ in sequences], dtype=torch.long)
    c_tensor = torch.tensor([c for _, _, _, c, _ in sequences], dtype=torch.long)
    lengths = torch.tensor([l for _, _, _, _, l in sequences], dtype=torch.long)
    
    return a_tensor, b_tensor, d_tensor, c_tensor, lengths


# ============================================================================
# MODELS (MLP, LSTM only)
# ============================================================================

class MLPSequenceArithmetic(nn.Module):
    """MLP: per-position with carry propagation"""
    def __init__(self, max_length):
        super().__init__()
        self.max_length = max_length
        self.embed_a = nn.Embedding(10, 8)
        self.embed_b = nn.Embedding(10, 8)
        self.fc1 = nn.Linear(8 + 8 + 2, 64)
        self.fc2 = nn.Linear(64, 32)
        self.digit_head = nn.Linear(32, 10)
        self.carry_head = nn.Linear(32, 2)
    
    def forward(self, a, b):
        batch_size = a.shape[0]
        a_emb = self.embed_a(a)
        b_emb = self.embed_b(b)
        
        digit_logits = []
        carry_logits = []
        
        carry_in = torch.zeros(batch_size, 2, device=a.device)
        carry_in[:, 0] = 1  # Start with carry=0
        
        for i in range(self.max_length):
            combined = torch.cat([a_emb[:, i, :], b_emb[:, i, :], carry_in], dim=1)
            h = torch.relu(self.fc1(combined))
            h = torch.relu(self.fc2(h))
            
            digit_logit = self.digit_head(h)
            carry_logit = self.carry_head(h)
            
            digit_logits.append(digit_logit)
            carry_logits.append(carry_logit)
            
            carry_in = torch.softmax(carry_logit, dim=1)
        
        digit_logits = torch.stack(digit_logits, dim=1)
        carry_logits = torch.stack(carry_logits, dim=1)
        
        return digit_logits, carry_logits


class LSTMSequenceArithmetic(nn.Module):
    """LSTM: sequential with carry propagation"""
    def __init__(self, max_length):
        super().__init__()
        self.max_length = max_length
        self.embed_a = nn.Embedding(10, 8)
        self.embed_b = nn.Embedding(10, 8)
        self.lstm = nn.LSTM(input_size=8 + 8 + 2, hidden_size=32, num_layers=2, batch_first=True)
        self.digit_head = nn.Linear(32, 10)
        self.carry_head = nn.Linear(32, 2)
    
    def forward(self, a, b):
        batch_size, max_len = a.shape
        a_emb = self.embed_a(a)
        b_emb = self.embed_b(b)
        
        # Process sequentially with dynamic carry propagation
        digit_logits_list = []
        carry_logits_list = []
        
        # LSTM state
        h, c = None, None
        
        carry_in = torch.zeros(batch_size, 2, device=a.device)
        carry_in[:, 0] = 1
        
        for i in range(max_len):
            # Combine embeddings with current carry
            combined = torch.cat([a_emb[:, i, :], b_emb[:, i, :], carry_in], dim=1)  # (batch, 18)
            combined = combined.unsqueeze(1)  # (batch, 1, 18)
            
            # LSTM step
            if h is None:
                lstm_out, (h, c) = self.lstm(combined)
            else:
                lstm_out, (h, c) = self.lstm(combined, (h, c))
            
            # Get predictions for this position
            digit_logit = self.digit_head(lstm_out.squeeze(1))  # (batch, 10)
            carry_logit = self.carry_head(lstm_out.squeeze(1))  # (batch, 2)
            
            digit_logits_list.append(digit_logit)
            carry_logits_list.append(carry_logit)
            
            # Update carry for next position
            carry_in = torch.softmax(carry_logit, dim=1)  # (batch, 2)
        
        # Stack results
        digit_logits = torch.stack(digit_logits_list, dim=1)  # (batch, max_length, 10)
        carry_logits = torch.stack(carry_logits_list, dim=1)  # (batch, max_length, 2)
        
        return digit_logits, carry_logits


# ============================================================================
# TRAINING & EVALUATION
# ============================================================================

def train_model(model, train_loader, epochs=30, lr=0.001):
    """Train model."""
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion_digit = nn.CrossEntropyLoss()
    criterion_carry = nn.CrossEntropyLoss()
    
    model.train()
    for epoch in range(epochs):
        for a, b, digit_true, carry_true in train_loader:
            a, b = a.to(DEVICE), b.to(DEVICE)
            digit_true, carry_true = digit_true.to(DEVICE), carry_true.to(DEVICE)
            
            digit_pred, carry_pred = model(a, b)
            
            loss_digit = criterion_digit(digit_pred.view(-1, 10), digit_true.view(-1))
            loss_carry = criterion_carry(carry_pred.view(-1, 2), carry_true.view(-1))
            loss = loss_digit + loss_carry
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


def evaluate_model(model, test_data_by_length):
    """Evaluate model on test sets by length."""
    model.eval()
    results = {}
    
    with torch.no_grad():
        for length, (a, b, digit_true, carry_true, lengths) in test_data_by_length.items():
            a, b = a.to(DEVICE), b.to(DEVICE)
            digit_true_t = digit_true.to(DEVICE)
            carry_true_t = carry_true.to(DEVICE)
            
            digit_pred, carry_pred = model(a, b)
            
            # Get predictions
            digit_pred_hard = digit_pred.argmax(dim=2)
            carry_pred_hard = carry_pred.argmax(dim=2)
            
            # Metrics by position
            digit_correct = (digit_pred_hard == digit_true_t).float()
            carry_correct = (carry_pred_hard == carry_true_t).float()
            combined_correct = (digit_correct * carry_correct)
            
            batch_size = a.shape[0]
            
            # Accuracy per sample
            digit_acc_list = []
            carry_acc_list = []
            
            for i in range(batch_size):
                actual_len = lengths[i].item()
                digit_acc = digit_correct[i, :actual_len].mean().item()
                carry_acc = carry_correct[i, :actual_len].mean().item()
                
                digit_acc_list.append(digit_acc)
                carry_acc_list.append(carry_acc)
            
            # Exact match at sequence level
            exact_match_list = [
                (digit_pred_hard[i, :lengths[i]] == digit_true_t[i, :lengths[i]]).all().item() and
                (carry_pred_hard[i, :lengths[i]] == carry_true_t[i, :lengths[i]]).all().item()
                for i in range(batch_size)
            ]
            
            results[length] = {
                'digit_acc': np.mean(digit_acc_list),
                'carry_acc': np.mean(carry_acc_list),
                'exact_match': np.mean(exact_match_list)
            }
    
    return results


# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def main():
    print("="*80)
    print("PHASE 30b: STRESS TEST — LONG-RANGE COMPOSITIONAL GENERALIZATION")
    print("="*80 + "\n")
    
    # Configuration
    train_lengths = [2, 3, 4, 5]
    test_lengths = [30, 50, 100]
    samples_per_length = 200
    max_length = 100
    batch_size = 32
    epochs = 30
    num_trials = 3
    
    architectures = [
        ('MLP', MLPSequenceArithmetic),
        ('LSTM', LSTMSequenceArithmetic)
    ]
    
    all_results = {}
    
    for arch_name, arch_class in architectures:
        print(f"\n{'='*80}")
        print(f"Testing {arch_name}...")
        print(f"{'='*80}\n")
        
        trial_results = {length: [] for length in test_lengths}
        
        for trial in range(1, num_trials + 1):
            print(f"Trial {trial}/{num_trials}", end=" ")
            
            # Generate training data
            train_seq = generate_multidigit_sequences(train_lengths, samples_per_length, seed=trial)
            
            # Generate test data by length
            test_seq_by_length = {}
            for length in test_lengths:
                test_seq = generate_multidigit_sequences([length], samples_per_length, seed=1000+trial)
                test_seq_by_length[length] = test_seq
            
            # Pad sequences
            train_seq_padded = pad_sequences(train_seq, max_length)
            test_seq_padded = {
                length: pad_sequences(test_seq_by_length[length], max_length)
                for length in test_lengths
            }
            
            # Convert to tensors
            a_train, b_train, d_train, c_train, _ = sequences_to_tensors(train_seq_padded, max_length)
            
            train_dataset = TensorDataset(a_train, b_train, d_train, c_train)
            train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
            
            # Initialize model
            model = arch_class(max_length).to(DEVICE)
            
            # Train
            train_model(model, train_loader, epochs=epochs)
            
            # Evaluate
            test_data_by_length = {
                length: sequences_to_tensors(test_seq_padded[length], max_length)
                for length in test_lengths
            }
            
            eval_results = evaluate_model(model, test_data_by_length)
            
            # Store results
            for length in test_lengths:
                trial_results[length].append(eval_results[length])
            
            print("✓")
        
        # Aggregate results
        aggregated = {}
        for length in test_lengths:
            digit_accs = [r['digit_acc'] for r in trial_results[length]]
            carry_accs = [r['carry_acc'] for r in trial_results[length]]
            exact_matches = [r['exact_match'] for r in trial_results[length]]
            
            aggregated[length] = {
                'digit_acc_mean': np.mean(digit_accs),
                'digit_acc_std': np.std(digit_accs),
                'carry_acc_mean': np.mean(carry_accs),
                'carry_acc_std': np.std(carry_accs),
                'exact_match_mean': np.mean(exact_matches),
                'exact_match_std': np.std(exact_matches)
            }
        
        all_results[arch_name] = aggregated
    
    # Print results
    print(f"\n{'='*80}")
    print("PHASE 30b: FINAL RESULTS")
    print(f"{'='*80}\n")
    
    for arch_name in ['MLP', 'LSTM']:
        print(f"\n{arch_name}:")
        print(f"{'Length':<8} {'Digit (±std)':<15} {'Carry (±std)':<15} {'Exact Match (±std)':<18}")
        print("-" * 60)
        
        results = all_results[arch_name]
        for length in sorted(results.keys()):
            r = results[length]
            digit_str = f"{r['digit_acc_mean']*100:>5.1f}±{r['digit_acc_std']*100:>4.1f}%"
            carry_str = f"{r['carry_acc_mean']*100:>5.1f}±{r['carry_acc_std']*100:>4.1f}%"
            exact_str = f"{r['exact_match_mean']*100:>5.1f}±{r['exact_match_std']*100:>4.1f}%"
            print(f"{length:<8} {digit_str:<15} {carry_str:<15} {exact_str:<18}")
    
    # Interpretation note
    print(f"\n{'='*80}")
    print("INTERPRETATION NOTE")
    print(f"{'='*80}")
    print("""
Note on exact_match decay:
Exact match = (digit_acc) ^ length

A small reduction in digit accuracy compounds exponentially over sequence length.
For example:
- digit_acc = 98% at length 30: exact_match ≈ 98%^30 ≈ 55%
- digit_acc = 95% at length 30: exact_match ≈ 95%^30 ≈ 21%
- digit_acc = 90% at length 100: exact_match ≈ 90%^100 ≈ 3%

This is expected behavior in compositional tasks, not a sign of failure.
    """)
    
    print(f"\n{'='*80}")
    print("PHASE 30b: STRESS TEST COMPLETE")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
