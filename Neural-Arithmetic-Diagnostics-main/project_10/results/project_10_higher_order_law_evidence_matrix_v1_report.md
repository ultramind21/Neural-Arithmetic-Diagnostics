# PROJECT 10 HIGHER-ORDER LAW EVIDENCE MATRIX V1

## Higher-Order Candidate
**When local competence reaches saturation without global robustness, successful rescue requires mechanisms aligned to the heterogeneous structure of family-level failure.**

## Summary
- counts: {'support': 5, 'partial_support': 1, 'boundary': 2, 'no_evidence': 0, 'contradiction': 0, 'falsification_candidate': 0}
- chain_counts: {'local_competence_without_global_robustness': 2, 'family_level_heterogeneity': 2, 'family_sensitive_rescue': 3, 'boundary_on_naive_rescue': 1}
- support_strength_score: 5.5
- overall_verdict: STRONG SUPPORT

## Matrix Rows
- [Project 5] P5-R9 | component=local_competence_without_global_robustness | role=support | confidence=high | Strong local performance still fails compositionally
  - comments: Direct support for the first half of the higher-order candidate
- [Project 6] P6-R10 | component=local_competence_without_global_robustness | role=boundary | confidence=high | Carry direction is causally important locally
  - comments: Local mechanistic strength alone does not guarantee family-level explanation
- [Project 7] P7-R2 | component=family_level_heterogeneity | role=support | confidence=high | One family is trigger-correctable, another is not
  - comments: Strong support for heterogeneous family-level failure
- [Project 6] P6-R8 | component=family_level_heterogeneity | role=support | confidence=high | Trajectory dynamics differ sharply across families
  - comments: Strong support that family-level internal dynamics are not uniform
- [Project 8] P8-R2 | component=family_sensitive_rescue | role=support | confidence=high | Different family-level failures respond to different architectural components
  - comments: Strong architecture-level support
- [Project 9] P9-R5 | component=family_sensitive_rescue | role=support | confidence=high | Adaptive family-aware rescue outperforms naive rescue
  - comments: Strong sandbox-level support
- [Project 4] P4-I1 | component=family_sensitive_rescue | role=partial_support | confidence=high | Seen-family gain without broad held-out transfer
  - comments: Supports narrow intervention gain pattern but not full architecture-level rescue
- [Project 6] P6-R11 | component=boundary_on_naive_rescue | role=boundary | confidence=high | Trajectory smoothing does not rescue failing family
  - comments: Shows that not all rescue-like interventions are valid causal levers

## Interpretation Boundary
- This matrix tests whether the higher-order law is supported as a chain, not just as isolated statements.
- It is the first structured higher-order law test in Project 10.
