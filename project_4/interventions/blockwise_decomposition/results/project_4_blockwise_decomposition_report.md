# PROJECT 4 BLOCKWISE DECOMPOSITION RESULTS

## Status
Initial bounded blockwise decomposition artifact generated.

## Variants Tested
- naive_chunking: {'in_distribution': 1.0, 'alternating_carry': 1.0, 'full_propagation_chain': 1.0, 'block_boundary_stress': 1.0}
- chunking_with_carry_interface: {'in_distribution': 0.0625, 'alternating_carry': 0.0, 'full_propagation_chain': 0.0, 'block_boundary_stress': 1.0}
- hierarchical_chunking: {'in_distribution': 0.0625, 'alternating_carry': 0.0, 'full_propagation_chain': 0.0, 'block_boundary_stress': 1.0}

## Qualification Notes
- This is a bounded first blockwise artifact.
- Local digitwise use of the Phase 30 MLP is an explicit Project 4 adapter assumption.
- Hierarchical chunking is currently a placeholder surrogate for interface-aware chunking.
- Results should be treated as first structural signals, not final blockwise verdicts.