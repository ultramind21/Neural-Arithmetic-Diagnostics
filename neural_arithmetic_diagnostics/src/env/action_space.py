"""
action_space.py - Action definitions

15 actions for W=12:
  GOTO_0 .. GOTO_11  (12 actions: jump directly to column i)
  ADD1                (add 1 to current column, carry auto)
  ADD5                (add 5 to current column, carry auto)
  DONE                (signal completion)

NO LEFT/RIGHT stepping. NO INC on whole number.
GOTO is how a real soroban operator works: look at column, move hand there.
"""

from typing import List, Optional


def build_action_names(num_columns: int) -> List[str]:
    """Build list of action names."""
    names = []
    for i in range(num_columns):
        names.append(f"GOTO_{i}")
    names.append("ADD1")
    names.append("ADD5")
    names.append("DONE")
    return names


def action_goto(col: int) -> int:
    """Action index for GOTO column col."""
    return col


def action_add1(num_columns: int) -> int:
    """Action index for ADD1."""
    return num_columns


def action_add5(num_columns: int) -> int:
    """Action index for ADD5."""
    return num_columns + 1


def action_done(num_columns: int) -> int:
    """Action index for DONE."""
    return num_columns + 2


def num_actions(num_columns: int) -> int:
    """Total number of actions."""
    return num_columns + 3


def is_goto(action: int, num_columns: int) -> bool:
    """Check if action is a GOTO."""
    return 0 <= action < num_columns


def decode_action(action: int, num_columns: int) -> str:
    """Human-readable action name."""
    if action < num_columns:
        return f"GOTO_{action}"
    elif action == num_columns:
        return "ADD1"
    elif action == num_columns + 1:
        return "ADD5"
    elif action == num_columns + 2:
        return "DONE"
    return f"UNKNOWN_{action}"
