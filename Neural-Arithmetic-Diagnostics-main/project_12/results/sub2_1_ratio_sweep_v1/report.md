# SUB2.1 Ratio Sweep v1

## Overview
Fast sensitivity scan over mix ratios (seed=0, no noise estimation yet). Produces point estimates for curve fitting.

## Results
- **{'no_borrow': 0.9, 'borrow_heavy': 0.1}**: no_borrow=0.6060, borrow_heavy=0.5107
- **{'no_borrow': 0.7, 'borrow_heavy': 0.3}**: no_borrow=0.6000, borrow_heavy=0.5107
- **{'no_borrow': 0.5, 'borrow_heavy': 0.5}**: no_borrow=0.5980, borrow_heavy=0.5080
- **{'no_borrow': 0.3, 'borrow_heavy': 0.7}**: no_borrow=0.5987, borrow_heavy=0.5093
- **{'no_borrow': 0.1, 'borrow_heavy': 0.9}**: no_borrow=0.6000, borrow_heavy=0.5080

## Observations
- No_borrow accuracy: stable ~0.60 across all mixes
- Borrow_heavy accuracy: stable ~0.51 across all mixes
- Minimal sensitivity to mix ratio in this configuration
