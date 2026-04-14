# PROJECT 5 POST-INTERVENTION FAILURE ANALYSIS

## Family-by-Family Summary

### alternating_carry
- digit_acc: 0.8333333333333334
- carry_acc: 1.0
- exact_acc: 0.8333333333333334
- position_digit_acc: [1.0, 1.0, 1.0, 1.0, 1.0, 0.0]
- position_carry_acc: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
- position_exact_acc: [1.0, 1.0, 1.0, 1.0, 1.0, 0.0]
- first true digit: [0, 1, 0, 1, 0, 0]
- first pred digit: [0, 1, 0, 1, 0, 1]
- first true carry: [1, 0, 1, 0, 1, 0]
- first pred carry: [1, 0, 1, 0, 1, 0]

### full_propagation_chain
- digit_acc: 1.0
- carry_acc: 1.0
- exact_acc: 1.0
- position_digit_acc: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
- position_carry_acc: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
- position_exact_acc: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
- first true digit: [1, 1, 1, 1, 1, 0]
- first pred digit: [1, 1, 1, 1, 1, 0]
- first true carry: [1, 1, 1, 1, 1, 1]
- first pred carry: [1, 1, 1, 1, 1, 1]

### block_boundary_stress
- digit_acc: 0.5
- carry_acc: 1.0
- exact_acc: 0.5
- position_digit_acc: [0.0, 0.0, 1.0, 1.0, 1.0, 0.0]
- position_carry_acc: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
- position_exact_acc: [0.0, 0.0, 1.0, 1.0, 1.0, 0.0]
- first true digit: [0, 0, 9, 9, 9, 0]
- first pred digit: [1, 1, 9, 9, 9, 1]
- first true carry: [0, 0, 0, 0, 0, 0]
- first pred carry: [0, 0, 0, 0, 0, 0]

## Interpretation Boundary
- This analysis compares the rescued family and still-failing families after explicit carry-conditioned representation.
- It aims to identify where structured failure remains concentrated.
