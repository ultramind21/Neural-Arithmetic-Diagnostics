"""Integration tests for soroban environment."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.env.soroban_env import SorobanEnv
from src.env.action_space import action_goto, action_add1, action_add5, action_done
from src.utils.config import DEFAULT_CONFIG


def run_tests():
    print("=" * 50)
    print("  Soroban Env - Integration Tests")
    print("=" * 50)

    config = DEFAULT_CONFIG
    W = config.num_columns

    # Basic reset
    print("  reset loads a correctly...", end=" ")
    env = SorobanEnv(config)
    env.reset(42, 13)
    assert env.get_result() == 42
    assert env.target == 55
    print("✅")

    # GOTO
    print("  GOTO moves cursor...", end=" ")
    env.reset(0, 0)
    env.step(action_goto(5))
    assert env.cursor == 5
    env.step(action_goto(0))
    assert env.cursor == 0
    print("✅")

    # ADD1 through env
    print("  ADD1 works...", end=" ")
    env.reset(0, 1)
    env.step(action_add1(W))
    assert env.get_result() == 1
    print("✅")

    # ADD5 through env
    print("  ADD5 works...", end=" ")
    env.reset(0, 5)
    env.step(action_add5(W))
    assert env.get_result() == 5
    print("✅")

    # Carry through env
    print("  Carry (9+1=10)...", end=" ")
    env.reset(9, 1)
    env.step(action_add1(W))
    assert env.get_result() == 10
    print("✅")

    # Carry chain
    print("  Carry chain (999+1=1000)...", end=" ")
    env.reset(999, 1)
    env.step(action_add1(W))
    assert env.get_result() == 1000
    print("✅")

    # DONE correct
    print("  DONE correct answer...", end=" ")
    env.reset(3, 5)
    env.step(action_add5(W))
    _, reward, done, info = env.step(action_done(W))
    assert done and info["correct"] and reward > 0
    print("✅")

    # DONE wrong
    print("  DONE wrong answer...", end=" ")
    env.reset(3, 5)
    _, reward, done, info = env.step(action_done(W))
    assert done and not info["correct"] and reward < 0
    print("✅")

    # Observation shape
    print("  Observation shape...", end=" ")
    env.reset(123, 456)
    obs = env._obs()
    assert obs.shape == (W, 6), f"Expected ({W}, 6), got {obs.shape}"
    print("✅")

    print("\n  ✅ ALL ENV TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
