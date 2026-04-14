# PROGRAM PUBLICATION STRATEGY
## Neural-Arithmetic-Diagnostics (Post-Audit Program + Project 12 Validation Layer)

**Date:** April 2026  
**Purpose:** Define a publication strategy that separates (a) validated evidence bundles from (b) program-level research synthesis.

---

## TL;DR
The repository is no longer "a project"; it is a research program with multiple paper directions.  
**Project 12 Phase 1** changes the publication strategy materially: it produces a **paper-ready, validated evidence bundle** (P11 + P4) and provides a reusable validation protocol.

**Core rule:** publish coherent narratives, one question per paper, with explicit evidence boundaries.

---

## Verification
All project artifacts are tracked under `project_12/results/_hashes/p12_results_sha256.json`.
To verify infrastructure is working:
```bash
python tools/verify_platform_p0.py
python -m pytest -q
```

---

## 1) Why this document exists
The post-audit program contains:
- a diagnostic framework (Project 4),
- decomposition and failure-structure work (Project 5),
- mechanistic interpretability results (Project 6),
- local-to-global bridge findings (Project 7),
- architecture-level rescue design (Project 8),
- higher-dimensional compositional sandboxes (Project 9),
- theory-building under falsification pressure (Project 10),
- and an efficiency/sampling frontier (Project 11).

Project 12 adds a new need:
> separate "research synthesis" from "validated evidence", and publish the validated bundles first.

---

## 2) Publication principle (non-negotiable)
Do not force Projects 4–10 into one giant paper.

Instead:
- publish the strongest coherent narratives,
- keep each paper centered on one scientific question,
- explicitly state what is validated vs what is synthesis.

---

## 3) Two publication lanes (new, after Project 12)
### Lane 1 — Validation / methodology (evidence-first)
Goal: publish the validation protocol itself as a scientific contribution, using case studies.

**Already paper-ready (Phase 1):**
- Draft: `project_12/docs/PAPER_DRAFT_PHASE1.md`
- Figures/tables: `project_12/paper_assets/`
- Submission checklist: `project_12/docs/SUBMISSION_CHECKLIST_PHASE1.md`
- PDF build: `project_12/paper_build/README.md`
- Master snapshot: `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`

### Lane 2 — Domain papers (diagnostics, mechanisms, architecture, theory)
Goal: publish deeper domain-facing papers once each narrative is consolidated and (ideally) validated under Project 12 in later phases.

---

## 4) Current publication axes (updated)
### Axis V (NEW) — Validation protocol as a scientific layer
Centered on:
- Project 12 methodology (claim locking, manifests, diff gates, repro vs policy checks)
- Phase 1 validated case studies: Project 11 + Project 4

This axis is now the fastest path to a publication-safe paper.

### Axis A — Diagnostic framework & narrow vs broad robustness
Centered on:
- Project 4 (framework + baselines + intervention)
- Context from later projects as needed (but keep scope tight)

### Axis B — Mechanistic interpretability
Centered on:
- Project 6 (carry selectivity, dissociation, causal evidence)
- Selected Project 7 bridge findings (only if essential)

### Axis C — Local-to-global composition and architecture rescue
Centered on:
- Projects 5, 7, 8 (bridge heterogeneity → family-sensitive design)

### Axis D — Higher-dimensional compositional worlds
Centered on:
- Project 9 (3D sandbox, topology-sensitive structure, family-aware rescue)

### Axis E — Theory-building and rescue regime theory
Centered on:
- Project 10 (law testing under adversarial pressure → regime-space / threshold structure)

### Axis F — Efficiency frontier of structured inference
Centered on:
- Project 11 (sampling vs resolution vs retrieval cost; efficiency frontier)
Note: Phase 1 already validates key P11 claims via Project 12.

---

## 5) Recommended publication order (calibrated for April 2026)
### Paper 1 (recommended first): Project 12 Phase 1 (Validation + case studies)
Reason:
- already paper-ready and evidence-locked,
- provides a reusable methodology contribution,
- includes two strong case studies (P11 + P4),
- explicitly separates validated vs rejected-as-stated vs revised claims.

Primary pointers:
- `project_12/docs/PAPER_DRAFT_PHASE1.md`
- `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`

### Paper 2: Project 4 domain paper (diagnostic framework)
Reason:
- conceptually clean and already validated in Phase 1,
- can be written more domain-forward without spending space explaining validation machinery.

### Paper 3: Project 6 mechanistic paper
Reason:
- strongest mechanistic novelty,
- stands well as a self-contained interpretability sandbox contribution.

### Paper 4: Projects 5/7/8 (bridge + architecture)
Reason:
- high upside, but narrative must be tight (avoid "collection of results").

### Paper 5: Project 10 theory-building paper / synthesis note
Reason:
- distinctive contribution about falsification discipline and regime-space theory framing.

### Paper 6 (conditional): Project 9 higher-dimensional sandbox
Reason:
- highly original, but should be packaged when framing is sharp and validated enough for the intended venue.

---

## 6) What should be explicit in every paper package
For each paper:
- claim list (what is asserted)
- evidence pointers (where artifacts/reports live)
- validation mode used:
  - reproduction check (strict/tolerance) vs
  - policy check (stochastic interventions)
- threats to validity
- clear boundary of what is not claimed

Phase 1 already implements this discipline (see `project_12/docs/SUBMISSION_CHECKLIST_PHASE1.md`).

---

## 7) What should NOT be done
- Do not merge Projects 4–10 into one monolith.
- Do not use "grand narrative" tone without evidence pointers.
- Do not report stochastic training outcomes as exact-reproducible numeric claims.

---

## 8) Strategic position now (best statement)
The repository is now:
- a research program,
- plus a validation layer that converts parts of the program into publication-safe evidence.

Project 12 Phase 1 demonstrates that:
- some claims are robust only in mechanism-based form (P11-C07 → P11-C07R),
- adversarial training can produce narrow transfer with negative transfer (P4-C04),
- and a reproducibility-first workflow can prevent narrative drift while preserving strong discoveries.

---

## 9) Next macro-direction (after Phase 1)
- Phase 2: extend Project 12 consolidation to additional projects (5–10), project by project.
- Continue producing "validated result snapshots" and paper-ready bundles per coherent axis.
