# PROJECT 4 DIAGNOSTIC FRAMEWORK
## Diagnostic Arithmetic Reasoning After Audit Closure

**Date:** March 31, 2026  
**Status:** ACTIVE WORKING FRAMEWORK  
**Prerequisite:** Primary trust-recovery audit (Phases 1–6) completed

---

## 1. Background and Motivation

Projects 1–3, together with the trust-recovery audit sequence, established that high arithmetic accuracy in neural models does not by itself justify strong claims of robust algorithm-like reasoning.

The audited record showed that:
- strong in-distribution performance can coexist with important structured failures
- architectural and representational choices matter substantially
- structured adversarial testing can reveal limitations hidden by standard random benchmarks
- source/setup, semantics, and metric verification are necessary before broad interpretation

Project 4 therefore shifts the focus from:

> **"Can a model achieve high arithmetic accuracy?"**

to:

> **"How can we rigorously distinguish distribution-bound approximation, bounded compositional competence, and stronger algorithm-like behavior?"**

---

## 2. Core Objective

The central goal of Project 4 is to build a **diagnostic framework** for arithmetic reasoning that classifies models into three working regimes:

1. **Distribution-bound fit**
2. **Bounded compositional competence**
3. **Stronger algorithm-like generalization**

Project 4 is therefore primarily a **diagnostic framework project**, not merely a model-improvement project.

### Important Success Criterion
Project 4 does **not** require discovering a Regime 3 model.

A fully valid and publishable outcome is:

- the framework is built,
- tested models are classified rigorously,
- and all tested models remain in Regime 1 or 2.

That would still be a strong scientific result.

---

## 3. Working Regime Definitions

These regimes are working diagnostic categories, not metaphysical labels.

### Regime 1 — Distribution-Bound Fit
A model performs well on in-distribution data but degrades sharply under structured or mechanism-relevant shifts.

Typical signature:
- high random-test accuracy
- weak adversarial robustness
- high post-processing dependence
- brittle behavior under mechanism-sensitive perturbations

---

### Regime 2 — Bounded Compositional Competence
A model exhibits meaningful compositional structure within a bounded range, but does not remain robust under stronger extrapolation or combinatorially novel structure.

Typical signature:
- good held-out and moderate OOD performance
- partial structural robustness
- failure on harder adversarial families
- no evidence of open-ended robustness

---

### Regime 3 — Stronger Algorithm-Like Generalization
A model remains stable across longer lengths, structured adversarial families, and equivalent formulations of the same rule.

Typical signature:
- strong length robustness
- strong structured-adversarial robustness
- low dependence on accidental discretization
- stability across mechanism-preserving transformations

---

## 4. Core Hypotheses

### H1
High in-distribution accuracy can hide non-robust or non-general behavior.

### H2
Structured adversarial patterns are more diagnostic than length-based testing alone.

### H3
Rounding, discretization, and post-processing can create an illusion of reasoning.

### H4
Robust compositional behavior must survive structure-relevant perturbations, not just mild OOD variation.

### H5
Blockwise decomposition may reduce some forms of error accumulation, but may also merely enlarge the approximation bubble unless carry interfaces are handled explicitly.

---

## 5. Scope: MVP vs Extended

### 5.1 MVP Scope
The minimum viable and publishable scope of Project 4 consists of:

1. **Diagnostic framework v1.0**
2. **Core scorecard with operational definitions**
3. **Baseline re-evaluation under the framework**
4. **One intervention tested properly**

Recommended MVP intervention:
- **adversarial training**

---

### 5.2 Extended Scope
If MVP is successful and stable, Project 4 may expand to include:

- blockwise decomposition experiments
- explicit carry-interface interventions
- additional adversarial families
- extended scorecard dimensions
- larger benchmark families

---

## 6. Diagnostic Test Families

### Family A — In-Distribution Random
Purpose:
- baseline sanity and fit measurement

---

### Family B — Structured Adversarial
Purpose:
- structural robustness testing

The minimum adversarial core for framework v1.0 will contain at least:

#### Pattern B1 — Alternating Carry
A periodic carry configuration requiring regular alternation across positions.

#### Pattern B2 — Full Propagation Chain
A pattern forcing carry propagation across a long contiguous region.

#### Pattern B3 — Block-Boundary Stress
A pattern designed so that carry repeatedly crosses local block boundaries.

These three patterns form the minimum structured-adversarial core for v1.0.

### Required Reporting Rule
For every adversarial evaluation, the following must always be reported:

1. **pattern-wise breakdown**
2. **mean adversarial accuracy**
3. **worst-case pattern accuracy**

This is mandatory because averages alone can hide catastrophic failure on individual patterns.

---

### Family C — Length Extrapolation
Purpose:
- distinguish bounded competence from stronger length robustness

Length extrapolation must be reported not only descriptively, but also through a
computable robustness view.

