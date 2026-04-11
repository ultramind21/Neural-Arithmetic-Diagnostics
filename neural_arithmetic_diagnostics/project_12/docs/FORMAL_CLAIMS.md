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

---

## Project 4 — Locked Claims (Draft v1)

### ID: P4-C01
**Project source:** project_4
**Type:** weak (infrastructure/methodology)
**Claim:** The Project 4 diagnostic framework can execute end-to-end and produce per-family performance scorecards for multiple architectures and adversarial pattern families.
**Scope/Conditions:** Framework implementation (scorecard, protocol, validation rules); arithmetic reasoning task context.
**Baselines:** Framework specification vs. actual execution; internal consistency.
**Metrics:** framework component availability; successful end-to-end runs; scorecard output structure.
**Observed (Project 4):**
- 7 executable components documented (scorecard.py, protocol.md, etc.)
- Three baseline models (MLP, LSTM, Transformer) evaluated; repeated-run stability confirmed
- Framework produced per-family accuracy breakdown
**Validation targets (Project 12; pre-registered):**
- All 7 framework components executable without modification
- Framework produces scorecard output for ≥3 architectures
- Framework produces per-family accuracy for ≥3 adversarial families
- Individual runs reproducible (same architecture/family → same seed)
**Runs:** Single deterministic framework execution run.
**Evidence:**
- Framework specification: `project_4/framework/PROJECT_4_DIAGNOSTIC_FRAMEWORK.md`
- Framework components: `project_4/results/PROJECT_4_CLOSURE_SUMMARY.md` (section 2)
- Extraction source: `project_12/docs/CLAIM_EXTRACTION_PROJECT_4.md`
**Status:** validated (Project 12; artifact-based infra check)
**Evidence Pointers:**
- P12 infra validation report: `project_12/reports/P4_INFRA_VALIDATION_REPORT.md` (P4-C01 section)
- Baseline artifacts: `project_12/results/repro_p4/baselines/{mlp,lstm,transformer}/artifact.json`
- Baseline entrypoints: `project_12/scripts/p4/run_p4_*_baseline_repro.py`
**Notes:** Framework produces required scorecard structure and per-family metrics for 3 architectures. Validated from artifacts without re-execution.

---

### ID: P4-C02
**Project source:** project_4
**Type:** strong
**Claim:** A meaningful architecture-dependent difference exists on block-boundary-stress: MLP and Transformer show substantially higher robustness than LSTM on this adversarial family.
**Scope/Conditions:** Diagnostic evaluation of three baseline models (MLP, LSTM, Transformer) on block-boundary-stress adversarial family; repeated-stability protocol.
**Baselines:** All three architectures evaluated on same adversarial pattern.
**Metrics:** block-boundary-stress accuracy per architecture; cross-architecture difference.
**Observed (Project 4):**
- MLP: 1.0 (success)
- LSTM: 0.0 (failure)
- Transformer: 1.0 (success)
- Status: STABLE under repeated runs
**Validation targets (Project 12; pre-registered):**
- MLP block-boundary accuracy ≥ 0.80
- Transformer block-boundary accuracy ≥ 0.80
- LSTM block-boundary accuracy ≤ 0.20
- Gap threshold: min(MLP, Transformer) − LSTM ≥ 0.50
**Runs:** Repeated-stability runs (count and seeds TBD).
**Evidence:**
- Baseline classification summary: `project_4/baselines/PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md` (stable baseline matrix)
- Baseline artifacts: `project_4/results/baseline_runs/phase30_*_baseline_artifact.json`
- Extraction: `project_12/docs/CLAIM_EXTRACTION_PROJECT_4.md`
**Status:** validated (Project 12; baseline repro)
**Evidence Pointers:**
- P12 validation report: `project_12/reports/P4_VALIDATION_REPORT_BASELINES.md` (P4-C02 section)
- Baseline artifacts: `project_12/results/repro_p4/baselines/{mlp,lstm,transformer}/artifact.json`
- Repro check: `project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md`
**Notes:** All targets met in Project 12 baseline repro. MLP/Transformer block-boundary=1.0, LSTM=0.0, gap=1.0 (exceeds threshold of 0.50).

