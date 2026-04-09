# PROJECT 11 — HOLDOUT SYSTEM V1 REPORT

- accuracy: 0.417
- boundary_accuracy: 0.4444444444444444

## Confusion Matrix
```json
{
  "family_aware_region": {
    "family_aware_region": 0,
    "transition_region": 1,
    "universal_region": 0
  },
  "transition_region": {
    "family_aware_region": 2,
    "transition_region": 3,
    "universal_region": 2
  },
  "universal_region": {
    "family_aware_region": 0,
    "transition_region": 2,
    "universal_region": 2
  }
}
```

## Per-Point
- S1: pred=transition_region actual=transition_region correct=True boundary=True H_obs=0.000402 P_obs=0.143750
- S2: pred=transition_region actual=transition_region correct=True boundary=True H_obs=0.000767 P_obs=0.118750
- S3: pred=family_aware_region actual=transition_region correct=False boundary=True H_obs=0.000301 P_obs=0.138125
- S4: pred=family_aware_region actual=transition_region correct=False boundary=False H_obs=0.002551 P_obs=0.144375
- S5: pred=transition_region actual=universal_region correct=False boundary=True H_obs=0.000473 P_obs=0.179375
- S6: pred=universal_region actual=transition_region correct=False boundary=True H_obs=0.000369 P_obs=0.160000
- S7: pred=universal_region actual=universal_region correct=True boundary=True H_obs=0.000022 P_obs=0.177500
- S8: pred=transition_region actual=family_aware_region correct=False boundary=True H_obs=0.000442 P_obs=0.133750
- S9: pred=transition_region actual=transition_region correct=True boundary=True H_obs=0.000072 P_obs=0.145000
- S10: pred=universal_region actual=transition_region correct=False boundary=True H_obs=0.000832 P_obs=0.199375
- S11: pred=universal_region actual=universal_region correct=True boundary=False H_obs=0.000395 P_obs=0.181250
- S12: pred=transition_region actual=universal_region correct=False boundary=False H_obs=0.000595 P_obs=0.211875