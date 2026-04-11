# From Ideas to Evidence: Project 12 Phase 1 (P11 + P4)
Date: 2026-04-11  
Branch: project12-validation  

## Abstract
Research codebases in neural arithmetic often accumulate compelling results without a clear separation between observations, claims, and reproducible evidence. In this work we present Project 12, a reproducibility-first validation protocol that converts a "system of ideas" into a "system of evidence" via (i) claim locking with pre-registered targets, (ii) baseline-grounded metrics and failure-family breakdowns, (iii) manifest-driven execution with standardized artifacts and metadata, and (iv) copy+patch reproduction enforced by diff gates, complemented by policy-based validation for stochastic interventions. We apply the protocol to two case studies. For Project 11 (soft clamp + sampling/retrieval diagnostics), we validate eight claims and reject one absolute boundary-threshold claim as brittle under holdout-seed variation, replacing it with a mechanism-based revised claim that remains robust across a 20-seed sweep. For Project 4 (baseline diagnostics + adversarial training), we reproduce baseline artifacts and validate that adversarial training yields narrow transfer: strong improvement on seen adversarial families coupled with degradation on held-out structure, supported by a 3-seed smoke check. Overall, the protocol provides a practical blueprint for trustworthy evaluation and claim revision in neural arithmetic diagnostics.

## 1. Introduction
Neural arithmetic is a convenient testbed for studying whether learned systems exhibit algorithm-like behavior, compositional generalization, and robust structure sensitivity. However, results in this space are frequently fragile: performance can look strong under one evaluation setup yet degrade under small changes in sampling, holdout construction, or random seeds. In practice, research repositories often accumulate convincing artifacts (plots, tables, "best runs") without a clear boundary between (i) observations that happened once, (ii) claims that are intended to generalize, and (iii) evidence that supports those claims under controlled variation.

Project 12 addresses this gap by treating validation as a first-class deliverable. Instead of optimizing for additional new results, we convert prior project outputs into a system of evidence via claim locking, baseline-grounded comparisons, and reproducible execution rules. Two case studies illustrate why this matters. In Project 11, an absolute boundary-threshold claim fails under holdout-seed variation even though a mechanism-based version of the same idea remains robust; the protocol makes the difference explicit (C07 → C07R). In Project 4, adversarial training produces narrow transfer—improvements on targeted families coupled with degradation on held-out structure—validated via policy-based checks and a multi-seed smoke test. Together, these cases show that validation discipline can reliably separate brittle thresholds from robust mechanisms and prevent narrative drift in empirical claims.

## Key Contributions
1. **Practical protocol:** Claim locking + manifests + standardized metadata + diff gates + reproducibility and policy-based validation checks.
2. **Methodological insight from Project 11:** Absolute thresholds are brittle under holdout-seed variation; mechanism-based claims remain robust (C07 → C07R across 20-seed sweep).
3. **Intervention validation from Project 4:** Adversarial training yields narrow transfer—strong improvement on seen adversarial families coupled with degradation on held-out structure (policy-validated with 3-seed smoke check).

## 2. Project 12 Validation Protocol
Project 12 is designed to transform a repository of experimental outcomes into a repository of reproducible, baseline-grounded evidence. The protocol is intentionally operational: every validated statement must be traceable to a locked claim, an executable manifest, and a concrete artifact.

**Claim locking (Observed vs Targets).** Each claim is written in an operational form with a unique ID and an explicit scope (task, distribution, noise, sampling regime). We separate historical observations from Phase 1 validation targets. Observations record what Project 4/11 previously reported; targets define what will be considered a pass under Project 12, using rounded, independent thresholds or ordering constraints (and marking targets as TBD when magnitudes are unavailable without artifact inspection). This avoids confirmation bias in which a previously observed value is reused as its own acceptance criterion.

**Baseline-first comparisons and unified metrics.** All non-trivial claims must beat (or be compared against) a known baseline: dense sampling, uniform sampling, boundary sampling, or nearest-neighbor references, depending on the task. Metrics are unified across runs and emphasize failure structure: per-family breakdowns, worst-family behavior, and stability across runs where stochasticity is present.

**Manifest-driven execution and artifact discipline.** Every run is described by a JSON manifest that specifies inputs, seeds, output directories, and the claim IDs it supports. Outputs are required to be written under `project_12/results/` only. Artifacts include standardized metadata (git hash, timestamp, environment, manifest hash) to make results attributable and debuggable.

