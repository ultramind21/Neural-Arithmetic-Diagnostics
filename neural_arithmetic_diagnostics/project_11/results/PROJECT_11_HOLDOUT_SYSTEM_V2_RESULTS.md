# PROJECT 11 HOLDOUT SYSTEM V2 RESULTS
## Identifiability-Preserving Structural OOD Attempt (V2)

**Date:** April 2026  
**Project:** 11  
**Status:** COMPLETE

---

## 1. Main Result (from artifact)

### Summary Metrics

- **accuracy:** 0.6667 (66.67%)
- **boundary_accuracy:** 0.7778 (77.78%)
- **boundary_n:** 9
- **n_points:** 12
- **spearman(h_scale, H_obs):** -0.0280
- **spearman(u_power, P_obs):** 0.6644

### Confusion Matrix

```
family_aware_region:
  → family_aware_region: 0
  → transition_region: 0
  → universal_region: 0

transition_region:
  → family_aware_region: 1
  → transition_region: 5
  → universal_region: 0

universal_region:
  → family_aware_region: 1
  → transition_region: 2
  → universal_region: 3
```

---

## 2. Interpretation (bounded)

The correct bounded interpretation is:

> Under Holdout System V2 with signed heterogeneity interaction, we test whether H becomes structurally identifiable. Compared to V1:
> - Accuracy improved: 41.7% → 66.7%
> - Boundary accuracy improved: 44.4% → 77.8%
> - BUT: Spearman(h_scale, H_obs) worsened: -0.007 → -0.0280
>
> This suggests the system design (V2) successfully improved region prediction, but H_obs remains structurally non-monotonic with h_scale.

No further causal claims are made here without additional diagnostic analysis.

---
