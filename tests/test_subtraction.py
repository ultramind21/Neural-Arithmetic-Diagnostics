"""
test_subtraction.py - Unit tests for subtraction (MVP)
"""

import sys
from pathlib import Path

# Add repo root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.env.soroban_env import SorobanEnv
from src.teacher.teacher_sub import teacher_trace_sub
from src.utils.config import DEFAULT_CONFIG


def test_sub_simple():
    """Test: 5 - 3 = 2"""
    env = SorobanEnv(DEFAULT_CONFIG)
    actions = teacher_trace_sub(5, 3)
    
    obs = env.reset(5, 3, operation="sub")
    for action in actions:
        obs, reward, done, info = env.step(action)
    
    result = env.get_result()
    assert result == 2, f"Expected 2, got {result}"
    assert info.get("correct"), "Should be correct"
    print("✓ test_sub_simple passed (5 - 3 = 2)")


def test_sub_borrow():
    """Test: 10 - 1 = 9 (borrow)"""
    env = SorobanEnv(DEFAULT_CONFIG)
    actions = teacher_trace_sub(10, 1)
    
    obs = env.reset(10, 1, operation="sub")
    for action in actions:
        obs, reward, done, info = env.step(action)
    
    result = env.get_result()
    assert result == 9, f"Expected 9, got {result}"
    assert info.get("correct"), "Should be correct"
    print("✓ test_sub_borrow passed (10 - 1 = 9)")


def test_sub_borrow_chain():
    """Test: 1000 - 1 = 999 (borrow chain)"""
    env = SorobanEnv(DEFAULT_CONFIG)
    actions = teacher_trace_sub(1000, 1)
    
    obs = env.reset(1000, 1, operation="sub")
    for action in actions:
        obs, reward, done, info = env.step(action)
    
    result = env.get_result()
    assert result == 999, f"Expected 999, got {result}"
    assert info.get("correct"), "Should be correct"
    print("✓ test_sub_borrow_chain passed (1000 - 1 = 999)")


def test_sub_no_borrow():
    """Test: 987 - 654 = 333 (no borrow)"""
    env = SorobanEnv(DEFAULT_CONFIG)
    actions = teacher_trace_sub(987, 654)
    
    obs = env.reset(987, 654, operation="sub")
    for action in actions:
        obs, reward, done, info = env.step(action)
    
    result = env.get_result()
    assert result == 333, f"Expected 333, got {result}"
    assert info.get("correct"), "Should be correct"
    print("✓ test_sub_no_borrow passed (987 - 654 = 333)")


def test_sub_zero():
    """Test: 5 - 0 = 5"""
    env = SorobanEnv(DEFAULT_CONFIG)
    actions = teacher_trace_sub(5, 0)
    
    obs = env.reset(5, 0, operation="sub")
    for action in actions:
        obs, reward, done, info = env.step(action)
    
    result = env.get_result()
    assert result == 5, f"Expected 5, got {result}"
    assert info.get("correct"), "Should be correct"
    print("✓ test_sub_zero passed (5 - 0 = 5)")


def test_sub_same():
    """Test: 7 - 7 = 0"""
    env = SorobanEnv(DEFAULT_CONFIG)
    actions = teacher_trace_sub(7, 7)
    
    obs = env.reset(7, 7, operation="sub")
    for action in actions:
        obs, reward, done, info = env.step(action)
    
    result = env.get_result()
    assert result == 0, f"Expected 0, got {result}"
    assert info.get("correct"), "Should be correct"
    print("✓ test_sub_same passed (7 - 7 = 0)")


def run_tests():
    """Run all tests."""
    test_sub_simple()
    test_sub_borrow()
    test_sub_borrow_chain()
    test_sub_no_borrow()
    test_sub_zero()
    test_sub_same()
    print("\n[OK] ALL SUBTRACTION TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
