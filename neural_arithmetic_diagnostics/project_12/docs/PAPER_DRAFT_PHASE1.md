# From Ideas to Evidence: Project 12 Phase 1 (P11 + P4)
Date: 2026-04-11  
Branch: project12-validation  

## Abstract
Research codebases in neural arithmetic often accumulate compelling results without a clear separation between observations, claims, and reproducible evidence. In this work we present Project 12, a reproducibility-first validation protocol that converts a "system of ideas" into a "system of evidence" via (i) claim locking with pre-registered targets, (ii) baseline-grounded metrics and failure-family breakdowns, (iii) manifest-driven execution with standardized artifacts and metadata, and (iv) copy+patch reproduction enforced by diff gates, complemented by policy-based validation for stochastic interventions. We apply the protocol to two case studies. For Project 11 (soft clamp + sampling/retrieval diagnostics), we validate eight claims and reject one absolute boundary-threshold claim as brittle under holdout-seed variation, replacing it with a mechanism-based revised claim that remains robust across a 20-seed sweep. For Project 4 (baseline diagnostics + adversarial training), we reproduce baseline artifacts and validate that adversarial training yields narrow transfer: strong improvement on seen adversarial families coupled with degradation on held-out structure, supported by a 3-seed smoke check. Overall, the protocol provides a practical blueprint for trustworthy evaluation and claim revision in neural arithmetic diagnostics.

## 1. Introduction
- Why neural arithmetic diagnostics tends to produce brittle claims.
- Why "accuracy-only" and "single-run" conclusions fail.
- What this paper contributes: a reproducibility-first protocol (Project 12).

## Key Contributions
1. **Practical protocol:** Claim locking + manifests + standardized metadata + diff gates + reproducibility and policy-based validation checks.
2. **Methodological insight from Project 11:** Absolute thresholds are brittle under holdout-seed variation; mechanism-based claims remain robust (C07 → C07R across 20-seed sweep).
3. **Intervention validation from Project 4:** Adversarial training yields narrow transfer—strong improvement on seen adversarial families coupled with degradation on held-out structure (policy-validated with 3-seed smoke check).

## 2. Project 12 Validation Protocol
### 2.1 Claim locking
- Observed vs. pre-registered targets.
- Status taxonomy (validated / partial / rejected-as-stated / revised).

### 2.2 Baselines + metrics
- Performance, cost proxy, stability.
- Failure-family breakdown.

### 2.3 Execution discipline
- Manifests, output safety, metadata schema.
- Copy+patch + diff gate.
- Repro checks vs policy checks.

**Table 1 (Protocol checklist):**  
See: `project_12/paper_assets/table1_protocol_checklist.md`

## 3. Case Study A — Project 11 (Soft clamp + sampling/retrieval)
### 3.1 Setup
- Task/metric: macroF1_present (as defined in Project 11 artifacts).
- Systems: V3, V3.1, NN11/21/41/81; sampling regimes.

### 3.2 Validated claims (Phase 1)
Summarize:
- P11-C01..C06, C08 validated
- P11-C07 rejected-as-stated (absolute threshold)
- P11-C07R validated (mechanism-based)

**Figure 1 (NN resolution sweep):**  
`project_12/paper_assets/fig1_nn_resolution.png`

**Figure 2 (sample efficiency):**  
`project_12/paper_assets/fig2_sample_efficiency.png`

**Figure 3 (C07 sweep distribution):**  
`project_12/paper_assets/fig3_c07_sweep_distribution.png`

**Table 2 (P11 evidence summary):**  
See: `project_12/paper_assets/table2_p11_evidence_summary.md`

## 4. Case Study B — Project 4 (Baselines + adversarial training)
### 4.1 Baseline reproduction + validated baseline claims
- P4-C01/C06 infra validation (artifact-based)
- P4-C02 architecture split (block-boundary)
- P4-C03 weak in-dist
- P4-C05 universal collapse on alternating/full-prop

**Figure 4 (P4 baseline family table):**  
`project_12/paper_assets/fig4_p4_baseline_family_table.png`

### 4.2 Intervention: narrow transfer (P4-C04)
- Formal definition of seen/held-out gains (baseline artifact + post-training artifact).
- Policy-based validation.
- Multi-seed smoke check (3 seeds).

**Figure 5 (P4 pre vs post):**  
`project_12/paper_assets/fig5_p4_pre_post_intervention.png`

**Figure 6 (P4 3-seed sweep summary):**  
`project_12/paper_assets/fig6_p4_seed_sweep_summary.png`

## 5. Threats to Validity
See: `project_12/docs/PAPER_READY_PHASE1_THREATS_TO_VALIDITY.md`

## 6. Practical guidance (how to reuse this protocol)
- Minimal steps to convert a "project of ideas" into evidence.
- Common failure modes (target calibration, rewrites, missing metadata).

## 7. Conclusion
- Phase 1 shows: brittle absolute thresholds vs robust mechanism claims (P11-C07 → P11-C07R).
- Adversarial training can produce narrow transfer and negative transfer (P4-C04).
- Project 12 protocol makes these conclusions trustworthy.

## Appendix: Evidence pointers
- Master snapshot: `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
- P11 snapshot: `project_12/docs/VALIDATED_RESULTS_P11_PROJECT12.md`
- P4 snapshot: `project_12/docs/VALIDATED_RESULTS_P4_PROJECT12.md`
