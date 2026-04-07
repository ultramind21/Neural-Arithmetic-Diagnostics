# PROJECT 9 SMALL 3D LATTICE V2

## Base Lattice
- shape: [3, 2, 2]
- base_total_carry_count: 2

## Position Sensitivity Map
- pos=[0, 0, 0] (corner_like) | old=0 -> new=5 | changed_count=4 | carry_before=2 | carry_after=2
- pos=[0, 0, 1] (corner_like) | old=7 -> new=2 | changed_count=4 | carry_before=2 | carry_after=1
- pos=[0, 1, 0] (corner_like) | old=6 -> new=1 | changed_count=4 | carry_before=2 | carry_after=2
- pos=[0, 1, 1] (corner_like) | old=4 -> new=9 | changed_count=4 | carry_before=2 | carry_after=3
- pos=[1, 0, 0] (edge_like) | old=4 -> new=9 | changed_count=5 | carry_before=2 | carry_after=3
- pos=[1, 0, 1] (edge_like) | old=8 -> new=3 | changed_count=5 | carry_before=2 | carry_after=1
- pos=[1, 1, 0] (edge_like) | old=0 -> new=5 | changed_count=5 | carry_before=2 | carry_after=2
- pos=[1, 1, 1] (edge_like) | old=6 -> new=1 | changed_count=5 | carry_before=2 | carry_after=1
- pos=[2, 0, 0] (corner_like) | old=2 -> new=7 | changed_count=4 | carry_before=2 | carry_after=2
- pos=[2, 0, 1] (corner_like) | old=0 -> new=5 | changed_count=4 | carry_before=2 | carry_after=2
- pos=[2, 1, 0] (corner_like) | old=5 -> new=0 | changed_count=4 | carry_before=2 | carry_after=2
- pos=[2, 1, 1] (corner_like) | old=9 -> new=4 | changed_count=4 | carry_before=2 | carry_after=1

## Ranked Influence
- pos=[1, 0, 0] (edge_like) | changed_count=5 | carry_before=2 | carry_after=3
- pos=[1, 0, 1] (edge_like) | changed_count=5 | carry_before=2 | carry_after=1
- pos=[1, 1, 0] (edge_like) | changed_count=5 | carry_before=2 | carry_after=2
- pos=[1, 1, 1] (edge_like) | changed_count=5 | carry_before=2 | carry_after=1
- pos=[0, 0, 0] (corner_like) | changed_count=4 | carry_before=2 | carry_after=2
- pos=[0, 0, 1] (corner_like) | changed_count=4 | carry_before=2 | carry_after=1
- pos=[0, 1, 0] (corner_like) | changed_count=4 | carry_before=2 | carry_after=2
- pos=[0, 1, 1] (corner_like) | changed_count=4 | carry_before=2 | carry_after=3
- pos=[2, 0, 0] (corner_like) | changed_count=4 | carry_before=2 | carry_after=2
- pos=[2, 0, 1] (corner_like) | changed_count=4 | carry_before=2 | carry_after=2
- pos=[2, 1, 0] (corner_like) | changed_count=4 | carry_before=2 | carry_after=2
- pos=[2, 1, 1] (corner_like) | changed_count=4 | carry_before=2 | carry_after=1

## Interpretation Boundary
- This experiment tests whether a larger 3D lattice breaks the perturbation symmetry of v1.
- It is the first scale-up result in Project 9.
