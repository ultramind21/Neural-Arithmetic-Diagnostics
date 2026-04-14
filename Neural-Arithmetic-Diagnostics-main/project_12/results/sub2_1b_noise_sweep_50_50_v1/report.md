# SUB2.1b Noise Sweep (50/50 mix, seeds 0-4)

## Overview
Fixed 50/50 mix, varying seeds to estimate variance.
n=5 runs

## Statistics
no_borrow:
  - mean: 0.5992
  - stdev: 0.0056

borrow_heavy:
  - mean: 0.5081
  - stdev: 0.0075

## Interpretation
- Noise floor (stdev): ~±0.005-0.008
- SUB2.1 ratio differences (<0.01): **within noise**
- Conclusion: **'flat surface' is real**, not masking hidden optimum

## Per-seed results
- seed=0: no_borrow=0.5993, borrow_heavy=0.5107
- seed=1: no_borrow=0.6060, borrow_heavy=0.5060
- seed=2: no_borrow=0.6047, borrow_heavy=0.5107
- seed=3: no_borrow=0.5920, borrow_heavy=0.5180
- seed=4: no_borrow=0.5940, borrow_heavy=0.4953
