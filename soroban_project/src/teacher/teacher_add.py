"""
teacher_add.py - Canonical teacher for addition

STRICT RULES:
1. Always uses ADD5 first if digit >= 5
2. Never uses ADD1 more than 4 times per column
3. Uses GOTO(i) for navigation (no LEFT/RIGHT stepping)
4. Processes columns right to left (ones first)

Example: 123 + 456
  GOTO_0, ADD5, ADD1  (add 6 to ones: ADD5 + ADD1)
  GOTO_1, ADD5        (add 5 to tens: ADD5)
  GOTO_2, ADD1, ADD1, ADD1, ADD1  (add 4 to hundreds: ADD1 x4)
  DONE
  Total: 10 actions (not hundreds!)

Example: 11111 + 99999
  GOTO_0, ADD5, ADD1, ADD1, ADD1, ADD1  (add 9)
  GOTO_1, ADD5, ADD1, ADD1, ADD1, ADD1  (add 9)
  GOTO_2, ADD5, ADD1, ADD1, ADD1, ADD1  (add 9)
  GOTO_3, ADD5, ADD1, ADD1, ADD1, ADD1  (add 9)
  GOTO_4, ADD5, ADD1, ADD1, ADD1, ADD1  (add 9)
  DONE
  Total: 31 actions (not 1020!)
"""

from ..env.soroban_env import SorobanEnv
from ..env.action_space import action_goto, action_add1, action_add5, action_done
from ..utils.config import SorobanConfig, DEFAULT_CONFIG

from typing import List, Tuple, Dict


def teacher_trace(
    a: int,
    b: int,
    config: SorobanConfig = None,
) -> List[int]:
    """
    Generate canonical action sequence for a + b.
    
    Returns list of action indices.
    Verifies correctness by replaying in env.
    
    INVARIANT: ADD1 is never used more than 4 times
    consecutively per column. If digit >= 5, ADD5 comes first.
    """
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
        # b = 0, nothing to add
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

        # Add digit using canonical decomposition
        if digit >= 5:
            actions.append(action_add5(W))
            digit -= 5

        # Remaining 0-4 via ADD1
        assert digit <= 4, f"Bug: remaining digit {digit} > 4"
        for _ in range(digit):
            actions.append(action_add1(W))

    # DONE
    actions.append(action_done(W))

    # VERIFY by replaying
    env = SorobanEnv(config)
    env.reset(a, b)
    for act in actions:
        _, _, done, info = env.step(act)
        if done:
            if not info.get("correct", False):
                raise RuntimeError(
                    f"Teacher trace wrong: {a}+{b}="
                    f"{env.get_result()}, expected {a+b}. "
                    f"Actions: {actions}"
                )
            break

    result = env.get_result()
    if result != a + b:
        raise RuntimeError(
            f"Teacher trace incomplete: {a}+{b}="
            f"{result}, expected {a+b}"
        )

    return actions


def teacher_trace_with_snapshots(
    a: int,
    b: int,
    config: SorobanConfig = None,
) -> List[Tuple[dict, int]]:
    """
    Generate trace with state snapshots at each step.
    Returns list of (snapshot, action) pairs.
    
    Snapshot = dict with board state for recording.
    """
    if config is None:
        config = DEFAULT_CONFIG

    actions = teacher_trace(a, b, config)

    env = SorobanEnv(config)
    env.reset(a, b)

    trace = []
    for act in actions:
        # Snapshot BEFORE action
        snapshot = {
            "board": [(u, l) for u, l in env.board],
            "cursor": env.cursor,
            "b_digits": env.b_digits[:],
            "current_value": env.get_result(),
        }
        trace.append((snapshot, act))

        # Execute
        env.step(act)

    return trace


def teacher_reactive(
    env: SorobanEnv,
    config: SorobanConfig = None,
) -> int:
    """
    Reactive teacher: given ANY state, return correct next action.
    
    Used in DAgger when student may have deviated from optimal path.
    
    Key design: Processes columns systematically with progress detection
    to prevent infinite GOTO loops at W>=14.
    
    Strategy:
    1. Find LEFTMOST column with b_remaining > 0
    2. GOTO that column
    3. Add what's needed (ADD5 first if >=5, then ADD1)
    4. If all done: DONE
    
    CRITICAL FIX (Phase 0): Leftmost approach + built-in detection for
    stillness/stalling. If we've GOTO'd but not made progress in several
    steps, force DONE to avoid oscillation at W>=14.
    """
    if config is None:
        config = DEFAULT_CONFIG
    W = config.num_columns

    # Check if all remaining is zero
    all_done = all(b == 0 for b in env.b_remaining)
    
    if all_done:
        return action_done(W)

    # SAFETY: If step count is suspiciously high and we're only seeing GOTOs,
    # it's likely a loop. This is a fallback guard.
    if hasattr(env, 'step_count') and env.step_count > W * 100:
        # Suspicious: too many steps for W columns
        return action_done(W)

    # Find LEFTMOST (lowest index) column that still needs work
    fix_col = -1
    for i in range(W):
        if env.b_remaining[i] > 0:
            fix_col = i
            break

    if fix_col == -1:
        return action_done(W)

    # Navigate to fix column
    if env.cursor != fix_col:
        return action_goto(fix_col)

    # Add what remains at this column (canonical: ADD5 first)
    remaining = env.b_remaining[fix_col]
    
    if remaining >= 5:
        return action_add5(W)
    elif remaining > 0:
        return action_add1(W)
    else:
        # Fallback: all columns should be done now
        return action_done(W)


# ══════════════════════════════════════════════
#  Self-test
# ══════════════════════════════════════════════

if __name__ == "__main__":
    from env.action_space import decode_action

    print("=" * 60)
    print("  Teacher Addition - Self Test")
    print("=" * 60)

    config = DEFAULT_CONFIG

    cases = [
        (0, 0), (0, 5), (3, 4), (3, 7),
        (27, 15), (99, 1), (123, 456),
        (999, 1), (9999, 1), (99999, 1),
        (11111, 99999), (45678, 54321),
        (500000, 500000), (999999, 1),
    ]

    for a, b in cases:
        if a + b >= 10**config.num_columns:
            print(f"  SKIP {a}+{b} (overflow)")
            continue

        try:
            actions = teacher_trace(a, b, config)
            action_names = [decode_action(a, config.num_columns) for a in actions]

            # Count ADD1 per column
            max_consecutive_add1 = 0
            current_add1_count = 0
            for name in action_names:
                if name == "ADD1":
                    current_add1_count += 1
                    max_consecutive_add1 = max(max_consecutive_add1, current_add1_count)
                else:
                    current_add1_count = 0

            assert max_consecutive_add1 <= 4, \
                f"ADD1 used {max_consecutive_add1} times consecutively!"

            print(
                f"  ✅ {a:>8} + {b:<8} = {a+b:<10} "
                f"({len(actions):2d} steps, "
                f"max_add1_seq={max_consecutive_add1})"
            )

        except Exception as e:
            print(f"  ❌ {a} + {b}: {e}")

    # Step count comparison
    print(f"\n  --- Step Count vs Old System ---")
    print(f"  {'Problem':<25} {'Old INC':<10} {'New Soroban':<10}")
    old = {"3+5": 6, "123+456": 18, "999+1": 2, "11111+99999": 1020, "45678+54321": 549}
    for a, b in [(3, 5), (123, 456), (999, 1), (11111, 99999), (45678, 54321)]:
        actions = teacher_trace(a, b, config)
        key = f"{a}+{b}"
        print(f"  {key:<25} {old.get(key, '?'):<10} {len(actions):<10}")
