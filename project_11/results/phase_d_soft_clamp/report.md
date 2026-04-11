# PROJECT 11 — PHASE D REPORT (Soft-Clamp ground truth)

- points: 800 (reusing locked C3 holdout)
- soft clamp k: 15

- label shift hard→soft: 50 / 800 = 0.0625

## Overall (evaluated vs SOFT labels)
- V3: acc=0.8488 | macro-F1=0.8435
- V3.1: acc=0.9300 | macro-F1=0.9353
- NN11: acc=0.8938 | macro-F1=0.8770

## Subsets (evaluated vs SOFT labels)
- uniform:
  - V3:    n=400 | acc=0.9525 | macro-F1=0.9043
  - V3.1:  n=400 | acc=0.9725 | macro-F1=0.9490
  - NN11:  n=400 | acc=0.9400 | macro-F1=0.8985
- boundary:
  - V3:    n=400 | acc=0.7450 | macro-F1=0.6685
  - V3.1:  n=400 | acc=0.8875 | macro-F1=0.8693
  - NN11:  n=400 | acc=0.8475 | macro-F1=0.5938

Artifacts:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_11/results/phase_d_soft_clamp/artifact.json`