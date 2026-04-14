# PHASE D AUDIT — RECOMPUTE (softplus-based soft clamp)

- points: 800
- k (soft clamp): 15
- label shift hard→soft: 50 / 800 = 0.0625

## True label distribution (SOFT)
- {'family-aware region': 127, 'transition region': 310, 'universal region': 363}

## Overall metrics (vs SOFT labels)
- V3: acc=0.8488 | macroF1_fixed3=0.8435 | macroF1_present=0.8435 | pred_dist={'family-aware region': 162, 'transition region': 189, 'universal region': 449}
- V3.1: acc=0.9300 | macroF1_fixed3=0.9353 | macroF1_present=0.9353 | pred_dist={'family-aware region': 134, 'transition region': 256, 'universal region': 410}
- NN11: acc=0.8938 | macroF1_fixed3=0.8770 | macroF1_present=0.8770 | pred_dist={'family-aware region': 136, 'transition region': 279, 'universal region': 385}
- NN21: acc=0.9600 | macroF1_fixed3=0.9481 | macroF1_present=0.9481 | pred_dist={'family-aware region': 124, 'transition region': 310, 'universal region': 366}
- NN41: acc=0.9700 | macroF1_fixed3=0.9674 | macroF1_present=0.9674 | pred_dist={'family-aware region': 123, 'transition region': 310, 'universal region': 367}

## Subsets (vs SOFT labels) — macroF1_fixed3
- uniform: {'n': 400, 'V3': 0.9043289831376887, 'V3.1': 0.9490385986891386, 'NN11': 0.8984855300644773, 'NN21': 0.9374001387649916, 'NN41': 0.9787457754686318, 'true_dist': {'family-aware region': 114, 'transition region': 50, 'universal region': 236}}
- boundary: {'n': 400, 'V3': 0.6684888479190748, 'V3.1': 0.8693061378484614, 'NN11': 0.5937898870888562, 'NN21': 0.7671791835300548, 'NN41': 0.8624817135455434, 'true_dist': {'family-aware region': 13, 'transition region': 260, 'universal region': 127}}

## Confusion (NN11 vs SOFT labels)
```json
{
  "family-aware region": {
    "family-aware region": 109,
    "transition region": 18,
    "universal region": 0
  },
  "transition region": {
    "family-aware region": 27,
    "transition region": 252,
    "universal region": 31
  },
  "universal region": {
    "family-aware region": 0,
    "transition region": 9,
    "universal region": 354
  }
}
```