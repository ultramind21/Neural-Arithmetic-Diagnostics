"""
soroban_env.py - Soroban Environment

Key design decisions (from Blueprint v2 + M1 fixes):
1. Board starts with 'a' pre-loaded. Model never loads 'a'.
2. Actions: GOTO_i (direct jump), ADD1, ADD5, DONE. No LEFT/RIGHT.
3. Carry is automatic physics inside ADD1/ADD5.

4. **M1 INDUCTIVE BIAS: rem[col]** (remaining per column)
   - Stored internally in self.b_remaining (not exposed to model)
   - Deterministic constraint: ADD1/ADD5 only if rem[col] >= amount
   - Illegal actions terminate immediately (prevents loops)
   - Enables length generalization without NN extrapolation

5. Safe observable: b_done_mask[col] = 1 if rem[col]==0
   - NOT oracle (deterministic consequence of action history)
   - Helps model avoid overspend patterns

6. Model sees: board state + cursor + b_digits + b_done_mask + active_col
7. No oracle, no rem exposure, no privileged signals.
"""

import numpy as np
from typing import Dict, Tuple, List

from .soroban_rules import (
    digit_to_beads, beads_to_digit, number_to_board, board_to_number,
    apply_add1, apply_add5, apply_sub1, apply_sub5, validate_board,
)
from .action_space import (
    action_add1, action_add5, action_sub1, action_sub5, action_done,
    is_goto, decode_action, num_actions,
)
from ..utils.config import SorobanConfig, DEFAULT_CONFIG


