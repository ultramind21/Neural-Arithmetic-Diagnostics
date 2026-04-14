# TRACEABILITY_PROJECT_4 — Claim-to-Evidence Mapping

**Date:** April 11, 2026  
**Purpose:** Enable rapid cross-reference between locked claims and source evidence

---

## Traceability Matrix

| Claim ID | Type | Primary Source | Key Table/Section | Observed Metrics | Associated Artifact |
|----------|------|-----------------|-------------------|------------------|---------------------|
| **P4-C01** | strong | PROJECT_4_EXECUTIVE_SUMMARY.md | "diagnostic framework" section | Framework = 7 components; Intervention → narrow transfer | PROJECT_4_DIAGNOSTIC_FRAMEWORK.md |
| **P4-C01** | strong | PROJECT_4_CLOSURE_SUMMARY.md | "Project 4 Built" (section 2) | Components: scorecard.py, benchmark_adversarial.py, regime_classification.py, etc. | project_4/framework/* |
| **P4-C02** | strong | PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md | "Stable Baseline Matrix" (table) | MLP=1.0, LSTM=0.0, Transformer=1.0 | project_4/baselines/* |
| **P4-C02** | strong | PROJECT_4_RESULTS_SUMMARY.md | "block_boundary_stress separates architectures" | Block-boundary: MLP/Transformer success; LSTM failure | Baseline runs (exact paths TBD) |
| **P4-C03** | strong | PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md | "In-distribution exact-match" row | MLP=0.0859, LSTM=0.0469, Transformer=0.0339 | Baseline artifacts (paths TBD) |
| **P4-C03** | strong | PROJECT_4_RESULTS_SUMMARY.md | "All three baselines are weak" → "none currently strong" | All ≤ 0.09 exact-match | Baseline runs |
| **P4-C04** | strong | PROJECT_4_RESULTS_SUMMARY.md | "First MVP Intervention" (section 4) | Seen family: strong gain; Held-out: failure | Intervention artifacts (paths TBD) |
| **P4-C04** | strong | PROJECT_4_CLOSURE_SUMMARY.md | "First Intervention Result" (section 4) | "strong gain on seen family... failure on held-out" | Adversarial-training intervention logs (paths TBD) |
| **P4-C04** | strong | PROJECT_4_FINAL_JUDGMENT.md | "stable first intervention result" | Narrow transfer, not broad robustness | Intervention validation artifacts |
| **P4-C05** | medium | PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md | "Alternating carry" row | All three = 0.0 (collapse) | Baseline artifacts |
| **P4-C05** | medium | PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md | "Full propagation chain" row | All three = 0.0 (collapse) | Baseline artifacts |
| **P4-C06** | weak | PROJECT_4_CLOSURE_SUMMARY.md | "What Project 4 Built" (section 2) | diagnostic_scorecard.py, RESULT_VALIDATION_PROTOCOL.md, etc. | project_4/framework/* |
| **P4-C06** | weak | PROJECT_4_DIAGNOSTIC_FRAMEWORK.md | Framework specification document | Framework structure, dimensions, protocol | project_4/framework/PROJECT_4_DIAGNOSTIC_FRAMEWORK.md |

---

## Evidence Path Index (Project 4)

### Framework & Documentation
| File | Purpose |
|------|---------|
| `project_4/framework/PROJECT_4_DIAGNOSTIC_FRAMEWORK.md` | Framework specification (C01, C06) |
| `project_4/framework/FRAMEWORK_CHANGELOG.md` | Framework evolution history |
| `project_4/framework/RESULT_VALIDATION_PROTOCOL.md` | Repeated-run validation procedure |

### Baselines & Metrics
| File | Purpose |
|------|---------|
| `project_4/baselines/PROJECT_4_BASELINE_CLASSIFICATION_SUMMARY.md` | Numerical table (C02, C03, C05) |
| `project_4/baselines/PROJECT_4_BASELINE_RESULTS.md` | Baseline evaluation template |
| `project_4/results/baseline_runs/phase30_mlp_baseline_artifact.json` | MLP run output (C02, C03, C05) |
| `project_4/results/baseline_runs/phase30_lstm_baseline_artifact.json` | LSTM run output (C02, C03, C05) |
| `project_4/results/baseline_runs/phase30_transformer_baseline_artifact.json` | TX run output (C02, C03, C05) |
| `project_4/results/baseline_runs/phase30_*_validation_runs.json` | Per-arch validation runs |

### Intervention & Results
| File | Purpose |
|------|---------|
| `project_4/interventions/adversarial_training/results/project_4_adversarial_training_artifact.json` | Intervention run output (C04) |
| `project_4/interventions/adversarial_training/results/project_4_adversarial_training_validation_runs.json` | Intervention validation (C04) |
| `project_4/results/PROJECT_4_RESULTS_SUMMARY.md` | All results synthesis (C02, C04) |
| `project_4/results/PROJECT_4_FINAL_JUDGMENT.md` | Verdict & scope (C01, C04) |
| `project_4/results/PROJECT_4_CLOSURE_SUMMARY.md` | Closure record (C01, C04, C06) |
| `project_4/results/PROJECT_4_EXECUTIVE_SUMMARY.md` | High-level summary (C01, C04) |

### Scripts & Executables
| File | Purpose |
|------|---------|
| `project_4/framework/diagnostic_scorecard.py` | Scorecard component (C01, C06) |
| `project_4/framework/benchmark_adversarial_patterns.py` | Family implementation (C02, C04, C05) |
| `project_4/framework/regime_classification.py` | Regime logic (C01) |

---

## Artifact Gaps → Resolved (Sprint 3.1)

The following artifact paths are now confirmed and available for Project 12 validation:

### Baseline Artifacts (Confirmed)
- **MLP baseline:** `project_4/results/baseline_runs/phase30_mlp_baseline_artifact.json`
- **LSTM baseline:** `project_4/results/baseline_runs/phase30_lstm_baseline_artifact.json`
- **Transformer baseline:** `project_4/results/baseline_runs/phase30_transformer_baseline_artifact.json`
- **Validation runs** (per-architecture): `project_4/results/baseline_runs/phase30_*_validation_runs.json`

### Intervention Artifacts (Confirmed)
- **Adversarial training artifact:** `project_4/interventions/adversarial_training/results/project_4_adversarial_training_artifact.json`
- **Intervention validation runs:** `project_4/interventions/adversarial_training/results/project_4_adversarial_training_validation_runs.json`

### Status
- ✅ P4-C02, C03, C05 baseline paths confirmed
- ✅ P4-C04 intervention paths confirmed
- ✅ No TBD remaining; all evidence ready for Sprint 4A inspection

---

## Validation Readiness (Sprint 3.1)

| Claim | Evidence Status | Ready for Sprint 4A? | Notes |
|-------|---------|---|-------|
| P4-C01 | Framework spec + components documented | ✅ READY | Infrastructure; no numeric data needed |
| P4-C02 | Metrics extracted + artifact paths confirmed | ✅ READY | Baseline artifact confirmed; targets independent |
| P4-C03 | Metrics extracted + artifact paths confirmed | ✅ READY | Baseline artifact confirmed; targets independent |
| P4-C04 | Narrative confirmed + intervention artifact paths confirmed | ✅ READY | Intervention artifacts confirmed; numeric targets to extract in Sprint 4 |
| P4-C05 | Metrics extracted + artifact paths confirmed | ✅ READY | Baseline artifact confirmed; targets independent |
| P4-C06 | Framework components + baseline artifact documented | ✅ READY | Infrastructure; reproducibility check in Sprint 4 |

**Overall Status:** ALL 6 CLAIMS READY FOR SPRINT 4A

---
