# PROJECT 6 TRAJECTORY-PRESERVING INTERVENTION V1

## Parameters
- alpha: 0.5
- threshold: 5.0

## Family Results

### alternating_carry
- exact_match: 0.0
- trajectory_diff_mean: 10.771375465393067
- trajectory_diff_sequence: [15.117719650268555, 7.558859825134277, 11.338290214538574, 9.448575019836426, 10.3934326171875]
- smoothing_count: 5

### full_propagation_chain
- exact_match: 1.0
- trajectory_diff_mean: 0.26288931369781493
- trajectory_diff_sequence: [1.3144465684890747, 0.0, 0.0, 0.0, 0.0]
- smoothing_count: 0

### block_boundary_stress
- exact_match: 0.0
- trajectory_diff_mean: 10.168124771118164
- trajectory_diff_sequence: [15.8014497756958, 7.729362487792969, 3.8646812438964844, 15.630086898803711, 7.8150434494018555]
- smoothing_count: 4

## Interpretation Boundary
- This probe tests selective trajectory smoothing rather than uniform damping.
- It asks whether harmful jumps can be reduced without destroying useful dynamics.