class SorobanEnv:
    """
    Gym-like soroban environment for addition.
    
    Observation layout (per column, structured):
        upper:     0 or 1
        lower:     0-4
        is_cursor: 0 or 1
        b_digit:   0-9  (what to add at this column)
        b_done_mask: 0 or 1 (has all been added to this column?)
        is_active_col: 0 or 1 (are we working on this column now?)
    
    Shape: (num_columns, F) where F is defined by _obs() implementation.
    Current implementation: F=6 (upper, lower, is_cursor, b_digit, b_done_mask, is_active_col).
    """

    def __init__(self, config: SorobanConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.W = self.config.num_columns
        
        # State
        self.board: List[Tuple[int, int]] = []  # (upper, lower) per column
        self.cursor: int = 0
        self.active_col: int = 0  # Which column we're currently working on (for obs)
        self.b_digits: List[int] = []
        self.b_remaining: List[int] = []  # Internal tracking for teacher (NOT in obs)
        self.target: int = 0
        self.steps: int = 0
        self.done: bool = False
        self.a: int = 0
        self.b: int = 0
        self.operation: str = "add"  # "add" or "sub"

    def reset(self, a: int, b: int, operation: str = "add") -> np.ndarray:
        """
        Start new episode.
        For addition: Board is PRE-LOADED with 'a'. Model's job: add 'b'.
        For subtraction: Board is PRE-LOADED with 'a'. Model's job: subtract 'b'. (MVP: requires a >= b)
        """
        if operation == "sub" and b > a:
            raise ValueError(f"SUB MVP: a must be >= b (got a={a}, b={b})")
        
        self.a = a
        self.b = b
        self.operation = operation
        
        if operation == "add":
            self.target = a + b
        elif operation == "sub":
            self.target = a - b
        else:
            raise ValueError(f"Unknown operation: {operation}")

        # Load 'a' directly onto board (NO model involvement)
        self.board = number_to_board(a, self.W)

        # Extract b's digits and track completion per column
        self.b_digits = []
        self.b_remaining = []  # Internal tracker for teacher (not exposed to obs)
        temp = b
        for _ in range(self.W):
            digit = temp % 10
            self.b_digits.append(digit)
            self.b_remaining.append(digit)  # Track what needs to be added/subtracted
            temp //= 10

        self.cursor = 0
        self.active_col = 0  # Start working on column 0
        self.steps = 0
        self.done = False

        assert validate_board(self.board)
        return self._obs()

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict]:
        """Execute one action. Returns (obs, reward, done, info)."""
        if self.done:
            return self._obs(), 0.0, True, {"error": "already_done"}

        self.steps += 1
        info = {"action": decode_action(action, self.W), "step": self.steps}
        reward = self.config.step_penalty  # -0.01 per step

        if is_goto(action, self.W):
            # Direct jump to column
            self.cursor = action
            self.active_col = action  # We're now working on this column

        elif action == action_add1(self.W):
            # ADD1 at cursor column with automatic carry
            # GUARD: Check if we still need to add at this column (M1 fix)
            if self.b_remaining[self.cursor] >= 1:
                self.active_col = self.cursor
                u, l = self.board[self.cursor]
                new_u, new_l, carry = apply_add1(u, l)
                self.board[self.cursor] = (new_u, new_l)
                self.b_remaining[self.cursor] -= 1
                if carry:
                    self._propagate_carry(self.cursor)
            else:
                # M1: ILLEGAL ACTION → IMMEDIATE TERMINATION
                # (prevents ADD5 loop patterns)
                self.done = True
                reward = -1.0
                info["illegal"] = True
                info["illegal_reason"] = "overspend_add1"
                info["correct"] = False

        elif action == action_add5(self.W):
            # ADD5 at cursor column with automatic carry
            # GUARD: Check if we still need to add >=5 at this column (M1 fix)
            if self.b_remaining[self.cursor] >= 5:
                self.active_col = self.cursor
                u, l = self.board[self.cursor]
                new_u, new_l, carry = apply_add5(u, l)
                self.board[self.cursor] = (new_u, new_l)
                self.b_remaining[self.cursor] -= 5
                if carry:
                    self._propagate_carry(self.cursor)
            else:
                # M1: ILLEGAL ACTION → IMMEDIATE TERMINATION
                # (prevents ADD5 loop patterns)
                self.done = True
                reward = -1.0
                info["illegal"] = True
                info["illegal_reason"] = "overspend_add5"
                info["correct"] = False

        elif action == action_sub1(self.W):
            # SUB1 at cursor column with automatic borrow
            if self.b_remaining[self.cursor] >= 1:
                self.active_col = self.cursor
                u, l = self.board[self.cursor]
                new_u, new_l, borrow = apply_sub1(u, l)
                self.board[self.cursor] = (new_u, new_l)
                self.b_remaining[self.cursor] -= 1
                if borrow:
                    self._propagate_borrow(self.cursor)
            else:
                # ILLEGAL: trying to subtract more than available
                self.done = True
                reward = -1.0
                info["illegal"] = True
                info["illegal_reason"] = "overspend_sub1"
                info["correct"] = False

        elif action == action_sub5(self.W):
            # SUB5 at cursor column with automatic borrow
            if self.b_remaining[self.cursor] >= 5:
                self.active_col = self.cursor
                u, l = self.board[self.cursor]
                new_u, new_l, borrow = apply_sub5(u, l)
                self.board[self.cursor] = (new_u, new_l)
                self.b_remaining[self.cursor] -= 5
                if borrow:
                    self._propagate_borrow(self.cursor)
            else:
                # ILLEGAL: trying to subtract more than available
                self.done = True
                reward = -1.0
                info["illegal"] = True
                info["illegal_reason"] = "overspend_sub5"
                info["correct"] = False

        elif action == action_done(self.W):
            # M1: Check if all remaining additions are done
            # (prevents DONE_early pattern)
            if any(r > 0 for r in self.b_remaining):
                # Illegal: trying to finish before all additions complete
                self.done = True
                reward = -1.0
                info["illegal"] = True
                info["illegal_reason"] = "done_early"
                info["correct"] = False
            else:
                self.done = True
                result = self.get_result()
                if result == self.target:
                    reward = self.config.correct_reward
                    info["correct"] = True
                else:
                    reward = self.config.wrong_penalty
                    info["correct"] = False
                    info["result"] = result
                    info["expected"] = self.target

        else:
            # Unknown action (not GOTO, ADD1, ADD5, or DONE)
            self.done = True
            reward = -1.0
            info["illegal"] = True
            info["illegal_reason"] = "unknown_action"
            info["correct"] = False

        # Timeout guard
        if self.steps >= self.config.max_steps and not self.done:
            self.done = True
            reward = self.config.wrong_penalty
            info["timeout"] = True
            info["correct"] = False

        assert validate_board(self.board), "Board invariant violated!"
        return self._obs(), reward, self.done, info

    def _propagate_carry(self, from_col: int):
        """Carry cascades upward. This is PHYSICS, not a decision."""
        col = from_col + 1
        while col < self.W:
            u, l = self.board[col]
            new_u, new_l, carry = apply_add1(u, l)
            self.board[col] = (new_u, new_l)
            if not carry:
                break
            col += 1

    def _propagate_borrow(self, from_col: int):
        """Borrow cascades upward. This is PHYSICS, not a decision."""
        col = from_col + 1
        while col < self.W:
            u, l = self.board[col]
            new_u, new_l, borrow = apply_sub1(u, l)
            self.board[col] = (new_u, new_l)
            if not borrow:
                break
            col += 1

    def get_result(self) -> int:
        """Read current number from board."""
        return board_to_number(self.board)

    def _obs(self) -> np.ndarray:
        """
        Observation: (num_columns, 6) array.
        Per column: [upper, lower, is_cursor, b_digit, b_done_mask, is_active_col]
        
        Features:
          upper:         0 or 1 (upper bead state)
          lower:         0-4 (lower beads count)
          is_cursor:     0 or 1 (is this the cursor column)
          b_digit:       0-9  (what needs to be added)
          b_done_mask:   0 or 1 (has all of b_digit[i] been added to this column?)
          is_active_col: 0 or 1 (is this the column we're working on NOW)
        """
        obs = np.zeros((self.W, 6), dtype=np.float32)
        for i in range(self.W):
            u, l = self.board[i]
            obs[i, 0] = u                            # upper bead
            obs[i, 1] = l                            # lower beads
            obs[i, 2] = 1.0 if i == self.cursor else 0.0  # cursor marker
            obs[i, 3] = float(self.b_digits[i])     # target digit for this column
            # b_done_mask: 1 only if we've fully added this column (remaining == 0)
            obs[i, 4] = 1.0 if self.b_remaining[i] == 0 else 0.0
            obs[i, 5] = 1.0 if i == self.active_col else 0.0  # are we working on this col now?
        return obs

    def get_obs_shape(self) -> Tuple[int, int]:
        return (self.W, 6)

    def render(self) -> str:
        """Text display of current state."""
        lines = []
        result = self.get_result()
        lines.append(
            f"Board: {result} | Target: {self.target} | "
            f"Cursor: {self.cursor} | Steps: {self.steps}"
        )

        # Show first 8 columns
        show = min(8, self.W)
        digits_str = " ".join(
            f"{'>' if i == self.cursor else ' '}"
            f"{beads_to_digit(*self.board[i])}"
            f"{'<' if i == self.cursor else ' '}"
            for i in range(show)
        )
        b_str = " ".join(f" {self.b_digits[i]} " for i in range(show))

        lines.append(f"  Board: {digits_str}")
        lines.append(f"  B:     {b_str}")
        return "\n".join(lines)
