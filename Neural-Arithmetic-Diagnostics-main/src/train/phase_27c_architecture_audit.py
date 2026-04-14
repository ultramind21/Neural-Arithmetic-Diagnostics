"""
PHASE 27C: ARCHITECTURE AUDIT (30 PAIRS ONLY)
═════════════════════════════════════════════════════════════════════════════

Clean failure counting for all 3 architectures
Evaluate on 30 pairs × 2 carry states = 60 examples per trial
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
import random

torch.manual_seed(42)
np.random.seed(42)

# ============================================================================
# ARCHITECTURES (from Phase 27)
# ============================================================================

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 11)
        )
    
    def forward(self, x):
        out = self.net(x)
        return out[:, :10], out[:, 10:11]


class LSTMModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Linear(3, 64)
        self.lstm = nn.LSTM(input_size=64, hidden_size=128, batch_first=True)
        self.digit_head = nn.Linear(128, 10)
        self.carry_head = nn.Linear(128, 1)
    
    def forward(self, x):
        embedded = self.embedding(x)
        embedded = embedded.unsqueeze(1)
        lstm_out, _ = self.lstm(embedded)
        lstm_out = lstm_out[:, -1, :]
        return self.digit_head(lstm_out), self.carry_head(lstm_out)


class TransformerModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Linear(3, 128)
        self.attention = nn.MultiheadAttention(128, num_heads=4, batch_first=True)
        self.fc1 = nn.Linear(128, 256)
        self.fc2 = nn.Linear(256, 128)
        self.digit_head = nn.Linear(128, 10)
        self.carry_head = nn.Linear(128, 1)
    
    def forward(self, x):
        embedded = self.embedding(x)
        embedded = embedded.unsqueeze(1)
        attn_out, _ = self.attention(embedded, embedded, embedded)
        attn_out = attn_out.squeeze(1)
        ff_out = self.fc2(torch.relu(self.fc1(attn_out)))
        return self.digit_head(ff_out), self.carry_head(ff_out)


# ============================================================================
# DATA & TRAINING
# ============================================================================

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
    """CLEAN: 30 pairs × 2 = 60 samples only"""
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


def run_trial(model_class, train_pairs, test_pairs, trial_num, device='cpu'):
    """Single trial"""
    X_train, y_train = create_train_data(train_pairs)
    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=256,
        shuffle=True
    )
    
    model = model_class().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    digit_criterion = nn.CrossEntropyLoss()
    carry_criterion = nn.BCEWithLogitsLoss()
    
    for epoch in range(50):
        model.train()
        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)
            optimizer.zero_grad()
            digit_logits, carry_logits = model(batch_x)
            digit_loss = digit_criterion(digit_logits, batch_y[:, 0])
            carry_loss = carry_criterion(carry_logits.squeeze(), batch_y[:, 1].float())
            (digit_loss + carry_loss).backward()
            optimizer.step()
    
    # EVALUATE: SIMPLE (30 pairs × 2 = 60 examples)
    X_test, y_test = create_test_data_simple(test_pairs)
    X_test = X_test.to(device)
    y_test = y_test.to(device)
    
    model.eval()
    with torch.no_grad():
        digit_logits, carry_logits = model(X_test)
        digit_pred = digit_logits.argmax(dim=1)
        carry_pred = (carry_logits > 0).long().squeeze()
        both_correct = (digit_pred == y_test[:, 0]) & (carry_pred == y_test[:, 1])
    
    both_correct = both_correct.cpu().numpy()
    X_test = X_test.cpu().numpy()
    
    # Count failures
    carry_failures = 0
    carry_examples = 0
    noncarry_failures = 0
    noncarry_examples = 0
    
    for i in range(len(X_test)):
        a, b, c_in = int(X_test[i, 0]), int(X_test[i, 1]), int(X_test[i, 2])
        s = a + b + c_in
        is_carry = (s >= 10)
        failed = not both_correct[i]
        
        if is_carry:
            carry_examples += 1
            if failed:
                carry_failures += 1
        else:
            noncarry_examples += 1
            if failed:
                noncarry_failures += 1
    
    test_acc = (60 - carry_failures - noncarry_failures) / 60
    
    return {
        'test_acc': test_acc,
        'carry_failures': carry_failures,
        'carry_examples': carry_examples,
        'noncarry_failures': noncarry_failures,
        'noncarry_examples': noncarry_examples,
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    print("\n" + "="*80)
    print("PHASE 27C: ARCHITECTURE AUDIT - CLEAN FAILURE COUNTING")
    print("="*80)
    print(f"Device: {device}\n")
    
    all_pairs = [(a, b) for a in range(10) for b in range(10)]
    
    architectures = {
        'MLP': MLP,
        'LSTM': LSTMModel,
        'Transformer': TransformerModel,
    }
    
    for arch_name, arch_class in architectures.items():
        print(f"\n{'='*80}")
        print(f"Testing {arch_name}...")
        print(f"{'='*80}\n")
        
        results = []
        total_carry_examples = 0
        total_carry_failures = 0
        total_noncarry_examples = 0
        total_noncarry_failures = 0
        
        for trial in range(30):
            random.seed(trial)
            random.shuffle(all_pairs)
            
            train_pairs = all_pairs[:70]
            test_pairs = all_pairs[70:]
            
            result = run_trial(arch_class, train_pairs, test_pairs, trial, device=device)
            results.append(result)
            
            total_carry_examples += result['carry_examples']
            total_carry_failures += result['carry_failures']
            total_noncarry_examples += result['noncarry_examples']
            total_noncarry_failures += result['noncarry_failures']
            
            if (trial + 1) % 5 == 0:
                print(f"Trial {trial+1:2d}/30: Test={result['test_acc']*100:5.1f}% "
                      f"C_fail={result['carry_failures']:2d}/{result['carry_examples']:2d} "
                      f"NC_fail={result['noncarry_failures']:2d}/{result['noncarry_examples']:2d}")
        
        # Aggregate
        test_accs = [r['test_acc'] for r in results]
        test_mean = np.mean(test_accs)
        test_std = np.std(test_accs)
        
        print(f"\n{arch_name} FINAL RESULTS:")
        print(f"  Test accuracy: {test_mean*100:.1f}% ± {test_std*100:.1f}%")
        print(f"  Total evaluations: {total_carry_examples + total_noncarry_examples}")
        print(f"  Total failures: {total_carry_failures + total_noncarry_failures}")
        
        if total_carry_examples > 0:
            carry_fail_rate = total_carry_failures / total_carry_examples * 100
            print(f"\n  CARRY cases ({total_carry_examples} total):")
            print(f"    Failures: {total_carry_failures}")
            print(f"    Failure rate: {carry_fail_rate:.1f}%")
        
        if total_noncarry_examples > 0:
            noncarry_fail_rate = total_noncarry_failures / total_noncarry_examples * 100
            print(f"\n  NON-CARRY cases ({total_noncarry_examples} total):")
            print(f"    Failures: {total_noncarry_failures}")
            print(f"    Failure rate: {noncarry_fail_rate:.1f}%")
        
        if total_carry_examples > 0 and total_noncarry_examples > 0:
            diff = carry_fail_rate - noncarry_fail_rate
            print(f"\n  Difference: {diff:+.1f}%")
            print(f"  Carry is {carry_fail_rate/noncarry_fail_rate:.2f}× harder")

print("\n" + "="*80)
print("AUDIT COMPLETE")
print("="*80)