**Copy+patch reproduction with diff gates.** For reproduction of legacy experiments, entrypoints are created by copying the original script and applying minimal patches (manifest input, output routing, metadata). We enforce this via a diff gate that measures similarity between original and reproduced scripts; the gate prevents "silent rewrites" that would undermine reproduction claims.

**Reproduction checks vs policy checks.** When a procedure is deterministic (or expected to be quasi-deterministic), we perform reproduction checks that compare Project 12 artifacts against historical artifacts within a strict tolerance. When an intervention is stochastic (e.g., training), we validate using policy checks: pre-registered ordering and gap criteria evaluated on the recorded artifact, optionally strengthened by limited seed sweeps.

**Table 1 (Protocol checklist):**  
See: `project_12/paper_assets/table1_protocol_checklist.md`

## 3. Case Study A — Project 11 (Soft clamp + sampling/retrieval)

### 3.1 Setup
Project 11 studies a regime-structured arithmetic diagnostic setting where performance depends on how decision boundaries and transitions are represented and sampled. The evaluated systems include compact interpretable rule baselines (V3, V3.1), dense nearest-neighbor references at multiple resolutions (NN11/NN21/NN41/NN81), and structured sampling strategies (uniform, boundary-focused, and mixed). Evaluation is reported using macroF1_present and related per-subset breakdowns as recorded in the Project 12 artifacts.

### 3.2 Validated findings (P11-C01 to P11-C06, P11-C08)
Across procedure-preserving re-validation, soft clamp enables a competitive interpretable rule baseline overall (P11-C01). Dense nearest-neighbor performance improves with resolution, providing a strong upper-performance reference (P11-C02), illustrated by the monotonic trend in the resolution sweep (Fig. 1). Sampling strategy matters: boundary-only sampling underperforms substantially, while mixed sampling that combines global coverage with boundary emphasis achieves near-dense performance at much lower reference cost (P11-C03, P11-C04), summarized in the sample-efficiency curve (Fig. 2). A ratio + kNN sweep further supports that intermediate mixing ratios are competitive and that kNN settings can change performance in structured ways (P11-C05). Finally, increasing reference set size beyond N=1000 yields diminishing returns under the mixed strategy in this setting (P11-C06). Engineering/protocol checks (P11-C08) confirm that the reference construction and evaluation procedure meet the specified efficiency and leakage-prevention requirements under the Project 12 run discipline.

### 3.3 Brittle absolute threshold → mechanism-based revision (P11-C07 → P11-C07R)
A key contribution of Project 12 is making "threshold brittleness" observable. Project 11 originally included an absolute boundary-performance threshold claim (P11-C07). Under a procedure-preserving holdout-seed sweep, this absolute threshold is not robust: only 1/20 seeds satisfies the V3.1 boundary ≥ 0.85 requirement (Fig. 3). Importantly, the same set of experiments supports a stronger, mechanism-based conclusion: relative improvement of V3.1 over V3 on boundary subsets and closeness of V3.1 to NN81 remain robust across holdout seeds (P11-C07R). Project 12 therefore rejects the absolute-threshold claim as stated while validating the mechanism-based revision, demonstrating how the protocol separates brittle numeric thresholds from stable structural effects.

**Figures and tables.**
- Fig. 1: NN resolution sweep (P11-C02).
- Fig. 2: Sample efficiency across strategies (P11-C03, P11-C04, P11-C06).
- Fig. 3: Boundary-threshold sensitivity sweep (P11-C07 rejected-as-stated; P11-C07R validated).
- Table 2: P11 claim-to-evidence summary.

## 4. Case Study B — Project 4 (Baselines + adversarial training)

### 4.1 Baseline reproduction and validated baseline claims (P4-C01, P4-C02, P4-C03, P4-C05, P4-C06)
Project 4 provides a diagnostic framework that evaluates multiple model architectures (MLP, LSTM, Transformer) across structured adversarial families. Project 12 first reproduces baseline artifacts under a strict copy+patch discipline and validates baseline claims using per-family exact-match metrics recorded in standardized artifacts. Baseline diagnostics show a clear architecture-dependent split on block-boundary stress: MLP and Transformer succeed while LSTM fails (P4-C02). At the same time, in-distribution exact-match remains weak across all three architectures under the bounded evaluation path (P4-C03). Two adversarial families—alternating carry and full-propagation chain—produce universal collapse across architectures (P4-C05). Infrastructure claims are validated artifact-based: the framework outputs contain the required per-family scorecard structure (P4-C01), and artifact schemas and metadata are consistent under Project 12 execution discipline (P4-C06). The baseline family pattern table is summarized in Fig. 4.

