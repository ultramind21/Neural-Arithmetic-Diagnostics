"""
================================================================================
RESIDUAL + LOGIC LAYER ADDER
================================================================================

Core Idea:
- Neural network learns: sum ∈ [0..18]
- Logic layer (deterministic) computes: digit = sum % 10, carry = sum // 10

Separation principle:
- Approximation (neural): Learn smooth sum function
- Correctness (symbolic): Deterministic modulo/division

================================================================================
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ResidualLogicAdder(nn.Module):
    """
    Single-digit adder using residual connections + logic layer.
    
    Input: (a, b, carry_in) where a,b ∈ [0..9], carry_in ∈ {0,1}
    Output: (digit, carry) computed from sum ∈ [0..19]
    
    Training target: sum = a + b + carry_in (cross-entropy classification)
    Inference logic: digit = sum % 10, carry = sum // 10 (deterministic)
    """
    
    def __init__(self, embedding_dim=8, hidden_dim=64):
        super().__init__()
        
        # Embeddings for input digits
        self.embed = nn.Embedding(10, embedding_dim)
        
        # Main network
        self.fc1 = nn.Linear(embedding_dim * 2 + 1, hidden_dim)  # [a_emb, b_emb, carry_in]
        self.fc2 = nn.Linear(hidden_dim, 32)
        
        # Output: regression head for continuous sum ∈ [0..19]
        self.sum_head = nn.Linear(32, 1)
        
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
    
    def forward(self, a, b, carry_in):
        """
        Forward pass.
        
        Args:
            a: torch.LongTensor of shape (batch_size,) or (batch_size, seq_len)
               Values in [0..9]
            b: torch.LongTensor of shape (batch_size,) or (batch_size, seq_len)
               Values in [0..9]
            carry_in: torch.FloatTensor of shape (batch_size,) or (batch_size, seq_len)
                     Values in {0, 1} or [0, 1]
        
        Returns:
            sum_pred: torch.FloatTensor of shape (batch_size,) or (batch_size, seq_len)
                     Continuous predictions for sum ∈ [0..19]
        """
        # Embed input digits
        a_emb = self.embed(a)  # (..., embedding_dim)
        b_emb = self.embed(b)  # (..., embedding_dim)
        
        # Concatenate embeddings with carry
        # Handle both 1D (batch,) and 2D (batch, seq_len) inputs
        if carry_in.dim() == a_emb.dim() - 1:
            carry_expanded = carry_in.unsqueeze(-1)
        else:
            carry_expanded = carry_in.unsqueeze(-1)
        
        x = torch.cat([a_emb, b_emb, carry_expanded], dim=-1)  # (..., 2*emb_dim + 1)
        
        # Main network with ReLU
        x = F.relu(self.fc1(x))  # (..., hidden_dim)
        x = F.relu(self.fc2(x))  # (..., 32)
        
        # Regression output: continuous sum
        sum_pred = self.sum_head(x)  # (..., 1)
        sum_pred = sum_pred.squeeze(-1)  # (...,)
        
        return sum_pred
    
    @staticmethod
    def logic_layer(sum_pred):
        """
        Deterministic logic layer: extract digit and carry from sum.
        
        Args:
            sum_pred: torch.Tensor of shape (...,) with values in [0..18]
        
        Returns:
            digit: torch.Tensor of shape (...,) with values in [0..9]
            carry: torch.Tensor of shape (...,) with values in {0, 1}
        """
        digit = sum_pred % 10
        carry = sum_pred // 10
        return digit, carry
    
    def forward_with_logic(self, a, b, carry_in):
        """
        End-to-end forward with logic layer.
        
        Args:
            a, b, carry_in: as in forward()
        
        Returns:
            sum_pred: continuous sum predictions ∈ [0..19]
            sum_int: rounded integer sum ∈ [0..19]
            digit: extracted digit ∈ [0..9]
            carry_out: extracted carry ∈ {0, 1}
        """
        sum_pred = self.forward(a, b, carry_in)
        sum_int = torch.round(sum_pred).clamp(0, 19).long()
        digit, carry_out = self.logic_layer(sum_int)
        
        return sum_pred, sum_int, digit, carry_out


if __name__ == "__main__":
    # Quick test
    model = ResidualLogicAdder()
    
    # Batch of examples
    a = torch.randint(0, 10, (4, 8))  # 4 sequences of length 8
    b = torch.randint(0, 10, (4, 8))
    carry_in = torch.randint(0, 2, (4, 8)).float()
    
    # Forward pass
    sum_logits, sum_pred, digit, carry_out = model.forward_with_logic(a, b, carry_in)
    
    print(f"Input shape: {a.shape}")
    print(f"Output shapes:")
    print(f"  sum_logits: {sum_logits.shape}")
    print(f"  sum_pred: {sum_pred.shape}")
    print(f"  digit: {digit.shape}")
    print(f"  carry_out: {carry_out.shape}")
    
    print("\nExample predictions:")
    print(f"  a[0,0] = {a[0,0].item()}, b[0,0] = {b[0,0].item()}, carry_in[0,0] = {carry_in[0,0].item()}")
    print(f"  sum = {a[0,0].item() + b[0,0].item() + int(carry_in[0,0].item())}")
    print(f"  predicted sum = {sum_pred[0,0].item()}")
    print(f"  digit = {digit[0,0].item()}, carry_out = {carry_out[0,0].item()}")
