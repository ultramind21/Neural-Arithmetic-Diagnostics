# PHASE D — Resolution Sweep Extended (soft labels)

- points: 800
- soft clamp k: 15
- true label dist: {'family-aware region': 112, 'transition region': 311, 'universal region': 377}

## Overall (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 | 0.8538 | 0.8386 | 0.8386 |
| V3.1 | 0.9400 | 0.9391 | 0.9391 |
| NN11 | 0.9113 | 0.8877 | 0.8877 |
| NN21 | 0.9550 | 0.9409 | 0.9409 |
| NN41 | 0.9800 | 0.9760 | 0.9760 |
| NN81 | 0.9838 | 0.9771 | 0.9771 |

## Boundary subset (macro_f1_present)
| model | acc | macroF1_present | macroF1_fixed3 |
|---|---:|---:|---:|
| V3 (boundary) | 0.7550 | 0.5975 | 0.5975 |
| V3.1 (boundary) | 0.9000 | 0.7593 | 0.7593 |
| NN11 (boundary) | 0.8675 | 0.6098 | 0.6098 |
| NN21 (boundary) | 0.9375 | 0.7022 | 0.7022 |
| NN41 (boundary) | 0.9725 | 0.8573 | 0.8573 |
| NN81 (boundary) | 0.9700 | 0.7578 | 0.7578 |

## NN grid build cost
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0010 |
| 21x21 | 441 | 0.0032 |
| 41x41 | 1681 | 0.0133 |
| 81x81 | 6561 | 0.0523 |

Artifact:
- `project_12/results/revalidate_p11proc/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`