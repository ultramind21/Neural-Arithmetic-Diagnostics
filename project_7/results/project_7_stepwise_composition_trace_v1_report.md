# PROJECT 7 STEPWISE COMPOSITION TRACE V1

## Families

### alternating_carry
- truth_full_sequence: [1, 0, 1, 0, 1, 0, 0]
- predicted_full_sequence: [1, 0, 1, 0, 1, 0, 1]
- exact_match: False
- step trace:
  - {'position': 5, 'a_digit': 0, 'b_digit': 0, 'carry_in': 0, 'digit_true': 0, 'carry_true': 0, 'digit_pred': 1, 'carry_pred': 0, 'digit_correct': False, 'carry_correct': True, 'hidden_first5': [-8.441204071044922, 8.804788589477539, 6.297584533691406, -11.57761001586914, -4.662834167480469], 'hidden_diff_from_prev': None}
  - {'position': 4, 'a_digit': 9, 'b_digit': 1, 'carry_in': 0, 'digit_true': 0, 'carry_true': 1, 'digit_pred': 0, 'carry_pred': 1, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-2.233380079269409, 1.9005969762802124, -0.76565021276474, -0.6919878721237183, 0.9377197027206421], 'hidden_diff_from_prev': 13.465715408325195}
  - {'position': 3, 'a_digit': 0, 'b_digit': 0, 'carry_in': 1, 'digit_true': 1, 'carry_true': 0, 'digit_pred': 1, 'carry_pred': 0, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-6.131756782531738, 7.058542728424072, 4.5002570152282715, -10.659716606140137, -5.069783687591553], 'hidden_diff_from_prev': 11.522928237915039}
  - {'position': 2, 'a_digit': 9, 'b_digit': 1, 'carry_in': 0, 'digit_true': 0, 'carry_true': 1, 'digit_pred': 0, 'carry_pred': 1, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-2.233380079269409, 1.9005969762802124, -0.76565021276474, -0.6919878721237183, 0.9377197027206421], 'hidden_diff_from_prev': 11.522928237915039}
  - {'position': 1, 'a_digit': 0, 'b_digit': 0, 'carry_in': 1, 'digit_true': 1, 'carry_true': 0, 'digit_pred': 1, 'carry_pred': 0, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-6.131756782531738, 7.058542728424072, 4.5002570152282715, -10.659716606140137, -5.069783687591553], 'hidden_diff_from_prev': 11.522928237915039}
  - {'position': 0, 'a_digit': 9, 'b_digit': 1, 'carry_in': 0, 'digit_true': 0, 'carry_true': 1, 'digit_pred': 0, 'carry_pred': 1, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-2.233380079269409, 1.9005969762802124, -0.76565021276474, -0.6919878721237183, 0.9377197027206421], 'hidden_diff_from_prev': 11.522928237915039}

### full_propagation_chain
- truth_full_sequence: [1, 1, 1, 1, 1, 1, 0]
- predicted_full_sequence: [1, 1, 1, 1, 1, 1, 0]
- exact_match: True
- step trace:
  - {'position': 5, 'a_digit': 9, 'b_digit': 1, 'carry_in': 0, 'digit_true': 0, 'carry_true': 1, 'digit_pred': 0, 'carry_pred': 1, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-2.233380079269409, 1.9005969762802124, -0.76565021276474, -0.6919878721237183, 0.9377197027206421], 'hidden_diff_from_prev': None}
  - {'position': 4, 'a_digit': 9, 'b_digit': 1, 'carry_in': 1, 'digit_true': 1, 'carry_true': 1, 'digit_pred': 1, 'carry_pred': 1, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-4.3187150955200195, 3.6334946155548096, 1.4840888977050781, 0.6512662768363953, 2.779905080795288], 'hidden_diff_from_prev': 1.2895357608795166}
  - {'position': 3, 'a_digit': 9, 'b_digit': 1, 'carry_in': 1, 'digit_true': 1, 'carry_true': 1, 'digit_pred': 1, 'carry_pred': 1, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-4.3187150955200195, 3.6334946155548096, 1.4840888977050781, 0.6512662768363953, 2.779905080795288], 'hidden_diff_from_prev': 0.0}
  - {'position': 2, 'a_digit': 9, 'b_digit': 1, 'carry_in': 1, 'digit_true': 1, 'carry_true': 1, 'digit_pred': 1, 'carry_pred': 1, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-4.3187150955200195, 3.6334946155548096, 1.4840888977050781, 0.6512662768363953, 2.779905080795288], 'hidden_diff_from_prev': 0.0}
  - {'position': 1, 'a_digit': 9, 'b_digit': 1, 'carry_in': 1, 'digit_true': 1, 'carry_true': 1, 'digit_pred': 1, 'carry_pred': 1, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-4.3187150955200195, 3.6334946155548096, 1.4840888977050781, 0.6512662768363953, 2.779905080795288], 'hidden_diff_from_prev': 0.0}
  - {'position': 0, 'a_digit': 9, 'b_digit': 1, 'carry_in': 1, 'digit_true': 1, 'carry_true': 1, 'digit_pred': 1, 'carry_pred': 1, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [-4.3187150955200195, 3.6334946155548096, 1.4840888977050781, 0.6512662768363953, 2.779905080795288], 'hidden_diff_from_prev': 0.0}

