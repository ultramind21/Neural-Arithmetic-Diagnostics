"""
================================================================================
PHASE 30: COMPOSITIONAL MULTI-DIGIT ARITHMETIC GENERALIZATION
================================================================================

Question: Do digit-pair generalization insights transfer to multi-digit sequences?

Protocol:
- Train: lengths 2-5
- Test in-distribution: 2-5
- Test OOD: 6, 8, 10, 15, 20

Models: MLP (baseline), LSTM, Transformer
Metrics: digit_acc, carry_acc, exact_match, by_length

Decision: Execute only Phase 30, then hard stop. No Phase 31.

================================================================================
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

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
    
    Input: sequences of (a_i, b_i) pairs
    Output: (digit_i, carry_i) for each position
    
    Returns:
        sequences: list of (a_seq, b_seq, digit_out, carry_out)
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


def pad_sequences(sequences, max_length):
    """Pad sequences to max_length."""
    padded = []
    for a, b, d, c in sequences:
        a_pad = a + [0] * (max_length - len(a))  # pad with 0
        b_pad = b + [0] * (max_length - len(b))
        d_pad = d + [0] * (max_length - len(d))
        c_pad = c + [0] * (max_length - len(c))
        
        # Also store the original length for masking
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
# MODELS
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
        # a, b: (batch, max_length, 10-class indices)
        batch_size = a.shape[0]
        
        a_emb = self.embed_a(a)  # (batch, max_length, 8)
        b_emb = self.embed_b(b)  # (batch, max_length, 8)
        
        digit_logits = []
        carry_logits = []
        
        # Process sequentially with carry propagation
        carry_in = torch.zeros(batch_size, 2, device=a.device)  # (batch, 2) one-hot-like
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
            carry_in = torch.softmax(carry_logit, dim=1)  # (batch, 2) probabilities
        
        digit_logits = torch.stack(digit_logits, dim=1)  # (batch, max_length, 10)
        carry_logits = torch.stack(carry_logits, dim=1)  # (batch, max_length, 2)
        
        return digit_logits, carry_logits


class LSTMSequenceArithmetic(nn.Module):
    """LSTM: sequence-aware model with carry propagation"""
    def __init__(self, max_length):
        super().__init__()
        self.max_length = max_length
        self.embed_a = nn.Embedding(10, 8)
        self.embed_b = nn.Embedding(10, 8)
        
        # Include carry_in (2-dim one-hot-like) in input
        self.lstm = nn.LSTM(input_size=8 + 8 + 2, hidden_size=32, num_layers=2, batch_first=True)
        
        self.digit_head = nn.Linear(32, 10)
        self.carry_head = nn.Linear(32, 2)
    
    def forward(self, a, b):
        # a, b: (batch, max_length)
        batch_size, max_len = a.shape
        
        a_emb = self.embed_a(a)  # (batch, max_length, 8)
        b_emb = self.embed_b(b)  # (batch, max_length, 8)
        
        # Process sequentially with dynamic carry propagation
        digit_logits_list = []
        carry_logits_list = []
        
        # LSTM state
        h, c = None, None
        
        carry_in = torch.zeros(batch_size, 2, device=a.device)
        carry_in[:, 0] = 1  # Start with carry=0
        
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


class TransformerSequenceArithmetic(nn.Module):
    """Transformer: attention-based model with carry propagation"""
    def __init__(self, max_length):
        super().__init__()
        self.max_length = max_length
        self.embed_a = nn.Embedding(10, 8)
        self.embed_b = nn.Embedding(10, 8)
        
        # Include carry_in (2-dim) in input
        self.attn = nn.MultiheadAttention(embed_dim=18, num_heads=3, batch_first=True)
        self.fc = nn.Linear(18, 32)
        
        self.digit_head = nn.Linear(32, 10)
        self.carry_head = nn.Linear(32, 2)
    
    def forward(self, a, b):
        # a, b: (batch, max_length)
        batch_size, max_len = a.shape
        
        a_emb = self.embed_a(a)  # (batch, max_length, 8)
        b_emb = self.embed_b(b)  # (batch, max_length, 8)
        
        # Process sequentially with carry propagation (like LSTM)
        digit_logits_list = []
        carry_logits_list = []
        
        carry_in = torch.zeros(batch_size, 2, device=a.device)
        carry_in[:, 0] = 1  # Start with carry=0
        
        for i in range(max_len):
            # Combine embeddings with carry_in
            combined = torch.cat([a_emb[:, i, :], b_emb[:, i, :], carry_in], dim=1)
            combined = combined.unsqueeze(1)  # (batch, 1, 18)
            
            # Apply attention (self-attention on single position for feature extraction)
            attn_out, _ = self.attn(combined, combined, combined)
            h = torch.relu(self.fc(attn_out))  # (batch, 1, 32)
            
            digit_logits = self.digit_head(h)  # (batch, 1, 10)
            carry_logits = self.carry_head(h)  # (batch, 1, 2)
            
            digit_logits_list.append(digit_logits.squeeze(1))
            carry_logits_list.append(carry_logits.squeeze(1))
            
            # Update carry_in for next position
            carry_in = carry_logits.squeeze(1).detach()
        
        # Stack results back to (batch, max_length, *)
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
        total_loss = 0
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
            
            total_loss += loss.item()


def evaluate_model(model, test_data_by_length):
    """
    Evaluate model on test sets.
    
    Returns metrics organized by length.
    """
    model.eval()
    results = {}
    
    with torch.no_grad():
        for length, (a, b, digit_true, carry_true, lengths) in test_data_by_length.items():
            a, b = a.to(DEVICE), b.to(DEVICE)
            digit_true_t = digit_true.to(DEVICE)
            carry_true_t = carry_true.to(DEVICE)
            
            digit_pred, carry_pred = model(a, b)
            
            # Get predictions
            digit_pred_hard = digit_pred.argmax(dim=2)  # (batch, max_length)
            carry_pred_hard = carry_pred.argmax(dim=2)  # (batch, max_length)
            
            # Metrics by position
            digit_correct = (digit_pred_hard == digit_true_t).float()
            carry_correct = (carry_pred_hard == carry_true_t).float()
            combined_correct = (digit_correct * carry_correct)
            
            # Aggregate
            batch_size = a.shape[0]
            
            # Accuracy per length (only at positions < length)
            digit_acc_list = []
            carry_acc_list = []
            combined_acc_list = []
            
            for i in range(batch_size):
                actual_len = lengths[i].item()
                digit_acc = digit_correct[i, :actual_len].mean().item()
                carry_acc = carry_correct[i, :actual_len].mean().item()
                combined_acc = combined_correct[i, :actual_len].mean().item()
                
                digit_acc_list.append(digit_acc)
                carry_acc_list.append(carry_acc)
                combined_acc_list.append(combined_acc)
            
            # Exact match at sequence level
            exact_match_list = [
                (digit_pred_hard[i, :lengths[i]] == digit_true_t[i, :lengths[i]]).all().item() and
                (carry_pred_hard[i, :lengths[i]] == carry_true_t[i, :lengths[i]]).all().item()
                for i in range(batch_size)
            ]
            
            results[length] = {
                'digit_acc': np.mean(digit_acc_list),
                'carry_acc': np.mean(carry_acc_list),
                'combined_acc': np.mean(combined_acc_list),
                'exact_match': np.mean(exact_match_list)
            }
    
    return results


# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def main():
    print("="*80)
    print("PHASE 30: COMPOSITIONAL MULTI-DIGIT ARITHMETIC GENERALIZATION")
    print("="*80 + "\n")
    
    # Hyperparameters
    train_lengths = [2, 3, 4, 5]
    test_lengths = [2, 3, 4, 5, 6, 8, 10, 15, 20]
    samples_per_length = 1000
    max_length = 20
    batch_size = 32
    epochs = 30
    num_trials = 5  # Fewer trials for speed (Phase 30 is exploratory)
    
    architectures = [
        ('MLP', MLPSequenceArithmetic),
        ('LSTM', LSTMSequenceArithmetic),
        ('Transformer', TransformerSequenceArithmetic)
    ]
    
    all_results = {}
    
    for arch_name, arch_class in architectures:
        print(f"\n{'='*80}")
        print(f"Testing {arch_name}...")
        print(f"{'='*80}\n")
        
        trial_results = {length: [] for length in test_lengths}
        
        for trial in range(1, num_trials + 1):
            print(f"Trial {trial}/{num_trials}")
            
            # Generate data
            train_seq = generate_multidigit_sequences(train_lengths, samples_per_length)
            
            test_seq_by_length = {}
            for length in test_lengths:
                test_seq = generate_multidigit_sequences([length], 200)
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
            
            # Create model
            model = arch_class(max_length).to(DEVICE)
            
            # Train
            train_model(model, train_loader, epochs=epochs)
            
            # Evaluate
            test_data_tensors = {}
            for length in test_lengths:
                a_test, b_test, d_test, c_test, lengths = sequences_to_tensors(
                    test_seq_padded[length], max_length
                )
                test_data_tensors[length] = (a_test, b_test, d_test, c_test, lengths)
            
            eval_results = evaluate_model(model, test_data_tensors)
            
            # Store results
            for length, metrics in eval_results.items():
                trial_results[length].append(metrics)
            
            if trial % 2 == 0:
                print(f"  Trial {trial}: In-dist=", end="")
                for l in train_lengths:
                    print(f"{l}→{eval_results[l]['exact_match']:.1%} ", end="")
                print(f"| OOD→", end="")
                for l in [6, 10, 20]:
                    if l in eval_results:
                        print(f"{l}→{eval_results[l]['exact_match']:.1%} ", end="")
                print()
        
        # Aggregate results across trials
        aggregated = {}
        for length in test_lengths:
            metrics_list = trial_results[length]
            
            digit_accs = [m['digit_acc'] for m in metrics_list]
            carry_accs = [m['carry_acc'] for m in metrics_list]
            combined_accs = [m['combined_acc'] for m in metrics_list]
            exact_matches = [m['exact_match'] for m in metrics_list]
            
            aggregated[length] = {
                'digit_acc': np.mean(digit_accs),
                'digit_std': np.std(digit_accs),
                'carry_acc': np.mean(carry_accs),
                'carry_std': np.std(carry_accs),
                'combined_acc': np.mean(combined_accs),
                'combined_std': np.std(combined_accs),
                'exact_match': np.mean(exact_matches),
                'exact_match_std': np.std(exact_matches)
            }
        
        all_results[arch_name] = aggregated
    
    # Print summary
    print(f"\n{'='*80}")
    print("PHASE 30: FINAL RESULTS")
    print(f"{'='*80}\n")
    
    for arch_name in ['MLP', 'LSTM', 'Transformer']:
        print(f"\n{arch_name}:")
        print("Length | Digit (±std) | Carry (±std) | Exact Match (±std)")
        print("-" * 60)
        
        for length in test_lengths:
            metrics = all_results[arch_name][length]
            print(
                f"{length:6d} | {metrics['digit_acc']*100:5.1f}±{metrics['digit_std']*100:4.1f} | "
                f"{metrics['carry_acc']*100:5.1f}±{metrics['carry_std']*100:4.1f} | "
                f"{metrics['exact_match']*100:5.1f}±{metrics['exact_match_std']*100:4.1f}"
            )
    
    print(f"\n{'='*80}")
    print("PHASE 30: COMPOSITIONAL MULTI-DIGIT ARITHMETIC GENERALIZATION COMPLETE")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
