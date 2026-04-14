# PROJECT 6 SUCCESS VS FAILURE PROBE V1

## Overall
- digit_acc: 0.96
- carry_acc: 1.0
- exact_acc: 0.96
- success_count: 192
- failure_count: 8

## Top Units Distinguishing Success vs Failure
- unit indices: [18, 29, 13, 11, 9]
- scores: [8.2703218460083, 7.376978397369385, 6.400684833526611, 6.004878044128418, 5.3606109619140625]

## Hidden Means (First 5 dims)
- success mean: [2.7902114391326904, 0.10389068722724915, -0.8342098593711853, -5.595850467681885, -1.1231855154037476]
- failure mean: [-1.8704404830932617, -4.700680732727051, -5.419096946716309, -4.719346523284912, -5.2820234298706055]

## Sample Failure Cases
- {'a': 0, 'b': 0, 'carry_in': 0, 'digit_true': 0, 'digit_pred': 1, 'carry_true': 0, 'carry_pred': 0}
- {'a': 0, 'b': 0, 'carry_in': 1, 'digit_true': 1, 'digit_pred': 0, 'carry_true': 0, 'carry_pred': 0}
- {'a': 7, 'b': 8, 'carry_in': 1, 'digit_true': 6, 'digit_pred': 7, 'carry_true': 1, 'carry_pred': 1}
- {'a': 8, 'b': 7, 'carry_in': 1, 'digit_true': 6, 'digit_pred': 7, 'carry_true': 1, 'carry_pred': 1}
- {'a': 8, 'b': 9, 'carry_in': 1, 'digit_true': 8, 'digit_pred': 7, 'carry_true': 1, 'carry_pred': 1}
- {'a': 9, 'b': 8, 'carry_in': 1, 'digit_true': 8, 'digit_pred': 7, 'carry_true': 1, 'carry_pred': 1}
- {'a': 9, 'b': 9, 'carry_in': 0, 'digit_true': 8, 'digit_pred': 7, 'carry_true': 1, 'carry_pred': 1}
- {'a': 9, 'b': 9, 'carry_in': 1, 'digit_true': 9, 'digit_pred': 8, 'carry_true': 1, 'carry_pred': 1}

## Interpretation Boundary
- This probe asks whether failure is behaviorally and internally distinguishable.
- It is still exploratory and does not yet establish a full mechanistic circuit claim.