### 4.2 Intervention: adversarial training yields narrow transfer (P4-C04)
Project 4 also tests an adversarial-training intervention intended to improve performance on specifically targeted adversarial families. Because training is stochastic, Project 12 validates the intervention claim using policy-based criteria rather than exact numeric reproduction: improvements are evaluated as gains relative to baseline per-family exact-match under a locked definition of seen vs held-out families. The reproduced intervention shows strong improvement on seen families (notably alternating carry) while degrading held-out structure (block-boundary stress), producing a large positive gap between seen and held-out gains and satisfying the P4-C04 acceptance criteria. Fig. 5 visualizes the pre/post shift per family.

To strengthen confidence beyond a single run, Project 12 additionally performs a 3-seed manifest-driven smoke check: all three seeds satisfy the policy acceptance criteria (Fig. 6). While this does not fully characterize variance, it provides evidence that the narrow-transfer conclusion is not an isolated artifact of a single random seed.

**Figures.**
- Fig. 4: Baseline family table across architectures (P4-C02, P4-C03, P4-C05).
- Fig. 5: Pre vs post intervention by family (P4-C04).
- Fig. 6: 3-seed stability smoke check for P4-C04.

## 5. Threats to Validity

**Stochastic interventions.** Training-based interventions are inherently stochastic. Project 12 therefore validates such claims via policy checks (pre-registered ordering/gap criteria evaluated on recorded artifacts) rather than requiring exact numeric reproduction. For Phase 1, the P4 intervention conclusion is additionally supported by a limited 3-seed smoke check; this increases confidence that the effect is not a single-run artifact but does not fully characterize variance.

**Finite seed sweeps.** Sensitivity analyses are necessarily limited to a finite set of seeds. In Project 11, the C07 boundary-threshold brittleness conclusion is supported by a 20-seed holdout sweep; while this is strong evidence against universal absolute thresholds, it does not exhaustively map all possible holdout regimes.

**Artifact schema dependence.** The protocol assumes that artifacts encode the metrics needed to evaluate locked claims (e.g., per-family exact-match or macroF1_present). We mitigate this by (i) enforcing standardized Project 12 metadata and (ii) using explicit schema probes and fail-fast extraction rules to avoid silent misparsing.

**Scope limitations.** Phase 1 validates two case-study projects (P11 and P4). The protocol is intended to generalize, but empirical generalization to additional tasks, architectures, or arithmetic regimes remains future work.

## 6. Practical guidance (how to reuse this protocol)

Phase 1 suggests a practical recipe for converting a research repository into a reproducible evidence system:

1) **Lock claims early.** Write operational claims with IDs, explicit scope, and pass/fail targets. Separate historical observations from validation targets to avoid calibration on outcomes.

2) **Start with baselines.** Ensure every claim is baseline-grounded ("better than something known") and uses unified metrics that include failure-family breakdowns, not only aggregate accuracy.

3) **Make execution manifest-driven.** Encode every run in a JSON manifest (inputs, seeds, output_dir, claim IDs). Require that all outputs are written under a dedicated results directory.

4) **Enforce copy+patch reproduction.** When reproducing legacy scripts, copy them verbatim and apply minimal patches only (manifest input, output routing, metadata). Use a diff gate to prevent silent rewrites.

5) **Choose the right validation mode.** Use strict reproduction checks for deterministic procedures; use policy checks for stochastic interventions, optionally strengthened with limited seed sweeps.

6) **Compress results.** Maintain an evidence-only snapshot that lists validated, partial/conditional, and rejected-as-stated claims, with direct paths to artifacts and reports.

These steps are lightweight enough to apply incrementally while being strict enough to prevent narrative drift and irreproducible conclusions.

## 7. Conclusion

Project 12 Phase 1 demonstrates that validation discipline can be treated as a deliverable rather than an afterthought. In Project 11, the protocol distinguishes a brittle absolute boundary threshold (rejected-as-stated) from a robust mechanism-based alternative (validated), showing how seed sensitivity can invalidate numeric guarantees while preserving meaningful structural conclusions. In Project 4, the protocol validates that adversarial training can yield narrow transfer—large improvements on seen families coupled with degradation on held-out structure—under policy-based checks and a multi-seed smoke test. Together, these case studies show how a reproducibility-first workflow can turn a system of ideas into a system of evidence and produce publication-safe claims with explicit provenance.

## Appendix: Evidence pointers
- Master snapshot: `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
- P11 snapshot: `project_12/docs/VALIDATED_RESULTS_P11_PROJECT12.md`
- P4 snapshot: `project_12/docs/VALIDATED_RESULTS_P4_PROJECT12.md`
