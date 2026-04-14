"""
teacher_sub.py - Canonical teacher for subtraction

STRICT RULES:
1. Always uses SUB5 first if digit >= 5
2. Never uses SUB1 more than 4 times per column
3. Uses GOTO(i) for navigation (no LEFT/RIGHT stepping)
4. Processes columns right to left (ones first)
5. MVP: requires a >= b (no negative numbers)

Example: 9-4
  GOTO_0, SUB5, SUB1, SUB1, SUB1, SUB1  (subtract 4: SUB5 - 4*SUB1 = 9 - 4)
  Wait no, that subtracts 9. Let me reconsider...
  Actually:
  GOTO_0, SUB1, SUB1, SUB1, SUB1  (subtract 4)
  DONE
  
Example: 100 - 1
  GOTO_0, SUB1  (subtract 1 from ones)
  DONE
"""

from ..env.soroban_env import SorobanEnv
from ..env.action_space import action_goto, action_sub1, action_sub5, action_done
from ..utils.config import SorobanConfig, DEFAULT_CONFIG

from typing import List


def teacher_trace_sub(
    a: int,
    b: int,
    config: SorobanConfig = None,
) -> List[int]:
    """
    Generate canonical action sequence for a - b.
    MVP: requires a >= b.
    
    Returns list of action indices.
    Verifies correctness by replaying in env.
    
    INVARIANT: SUB1 is never used more than 4 times
    consecutively per column. If digit >= 5, SUB5 comes first.
    """
    if b > a:
        raise ValueError(f"SUB MVP: requires a >= b (got a={a}, b={b})")
    
    if config is None:
        config = DEFAULT_CONFIG
    W = config.num_columns

    # Extract b digits
    b_digits = []
    temp = b
    for _ in range(W):
        b_digits.append(temp % 10)
        temp //= 10

    # Find highest non-zero digit
    highest = -1
    for i in range(W - 1, -1, -1):
        if b_digits[i] > 0:
            highest = i
            break

    actions = []

    if highest == -1:
        # b = 0, nothing to subtract
        actions.append(action_done(W))
        return actions

    # Process each column right to left
    current_col = 0  # Track where we are
    for col in range(highest + 1):
        digit = b_digits[col]
        if digit == 0:
            continue

        # GOTO this column (only if not already there)
        if current_col != col:
            actions.append(action_goto(col))
            current_col = col

        # Subtract digit using canonical decomposition
        if digit >= 5:
            actions.append(action_sub5(W))
            digit -= 5

        # Remaining 0-4 via SUB1
        assert digit <= 4, f"Bug: remaining digit {digit} > 4"
        for _ in range(digit):
            actions.append(action_sub1(W))

    # DONE
    actions.append(action_done(W))

    # VERIFY by replaying
    env = SorobanEnv(config)
    env.reset(a, b, operation="sub")
    for action_idx in actions:
        obs, reward, done, info = env.step(action_idx)
        if "illegal" in info and info["illegal"]:
            raise RuntimeError(f"Teacher generated illegal action: {info}")
    
    result = env.get_result()
    expected = a - b
    if result != expected:
        raise RuntimeError(f"Teacher trace failed: got {result}, expected {expected}")

    return actions
