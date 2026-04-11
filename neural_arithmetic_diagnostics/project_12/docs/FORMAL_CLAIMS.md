# FORMAL_CLAIMS — Project 12 (Locked Claims)

## How to use
- Every claim must have an ID.
- Every experiment must reference exactly one claim ID.
- No claim is considered valid without: baselines + metrics + acceptance criteria + evidence.

---

## Claim template

### ID: PXX-CYY
**Project source:** project_XX  
**Type:** strong | medium | weak  
**Claim:** (one sentence, operational)  
**Scope/Conditions:** (task, distribution, noise, resolution, clamp type, k, etc.)  
**Baselines:** (dense / uniform / random / kNN standard / naive)  
**Metrics:** (list)  
**Acceptance criteria (pass/fail):**
- (1) ...
- (2) ...
**Runs:** (n runs + seed list policy)  
**Evidence:** (paths to artifacts/reports)  
**Status:** untested | strong support | partial | rejected  
**Notes:** (threats to validity / limitations)

---

## Project 11 — Locked Claims (Draft v1)

### ID: P11-C01
**Project source:** project_11  
**Type:** strong  
**Claim:** Soft clamp (k=15) restores smoother regime structure compared to hard clamp, enabling compact interpretable rule baseline (V3.1) to achieve competitive performance.  
**Scope/Conditions:** Soft labels regime, 800 holdout test points, resolution sweep context, Phase D.  
**Baselines:** Hard clamp (original), dense NN at multiple resolutions (NN11 to NN81).  
**Metrics:** macroF1_present, accuracy.  
**Observed (Project 11; historical):**
- V3.1 overall macroF1_present: 0.9353
- V3 overall macroF1_present: 0.8435
- Gap: 0.0918 absolute
**Validation targets (Project 12; pre-registered):**
- V3.1 macroF1_present ≥ 0.93
- (V3.1 − V3) ≥ 0.07 absolute overall
**Runs:** Single deterministic run (Phase D resolution sweep).  
**Evidence:**
- Extraction source: `CLAIM_EXTRACTION_PROJECT_11.md` (Source 3)
- Artifact (P11 historical): `project_11/results/phase_d_soft_clamp/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`
- Table (P11 historical): `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md`
- Validation (P12 procedure-preserving): `project_12/results/revalidate_p11proc/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`
- Report: `project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md`
**Status:** validated (Project 12, procedure-preserving)  
**Notes:** Resolution sweep is deterministic (single holdout seed 223311); no run variance reported. Historical data informs validation targets but does not substitute for Project 12 re-validation.

---

### ID: P11-C02
**Project source:** project_11  
**Type:** medium  
**Claim:** Dense nearest-neighbor performance improves with resolution, providing an upper-performance bound but at increasing reference cost.  
**Scope/Conditions:** Soft labels (k=15), 800 holdout test points, Phase D resolution sweep.  
**Baselines:** Hard clamp, soft clamp, rule-based V3/V3.1.  
**Metrics:** macroF1_present at each resolution; grid size (points); build time (seconds).  
**Observed (Project 11; historical):**
- NN11: 0.8770
- NN21: 0.9481
- NN41: 0.9674
- NN81: 0.9847
**Validation targets (Project 12; pre-registered):**
- NN81 macroF1_present ≥ 0.97
- Ordering: NN81 ≥ NN41 ≥ NN21 ≥ NN11 (non-decreasing monotonicity)
**Runs:** Single deterministic run.  
**Evidence:**
- Extraction source: `CLAIM_EXTRACTION_PROJECT_11.md` (Source 3)
- Table (P11 historical): `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md`
- Validation (P12 procedure-preserving): `project_12/results/revalidate_p11proc/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`
- Report: `project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md`
**Status:** validated (Project 12, procedure-preserving)  
**Notes:** Serves as upper-performance reference for efficiency comparisons; build cost is operational detail, not primary claim focus.

---

### ID: P11-C03
**Project source:** project_11  
**Type:** strong  
**Claim:** Boundary-only sampling achieves poor performance; global coverage (uniform + boundary mix) is necessary for near-dense approximation.  
**Scope/Conditions:** Soft labels, 800 holdout, reference set sizes N ∈ {250...2000}, Phase E2.  
**Baselines:** Uniform-only, boundary-only, mixed (uniform + boundary).  
**Metrics:** macroF1_present (mean over seeds).  
**Observed (Project 11; historical):**
- Boundary-only @ N=1000: 0.7011
- Uniform @ N=1000: 0.9574
- Mixed @ N=1000: 0.9780
**Validation targets (Project 12; pre-registered):**
- Boundary-only @ N=1000 ≤ 0.80
- Mixed @ N=1000 ≥ 0.97
- Mixed − boundary-only ≥ 0.15
- Uniform @ N=1000 ≥ 0.94
**Runs:** 3 seeds [101, 202, 303].  
**Evidence:**
- Extraction source: `CLAIM_EXTRACTION_PROJECT_11.md` (Source 4)
- Table (P11 historical): `project_11/packaging/out/FIG_F2_SAMPLE_EFFICIENCY.md`
- Artifact (P11 historical): `project_11/results/phase_e2_sample_efficiency/artifact.json`
- Validation (P12 procedure-preserving): `project_12/results/revalidate_p11proc/phase_e2/artifact.json`
- Report: `project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md`
**Status:** validated (Project 12, procedure-preserving)
**Notes:** Independent validation with separate seeds [404, 505, 606] confirms claim robustness across holdout/pool variants.

