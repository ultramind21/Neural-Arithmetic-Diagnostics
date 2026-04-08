# PROJECT 11 PREDICTION GATE V1 — REPORT

**Verdict:** PASS

## Summary
- n_points: 12
- accuracy: 0.917
- random_baseline: 0.333
- majority_class: transition_region
- majority_baseline: 0.500
- boundary_n: 10
- boundary_accuracy: 0.9

## Confusion Matrix
```json
{
  "family_aware_region": {
    "family_aware_region": 2,
    "transition_region": 1,
    "universal_region": 0
  },
  "transition_region": {
    "family_aware_region": 0,
    "transition_region": 6,
    "universal_region": 0
  },
  "universal_region": {
    "family_aware_region": 0,
    "transition_region": 0,
    "universal_region": 3
  }
}
```

## Point Results
- G1: H=0.0058, P=0.3, pred=transition_region, actual=transition_region, correct=True, boundary=True
- G2: H=0.0063, P=0.3, pred=transition_region, actual=family_aware_region, correct=False, boundary=True
- G3: H=0.0067, P=0.3, pred=family_aware_region, actual=family_aware_region, correct=True, boundary=True
- G4: H=0.0078, P=0.3, pred=family_aware_region, actual=family_aware_region, correct=True, boundary=False
- G5: H=0.0105, P=0.32, pred=transition_region, actual=transition_region, correct=True, boundary=True
- G6: H=0.0105, P=0.327, pred=transition_region, actual=transition_region, correct=True, boundary=True
- G7: H=0.0105, P=0.333, pred=universal_region, actual=universal_region, correct=True, boundary=True
- G8: H=0.0105, P=0.338, pred=universal_region, actual=universal_region, correct=True, boundary=False
- G9: H=0.0135, P=0.32, pred=transition_region, actual=transition_region, correct=True, boundary=True
- G10: H=0.0135, P=0.327, pred=transition_region, actual=transition_region, correct=True, boundary=True
- G11: H=0.0135, P=0.333, pred=transition_region, actual=transition_region, correct=True, boundary=True
- G12: H=0.0135, P=0.338, pred=universal_region, actual=universal_region, correct=True, boundary=True