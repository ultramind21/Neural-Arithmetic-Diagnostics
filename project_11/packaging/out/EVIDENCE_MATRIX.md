# PROJECT 11 — EVIDENCE MATRIX (Phase D/E)

## Core results (soft labels, k=15)

| Item | Best setting | Metric | Value | Source |
|---|---|---:|---:|---|
| Rule baseline | V3.1 | macroF1_present | 0.9353 | Phase D resolution sweep |
| Dense NN | NN81 (6561 pts) | macroF1_present | 0.9847 | Phase D resolution sweep |
| Dense NN (mid) | NN41 (1681 pts) | macroF1_present | 0.9674 | Phase D resolution sweep |
| Adaptive NN | N=2000 (1000 uniform + 1000 boundary) | macroF1_present | 0.9752 | Phase E1 report |
| Sample-efficiency peak | N=1000 mixed | macroF1_present (mean over seeds) | 0.9780 | Phase E2 report/analysis |
| Ratio sweep best | N=1500, frac=0.5, 1-NN | macroF1_present (mean over seeds) | 0.9747 | Phase E3 report |
