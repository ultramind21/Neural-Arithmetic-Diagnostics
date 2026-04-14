# PROJECT 5 LOCAL DIGIT BOTTLENECK ANALYSIS

## Overall
- digit_acc: 0.415
- carry_acc: 1.0
- exact_acc: 0.415

## By carry_in
- carry_in = 0: {'count': 100, 'digit_acc': 0.39, 'carry_acc': 1.0, 'exact_acc': 0.39}
- carry_in = 1: {'count': 100, 'digit_acc': 0.44, 'carry_acc': 1.0, 'exact_acc': 0.44}

## By carry_out
- carry_out = 0: {'count': 100, 'digit_acc': 0.59, 'carry_acc': 1.0, 'exact_acc': 0.59}
- carry_out = 1: {'count': 100, 'digit_acc': 0.24, 'carry_acc': 1.0, 'exact_acc': 0.24}

## Most Common Digit Confusions
- true 8 -> pred 9: 8
- true 1 -> pred 2: 5
- true 2 -> pred 3: 5
- true 6 -> pred 5: 5
- true 1 -> pred 0: 5
- true 3 -> pred 2: 5
- true 3 -> pred 4: 4
- true 6 -> pred 7: 4
- true 7 -> pred 6: 4
- true 2 -> pred 1: 4
- true 9 -> pred 8: 4
- true 4 -> pred 2: 4
- true 0 -> pred 1: 3
- true 7 -> pred 8: 3
- true 9 -> pred 0: 3

## Interpretation Boundary
- This analysis is about local digit/carry learnability only.
- It does not yet explain the full Project 5 decomposition behavior mechanistically.
