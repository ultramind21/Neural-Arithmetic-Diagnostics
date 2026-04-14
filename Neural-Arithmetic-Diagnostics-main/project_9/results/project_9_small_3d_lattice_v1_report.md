# PROJECT 9 SMALL 3D LATTICE V1

## Base Lattice
- shape: [2, 2, 2]
- base_lattice: [[[0, 7], [6, 4]], [[4, 8], [0, 6]]]

## Base Evaluation
- outputs: {'(0, 0, 0)': 2, '(0, 0, 1)': 8, '(0, 1, 0)': 6, '(0, 1, 1)': 7, '(1, 0, 0)': 5, '(1, 0, 1)': 0, '(1, 1, 0)': 2, '(1, 1, 1)': 7}
- carries: {'(0, 0, 0)': 0, '(0, 0, 1)': 0, '(0, 1, 0)': 0, '(0, 1, 1)': 0, '(1, 0, 0)': 0, '(1, 0, 1)': 1, '(1, 1, 0)': 0, '(1, 1, 1)': 0}
- total_carry_count: 1

## Perturbation Test
- perturbed_position: [0, 0, 0]
- old_value: 0
- new_value: 5
- output_changes: {'changed_count': 4, 'changed_positions': [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]]}
- carry_count_before: 1
- carry_count_after: 1

## Interpretation Boundary
- This first sandbox establishes whether local perturbation creates nontrivial global effects.
- It is a minimal higher-dimensional arithmetic-like composition environment.