### block_boundary_stress
- truth_full_sequence: [0, 0, 0, 9, 9, 9, 0]
- predicted_full_sequence: [0, 1, 1, 9, 9, 9, 1]
- exact_match: False
- step trace:
  - {'position': 5, 'a_digit': 0, 'b_digit': 0, 'carry_in': 0, 'digit_true': 0, 'carry_true': 0, 'digit_pred': 1, 'carry_pred': 0, 'digit_correct': False, 'carry_correct': True, 'hidden_first5': [-8.441204071044922, 8.804788589477539, 6.297584533691406, -11.57761001586914, -4.662834167480469], 'hidden_diff_from_prev': None}
  - {'position': 4, 'a_digit': 1, 'b_digit': 8, 'carry_in': 0, 'digit_true': 9, 'carry_true': 0, 'digit_pred': 9, 'carry_pred': 0, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [0.04977831244468689, 0.07151833176612854, -2.850926637649536, -1.7286722660064697, -0.7936480045318604], 'hidden_diff_from_prev': 13.409558296203613}
  - {'position': 3, 'a_digit': 9, 'b_digit': 0, 'carry_in': 0, 'digit_true': 9, 'carry_true': 0, 'digit_pred': 9, 'carry_pred': 0, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [0.22702863812446594, 0.03062465414404869, -3.361583948135376, -2.001830577850342, -1.0569075345993042], 'hidden_diff_from_prev': 0.20752832293510437}
  - {'position': 2, 'a_digit': 9, 'b_digit': 0, 'carry_in': 0, 'digit_true': 9, 'carry_true': 0, 'digit_pred': 9, 'carry_pred': 0, 'digit_correct': True, 'carry_correct': True, 'hidden_first5': [0.22702863812446594, 0.03062465414404869, -3.361583948135376, -2.001830577850342, -1.0569075345993042], 'hidden_diff_from_prev': 0.0}
  - {'position': 1, 'a_digit': 0, 'b_digit': 0, 'carry_in': 0, 'digit_true': 0, 'carry_true': 0, 'digit_pred': 1, 'carry_pred': 0, 'digit_correct': False, 'carry_correct': True, 'hidden_first5': [-8.441204071044922, 8.804788589477539, 6.297584533691406, -11.57761001586914, -4.662834167480469], 'hidden_diff_from_prev': 13.509405136108398}
  - {'position': 0, 'a_digit': 0, 'b_digit': 0, 'carry_in': 0, 'digit_true': 0, 'carry_true': 0, 'digit_pred': 1, 'carry_pred': 0, 'digit_correct': False, 'carry_correct': True, 'hidden_first5': [-8.441204071044922, 8.804788589477539, 6.297584533691406, -11.57761001586914, -4.662834167480469], 'hidden_diff_from_prev': 0.0}

## Interpretation Boundary
- This experiment traces where local competence first fails to produce globally correct behavior.
- It is a bridge experiment, not a final full theory.