---

### ID: P4-C03
**Project source:** project_4
**Type:** strong
**Claim:** In-distribution exact-match accuracy is universally weak across MLP, LSTM, and Transformer under the Project 4 bounded arithmetic task, with no architecture achieving strong performance.
**Scope/Conditions:** In-distribution evaluation of three baseline models; bounded Project 4 arithmetic task (addition/subtraction in bounded ranges).
**Baselines:** Common arithmetic reasoning task; no external reference.
**Metrics:** in-distribution exact-match accuracy (mean across runs).
**Observed (Project 4):**
- MLP: 0.0859 (STABLE)
- LSTM: 0.0469 (STABLE)
- Transformer: 0.0339 (STABLE)
- All three described as "universally weak"
**Validation targets (Project 12; pre-registered):**
- All three architectures: in-distribution accuracy ≤ 0.20
- No architecture exceeds 0.20 exact-match threshold
**Runs:** Repeated-stability runs (count and seeds TBD).
**Evidence:**
- Baseline classification: `project_4/baselines/PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md` (in-distribution exact-match row)
- Baseline artifacts: `project_4/results/baseline_runs/phase30_*_baseline_artifact.json`
- Results summary: `project_4/results/PROJECT_4_RESULTS_SUMMARY.md`
- Extraction: `project_12/docs/CLAIM_EXTRACTION_PROJECT_4.md`
**Status:** validated (Project 12; baseline repro)
**Evidence Pointers:**
- P12 validation report: `project_12/reports/P4_VALIDATION_REPORT_BASELINES.md` (P4-C03 section)
- Baseline artifacts: `project_12/results/repro_p4/baselines/{mlp,lstm,transformer}/artifact.json`
- Repro check: `project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md`
**Notes:** All three architectures confirmed weak: MLP=0.0625, LSTM=0.0391, Transformer=0.0391 (all ≤ 0.20 threshold).

---

### ID: P4-C04
**Project source:** project_4
**Type:** strong
**Claim:** Adversarial training can produce narrow transfer: improving performance on a specifically targeted adversarial family while failing to improve performance on held-out adversarial families.
**Scope/Conditions:** First MVP intervention test; adversarial training applied to one specific adversarial family (seen); evaluation includes both seen family (training target) and held-out adversarial families (generalization test).
**Baselines:** Baseline model (pre-intervention); untrained models for transfer reference.
**Metrics:** accuracy gain on seen family (absolute); accuracy change on held-out family (absolute); transfer ratio.
**Observed (Project 4):**
- Strong gain on seen adversarial family: (exact magnitude—to be extracted from intervention artifacts)
- Failure/no meaningful gain on held-out adversarial family: (exact value—to be extracted)
- Pattern: seen gain >> held-out gain
- Status: STABLE signal
**Validation targets (Project 12; pre-registered):**
- Ordering target (independent): (seen_gain − held_out_gain) ≥ 0.10
- Qualitative criterion: seen_gain > held_out_gain (narrow transfer confirmed)
- Numeric precision targets: TBD after Sprint 4 artifact extraction
**Runs:** Repeated-stability runs; intervention artifact paths TBD.
**Evidence:**
- Intervention artifact: `project_4/interventions/adversarial_training/results/project_4_adversarial_training_artifact.json`
- Intervention validation: `project_4/interventions/adversarial_training/results/project_4_adversarial_training_validation_runs.json`
- Results summary (intervention): `project_4/results/PROJECT_4_RESULTS_SUMMARY.md` (section 4)
- Closure (intervention): `project_4/results/PROJECT_4_CLOSURE_SUMMARY.md` (section 4)
- Extraction: `project_12/docs/CLAIM_EXTRACTION_PROJECT_4.md`
**Status:** untested (Project 12) — observed and validated in Project 4; requires Project 12 re-validation and exact magnitude extraction.
**Notes:** Core framework contribution: distinguishes narrow gains from broad robustness. Ordering threshold (≥0.10 gap) is independent pre-registered target. Numeric bounds (e.g., seen>0.20, held-out<0.05) to be calibrated in Sprint 4 when actual artifact values extracted. Blockwise decomposition excluded (unresolved).

