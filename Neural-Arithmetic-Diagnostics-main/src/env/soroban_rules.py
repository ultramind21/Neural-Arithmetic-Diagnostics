"""
soroban_rules.py - Physical rules of the Soroban

A column has:
    upper ∈ {0, 1}  (heaven bead, worth 5)
    lower ∈ {0..4}  (earth beads, worth 1 each)
    value = upper*5 + lower ∈ {0..9}

ADD1 and ADD5 work on the digit VALUE, then re-encode to (upper, lower).
Carry propagates automatically as physics.

Implementation choice (from blueprint):
    1. Convert column to digit value
    2. Add 1 or 5
    3. If result >= 10: subtract 10, carry = 1
    4. Re-encode to (upper, lower)

This is simpler and less error-prone than manipulating beads directly,
while still respecting soroban representation.
"""

from typing import Tuple, List


def digit_to_beads(d: int) -> Tuple[int, int]:
    """Convert digit 0-9 to (upper, lower) bead representation."""
    assert 0 <= d <= 9, f"Invalid digit: {d}"
    return (1 if d >= 5 else 0, d % 5)


def beads_to_digit(upper: int, lower: int) -> int:
    """Convert (upper, lower) beads to digit value."""
    assert upper in (0, 1), f"Invalid upper: {upper}"
    assert 0 <= lower <= 4, f"Invalid lower: {lower}"
    return upper * 5 + lower


def apply_add1(upper: int, lower: int) -> Tuple[int, int, int]:
    """
    Add 1 to column. Returns (new_upper, new_lower, carry).
    
    Carry propagates automatically - this is physics, not a decision.
    """
    d = beads_to_digit(upper, lower) + 1
    carry = 0
    if d >= 10:
        d -= 10
        carry = 1
    new_upper, new_lower = digit_to_beads(d)
    return new_upper, new_lower, carry


def apply_add5(upper: int, lower: int) -> Tuple[int, int, int]:
    """
    Add 5 to column. Returns (new_upper, new_lower, carry).
    """
    d = beads_to_digit(upper, lower) + 5
    carry = 0
    if d >= 10:
        d -= 10
        carry = 1
    new_upper, new_lower = digit_to_beads(d)
    return new_upper, new_lower, carry


def apply_sub1(upper: int, lower: int) -> Tuple[int, int, int]:
    """
    Subtract 1 from column. Returns (new_upper, new_lower, borrow).
    """
    d = beads_to_digit(upper, lower) - 1
    borrow = 0
    if d < 0:
        d += 10
        borrow = 1
    new_upper, new_lower = digit_to_beads(d)
    return new_upper, new_lower, borrow


def apply_sub5(upper: int, lower: int) -> Tuple[int, int, int]:
    """
    Subtract 5 from column. Returns (new_upper, new_lower, borrow).
    """
    d = beads_to_digit(upper, lower) - 5
    borrow = 0
    if d < 0:
        d += 10
        borrow = 1
    new_upper, new_lower = digit_to_beads(d)
    return new_upper, new_lower, borrow


def number_to_board(num: int, width: int) -> List[Tuple[int, int]]:
    """Convert integer to list of (upper, lower) tuples. Index 0 = ones."""
    assert num >= 0
    board = []
    for _ in range(width):
        board.append(digit_to_beads(num % 10))
        num //= 10
    if num > 0:
        raise ValueError(f"Number too large for {width} columns")
    return board


def board_to_number(board: List[Tuple[int, int]]) -> int:
    """Read integer from board."""
    result = 0
    for i in range(len(board) - 1, -1, -1):
        result = result * 10 + beads_to_digit(board[i][0], board[i][1])
    return result


def validate_column(upper: int, lower: int) -> bool:
    """Check column invariants."""
    return upper in (0, 1) and 0 <= lower <= 4


def validate_board(board: List[Tuple[int, int]]) -> bool:
    """Check all columns valid."""
    return all(validate_column(u, l) for u, l in board)
