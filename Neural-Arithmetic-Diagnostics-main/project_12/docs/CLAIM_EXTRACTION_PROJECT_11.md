# CLAIM_EXTRACTION_PROJECT_11 — Read-Only Extraction

**Purpose:** Extract claims, numbers, and baselines directly from Project 11 artifacts. No interpretation, no invention.

---

## Source 1: project_11/packaging/out/KEY_CLAIMS.md

**Path:** `project_11/packaging/out/KEY_CLAIMS.md`

**Extracted claims (verbatim):**
1. Hard clamp creates discontinuity artifacts that concentrate errors near boundaries; soft clamp restores smoother regime structure.
2. Under soft labels (k=15), an interpretable rule baseline (V3.1) becomes competitive (macroF1_present=0.9353).
3. Dense local interpolation (NN) improves with resolution and remains the top performer at high resolution (NN81=0.9847), but at increased reference cost.
4. Structure-guided sampling (uniform+boundary) yields strong sample efficiency: N=1000 mixed reaches macroF1_present≈0.9780 (mean over seeds), close to NN81 with far fewer reference points.
5. Boundary-only sampling fails; global coverage is necessary.

**Numbers/thresholds mentioned:**
- soft clamp k = 15
- V3.1 macroF1_present = 0.9353
- NN81 macroF1_present = 0.9847
- N=1000 mixed macroF1_present ≈ 0.9780 (mean over seeds)

**Baselines mentioned:**
- Hard clamp (baseline system)
- Soft clamp (mechanism variant)
- V3.1 (rule-based)
- Dense NN at various resolutions (NN81, NN41, etc.)
- Uniform sampling
- Boundary sampling
- Mixed sampling (uniform + boundary)

---

## Source 2: project_11/packaging/out/EVIDENCE_MATRIX.md

**Path:** `project_11/packaging/out/EVIDENCE_MATRIX.md`

**Table rows extracted (soft labels, k=15):**
| Item | Best setting | Metric | Value | Source |
|---|---|---:|---:|---|
| Rule baseline | V3.1 | macroF1_present | 0.9353 | Phase D resolution sweep |
| Dense NN | NN81 (6561 pts) | macroF1_present | 0.9847 | Phase D resolution sweep |
| Dense NN (mid) | NN41 (1681 pts) | macroF1_present | 0.9674 | Phase D resolution sweep |
| Adaptive NN | N=2000 (1000 uniform + 1000 boundary) | macroF1_present | 0.9752 | Phase E1 report |
| Sample-efficiency peak | N=1000 mixed | macroF1_present (mean over seeds) | 0.9780 | Phase E2 report/analysis |
| Ratio sweep best | N=1500, frac=0.5, 1-NN | macroF1_present (mean over seeds) | 0.9747 | Phase E3 report |

**Numbers/thresholds mentioned:**
- NN81: 6561 reference points
- NN41: 1681 reference points
- N=2000 mixed: 0.9752
- N=1000 mixed: 0.9780 (mean over seeds)
- N=1500 mixed (frac=0.5, 1-NN): 0.9747 (mean over seeds)

---

## Source 3: project_11/packaging/out/FIG_F1_NN_RESOLUTION.md

**Path:** `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md`

**Extracted data (Phase D — Resolution Sweep Extended, soft labels):**
- Test points: 800
- Soft clamp k: 15
- True label distribution: {'family-aware region': 127, 'transition region': 310, 'universal region': 363}

**Overall (macroF1_present):**
| model | macroF1_present |
|---|---:|
| V3 | 0.8435 |
| V3.1 | 0.9353 |
| NN11 | 0.8770 |
| NN21 | 0.9481 |
| NN41 | 0.9674 |
| NN81 | 0.9847 |

**Boundary subset (macroF1_present):**
| model | macroF1_present |
|---|---:|
| V3 (boundary) | 0.6685 |
| V3.1 (boundary) | 0.8693 |
| NN11 (boundary) | 0.5938 |
| NN21 (boundary) | 0.7672 |
| NN41 (boundary) | 0.8625 |
| NN81 (boundary) | 0.9291 |

**NN build cost:**
| grid | points | build_seconds |
|---:|---:|---:|
| 11x11 | 121 | 0.0012 |
| 21x21 | 441 | 0.0032 |
| 41x41 | 1681 | 0.0130 |
| 81x81 | 6561 | 0.0527 |

**Artifact:** `project_11/results/phase_d_soft_clamp/RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`

---

## Source 4: project_11/packaging/out/FIG_F2_SAMPLE_EFFICIENCY.md

**Path:** `project_11/packaging/out/FIG_F2_SAMPLE_EFFICIENCY.md`

**Extracted data (Phase E2 — Sample Efficiency Report, soft labels):**
- Test (holdout) points: 800
- True distribution: {'family-aware region': 127, 'transition region': 310, 'universal region': 363}
- Seeds: [101, 202, 303] (3 runs)
- Reference set sizes tested: [250, 500, 1000, 1500, 2000]
- Sampling strategies: ['uniform', 'boundary', 'mixed']
- Pool size: 60000
- Elapsed time: 19.75 seconds

**Phase E2 Baselines (context; computed once):**
- V3.1: acc=0.9300, macroF1=0.9353
- NN41: acc=0.9700, macroF1=0.9674
- NN81: acc=0.9862, macroF1=0.9847

