# PROJECT 5 FAMILY STRUCTURE ANALYSIS V1

## Purpose
This report compares the internal structural properties of the three Project 5 core families.

## alternating_carry
- a_first: [9, 0, 9, 0, 9, 0]
- b_first: [1, 0, 1, 0, 1, 0]
- carry_seq_first: [1, 0, 1, 0, 1, 0]
- a_transitions: 5
- b_transitions: 5
- carry_transitions: 5
- pair_diversity: 2
- triple_diversity: 2
- periodicity_hint: short_periodic
- most_common_pairs: [((9, 1), 3), ((0, 0), 3)]
- most_common_triples: [((9, 1, 1), 3), ((0, 0, 0), 3)]

## full_propagation_chain
- a_first: [9, 9, 9, 9, 9, 9]
- b_first: [1, 1, 1, 1, 1, 1]
- carry_seq_first: [1, 1, 1, 1, 1, 1]
- a_transitions: 0
- b_transitions: 0
- carry_transitions: 0
- pair_diversity: 1
- triple_diversity: 1
- periodicity_hint: uniform
- most_common_pairs: [((9, 1), 6)]
- most_common_triples: [((9, 1, 1), 6)]

## block_boundary_stress
- a_first: [0, 0, 9, 9, 1, 0]
- b_first: [0, 0, 0, 0, 8, 0]
- carry_seq_first: [0, 0, 0, 0, 0, 0]
- a_transitions: 3
- b_transitions: 2
- carry_transitions: 0
- pair_diversity: 3
- triple_diversity: 3
- periodicity_hint: block_or_mixed
- most_common_pairs: [((0, 0), 3), ((9, 0), 2), ((1, 8), 1)]
- most_common_triples: [((0, 0, 0), 3), ((9, 0, 0), 2), ((1, 8, 0), 1)]

## Interpretation Boundary
- This analysis identifies structural differences, not final causal proof.
- Its role is to narrow the next mechanistic or representational hypothesis.