---

### ID: P4-C05
**Project source:** project_4
**Type:** medium
**Claim:** Alternating-carry and full-propagation-chain adversarial families are equally hard across all three baseline architectures: all show universal collapse with no architecture-dependent differentiation.
**Scope/Conditions:** Adversarial robustness evaluation; two specific structured adversarial families (alternating-carry, full-propagation-chain).
**Baselines:** All three models (MLP, LSTM, Transformer) evaluated on same families.
**Metrics:** accuracy on each adversarial family per architecture.
**Observed (Project 4):**
- Alternating carry: 0.0 for MLP, LSTM, Transformer (universal collapse)
- Full propagation chain: 0.0 for MLP, LSTM, Transformer (universal collapse)
- Status: STABLE across runs
**Validation targets (Project 12; pre-registered):**
- For each family: max(model accuracy across all three) ≤ 0.10 (universal weakness)
- No architecture-specific split: max_accuracy − min_accuracy ≤ 0.10 (no differentiation)
**Runs:** Repeated-stability runs (count and seeds TBD).
**Evidence:**
- Baseline classification: `project_4/baselines/PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md` (alternating carry & full propagation chain rows)
- Baseline artifacts: `project_4/results/baseline_runs/phase30_*_baseline_artifact.json`
- Extraction: `project_12/docs/CLAIM_EXTRACTION_PROJECT_4.md`
**Status:** validated (Project 12; baseline repro)
**Evidence Pointers:**
- P12 validation report: `project_12/reports/P4_VALIDATION_REPORT_BASELINES.md` (P4-C05 section)
- Baseline artifacts: `project_12/results/repro_p4/baselines/{mlp,lstm,transformer}/artifact.json`
- Repro check: `project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md`
**Notes:** Both families universally collapsed: alternating-carry max=0.0, full-propagation-chain max=0.0 (both ≤ 0.10 threshold), no architecture split (gap=0 for both).

---

### ID: P4-C06
**Project source:** project_4
**Type:** weak (infrastructure/reproducibility)
**Claim:** Project 4 baseline repeated-run classifications (stability status) can be reproduced from artifacts or by re-running baseline scripts when framework is applied to the same models and adversarial families.
**Scope/Conditions:** Framework reproducibility (scorecard, protocol, validation rules); three baseline architectures (MLP, LSTM, Transformer) re-evaluated.
**Baselines:** Baseline framework itself (no external reference); internal consistency check.
**Metrics:** match between Project 4 reported stability classification and Project 12 re-run classification; execution success rate.
**Observed (Project 4):**
- 7 framework components documented and implemented
- Three baselines classified as STABLE (repeated-run consistency confirmed in Project 4)
**Validation targets (Project 12; pre-registered):**
- All 7 framework components execute without modification in Project 12 environment
- Baseline re-runs produce same architecture-level classification (stable/unstable) as Project 4
- Per-family results reproducible ±measurement tolerance
**Runs:** Framework implementation run; deterministic.
**Evidence:**
- Framework specification: `project_4/framework/PROJECT_4_DIAGNOSTIC_FRAMEWORK.md`
- Framework components: `project_4/results/PROJECT_4_CLOSURE_SUMMARY.md` (section 2: what was built)
- Baseline artifacts (Project 4): `project_4/results/baseline_runs/phase30_*_baseline_artifact.json`
- Extraction: `project_12/docs/CLAIM_EXTRACTION_PROJECT_4.md`
**Status:** validated (Project 12; artifact-based infra check)
**Evidence Pointers:**
- P12 infra validation report: `project_12/reports/P4_INFRA_VALIDATION_REPORT.md` (P4-C06 section)
- Baseline artifacts: `project_12/results/repro_p4/baselines/{mlp,lstm,transformer}/artifact.json`
- Repro check: `project_12/reports/REPRO_CHECK_PROJECT4_BASELINES.md`
**Notes:** Metadata structure (p12_metadata, env fields) present and consistent across all 3 architectures. Git hash same (eaca658...), entrypoints differentiated. Validated from artifacts without re-execution.

---
