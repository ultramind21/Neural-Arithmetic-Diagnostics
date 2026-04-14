# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 127, 'transition region': 310, 'universal region': 363}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8488 | 0.8435 | 0.8435 |
| V3.1 | 0.9300 | 0.9353 | 0.9353 |
| NN11 | 0.8938 | 0.8770 | 0.8770 |
| NN21 | 0.9600 | 0.9481 | 0.9481 |
| NN41 | 0.9700 | 0.9674 | 0.9674 |
| NN81 | 0.9862 | 0.9847 | 0.9847 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7450 | 0.6685 | 0.6685 |
| V3.1 (boundary) | 0.8875 | 0.8693 | 0.8693 |
| NN11 (boundary) | 0.8475 | 0.5938 | 0.5938 |
| NN21 (boundary) | 0.9550 | 0.7672 | 0.7672 |
| NN41 (boundary) | 0.9525 | 0.8625 | 0.8625 |
| NN81 (boundary) | 0.9800 | 0.9291 | 0.9291 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0031 |
| 41x41 | 1681 | 0.0143 |
| 81x81 | 6561 | 0.0512 |

Artifact:
- `project_12/results/repro/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`