### Required Reporting Rule
At minimum, report:
1. accuracy by tested length
2. relative drop beyond the training range
3. a simple trend summary (stable / gradual decline / sharp collapse)

A purely qualitative statement such as "stable trend" is not sufficient on its own.

---

### Family D — Mechanism Ablations
Purpose:
- test what the model is actually relying on

Initial ablations:
- no rounding / alternate discretization
- carry corruption
- optional carry lag / shift

---

### Family E — Optional Extended Tests
Possible later additions:
- permutation sensitivity
- held-out combinations
- equivalent formulation tests
- chunk-size sensitivity

---

## 7. Core Diagnostic Scorecard (v1.0 MVP)

Project 4 will begin with five core scorecard dimensions:

1. **In-distribution accuracy**
2. **Structured adversarial accuracy**
3. **Length extrapolation trend**
4. **Rounding sensitivity**
5. **Carry corruption sensitivity**

This core scorecard is sufficient for MVP regime classification.

### Critical Principle
**No single metric in the scorecard is sufficient for regime classification.**  
Classification must rely on **consistent patterns across multiple dimensions**.

---

## 8. Operational Definitions (v1.0)

These are **initial working definitions** and may be revised through documented framework updates.

### 8.1 In-Distribution Accuracy
**Definition:** Accuracy on standard random test data from the same family as training.

**Role:** baseline sanity check only

---

### 8.2 Structured Adversarial Accuracy
**Definition:** Accuracy across the v1.0 adversarial core:
- alternating carry
- full propagation chain
- block-boundary stress

**Role:** primary structural robustness indicator

**Mandatory outputs:**
- pattern-wise accuracy
- mean adversarial accuracy
- worst-case pattern accuracy

**Initial interpretation:**
- high and stable across all patterns → stronger evidence of structural robustness
- good mean with weak worst-case pattern → evidence of selective vulnerability
- broad collapse → evidence against robust compositional generalization

---

### 8.3 Length Extrapolation Trend
**Definition:** Accuracy behavior across increasing lengths beyond the training range.

**Role:** distinguish bounded from stronger scaling behavior

**Minimum operationalization:**
- report accuracy at each tested length
- report relative drop compared to in-range reference accuracy
- report a simple qualitative trend class:
  - stable
  - gradual decline
  - sharp collapse

**Initial interpretation:**
- low relative drop + stable trend → stronger length robustness
- moderate drop + bounded stability → bounded competence
- large drop or collapse → weak extrapolation robustness

---

### 8.4 Rounding Sensitivity
**Definition:**  
`|accuracy_with_rounding - accuracy_without_rounding|`

**Role:** detect dependence on discretization/post-processing

**Initial working thresholds (v1.0):**
- `< 2%` → low sensitivity
- `2–10%` → moderate sensitivity
- `> 10%` → high sensitivity

High sensitivity is evidence against strong internal robustness.

---

### 8.5 Carry Corruption Sensitivity
**Definition:** Accuracy degradation under controlled corruption of carry-related information.

**Method (v1.0):**
- inject carry corruption at controlled probability `p`
- measure degradation as `p` increases

**Role:** mechanism probe for carry dependence

**Important interpretation rule:**
Carry corruption sensitivity must be interpreted jointly with:
- baseline performance
- degradation curve shape
- and adversarial performance

This avoids over-interpreting a single corruption result.

**Initial interpretation:**
- graceful degradation with strong baseline may indicate meaningful carry dependence
- flat non-response may indicate weak carry usage or metric insensitivity
- catastrophic degradation may indicate fragile dependence, but should not be interpreted in isolation

---

## 9. Framework Versioning

The diagnostic framework itself is a research artifact.

### Versioning policy
- **v1.0** — initial framework before intervention experiments
- **v1.x** — minor updates after baseline reruns
- **v2.0** — major revision only if MVP reveals a fundamental framework gap

All updates must be recorded in:
- `FRAMEWORK_CHANGELOG.md`

---

## 10. Baseline Re-Evaluation Phase

Canonical models will be re-run under the same framework:

- MLP baseline
- LSTM baseline
- Transformer baseline
- residual model (if retained as reference)

### Goal
Classify each model into Regime 1, 2, or 3 using the MVP scorecard.

### Important Note
Regime classification is **rule-guided, not fully automatic**.

`diagnostic_scorecard.py` should compute metrics and indicators, but final classification must be explicitly documented with rationale.

### Planned outputs
- `project_4_baseline_comparison.py`
- `PROJECT_4_BASELINE_RESULTS.md`

---

## 11. MVP Intervention: Adversarial Training

### Central Question
Does adversarial training improve genuine structural robustness, or merely add memorized pattern families?

### Evaluation Rule
Adversarially trained models must be evaluated on:
1. seen adversarial families
2. unseen adversarial families

### Interpretation
- improvement only on seen families → expanded approximation / pattern memorization
- improvement on seen + unseen families → stronger evidence of robustness gain

