"""Tests for teacher traces."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.env.soroban_env import SorobanEnv
from src.env.action_space import action_add1, decode_action
from src.teacher.teacher_add import teacher_trace
from src.utils.config import DEFAULT_CONFIG


def run_tests():
    print("=" * 50)
    print("  Teacher - Tests")
    print("=" * 50)

    config = DEFAULT_CONFIG
    W = config.num_columns
    add1_id = action_add1(W)

    cases = [
        (0, 0, "zero+zero"),
        (0, 5, "zero+five"),
        (3, 4, "simple"),
        (3, 7, "with_complement"),
        (99, 1, "carry"),
        (123, 456, "3-digit"),
        (999, 1, "triple_carry"),
        (9999, 1, "quad_carry"),
        (11111, 99999, "heavy_carry"),
        (45678, 54321, "complex"),
        (999999, 1, "6-digit_carry"),
    ]

    for a, b, desc in cases:
        if a + b >= 10**W:
            print(f"  SKIP {desc} (overflow)")
            continue

        actions = teacher_trace(a, b, config)
        names = [decode_action(act, W) for act in actions]

        # Check no ADD1 > 4 consecutive
        max_add1 = 0
        cur_add1 = 0
        for name in names:
            if name == "ADD1":
                cur_add1 += 1
                max_add1 = max(max_add1, cur_add1)
            else:
                cur_add1 = 0

        assert max_add1 <= 4, f"{desc}: ADD1 used {max_add1} times consecutively!"

        # Verify result by replaying
        env = SorobanEnv(config)
        env.reset(a, b)
        for act in actions:
            env.step(act)
        result = env.get_result()
        assert result == a + b, f"{desc}: {a}+{b}={result}, expected {a+b}"

        print(f"  [OK] {desc:<20} {a:>8}+{b:<8}={a+b:<10} ({len(actions):2d} steps, max_add1={max_add1})")

    # Critical: step count comparison
    print(f"\n  --- Step Count Sanity ---")
    trace_11111 = teacher_trace(11111, 99999, config)
    assert len(trace_11111) <= 40, f"11111+99999: {len(trace_11111)} steps (should be ~31)"
    print(f"  [OK] 11111+99999: {len(trace_11111)} steps (was 1020 in old system)")

    trace_45678 = teacher_trace(45678, 54321, config)
    assert len(trace_45678) <= 40, f"45678+54321: {len(trace_45678)} steps"
    print(f"  [OK] 45678+54321: {len(trace_45678)} steps (was 549 in old system)")

    print("\n  [OK] ALL TEACHER TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
