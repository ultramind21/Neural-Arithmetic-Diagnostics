# Project 12 — Phase 3 Diversification v1 (Carry-Heavy vs No-Carry)

## Objective

Test how well the Transformer generalizes across different problem distributions:
- **No-Carry:** Each digit position sums to <10 (all additions straightforward)
- **Carry-Heavy:** Each digit position sums to ≥10 or >9 (frequent carry cascades)

## Outputs

Two artifact + report pairs:
- `phase3_addition_no_carry_v1/`
- `phase3_addition_carry_heavy_v1/`

## Approach

Same Transformer pipeline as Phase 2, with problem-mode parameter controlling (a,b) distribution.

## Note

Not a validated claim. Baseline experiments only to measure robustness across distributions.
