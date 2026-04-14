# Project 12 Phase 1 — Threats to Validity & Mitigations

## Purpose
Document known limitations, potential validity threats, and the mitigations already embedded in the validation framework.

---

## I. Known Limitations

### A. Training Non-Determinism (P4 Intervention)

**Threat:** Adversarial training uses random initialization and data shuffling. Different seeds may produce different results.

**Scope:** Affects P4-C04 (narrow transfer claim).

**Evidence of limitation:**
- Entry in FORMAL_CLAIMS.md P4-C04 notes: "Single-run validation... training is stochastic."
- Baseline/seed-dependent: identical seeds produce identical models, but different seeds may diverge.

**Magnitude:** Unknown without full sweep; Sprint 4F tested only 3 seeds (all identical results, suggesting either deterministic data generation or seed not fully utilized).

---

### B. Limited Seed Sweep Scope (P4 Intervention)

**Threat:** Only 3 seeds tested (42, 123, 456). Broader seed sweep might reveal variance not captured here.

**Scope:** P4-C04 stability claim is "smoke check," not full variance quantification.

**Evidence:**
- project_12/reports/P4_C04_STABILITY_SWEEP_REPORT.md explicitly states: "Evidence of robustness, not variance measurement."
- All 3 runs identical (gap=1.5), preventing quantification of variance across seeds.

**Magnitude:** Future multi-seed runs with e.g. 10-20 seeds could reveal variance currently hidden.

---

### C. Artifact Schema Dependency

**Threat:** Validation logic depends on specific JSON schema (pre_exact_match, post_exact_match, computed_gains, etc.). Schema change breaks all downstream checks.

**Scope:** Affects reproducibility of future interventions using same schema.

**Evidence:**
- Schema locked in FORMAL_CLAIMS.md per-claim definitions.
- Manifest-driven (e.g., project_12/manifests/p4_adversarial_training_repro_manifest.json) specifies baseline_artifact_path and output_dir, but not schema version.

**Magnitude:** Medium—schema evolves rarely, but breaking change *would* invalidate all policy checks downstream.

---

### D. Limited Architecture Scope (P4)

**Threat:** P4 validation focuses on MLP at phase 30 length-5. Larger architectures or different phases untested.

**Scope:** Affects claims C01-C06 (all P4 claims implicitly assume phase30 MLP context).

**Evidence:**
- Training loop hardcoded: max_length=5, 30 epochs, lr=0.001.
- Only baseline artifact for MLP checked; LSTM/Transformer mentioned in C05 but not reproduced in P12.

**Magnitude:** Medium—phase30/MLP is "bounded MVP"; generalization untested.

---

### E. Historical Data Dependency (P11)

**Threat:** P11 claims validated by *replicating* P11 procedures, not by independent data collection. If P11 data contaminated or biased, replication inherits bias.

**Scope:** Affects P11 claims C01-C06 and C08 (procedure-preserving validation).

**Evidence:**
- REPRO_CHECK_PROJECT11.md: exact phase D/E2/E3 outputs match P11 historical (intentional design).
- No new holdout test set or independent data replication.

**Magnitude:** Medium—but mitigated by sensitivity sweep (C07) which uses *different* seeds on same data, revealing robustness issues (threshold brittleness).

---

### F. Single-Run Policy Checks (P4-C04)

**Threat:** P4-C04 acceptance based on policy thresholds (gap ≥ 0.10, seen_gain > heldout_gain) set once. If policy thresholds too lenient or too strict, claim changes.

**Scope:** P4-C04 (and indirectly P4-C01-C06 which all assume same artifact schema).

**Evidence:**
- FORMAL_CLAIMS.md locks thresholds: min_gap = 0.10, require_ordering = true.
- No justification for why 0.10 chosen (vs. 0.05 or 0.15).

**Magnitude:** Low—thresholds pre-registered in FORMAL_CLAIMS before training; cannot claim p-hacking. But threshold choice remains somewhat arbitrary.

---

## II. Mitigations Already Implemented

### A. Artifact Consistency Checks (Multi-View Verification)

**Mitigation:** P4-C04 validated by reading artifact.json from 4 independent paths:
1. Direct repro_check_project4_intervention.py load
2. Direct Python JSON extraction (`json.load()`)
3. Policy check report
4. Validation report with manual extraction

**Evidence:** Sprint 4B.2E.1 audit showed all 4 paths agree on pre/post/gains metrics.

**Effectiveness:** Catches JSON parsing errors, missing fields, schema mismatches.

---

### B. Diff Gate Verification (Entrypoint Fidelity)

**Mitigation:** Entrypoint reproducibility measured via diff gate:
- Similarity ratio ≥ 0.85 required (copy+patch discipline)
- Lines changed ≤ 80 allowed

