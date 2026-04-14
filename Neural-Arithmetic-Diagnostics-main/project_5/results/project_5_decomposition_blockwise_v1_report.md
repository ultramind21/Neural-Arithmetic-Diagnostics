# PROJECT 5 DECOMPOSITION BLOCKWISE V1 RESULTS

## Status
First bounded decomposition experiment completed.

## Experiment Type
Small-block decomposition with explicit carry interface

## Chunk Size
- 2

## Family Results

### alternating_carry
- full_exact_reference: 1.0
- blockwise_with_carry_interface: 1.0
- blockwise_carry_reset: 0.0

### full_propagation_chain
- full_exact_reference: 1.0
- blockwise_with_carry_interface: 1.0
- blockwise_carry_reset: 0.0

### block_boundary_stress
- full_exact_reference: 1.0
- blockwise_with_carry_interface: 1.0
- blockwise_carry_reset: 1.0

## Interpretation Boundary
- This is a clean decomposition control experiment using exact local arithmetic.
- It does not yet use a learned local processor.
- Its role is to test whether decomposition itself is structurally favorable before learned local decomposition is attempted.