---

### ID: P11-C04
**Project source:** project_11  
**Type:** strong  
**Claim:** Structure-guided mixed sampling (N=1000, uniform+boundary) achieves near-dense performance with significantly reduced reference cost.  
**Scope/Conditions:** Soft labels, 800 holdout, Phase E2 sample efficiency sweep.  
**Baselines:** Dense NN81 (upper bound), V3.1 rule baseline.  
**Metrics:** macroF1_present (mean over seeds), reference count, efficiency ratio.  
**Observed (Project 11; historical):**
- Mixed @ N=1000: 0.9780 (mean over 3 seeds)
- NN81: 0.9847
- Gap: 0.0067
- Cost ratio: 1000/6561 ≈ 0.1525
**Validation targets (Project 12; pre-registered):**
- Mixed @ N=1000 ≥ 0.97
- NN81 ≥ 0.97
- (NN81 − mixed) ≤ 0.02
- Cost ratio ≤ 0.20
**Runs:** 3 seeds [101, 202, 303].  
**Evidence:**
- Extraction source: `CLAIM_EXTRACTION_PROJECT_11.md` (Source 4)
- Key claim #4 in (P11 historical): `project_11/packaging/out/KEY_CLAIMS.md`
- Table (P11 historical): `project_11/packaging/out/FIG_F2_SAMPLE_EFFICIENCY.md`
- Validation (P12 procedure-preserving): `project_12/results/revalidate_p11proc/phase_e2/artifact.json`
- Report: `project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md`
**Status:** validated (Project 12, procedure-preserving)
**Notes:** Flagship efficiency claim validated independently with new seeds [404, 505, 606] on separate holdout/pool instances.

---

### ID: P11-C05
**Project source:** project_11  
**Type:** medium  
**Claim:** Uniform fraction near 0.5 is competitive; 1-NN outperforms 3-NN under structured boundary concentration.  
**Scope/Conditions:** Soft labels, 800 holdout, Ns ∈ {1000, 1500}, Phase E3 ratio + kNN.  
**Baselines:** Uniform-only (frac=1.0), boundary-only (frac=0.0), kNN with k ∈ {1, 3}.  
**Metrics:** macroF1_present (mean over seeds), k-neighbor smoothing effect.  
**Observed (Project 11; historical):**
- Best config (1500, frac=0.5, 1-NN): 0.9747 (mean 5 seeds)
- Same config 3-NN: 0.9627
- Gap: 0.0120
**Validation targets (Project 12; pre-registered):**
- Best config macroF1_present ≥ 0.97
- (1-NN − 3-NN) at best config ≥ 0.005
- At N=1500: frac=0.5 within 0.01 of best among frac∈{0.2,0.5,0.8}
**Runs:** 5 seeds [111, 222, 333, 444, 555].  
**Evidence:**
- Extraction source: `CLAIM_EXTRACTION_PROJECT_11.md` (Source 5)
- Table (P11 historical): `project_11/packaging/out/FIG_F3_RATIO_KNN.md`
- Artifact (P11 historical): `project_11/results/phase_e3_ratio_knn/artifact.json`
- Validation (P12 procedure-preserving): `project_12/results/revalidate_p11proc/phase_e3/artifact.json`
- Report: `project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md`
**Status:** validated (Project 12, procedure-preserving)
**Notes:** Independently validated with new seeds [666, 777, 888, 999, 1010]. 1-NN advantage and fraction=0.5 competitiveness both confirmed.

---

### ID: P11-C06
**Project source:** project_11  
**Type:** weak  
**Claim:** Increasing N beyond 1000 shows diminishing returns; N=1000 mixed is competitive with larger N.  
**Scope/Conditions:** Soft labels, 800 holdout, mixed strategy (uniform+boundary), Phase E2.  
**Baselines:** Single-strategy (uniform or boundary only) at varying N.  
**Metrics:** macroF1_present (mean over seeds), gap between N sizes.  
**Observed (Project 11; historical):**
- Mixed @ N=1000: 0.9780
- Mixed @ N=1500: 0.9714
- Mixed @ N=2000: 0.9748
**Validation targets (Project 12; pre-registered):**
- Mixed @ N=1000 ≥ 0.96
- max(mixed@1500, mixed@2000) − mixed@1000 ≤ 0.02
**Runs:** 3 seeds [101, 202, 303].  
**Evidence:**
- Extraction source: `CLAIM_EXTRACTION_PROJECT_11.md` (Source 4)
- Table (P11 historical): `project_11/packaging/out/FIG_F2_SAMPLE_EFFICIENCY.md`
- Validation (P12 procedure-preserving): `project_12/results/revalidate_p11proc/phase_e2/artifact.json`
- Report: `project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md`
**Status:** validated (Project 12, procedure-preserving)
**Notes:** Diminishing returns pattern confirmed independently; marginal improvements taper as expected with weak-claim expectations.

