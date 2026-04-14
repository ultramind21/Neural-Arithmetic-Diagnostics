# PROJECT 8 MINIMAL COMPOSITION ARCHITECTURE V2

## Family-by-Variant Results

### alternating_carry
- baseline_composition: exact_match=False, interface_count=0, controller_count=0
- interface_only: exact_match=True, interface_count=1, controller_count=0
- controller_only: exact_match=False, interface_count=0, controller_count=0
- interface_plus_controller: exact_match=True, interface_count=1, controller_count=0

### full_propagation_chain
- baseline_composition: exact_match=False, interface_count=0, controller_count=0
- interface_only: exact_match=False, interface_count=0, controller_count=0
- controller_only: exact_match=True, interface_count=0, controller_count=5
- interface_plus_controller: exact_match=True, interface_count=0, controller_count=5

### block_boundary_stress
- baseline_composition: exact_match=False, interface_count=0, controller_count=0
- interface_only: exact_match=True, interface_count=3, controller_count=0
- controller_only: exact_match=False, interface_count=0, controller_count=0
- interface_plus_controller: exact_match=True, interface_count=3, controller_count=0

## Interpretation Boundary
- This v2 experiment uses controlled local error injection to make variant comparison meaningful.
- It tests whether interface or controller structure can prevent local failure from becoming global breakdown.
