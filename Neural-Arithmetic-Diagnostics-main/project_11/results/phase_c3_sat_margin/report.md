# PROJECT 11 — PHASE C3 REPORT (Saturation-aware margins)

- points: 800
- seed: 223311

## Overall
- V3-hard: acc=0.8638 | macro-F1=0.8771
- V3.1 sat-margin: acc=0.8875 | macro-F1=0.8893
- NN11: acc=0.9300 | macro-F1=0.9162

## Subsets (macro-F1)
- uniform: n=400 | V3=0.8901 | V3.1=0.9051 | NN11=0.9467
- boundary: n=400 | V3=0.8280 | V3.1=0.7755 | NN11=0.7789
- sat_risk_ge1: n=737 | V3=0.8673 | V3.1=0.8743 | NN11=0.9422
- sat_risk_0: n=63 | V3=0.6667 | V3.1=0.6667 | NN11=0.4444

## Saturation-linked errors
- V3 errors: 109 | errors_with_sat: 109
- V3.1 errors: 90 | errors_with_sat: 90

Artifacts:
- `D:/Music/Project 03 Abacus/neural_arithmetic_diagnostics/project_11/results/phase_c3_sat_margin/artifact.json`