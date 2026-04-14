# PROJECT 10 LAW 1 EVIDENCE MATRIX V1

## Candidate Law
**Local competence is not sufficient for global robustness.**

## Summary
- counts: {'support': 7, 'partial_support': 0, 'boundary': 2, 'no_evidence': 0, 'contradiction': 0, 'falsification_candidate': 0}
- support_strength_score: 7.0
- overall_verdict: STRONG SUPPORT

## Matrix Rows
- [Project 5] P5-R1 | role=support | confidence=high | Oracle decomposition works but learned local composition fails
  - boundary_note: Structural feasibility does not transfer automatically to learned composition
  - falsification_relevance: not a falsifier
  - comments: Direct strong support: local correctness in principle does not guarantee global learned success
- [Project 5] P5-R5 | role=support | confidence=high | Explicit carry-conditioned representation improves local behavior but rescues only one family
  - boundary_note: Improved local competence still does not imply broad family-level robustness
  - falsification_relevance: not a falsifier
  - comments: Very strong support
- [Project 5] P5-R9 | role=support | confidence=high | Strong local transition-aware performance still fails compositionally
  - boundary_note: Even strong local metrics do not guarantee successful composition
  - falsification_relevance: not a falsifier
  - comments: One of the strongest supports for Law 1
- [Project 6] P6-R10 | role=boundary | confidence=high | Carry-related direction is causally important for local arithmetic behavior
  - boundary_note: Shows strong local causal structure, but does not itself guarantee family-level success
  - falsification_relevance: not a falsifier
  - comments: Important boundary evidence
- [Project 6] P6-SYN | role=support | confidence=high | Mechanistic structure is real but not globally sufficient
  - boundary_note: Internal arithmetic structure can be real without complete family-level explanation
  - falsification_relevance: not a falsifier
  - comments: Strong support from synthesis
- [Project 7] P7-R1 | role=support | confidence=high | Stepwise trace reveals local recurring failures driving global mismatch
  - boundary_note: Local correctness is not uniformly enough for global exact success
  - falsification_relevance: not a falsifier
  - comments: Strong bridge support
- [Project 7] P7-R2 | role=support | confidence=high | One trigger correction rescues one family but not another
  - boundary_note: Fixing one local trigger is insufficient for universal family-level rescue
  - falsification_relevance: not a falsifier
  - comments: Very strong support
- [Project 8] P8-R2 | role=support | confidence=high | Integrated architecture rescues multiple families through distinct mechanisms
  - boundary_note: Architecture-level support is needed beyond local competence alone
  - falsification_relevance: not a falsifier
  - comments: Strong architecture-level support
- [Project 9] P9-R4 | role=boundary | confidence=medium | Rescue in higher-dimensional sandbox is itself family-sensitive
  - boundary_note: Higher-dimensional composition still needs structured rescue logic
  - falsification_relevance: not a falsifier
  - comments: Supports extension of the law into richer spaces

## Interpretation Boundary
- This matrix evaluates whether strong local competence repeatedly fails to guarantee robust global success.
- It is a structured law test, not a rhetorical summary.