**Key results (mean over 3 seeds):**
| N | strategy | macroF1_mean |
|---:|---|---:|
| 250 | mixed | 0.9252 |
| 500 | mixed | 0.9388 |
| **1000** | **mixed** | **0.9780** ← peak efficiency |
| 1500 | mixed | 0.9714 |
| 2000 | mixed | 0.9748 |

**Observation:** Boundary-only sampling consistently underperforms (e.g., N=1000 boundary: macroF1_mean=0.7011 vs. mixed=0.9780).

**Artifact:** `project_11/results/phase_e2_sample_efficiency/artifact.json`

---

## Source 5: project_11/packaging/out/FIG_F3_RATIO_KNN.md

**Path:** `project_11/packaging/out/FIG_F3_RATIO_KNN.md`

**Extracted data (Phase E3 — Ratio + kNN Sweep, soft labels):**
- Test (holdout) points: 800
- True distribution: {'family-aware region': 127, 'transition region': 310, 'universal region': 363}
- Seeds: [111, 222, 333, 444, 555] (5 runs)
- Reference set sizes: Ns ∈ {1000, 1500}
- Uniform fractions: uniform_frac ∈ {0.2, 0.5, 0.8}
- Pool size: 60000
- Elapsed time: 36.82 seconds

**Phase E3 Baselines (macroF1_present):**
- V3.1: 0.9353
- NN41: 0.9674
- NN81: 0.9847

**Results (mean over 5 seeds) — macroF1_present:**
| N | uniform_frac | 1-NN mean | 3-NN mean |
|---:|---:|---:|---:|
| 1000 | 0.2 | 0.9494 | 0.9273 |
| 1000 | 0.5 | 0.9682 | 0.9513 |
| 1000 | 0.8 | 0.9666 | 0.9628 |
| 1500 | 0.2 | 0.9663 | 0.9483 |
| **1500** | **0.5** | **0.9747** | **0.9627** ← best configuration |
| 1500 | 0.8 | 0.9722 | 0.9665 |

**Observation:** 1-NN performs better than 3-NN under structured sampling (suggests boundary concentration is interpretable, not noise).

**Artifact:** `project_11/results/phase_e3_ratio_knn/artifact.json`

---

## Source 6: project_11/packaging/EXECUTIVE_ABSTRACT.md

**Path:** `project_11/packaging/EXECUTIVE_ABSTRACT.md`

**Key statements extracted:**
- "Project 11 tests whether a regime-theory style predictor (compact, interpretable rules) can reliably classify outcomes in a structured synthetic rescue system."
- "A key discovery is that hard clamping induces boundary instability and concentrates rule errors; replacing hard clamp with soft saturation restores smoother structure where an interpretable rule baseline (V3.1) becomes competitive."
- "Under soft labels, dense nearest-neighbor improves with resolution (e.g., NN81 macroF1_present=0.9847) but at increased reference cost."
- "Crucially, Project 11 shows structure-guided sampling: combining uniform coverage with boundary-focused sampling achieves near-dense performance with far fewer points (e.g., N=1000 mixed reaches macroF1_present≈0.9780 mean over seeds)."
- "Boundary-only sampling fails, demonstrating that global coverage is necessary."

---

## Source 7: project_11 Protocols (seeds & run specifications)

**Path (examples):**
- `project_11/docs/PHASE_D_SOFT_CLAMP_PROTOCOL.md`
- `project_11/docs/PHASE_E2_SAMPLE_EFFICIENCY_PROTOCOL.md`
- `project_11/docs/PHASE_E3_RATIO_KNN_PROTOCOL.md`

**Extracted run specifications:**

### Phase D (Resolution Sweep):
- Test set (holdout): 800 points
- Locked seed for holdout: 223311
- Single run (deterministic comparison of V3 vs NN at different resolutions)
- Soft clamp parameter: k=15

### Phase E2 (Sample Efficiency):
- Test set (holdout): 800 points
- Seeds: [101, 202, 303] (3 runs)
- Reference pools: N ∈ {250, 500, 1000, 1500, 2000}
- Strategies: uniform, boundary, mixed
- Results reported: mean ± [implicit std or point estimates]

### Phase E3 (Ratio + kNN):
- Test set (holdout): 800 points
- Seeds: [111, 222, 333, 444, 555] (5 runs)
- Ns: {1000, 1500}
- uniform_frac: {0.2, 0.5, 0.8}
- 1-NN and 3-NN evaluated
- Results reported: mean over 5 seeds

---

## Summary of Numbers & Artifacts

**Top performance numbers (soft labels, k=15, 800 holdout points):**
- V3.1 rule baseline: 0.9353 macroF1_present
- NN81 (6561 pts): 0.9847 macroF1_present
- N=1000 mixed (mean 3 seeds): 0.9780 macroF1_present
- N=1500, frac=0.5, 1-NN (mean 5 seeds): 0.9747 macroF1_present

**Efficiency claim:** N=1000 mixed achieves 0.9780, very close to NN81's 0.9847, using ~15% of NN81's reference points (1000 vs 6561).

**Baselines & comparison points:**
- Hard clamp (original system)
- Soft clamp (k=15 variant)
- V3.1 (compact interpretable rule)
- NN at resolutions 11x11, 21x21, 41x41, 81x81
- Uniform sampling
- Boundary-only sampling
- Mixed (uniform + boundary) sampling
- Standard kNN (1-NN, 3-NN)

**Leakage notes:** Test set is locked and fixed across all runs. Sampling strategies draw from separate pool (pool_size=60000).
