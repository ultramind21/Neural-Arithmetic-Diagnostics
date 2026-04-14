# PROJECT 9 PERTURBATION MAP V1

## Base Lattice
- shape: [2, 2, 2]
- base_total_carry_count: 1

## Position Sensitivity Map
- pos=[0, 0, 0] | old=0 -> new=5 | changed_count=4 | carry_before=1 | carry_after=1
- pos=[0, 0, 1] | old=7 -> new=2 | changed_count=4 | carry_before=1 | carry_after=0
- pos=[0, 1, 0] | old=6 -> new=1 | changed_count=4 | carry_before=1 | carry_after=1
- pos=[0, 1, 1] | old=4 -> new=9 | changed_count=4 | carry_before=1 | carry_after=2
- pos=[1, 0, 0] | old=4 -> new=9 | changed_count=4 | carry_before=1 | carry_after=2
- pos=[1, 0, 1] | old=8 -> new=3 | changed_count=4 | carry_before=1 | carry_after=0
- pos=[1, 1, 0] | old=0 -> new=5 | changed_count=4 | carry_before=1 | carry_after=1
- pos=[1, 1, 1] | old=6 -> new=1 | changed_count=4 | carry_before=1 | carry_after=0

## Interpretation Boundary
- This experiment tests whether different positions have different local-to-global influence.
- It is the first topology-sensitive mapping result in Project 9.
