# CLAIM_EXTRACTION_PROJECT_4 — Source Analysis

**Extraction Date:** April 11, 2026  
**Project:** 4  
**Purpose:** Systematic claim extraction from Project 4 legacy documents (read-only)

---

## Sources Analyzed

### Source 1: PROJECT_4_EXECUTIVE_SUMMARY.md
- **Path:** `project_4/results/PROJECT_4_EXECUTIVE_SUMMARY.md`
- **Key Content:** MVP objective achieved; diagnostic framework for distinguishing robustness types

**Observation:**
> "Project 4 successfully demonstrated that strong-looking intervention gains can remain narrow and non-general, which is exactly the kind of distinction the framework was designed to detect."

**Extracted Signal:**
- Framework distinguishes distribution-bound fit from algorithm-like behavior
- Intervention gains can be narrow vs. generalizable
- This distinction is the core methodological contribution

---

### Source 2: PROJECT_4_RESULTS_SUMMARY.md
- **Path:** `project_4/results/PROJECT_4_RESULTS_SUMMARY.md`
- **Key Tables & Observations:**

#### 2A. Stable Baseline Matrix
| Dimension | MLP | LSTM | Transformer |
|----------|-----|------|-------------|
| In-distribution exact-match | low | low | low |
| Alternating carry | collapse | collapse | collapse |
| Full propagation chain | collapse | collapse | collapse |
| Block-boundary stress | **success** | **collapse** | **success** |

**Key Observation (Quoted):**
> "the strongest current architecture-dependent split appears on: `block_boundary_stress` — MLP succeeds, Transformer succeeds, LSTM fails. This is the clearest stable cross-model diagnostic difference currently available."

**Extracted Metrics:**
- All three architectures weak in exact-match (low values)
- All three fail on alternating carry and full propagation
- **Architecture-dependent difference:** MLP & Transformer succeed on block-boundary stress; LSTM fails
- Mean adversarial accuracy: MLP=0.67, LSTM=0.00, Transformer=0.33

#### 2B. First MVP Intervention (Adversarial Training)
**Quoted Result:**
> "strong gain on a **seen adversarial family**, no meaningful gain on another difficult family, failure on a **held-out adversarial family**"

**Interpretation provided in source:**
> "adversarial training can improve performance on specifically seen structured families, but this does not automatically translate into broad structural robustness."

This supports: **narrow transfer** over general robustness

#### 2C. Blockwise Decomposition
**Status:** NOT ACCEPTED as scientific core
- Reason: methodologically unresolved during debugging
- Classification: INCOMPLETE / METHODOLOGICALLY UNRESOLVED
- Future: marked as open extension, not current result

**Extracted:** This is out-of-scope for locked claims (unresolved)

---

### Source 3: PROJECT_4_FINAL_JUDGMENT.md
- **Path:** `project_4/results/PROJECT_4_FINAL_JUDGMENT.md`

**Verdict (Quoted):**
> "Project 4 is judged a **successful MVP-level research contribution**. Its main achievement is not the discovery of a model that cleanly reaches stronger algorithm-like behavior, but the construction of a diagnostic framework capable of separating narrow gains from broader structural robustness."

**Core Scientific Result (Quoted):**
> "The accepted scientific core of Project 4 therefore consists of the framework itself, the stable baseline matrix, and the stable adversarial-training signal."

**Extracted Scope:**
1. Framework ✅
2. Baseline matrix ✅
3. Adversarial training signal ✅
4. Blockwise decomposition ❌ (unresolved, excluded)

---

### Source 4: PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md
- **Path:** `project_4/baselines/PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md`

**Baseline Validation Status (Quoted):**
> "The following baseline families have now passed repeated-run stability validation under the current bounded Project 4 path: MLP → STABLE, LSTM → STABLE, Transformer → STABLE"

#### Stable Baseline Matrix (Numerical)
| Dimension | MLP | LSTM | Transformer |
|-----------|-----|------|-------------|
| In-dist exact-match (mean) | **0.0859** | **0.0469** | **0.0339** |
| Alternating carry | 0.0000 | 0.0000 | 0.0000 |
| Full propagation chain | 0.0000 | 0.0000 | 0.0000 |
| Block-boundary stress | **1.0000** | **0.0000** | **1.0000** |
| Mean adversarial accuracy | **0.67** | **0.00** | **0.33** |

**Extracted metrics:** All above (precise numerical values for verification)

**Key qualifications (Quoted):**
> "All three baselines remain in a **non-Regime-3 zone**. More specifically: none of the three currently provides evidence of strong algorithm-like generalization; all three show major structured weaknesses."

**Extracted conclusion:** Baselines are weak; framework is diagnostic (not success story)

---

### Source 5: PROJECT_4_CLOSURE_SUMMARY.md
- **Path:** `project_4/results/PROJECT_4_CLOSURE_SUMMARY.md`

**Framework Components Built (Quoted):**
> "PROJECT_4_DIAGNOSTIC_FRAMEWORK.md, FRAMEWORK_CHANGELOG.md, RESULT_VALIDATION_PROTOCOL.md, diagnostic_scorecard.py, benchmark_adversarial_patterns.py, regime_classification.py, validate_run_stability.py"

**Main Baseline Finding (Quoted):**
> "MLP → success on block_boundary_stress, Transformer → success on block_boundary_stress, LSTM → failure on block_boundary_stress"

**Intervention Finding (Quoted):**
> "adversarial training can improve performance on specific seen adversarial structures without automatically producing broad structural robustness transfer."

**Final Position (Quoted):**
> "Project 4 succeeded in its MVP objective. It built a real diagnostic framework, produced a stable baseline matrix, and generated a stable first intervention result."

---

## Extracted Claims (Preliminary)

### Claim Group A: Diagnostic Framework
**Observation:**
Project 4 built a framework distinguishing:
- Distribution-bound fit
- Bounded compositional competence
- Algorithm-like behavior

**Framework components:** 7 documented tools/specs (scorecard, protocol, etc.)

### Claim Group B: Stable Baseline Matrix
**Observations:**
1. Three architectures (MLP, LSTM, Transformer) evaluated under unified diagnostic framework—all show repeated-run stability
2. In-distribution exact-match universally weak (MLP=0.0859, LSTM=0.0469, Transformer=0.0339)
3. All fail on alternating-carry and full-propagation adversarial families
4. **Architecture-dependent split on block-boundary stress:**
   - MLP: 1.0 (success)
   - LSTM: 0.0 (failure)
   - Transformer: 1.0 (success)
5. Mean adversarial accuracy: MLP=0.67, LSTM=0.00, Transformer=0.33

### Claim Group C: Adversarial Training Intervention
**Observations:**
1. First tested intervention: adversarial training on a seen adversarial family
2. Result: strong gain on seen family; NO gain on held-out adversarial family
3. Interpretation: narrow transfer, not broad robustness
4. This result is stable (repeated-run validated)

### Claim Group D: Blockwise Decomposition
**Status:** EXCLUDED from scientific core
- Unresolved, methodologically drifted
- Not a claim; marked as future extension

---

## Summary for FORMAL_CLAIMS Integration

**Ready to lock:**
- Framework existence + components ✅
- Baseline matrix (MLP, LSTM, Transformer) ✅
- Architecture-dependent block-boundary split ✅
- Adversarial training narrow transfer ✅
- Validation: repeated-run stability ✅

**Out of scope (do not claim):**
- Blockwise decomposition (unresolved)
- Any model reaching Regime 3
- General robust arithmetic reasoning from adversarial training

---
