import torch
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.residual_logic_adder import ResidualLogicAdder

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

torch.manual_seed(42)
np.random.seed(42)

def create_fresh_model():
    import torch.optim as optim
    from torch.utils.data import DataLoader
    import random
    
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
    mse_criterion = torch.nn.MSELoss()
    
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
    
    return model

print("Creating and training model...")
model = create_fresh_model()
print("✅ Trained\n")

# Test alternating pattern
print("TESTING ALTERNATING PATTERN")
print("="*80)

length = 100
a = [9 if i % 2 == 0 else 0 for i in range(length)]
b = [1 if i % 2 == 0 else 0 for i in range(length)]

print(f"a[:20]: {a[:20]}")
print(f"b[:20]: {b[:20]}\n")

model.eval()
carry = 0

digit_correct = 0
digit_wrong = 0
carry_correct = 0
carry_wrong = 0

sum_predictions = []
digit_predictions = []
digit_truths = []

with torch.no_grad():
    for i in range(length):
        a_t = torch.LongTensor([a[i]]).to(device)
        b_t = torch.LongTensor([b[i]]).to(device)
        carry_t = torch.FloatTensor([carry]).to(device)
        
        sum_pred, sum_int, digit_pred, carry_out = model.forward_with_logic(a_t, b_t, carry_t)
        
        total_sum = a[i] + b[i] + carry
        digit_true = total_sum % 10
        carry_true = 1 if total_sum >= 10 else 0
        
        sum_predictions.append(sum_pred.item())
        digit_predictions.append(int(digit_pred.item()))
        digit_truths.append(int(digit_true))
        
        if digit_pred.item() == digit_true:
            digit_correct += 1
        else:
            digit_wrong += 1
        
        if carry_out.item() == carry_true:
            carry_correct += 1
        else:
            carry_wrong += 1
        
        if i < 20:
            print(f"Pos {i:2d}: a={a[i]} b={b[i]} carry_in={int(carry)} sum_true={total_sum}")
            print(f"         sum_pred={sum_pred.item():.4f} sum_int={sum_int.item()} digit_pred={int(digit_pred.item())} digit_true={digit_true} carry_out={int(carry_out.item())} carry_true={carry_true}")
            print(f"         DIGIT: {'✓' if digit_pred.item() == digit_true else '✗'} CARRY: {'✓' if carry_out.item() == carry_true else '✗'}\n")
        
        carry = carry_out.item()

print("\nSUMMARY:")
print(f"Digit Correct: {digit_correct}/{length} ({digit_correct/length*100:.1f}%)")
print(f"Digit Wrong:   {digit_wrong}/{length} ({digit_wrong/length*100:.1f}%)")
print(f"Carry Correct: {carry_correct}/{length} ({carry_correct/length*100:.1f}%)")
print(f"Carry Wrong:   {carry_wrong}/{length} ({carry_wrong/length*100:.1f}%)")

print("\nNumerical Analysis:")
print(f"Sum predictions (first 20): {[f'{x:.2f}' for x in sum_predictions[:20]]}")
print(f"Digit predictions:          {digit_predictions[:20]}")
print(f"Digit truths:               {digit_truths[:20]}")

# Analyze pattern
print("\n" + "="*80)
print("PATTERN ANALYSIS:")
if digit_correct == length // 2:
    print("⚠️ CRITICAL: Exactly 50% accuracy = systematic error!")
    print("Digit predictions vs Truths:")
    print(f"  When true=0: predicted={[digit_predictions[i] for i in range(length) if digit_truths[i] == 0][:20]}")
    print(f"  When true=1: predicted={[digit_predictions[i] for i in range(length) if digit_truths[i] == 1][:20]}")
