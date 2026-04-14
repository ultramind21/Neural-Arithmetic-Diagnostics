# PROJECT STRUCTURE
## Neural-Arithmetic-Diagnostics — Navigation Guide

**Last Updated:** April 2026

---

## Root Directory Overview

```text
neural_arithmetic_diagnostics/
├── src/                    # Core executable code (env/models/teacher/train/utils)
├── tests/                  # Unit tests
├── checkpoints/            # Original checkpoints
├── Papers/                 # Historical research line (Projects 1–3) + closure narratives
├── final_audit/            # Trust-recovery verification archive (code + reports + raw logs)
├── project_4/              # Diagnostic Arithmetic Reasoning (framework + baselines + interventions)
├── project_5/              # Decomposition Robustness Exploration
├── project_6/              # Mechanistic Interpretability Sandbox
├── project_7/              # Local-to-global failure bridge
├── project_8/              # Composition stabilization architectures
├── project_9/              # Higher-dimensional compositional sandboxes
├── project_10/             # Compositional failure laws + rescue regime theory
├── project_11/             # Boundary + sampling/resolution tradeoffs + packaging
├── project_12/             # Validation protocol + evidence bundle + paper-ready materials (Phase 1)
├── paper/                  # Legacy writing/submission materials (program-level)
├── assets/                 # Public-facing visual assets
├── meta/                   # Governance / naming / cleanup plans
├── archive_optional/       # Archived optional/debug/root legacy materials
├── tools/                  # Secondary helper scripts
├── README.md
├── GETTING_STARTED_FAST.md
├── WHY_THIS_PROJECT_MATTERS.md
├── STRATEGIC_RESEARCH_MAP.md
├── PROGRAM_LEVEL_SYNTHESIS.md
├── PROGRAM_PUBLICATION_STRATEGY.md
├── PROJECT_NAMING_CANON.md
├── LICENSE
└── requirements.txt
```

---

## 1) `src/` — Core executable code
**Purpose:** Original executable model/training/evaluation code used across the research line.

This folder is the code "substrate" that earlier projects and some audits reference.

---

## 2) `Papers/` — Historical research narratives (Projects 1–3)
**Purpose:** Preserve the historical research line and closure documents for Projects 1–3.

**Role:** Historical narrative layer (what was believed, what was concluded at the time).

**Start here:** `Papers/README.md`

---

## 3) `final_audit/` — Trust-recovery verification archive
**Purpose:** Preserve the multi-phase audit that revalidated, corrected, or qualified earlier claims.

**Role:** Verification layer (what passed, what failed, what remains qualified).

**Start here:** `final_audit/README.md`

---

## 4) `project_4/` — Diagnostic arithmetic reasoning framework
**Purpose:** Post-audit diagnostic framework: narrow gains vs broader robustness transfer.

**Start here:** `project_4/README.md`

---

## 5) `project_5/` — Decomposition robustness exploration
**Purpose:** Study whether decomposition improves structural robustness.

---

## 6) `project_6/` — Mechanistic interpretability sandbox
**Purpose:** Probe arithmetic-relevant internal structure and causal signals.

---

## 7) `project_7/` — Local-to-global failure bridge
**Purpose:** Bridge local competence and family-level global failure.

---

## 8) `project_8/` — Composition stabilization architectures
**Purpose:** Architecture design for family-sensitive rescue of failure modes.

---

## 9) `project_9/` — Higher-dimensional compositional sandboxes
**Purpose:** Extend the program into higher-dimensional structured spaces (topology/family-sensitive effects).

---

## 10) `project_10/` — Theory-building + rescue regime theory
**Purpose:** Stress-test higher-level law candidates and converge on regime/threshold-structured accounts.

---

## 11) `project_11/` — Boundary evaluation + sampling/resolution tradeoffs + packaging
**Purpose:** Evaluate boundary behavior, transfer, and cost-aware inference tradeoffs (structure vs resolution vs sampling).

**Packaged entry points:**
- `project_11/packaging/EXECUTIVE_ABSTRACT.md`
- `project_11/packaging/PACKAGING_INDEX.md`
- `project_11/packaging/out/EVIDENCE_MATRIX.md`
- `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md`
- `project_11/packaging/out/FIG_F2_SAMPLE_EFFICIENCY.md`
- `project_11/packaging/out/FIG_F3_RATIO_KNN.md`

**Important note:** Project 11 is evidence-packaged, and its key claims are validated/qualified in Project 12 Phase 1.

---

## 12) `project_12/` — Validation & consolidation protocol (Phase 1 complete)
**Purpose:** Convert projects into validated evidence via:
- claim locking (Observed vs Targets),
- manifest-driven execution,
- standardized artifacts + metadata,
- copy+patch reproduction enforced by diff gates,
- reproduction checks (deterministic) vs policy checks (stochastic).

**Phase 1 scope:** Project 11 + Project 4.

**Start here (evidence-first):**
- Master snapshot: `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
- Paper draft: `project_12/docs/PAPER_DRAFT_PHASE1.md`
- Figures/tables: `project_12/paper_assets/`
- Submission checklist: `project_12/docs/SUBMISSION_CHECKLIST_PHASE1.md`
- PDF build instructions: `project_12/paper_build/README.md`

---

## 13) `paper/` — Legacy writing/submission materials
**Purpose:** Program-level writing and submission preparation materials.
(Phase 1 "paper-ready" bundle lives in `project_12/`.)

---

## 14) `assets/` — Public-facing visual assets
Repository-level visuals (overview diagrams, etc.).

---

## 15) `meta/` — Governance / naming / cleanup plans
Repository-level planning docs (useful, but not the scientific entry path).

---

## 16) `archive_optional/` — Archived non-core materials
Debug/root archive material preserved to reduce clutter.

---

## 17) Root-level reading paths

### Path A — Evidence-only (recommended)
1) `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
2) `project_12/docs/PAPER_DRAFT_PHASE1.md`
3) `project_12/docs/SUBMISSION_CHECKLIST_PHASE1.md`

### Path B — Human overview
1) `README.md`
2) `WHY_THIS_PROJECT_MATTERS.md`
3) `GETTING_STARTED_FAST.md`

### Path C — Audit-first (verification layer)
1) `final_audit/README.md`
2) `final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md`

### Path D — Project 11 packaged takeaways (pre-validation packaging)
1) `project_11/packaging/EXECUTIVE_ABSTRACT.md`
2) `project_11/packaging/PACKAGING_INDEX.md`

---

## 18) Current high-level status

| Layer | Status |
|------|--------|
| Projects 1–3 (Papers/) | COMPLETE / HISTORICAL |
| Trust-Recovery Audit | COMPLETE |
| Project 4 | COMPLETE (validated in Project 12 Phase 1) |
| Project 5 | COMPLETE |
| Project 6 | COMPLETE |
| Project 7 | COMPLETE |
| Project 8 | COMPLETE |
| Project 9 | COMPLETE |
| Project 10 | COMPLETE |
| Project 11 | COMPLETE (packaged + validated/qualified in Project 12 Phase 1) |
| **Project 12 (Phase 1)** | **COMPLETE (validated evidence bundle + paper-ready materials)** |

---

## Final note
This repository is best understood as a **research program** plus an explicit **validation layer**.
If you are evaluating claims, prefer Project 12 snapshots and reports (evidence-first) over narrative summaries.
