# PROJECT 10 LAW 3 EVIDENCE MATRIX V1

## Candidate Law
**Rescue mechanisms are family-sensitive rather than universal.**

## Summary
- counts: {'support': 6, 'partial_support': 1, 'boundary': 1, 'no_evidence': 0, 'contradiction': 0, 'falsification_candidate': 0}
- support_strength_score: 6.5
- overall_verdict: STRONG SUPPORT

## Matrix Rows
- [Project 4] P4-I1 | role=partial_support | confidence=high | Adversarial training improves seen family without broad held-out transfer
  - boundary_note: Intervention gain was real but structurally narrow rather than broad
  - falsification_relevance: not a direct falsifier
  - comments: Supports family-sensitive gain logic, but was not framed as explicit family-specific rescue architecture
- [Project 5] P5-R5 | role=support | confidence=high | Explicit carry-conditioned representation rescues only the structurally simplest family
  - boundary_note: Rescue appears family-limited rather than broad
  - falsification_relevance: not a falsifier
  - comments: Strong support: one family rescued, others still fail
- [Project 5] P5-R8 | role=boundary | confidence=high | Local context expansion does not rescue other failing families
  - boundary_note: Simple richer context does not universalize rescue
  - falsification_relevance: not a falsifier
  - comments: Supports the idea that rescue is structurally constrained
- [Project 7] P7-R2 | role=support | confidence=high | Trigger intervention rescues one family but not another
  - boundary_note: The same local trigger fix is sufficient for one family and insufficient for another
  - falsification_relevance: not a falsifier
  - comments: One of the strongest direct supports for Law 3
- [Project 8] P8-R1 | role=support | confidence=high | Interface and controller rescue different family-level failure modes
  - boundary_note: No single rescue mechanism handles all tested family types by itself
  - falsification_relevance: not a falsifier
  - comments: Strong architecture-level support
- [Project 8] P8-R2 | role=support | confidence=high | Integrated architecture combines family-sensitive rescue mechanisms successfully
  - boundary_note: Different sub-mechanisms appear necessary for different families
  - falsification_relevance: not a falsifier
  - comments: Strong support at architecture-design level
- [Project 9] P9-R4 | role=support | confidence=high | Cross-family rescue can be harmful while same-family rescue can be safe
  - boundary_note: Rescue quality depends on family alignment
  - falsification_relevance: not a falsifier
  - comments: Strong support inside the 3D sandbox
- [Project 9] P9-R5 | role=support | confidence=high | Adaptive family-aware rescue outperforms naive cross-family rescue
  - boundary_note: Adaptive rescue improves because it respects family structure
  - falsification_relevance: not a falsifier
  - comments: One of the strongest supports for Law 3

## Interpretation Boundary
- This matrix is a stronger methodological step than plain textual pattern matching.
- It is still an early law-testing layer, not a final theory verdict.
