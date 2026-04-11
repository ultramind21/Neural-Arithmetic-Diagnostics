# PROJECT 9 FAMILY PATTERNS IN 3D V1

## Base Structure
- shape: [3, 2, 2]
- family_map: [[[0, 0], [0, 0]], [[1, 1], [1, 1]], [[2, 2], [2, 2]]]
- base_total_carry_count: 2

## Perturbation Results
- pos=[0, 0, 0] | family=0 | changed_count=4 | carry 2→2
- pos=[0, 0, 1] | family=0 | changed_count=4 | carry 2→2
- pos=[0, 1, 0] | family=0 | changed_count=4 | carry 2→2
- pos=[0, 1, 1] | family=0 | changed_count=4 | carry 2→4
- pos=[1, 0, 0] | family=1 | changed_count=5 | carry 2→3
- pos=[1, 0, 1] | family=1 | changed_count=5 | carry 2→1
- pos=[1, 1, 0] | family=1 | changed_count=5 | carry 2→3
- pos=[1, 1, 1] | family=1 | changed_count=5 | carry 2→2
- pos=[2, 0, 0] | family=2 | changed_count=4 | carry 2→3
- pos=[2, 0, 1] | family=2 | changed_count=4 | carry 2→2
- pos=[2, 1, 0] | family=2 | changed_count=4 | carry 2→2
- pos=[2, 1, 1] | family=2 | changed_count=4 | carry 2→1

## Family Aggregates
- family 0: {'mean_changed_count': 4.0, 'mean_carry_after': 2.5, 'positions': [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1]]}
- family 1: {'mean_changed_count': 5.0, 'mean_carry_after': 2.25, 'positions': [[1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]}
- family 2: {'mean_changed_count': 4.0, 'mean_carry_after': 2.0, 'positions': [[2, 0, 0], [2, 0, 1], [2, 1, 0], [2, 1, 1]]}

## Interpretation Boundary
- This experiment tests whether family identity affects perturbation propagation in the 3D sandbox.
- It extends Project 9 from topology-sensitive to family-sensitive higher-dimensional structure.