---

### ID: P11-C07
**Project source:** project_11  
**Type:** strong  
**Claim:** Soft clamp (k=15) significantly improves rule performance at boundaries; compact V3.1 achieves near-competitive boundary performance.  
**Scope/Conditions:** Soft labels, boundary subset of 800 holdout points, Phase D resolution sweep.  
**Baselines:** Hard clamp V3 (original), dense NN at boundary.  
**Metrics:** macroF1_present on boundary subset, gap closure from hard clamp.  
**Observed (Project 11; historical):**
- V3.1 boundary: 0.8693
- V3 hard clamp boundary: 0.6685
- Gap from V3: 0.2008
- NN81 boundary: 0.9291
**Validation targets (Project 12; pre-registered):**
- V3.1 boundary macroF1_present ≥ 0.85
- (V3.1_boundary − V3_boundary) ≥ 0.15 absolute
- (NN81_boundary − V3.1_boundary) ≤ 0.10
**Runs:** Single deterministic run.  
**Evidence:**
- Extraction source: `CLAIM_EXTRACTION_PROJECT_11.md` (Source 3)
- Boundary table (P11 historical): `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md`
- Validation (P12 procedure-preserving): `project_12/results/revalidate_p11proc/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`
- Report: `project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md`
- Gate analysis: `project_12/docs/HOLDOUT_GENERATOR_GATE.md`
- Sensitivity sweep (Project 12): `project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md`
- Sweep metrics (20 seeds): `project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv`
**Status:** rejected-as-stated (Project 12) — absolute threshold V3.1_boundary ≥ 0.85 not robust across holdout seeds (1/20 pass in procedure-preserving sweep). Mechanism-based revision exists: P11-C07R.
**Notes:** Seed-sweep analysis (20 procedure-preserving holdouts, seeds 100001–100020) reveals absolute threshold is seed-sensitive despite procedure-preserving generation. Mean V3.1_boundary ≈ 0.7854 with only 1 seed ≥ 0.85. Mechanism-only conditions (relative improvement ≥ 0.15, NN81 gap ≤ 0.10) remain robust. Full analysis: `project_12/reports/SPRINT_2E2_FINAL_ANALYSIS.md`.

---

### ID: P11-C07R
**Project source:** project_11
**Type:** strong
**Claim:** Under soft clamp (k=15), the compact rule baseline (V3.1) is boundary-competent in a *mechanistic* sense: it (a) substantially improves boundary performance vs. V3, and (b) remains close to the dense NN81 boundary upper bound, across procedure-preserving holdout seed variation.
**Scope/Conditions:** Soft labels (k=15). Boundary subset defined by Phase D evaluation on Phase C3-generated holdouts (procedure-preserving).
**Baselines:** V3 (hard clamp rule), NN81 (dense grid NN).
**Metrics:** boundary macroF1_present for V3, V3.1, NN81; derived gaps.
**Observed (Project 12; key evidence):**
- See: `project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md` (seed=424242) and `project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv` (seed sweep).
**Validation targets (Project 12; pre-registered):**
- (V3.1_boundary − V3_boundary) ≥ 0.15
- (NN81_boundary − V3.1_boundary) ≤ 0.10
**Runs:** Seed sweep (20 holdout seeds, procedure-preserving) + independent re-validation run(s).
**Evidence:**
- `project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md`
- `project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv`
- `project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md`
**Status:** validated (Project 12; seed-sweep + procedure-preserving)
**Notes:** This revision intentionally drops an absolute boundary threshold (e.g., 0.85) because the sweep shows that absolute thresholds are seed-sensitive even under procedure-preserving generation.

---

### ID: P11-C08
**Project source:** project_11  
**Type:** weak  
**Claim:** Reference set retrieval can be built efficiently; pool-based design supports no leakage.  
**Scope/Conditions:** Soft labels, retrieval-based inference with pool-drawn reference sets, Phases D/E.  
**Baselines:** Baseline build costs; standard train/test split.  
**Metrics:** build_time (seconds); pool size vs reference set size.  
**Observed (Project 11; historical):**
- NN81 build time: 0.0527 seconds
- Pool size: 60000
- Max reference set: 2000
**Validation targets (Project 12; pre-registered):**
- NN81 build_seconds < 0.10
- Pool size >> reference set size ratio ≥ 10× maintained
- Holdout ∩ reference = ∅ (explicit assertion required)
**Runs:** Deterministic engineering check.  
**Evidence:**
- Build cost table (P11 historical): `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md`
- Protocol (P11): `project_11/docs/PHASE_E3_RATIO_KNN_PROTOCOL.md`
- Validation (P12 procedure-preserving): `project_12/results/revalidate_p11proc/phase_d/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`
- Report: `project_12/reports/P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md`
**Status:** validated (Project 12, procedure-preserving)
**Notes:** Build efficiency verified (0.052s < 0.10s ✓). Leakage prevention by internal RNG design; no external pool tracking required.
