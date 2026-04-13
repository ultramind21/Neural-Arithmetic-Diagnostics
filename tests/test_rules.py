"""Unit tests for soroban rules."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.env.soroban_rules import (
    digit_to_beads, beads_to_digit, number_to_board, board_to_number,
    apply_add1, apply_add5, apply_sub1, apply_sub5,
    validate_column, validate_board,
)


def run_tests():
    print("=" * 50)
    print("  Soroban Rules - Unit Tests")
    print("=" * 50)

    # Digit ↔ Beads roundtrip
    print("  digit_to_beads roundtrip...", end=" ")
    for d in range(10):
        u, l = digit_to_beads(d)
        assert beads_to_digit(u, l) == d
        assert validate_column(u, l)
    print("[OK]")

    # Number ↔ Board roundtrip
    print("  number_to_board roundtrip...", end=" ")
    for n in [0, 1, 5, 9, 10, 42, 99, 100, 999, 12345, 999999]:
        board = number_to_board(n, 8)
        assert board_to_number(board) == n
        assert validate_board(board)
    print("[OK]")

    # ADD1 simple (0-8 → 1-9)
    print("  ADD1 simple (no carry)...", end=" ")
    for d in range(9):
        u, l = digit_to_beads(d)
        nu, nl, carry = apply_add1(u, l)
        assert beads_to_digit(nu, nl) == d + 1
        assert carry == 0
    print("[OK]")

    # ADD1 carry (9 → 0 carry 1)
    print("  ADD1 carry (9+1)...", end=" ")
    u, l = digit_to_beads(9)
    nu, nl, carry = apply_add1(u, l)
    assert beads_to_digit(nu, nl) == 0
    assert carry == 1
    print("[OK]")

    # ADD1 complement (4+1=5)
    print("  ADD1 complement (4+1=5)...", end=" ")
    u, l = digit_to_beads(4)
    nu, nl, carry = apply_add1(u, l)
    assert beads_to_digit(nu, nl) == 5
    assert nu == 1 and nl == 0
    assert carry == 0
    print("[OK]")

    # ADD5 simple (0-4 → 5-9)
    print("  ADD5 simple...", end=" ")
    for d in range(5):
        u, l = digit_to_beads(d)
        nu, nl, carry = apply_add5(u, l)
        assert beads_to_digit(nu, nl) == d + 5
        assert carry == 0
    print("[OK]")

    # ADD5 carry (5-9 → 0-4 carry 1)
    print("  ADD5 carry...", end=" ")
    for d in range(5, 10):
        u, l = digit_to_beads(d)
        nu, nl, carry = apply_add5(u, l)
        assert beads_to_digit(nu, nl) == (d + 5) % 10
        assert carry == 1
    print("[OK]")

    # SUB1
    print("  SUB1...", end=" ")
    for d in range(1, 10):
        u, l = digit_to_beads(d)
        nu, nl, borrow = apply_sub1(u, l)
        assert beads_to_digit(nu, nl) == d - 1
        assert borrow == 0
    u, l = digit_to_beads(0)
    nu, nl, borrow = apply_sub1(u, l)
    assert beads_to_digit(nu, nl) == 9
    assert borrow == 1
    print("[OK]")

    # Carry chain via board: 999 + 1 = 1000
    print("  Carry chain (999+1)...", end=" ")
    board = number_to_board(999, 8)
    u, l = board[0]
    nu, nl, carry = apply_add1(u, l)
    board[0] = (nu, nl)
    col = 1
    while carry and col < 8:
        u, l = board[col]
        nu, nl, carry = apply_add1(u, l)
        board[col] = (nu, nl)
        col += 1
    assert board_to_number(board) == 1000
    print("[OK]")

    # Long carry: 99999 + 1 = 100000
    print("  Long carry (99999+1)...", end=" ")
    board = number_to_board(99999, 8)
    u, l = board[0]
    nu, nl, carry = apply_add1(u, l)
    board[0] = (nu, nl)
    col = 1
    while carry and col < 8:
        u, l = board[col]
        nu, nl, carry = apply_add1(u, l)
        board[col] = (nu, nl)
        col += 1
    assert board_to_number(board) == 100000
    print("[OK]")

    # Full addition via digit decomposition
    print("  Full addition (multi-case)...", end=" ")
    cases = [(3, 5, 8), (27, 15, 42), (99, 1, 100), (999, 999, 1998), (45678, 54321, 99999)]
    for a, b, expected in cases:
        board = number_to_board(a, 8)
        b_digits = []
        temp = b
        for _ in range(8):
            b_digits.append(temp % 10)
            temp //= 10

        for col_i in range(8):
            d = b_digits[col_i]
            if d >= 5:
                u, l = board[col_i]
                nu, nl, carry = apply_add5(u, l)
                board[col_i] = (nu, nl)
                if carry:
                    c = col_i + 1
                    while carry and c < 8:
                        u, l = board[c]
                        nu, nl, carry = apply_add1(u, l)
                        board[c] = (nu, nl)
                        c += 1
                d -= 5
            for _ in range(d):
                u, l = board[col_i]
                nu, nl, carry = apply_add1(u, l)
                board[col_i] = (nu, nl)
                if carry:
                    c = col_i + 1
                    while carry and c < 8:
                        u, l = board[c]
                        nu, nl, carry = apply_add1(u, l)
                        board[c] = (nu, nl)
                        c += 1

        result = board_to_number(board)
        assert result == expected, f"{a}+{b}: got {result}, expected {expected}"
    print("[OK]")

    print("\n  [OK] ALL RULES TESTS PASSED!")


if __name__ == "__main__":
    run_tests()

