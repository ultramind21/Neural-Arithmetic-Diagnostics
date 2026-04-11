# Neural-Arithmetic-Diagnostics
## From arithmetic performance to robustness, mechanisms, and compositional structure

## TL;DR
Neural networks can achieve high arithmetic accuracy while failing under structured conditions.

This repository documents:
- a diagnostic framework for separating narrow gains from broader robustness (Project 4),
- a mechanism + sampling study showing how boundary behavior can be artifact-driven and how to evaluate efficiently (Project 11),
- and a reproducibility-first validation layer that turns results into evidence (Project 12, Phase 1).

## One-sentence identity
This repository is a research program on neural arithmetic reasoning that converts experiments into **validated evidence** (locked claims → manifests → artifacts → gates).

---

## Why this repository matters
High benchmark performance can hide:
- family-specific failures,
- boundary fragility,
- non-uniform internal mechanisms,
- and "narrow wins" that do not transfer.

The repository is organized to preserve not only results, but the *process* of stress-testing, auditing, and validating them.

Core message:
> **High arithmetic accuracy alone is not sufficient evidence of robust reasoning.**

---

## Start here (fast paths)

### Human motivation
- `WHY_THIS_PROJECT_MATTERS.md`

### Fast technical entry
- `GETTING_STARTED_FAST.md`

### Project 11 packaged results (evidence + figures)
- `project_11/packaging/EXECUTIVE_ABSTRACT.md`
- `project_11/packaging/PACKAGING_INDEX.md`

### Project 12 validation closure + paper bundle (Phase 1)
- Master validated snapshot: `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
- Paper draft (Markdown): `project_12/docs/PAPER_DRAFT_PHASE1.md`
- Paper assets (figures/tables): `project_12/paper_assets/`
- Submission checklist: `project_12/docs/SUBMISSION_CHECKLIST_PHASE1.md`
- PDF build: `project_12/paper_build/README.md`

---

!

---

## Quick mental model (how to read the repo)
- **Projects 1–3:** historical research line (what was believed early).
- **Audit + Projects 4–11:** structured diagnostics, mechanisms, composition, and theory under stress tests.
- **Project 12:** validation layer that consolidates claims into reproducible evidence (Phase 1 covers P11 + P4).

---

## Key results (Phase 1 summary: Projects 11 + 4, validated in Project 12)
Across the research line:
- Standard/random evaluations can look strong while structured families expose failures.
- In Project 11, a *mechanism shift* matters: hard clamp discontinuities can concentrate boundary errors; soft saturation (soft clamp) restores smoother structure and enables sample-efficient evaluation.
- In Project 11, an **absolute boundary threshold claim** is brittle under holdout-seed variation; a **mechanism-based revision** remains robust (C07 → C07R).
- In Project 4, adversarial training can yield **narrow transfer**: strong gains on seen families with degradation on held-out structure (validated via policy checks and a 3-seed smoke check).

---

## Repository at a glance
```text
neural_arithmetic_diagnostics/
├── src/                    # Core executable code (env/models/teacher/train/utils)
├── Papers/                 # Historical research line (Projects 1–3)
├── final_audit/            # Trust-recovery verification archive
├── project_4/              # Diagnostic Arithmetic Reasoning (framework + baselines + interventions)
├── project_5/              # Decomposition Robustness Exploration
├── project_6/              # Mechanistic Interpretability Sandbox
├── project_7/              # Local-to-global failure bridge analysis
├── project_8/              # Composition stabilization architectures
├── project_9/              # High-dimensional compositional sandboxes
├── project_10/             # Rescue regime theory / threshold-structured regime space
├── project_11/             # Mechanism + transfer + boundary + sampling + packaging
│   └── packaging/          # Packaged outputs (evidence + figures + claims)
├── project_12/             # Validation protocol + evidence bundle + paper-ready materials
├── tests/                  # Unit tests
├── checkpoints/            # Original checkpoints
└── README.md
```

---

## Main layers (where to look)

### 1) Projects 1–3 — Historical research line
Located in `Papers/`  
Start: `Papers/README.md`

### 2) Audit — Verification archive
Located in `final_audit/`  
Start: `final_audit/README.md`

### 3) Projects 4–11 — Core research program
Start: `PROJECT_STRUCTURE.md` and each project README.

### 4) Project 12 — Validation & paper-ready outputs (Phase 1)
Located in `project_12/`  
Start:
- `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
- `project_12/docs/PAPER_DRAFT_PHASE1.md`

---

## Current status (repository-wide)
- Projects 1–3: complete, historically preserved, audit-qualified where needed
- Audit: complete, integrity-checked, final trust position documented
- Projects 4–11: complete with bounded qualifications where appropriate
- Project 12 Phase 1: complete (validated evidence bundle + paper-ready outputs)

---

## License
Custom non-commercial license. Any commercial use requires prior written permission from Mohamed Mhamdi.