### Planned outputs
- `project_4_adversarial_training.py`
- `PROJECT_4_ADVERSARIAL_TRAINING_RESULTS.md`

---

## 12. Extended Intervention: Blockwise Decomposition

This is the first major planned extension beyond MVP.

### Central Question
Does blockwise processing improve genuine structural robustness, or merely redistribute approximation into smaller units?

### Structural Motivation
This intervention tests whether major limitations lie in:
- global sequence processing
- local carry-rule failure
- weak carry transfer across local groups

### Proposed variants

#### B1 — Naive Chunking
- split long input into small chunks
- local processing only
- no explicit carry interface

#### B2 — Chunking + Explicit Carry Interface
- each chunk receives carry-in
- each chunk emits carry-out

#### B3 — Hierarchical Chunking
- local chunk processing
- higher-level recomposition stage

### Default caution
Blockwise decomposition should **not** be presumed to solve the problem.  
It may simply enlarge the approximation bubble unless cross-boundary carry is genuinely handled.

### Blockwise stress test
A dedicated stress test should require carry to repeatedly cross chunk boundaries.

### Planned outputs
- `project_4_blockwise_decomposition.py`
- `PROJECT_4_BLOCKWISE_RESULTS.md`

---

## 13. Regime Classification Guidelines (v1.0)

These are guiding classification principles, not rigid automatic laws.

### Regime 1 indicators
Typically includes several of the following:
- high in-distribution accuracy
- low adversarial robustness
- poor worst-case pattern accuracy
- high rounding sensitivity
- weak or brittle behavior under carry perturbation
- clear collapse outside the core training regime

### Regime 2 indicators
Typically includes several of the following:
- strong in-distribution accuracy
- moderate adversarial robustness
- meaningful but incomplete worst-case robustness
- bounded length stability
- partial robustness under mechanism probes
- failure concentrated in harder structured conditions

### Regime 3 indicators
Typically includes several of the following:
- high adversarial robustness across all core patterns
- strong worst-case pattern performance
- low or moderate reliance on accidental post-processing
- stable length behavior well beyond training range
- robustness across mechanism-preserving transformations

### Classification Rule
A model should be assigned to a regime only when **multiple dimensions tell a consistent story**.

Borderline or mixed cases should be documented explicitly as such, rather than forced into an overconfident category.

---

## 14. Working Timeline

### Stage 1 — Post-Audit Initialization
- finalize framework v1.0
- create scorecard skeleton
- define adversarial family core
- initialize changelog and output conventions

### Stage 2 — Baseline Re-Evaluation
- rerun canonical baselines under Project 4 framework
- classify baseline regimes
- document rationale

### Stage 3 — MVP Intervention
- run adversarial-training intervention
- compare seen vs unseen adversarial robustness
- determine whether robustness genuinely transfers

### Stage 4 — MVP Synthesis
- decide whether MVP is sufficient for closure/publication
- or whether the project should expand to blockwise decomposition

### Stage 5 — Extended Scope (Optional)
- blockwise experiments
- carry-interface variants
- additional benchmark families
- expanded synthesis

---

## 15. Required Outputs

### MVP outputs
1. `PROJECT_4_DIAGNOSTIC_FRAMEWORK.md`
2. `FRAMEWORK_CHANGELOG.md`
3. `diagnostic_scorecard.py`
4. `benchmark_adversarial_patterns.py`
5. `project_4_baseline_comparison.py`
6. `project_4_adversarial_training.py`
7. `PROJECT_4_BASELINE_RESULTS.md`
8. `PROJECT_4_ADVERSARIAL_TRAINING_RESULTS.md`

### Extended outputs
9. `project_4_blockwise_decomposition.py`
10. `PROJECT_4_BLOCKWISE_RESULTS.md`
11. `PROJECT_4_RESULTS_SUMMARY.md`

---

## 16. Decision Rules

### GO
- framework v1.0 completed
- baselines classified
- one intervention tested properly
- results interpretable and reproducible

### GO WITH QUALIFICATIONS
- main findings stable
- but some dimensions or thresholds require revision

### HOLD
- baseline classification unstable
- framework missing a critical dimension
- or intervention results not interpretable

---

## 17. Non-Goals

Project 4 does not aim to:
- chase benchmark accuracy alone
- assume new architectures are automatically better
- interpret local gains as proof of algorithmic learning
- expand endlessly without producing a usable diagnostic tool

---

## 18. Final Strategic Principle

Project 4 is not primarily a model-improvement project.

Its main expected contribution is:

> **a practical and reproducible diagnostic framework for distinguishing distribution-bound approximation, bounded compositional competence, and stronger algorithm-like arithmetic behavior**

Within this framework:
- adversarial training is a robustness-transfer test
- blockwise decomposition is a structural hypothesis
- negative results remain scientifically valuable
- and interpretation must remain downstream of diagnostics, not ahead of them

---

# END OF PROJECT 4 DIAGNOSTIC FRAMEWORK
