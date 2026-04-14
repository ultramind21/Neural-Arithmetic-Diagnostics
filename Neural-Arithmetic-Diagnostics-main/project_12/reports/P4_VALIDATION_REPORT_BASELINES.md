# P4_VALIDATION_REPORT_BASELINES — Project 4 Baseline Claims Validation

**Purpose:** Evidence-only validation of Project 4 baseline claims against Project 12 baseline reproductions.

**Evaluated Claims:**
- P4-C02: Block-boundary split (strong architecture difference)
- P4-C03: Weak in-distribution (universal baseline weakness)
- P4-C05: Alternating-carry and full-propagation-chain collapse (universal robustness failure)

**Artifacts Used:**
- `project_12/results/repro_p4/baselines/mlp/artifact.json`
- `project_12/results/repro_p4/baselines/lstm/artifact.json`
- `project_12/results/repro_p4/baselines/transformer/artifact.json`

---


**P4-C02 Validation: Block-Boundary Split**

Targets (pre-registered):
1. MLP block-boundary ≥ 0.80: **PASS** (observed: 1.0000)
2. Transformer block-boundary ≥ 0.80: **PASS** (observed: 1.0000)
3. LSTM block-boundary ≤ 0.20: **PASS** (observed: 0.0000)
4. Gap (min(MLP,Transformer) − LSTM) ≥ 0.50: **PASS** (observed: 1.0000)

Overall: **✅ PASS** — All targets met


---


**P4-C03 Validation: Weak In-Distribution**

Targets (pre-registered):
- MLP in-dist ≤ 0.20: **PASS** (observed: 0.0625)
- LSTM in-dist ≤ 0.20: **PASS** (observed: 0.0391)
- Transformer in-dist ≤ 0.20: **PASS** (observed: 0.0391)

Overall: **✅ PASS** — All architectures weak


---


**P4-C05 Validation: Alternating-Carry & Full-Propagation-Chain Collapse**

Alternating-Carry Family:
- MLP: 0.0000
- LSTM: 0.0000
- Transformer: 0.0000
- Max accuracy: 0.0000
- Universal weak (max ≤ 0.10): **PASS**
- No split (gap ≤ 0.10): **PASS** (gap = 0.0000)

Full-Propagation-Chain Family:
- MLP: 0.0000
- LSTM: 0.0000
- Transformer: 0.0000
- Max accuracy: 0.0000
- Universal weak (max ≤ 0.10): **PASS**
- No split (gap ≤ 0.10): **PASS** (gap = 0.0000)

Overall: **✅ PASS** — Both families universally weak with no architecture split


---

## Overall Summary

**All Claims Status:** ✅ PASS

**Claim Breakdown:**
- P4-C02 (block-boundary split): ✅ PASS
- P4-C03 (weak in-dist): ✅ PASS
- P4-C05 (alternating/fullprop collapse): ✅ PASS

**Interpretation:**
- **P4-C01 (framework):** Untested (infrastructure only)
- **P4-C04 (intervention):** Untested (requires intervention artifacts)
- **P4-C06 (reproducibility):** Untested (infrastructure only)

**Evidence Path Pointers:**
- Baseline repro check: `project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md`
- Baseline artifacts: `project_12/results/repro_p4/baselines/*/artifact.json`
- Manifest specifications: `project_12/manifests/p4_*_baseline_repro.json`

---

**Report Generated:** Project 12 Sprint 4C