**Evidence:**
- P11: diff_gate_p11_entrypoint.py (if run)
- P4: DIFF_GATE_P4_INTERVENTION_ENTRYPOINT.md (similarity 0.8811)

**Effectiveness:** Ensures Project 12 scripts are true reproductions, not reimplementations. Catches architectural drift.

---

### C. Policy-Based Acceptance (Non-Comparison to History)

**Mitigation:** P4-C04 policy check does NOT compare to Project 4 historical values. Instead, checks ordering and gap thresholds set a priori.

**Evidence:**
- FORMAL_CLAIMS.md P4-C04: "Policy-based check suffices for validation."
- repro_check_project4_intervention.py: acceptance logic independent of artifact timestamp or commit hash.

**Effectiveness:** Avoids NumPy precision issues, random seed differences, or subtle hyperparameter drift. Stays robust across non-deterministic training.

---

### D. Sensitivity Sweep (Threshold Robustness Testing)

**Mitigation:** P11-C07 tested across seeds 101, 202, 303 to measure threshold brittleness (C07 rejects; C07R passes).

**Evidence:**
- C07_SENSITIVITY_SWEEP_REPORT.md: per_seed results, failed seeds identified.
- Refined claim C07R shows relative ordering > absolute threshold.

**Effectiveness:** Catches overfitting to specific seed/run. Informs design of future claims (prefer relative metrics over absolute thresholds).

---

### E. Manifest-Driven Configuration

**Mitigation:** All experiments configured via JSON manifests (baseline_artifact_path, output_dir, seed, acceptance criteria). Manifest hashed and stored in artifact metadata.

**Evidence:**
- project_12/manifests/p4_adversarial_training_repro_manifest.json
- p12_metadata.manifest_sha256 in all P12 artifacts

**Effectiveness:** Reproducibility portable; future runs can reuse exact manifest. Configuration drift detectable via hash mismatch.

---

### F. Procedure-Preserving Replication (P11)

**Mitigation:** P11 claims validated by re-executing exact same procedures from Project 11, not by independent re-derivation.

**Evidence:**
- REPRO_CHECK_PROJECT11.md phases D/E2/E3 all return "OK" (exact match).
- No reimplementation; entrypoint directly loads P11 scripts.

**Effectiveness:** Ensures fidelity to original methodology. Phase D/E2/E3 match proves no accidental change to evaluation logic.

---

### G. Multi-Seed Smoke Check (P4-C04 Stability)

**Mitigation:** Sprint 4F executes same training+policy-check on 3 seeds under identical manifest config.

**Evidence:**
- P4_C04_STABILITY_SWEEP_REPORT.md: 3/3 seeds PASS, gap=1.5 identical.
- Aggregated results in CSV for easy comparison.

**Effectiveness:** At minimum, demonstrates claim does not collapse under seed variation. Caveat: identical results suggest seed may not be fully controlling randomness (future diagnostic).

---

### H. Git Provenance & Branch Hygiene

**Mitigation:** All work on single clean branch (project12-validation). Each sprint is 1 commit with descriptive message.

**Evidence:**
- Git log: commits dd65259, ff38bd1, 83a03ac (Sprint 5, 4F, 5.1)
- No squashing or rebasing; full history preserved.

**Effectiveness:** Reproducible audit trail. Each claim tied to specific commit.

---

## III. Residual Risks (Not Fully Mitigated)

| Risk | Severity | Future Mitigation |
|------|----------|-------------------|
| Training non-determinism variance unknown | Medium | 10+ seed sweep with variance quantification |
| P4 limited to phase30/MLP/length5 | Medium | Generalization study: other phases, architectures, lengths |
| P11 threshold brittleness (C07) | Low | Avoid absolute thresholds; prefer relative metrics in future claims |
| Artifact schema fragility | Low | Schema versioning in manifest (v1.0, v2.0, etc.) |
| Policy threshold choice arbitrary | Low | Sensitivity analysis: test policy on boundary cases (gap=0.09, gap=0.11) |

---

## IV. How These Mitigations Support Publication

**For paper/report:**

1. **Replicability:** Diff gates + manifest hashing + git provenance → readers can reproduce Phase 1 exactly
2. **Confidence:** Multi-view consistency checks + policy checks → low risk of silent errors
3. **Honesty:** Limitations section + sensitivity sweep → shows we tested against our own claims
4. **Parsimony:** Focus on ordering/gap (not exact values) → robust across implementation details

**Recommended disclosure:**
- Mention C07 rejection + C07R refinement as success story (validation framework caught threshold overfitting)
- Note P4-C04 is "policy-validated, not variance-quantified" to set expectations
- Highlight diff gates as innovation (rarely done in ML papers)

---

**Last updated:** 2026-04-11 (Sprint 6)  
**Repository:** neural_arithmetic_diagnostics (project12-validation)
