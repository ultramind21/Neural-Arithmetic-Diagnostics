# PROJECT 6 CARRY SELECTIVITY PROBE V1 REPORT

## Experiment Summary
Extracted carry selectivity from two local processor architectures.

## Results

### SIMPLE
- Units: 32
- Cases (carry=0, carry=1): (100, 100)
- Average carry separability score: 0.988624
- Top 5 carry-selective unit indices: [6, 22, 7, 16, 20]
- Top 5 separability scores: ['2.7301', '2.7259', '2.6775', '2.6322', '2.4619']

### CARRY_CONDITIONED
- Units: 32
- Cases (carry=0, carry=1): (100, 100)
- Average carry separability score: 1.248519
- Top 5 carry-selective unit indices: [11, 31, 27, 17, 24]
- Top 5 separability scores: ['2.9775', '2.6650', '2.3306', '2.1263', '2.1156']

## Interpretation
- Higher separability score indicates stronger carry-selective encoding.
- Top unit indices show which hidden units best distinguish carry_out.
- This is the first probe; full interpretability requires deeper analysis.
