# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 194, 'transition region': 118, 'universal region': 488}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.9525 | 0.9184 | 0.9184 |
| V3.1 | 0.9825 | 0.9732 | 0.9732 |
| NN11 | 0.9487 | 0.9202 | 0.9202 |
| NN21 | 0.9750 | 0.9602 | 0.9602 |
| NN41 | 0.9925 | 0.9874 | 0.9874 |
| NN81 | 0.9912 | 0.9868 | 0.9868 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.0000 | 0.0000 | 0.0000 |
| V3.1 (boundary) | 0.0000 | 0.0000 | 0.0000 |
| NN11 (boundary) | 0.0000 | 0.0000 | 0.0000 |
| NN21 (boundary) | 0.0000 | 0.0000 | 0.0000 |
| NN41 (boundary) | 0.0000 | 0.0000 | 0.0000 |
| NN81 (boundary) | 0.0000 | 0.0000 | 0.0000 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0020 |
| 21x21 | 441 | 0.0027 |
| 41x41 | 1681 | 0.0137 |
| 81x81 | 6561 | 0.0534 |

Artifact:
- `project_12/results/revalidate/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`