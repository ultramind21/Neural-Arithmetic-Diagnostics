# PROJECT 7 CONTEXT-TRIGGER INTERVENTION V1

## Family Results

### alternating_carry
- truth_full_sequence: [1, 0, 1, 0, 1, 0, 0]
- predicted_full_sequence: [1, 0, 0, 0, 0, 0, 0]
- exact_match: False
- intervention_count: 1
- trace:
  - {'position': 5, 'a_digit': 0, 'b_digit': 0, 'carry_in': 0, 'digit_true': 0, 'carry_true': 0, 'digit_pred_before': 1, 'carry_pred_before': 0, 'digit_pred_after': 0, 'carry_pred_after': 0, 'intervention_applied': True}
  - {'position': 4, 'a_digit': 9, 'b_digit': 1, 'carry_in': 0, 'digit_true': 0, 'carry_true': 1, 'digit_pred_before': 0, 'carry_pred_before': 1, 'digit_pred_after': 0, 'carry_pred_after': 1, 'intervention_applied': False}
  - {'position': 3, 'a_digit': 0, 'b_digit': 0, 'carry_in': 1, 'digit_true': 1, 'carry_true': 0, 'digit_pred_before': 0, 'carry_pred_before': 0, 'digit_pred_after': 0, 'carry_pred_after': 0, 'intervention_applied': False}
  - {'position': 2, 'a_digit': 9, 'b_digit': 1, 'carry_in': 0, 'digit_true': 0, 'carry_true': 1, 'digit_pred_before': 0, 'carry_pred_before': 1, 'digit_pred_after': 0, 'carry_pred_after': 1, 'intervention_applied': False}
  - {'position': 1, 'a_digit': 0, 'b_digit': 0, 'carry_in': 1, 'digit_true': 1, 'carry_true': 0, 'digit_pred_before': 0, 'carry_pred_before': 0, 'digit_pred_after': 0, 'carry_pred_after': 0, 'intervention_applied': False}
  - {'position': 0, 'a_digit': 9, 'b_digit': 1, 'carry_in': 0, 'digit_true': 0, 'carry_true': 1, 'digit_pred_before': 0, 'carry_pred_before': 1, 'digit_pred_after': 0, 'carry_pred_after': 1, 'intervention_applied': False}

### full_propagation_chain
- truth_full_sequence: [1, 1, 1, 1, 1, 1, 0]
- predicted_full_sequence: [1, 1, 1, 1, 1, 1, 0]
- exact_match: True
- intervention_count: 0
- trace:
  - {'position': 5, 'a_digit': 9, 'b_digit': 1, 'carry_in': 0, 'digit_true': 0, 'carry_true': 1, 'digit_pred_before': 0, 'carry_pred_before': 1, 'digit_pred_after': 0, 'carry_pred_after': 1, 'intervention_applied': False}
  - {'position': 4, 'a_digit': 9, 'b_digit': 1, 'carry_in': 1, 'digit_true': 1, 'carry_true': 1, 'digit_pred_before': 1, 'carry_pred_before': 1, 'digit_pred_after': 1, 'carry_pred_after': 1, 'intervention_applied': False}
  - {'position': 3, 'a_digit': 9, 'b_digit': 1, 'carry_in': 1, 'digit_true': 1, 'carry_true': 1, 'digit_pred_before': 1, 'carry_pred_before': 1, 'digit_pred_after': 1, 'carry_pred_after': 1, 'intervention_applied': False}
  - {'position': 2, 'a_digit': 9, 'b_digit': 1, 'carry_in': 1, 'digit_true': 1, 'carry_true': 1, 'digit_pred_before': 1, 'carry_pred_before': 1, 'digit_pred_after': 1, 'carry_pred_after': 1, 'intervention_applied': False}
  - {'position': 1, 'a_digit': 9, 'b_digit': 1, 'carry_in': 1, 'digit_true': 1, 'carry_true': 1, 'digit_pred_before': 1, 'carry_pred_before': 1, 'digit_pred_after': 1, 'carry_pred_after': 1, 'intervention_applied': False}
  - {'position': 0, 'a_digit': 9, 'b_digit': 1, 'carry_in': 1, 'digit_true': 1, 'carry_true': 1, 'digit_pred_before': 1, 'carry_pred_before': 1, 'digit_pred_after': 1, 'carry_pred_after': 1, 'intervention_applied': False}

### block_boundary_stress
- truth_full_sequence: [0, 0, 0, 9, 9, 9, 0]
- predicted_full_sequence: [0, 0, 0, 9, 9, 9, 0]
- exact_match: True
- intervention_count: 3
- trace:
  - {'position': 5, 'a_digit': 0, 'b_digit': 0, 'carry_in': 0, 'digit_true': 0, 'carry_true': 0, 'digit_pred_before': 1, 'carry_pred_before': 0, 'digit_pred_after': 0, 'carry_pred_after': 0, 'intervention_applied': True}
  - {'position': 4, 'a_digit': 1, 'b_digit': 8, 'carry_in': 0, 'digit_true': 9, 'carry_true': 0, 'digit_pred_before': 9, 'carry_pred_before': 0, 'digit_pred_after': 9, 'carry_pred_after': 0, 'intervention_applied': False}
  - {'position': 3, 'a_digit': 9, 'b_digit': 0, 'carry_in': 0, 'digit_true': 9, 'carry_true': 0, 'digit_pred_before': 9, 'carry_pred_before': 0, 'digit_pred_after': 9, 'carry_pred_after': 0, 'intervention_applied': False}
  - {'position': 2, 'a_digit': 9, 'b_digit': 0, 'carry_in': 0, 'digit_true': 9, 'carry_true': 0, 'digit_pred_before': 9, 'carry_pred_before': 0, 'digit_pred_after': 9, 'carry_pred_after': 0, 'intervention_applied': False}
  - {'position': 1, 'a_digit': 0, 'b_digit': 0, 'carry_in': 0, 'digit_true': 0, 'carry_true': 0, 'digit_pred_before': 1, 'carry_pred_before': 0, 'digit_pred_after': 0, 'carry_pred_after': 0, 'intervention_applied': True}
  - {'position': 0, 'a_digit': 0, 'b_digit': 0, 'carry_in': 0, 'digit_true': 0, 'carry_true': 0, 'digit_pred_before': 1, 'carry_pred_before': 0, 'digit_pred_after': 0, 'carry_pred_after': 0, 'intervention_applied': True}

## Interpretation Boundary
- This is a surgical trigger intervention on a specific recurring local failure context.
- It tests whether correcting that trigger is enough to rescue family-level behavior.
