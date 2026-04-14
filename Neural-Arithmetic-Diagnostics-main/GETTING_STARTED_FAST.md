# GETTING_STARTED_FAST
## Neural-Arithmetic-Diagnostics in ~2 Minutes

If you are new to this repository, this is the fastest way to understand what it contains and where to start.

---

## TL;DR (one paragraph)
This repository is a long research line on **arithmetic reasoning in neural networks**. A core lesson repeats across projects:

> High arithmetic accuracy alone is not sufficient evidence of robust reasoning.

Phase 1 of **Project 12** consolidates prior work into a **validated evidence bundle** (locked claims → manifests → artifacts → gates), and includes a paper-ready draft and figures.

---

## One-sentence mental model
This is a research program that studies **robustness, mechanisms, and failure structure** in neural arithmetic, and uses **Project 12** to turn results into **validated evidence**.

---

## Repository layers (how it is organized)
A practical way to think about the repo:

1) **Projects 1–3 (historical line)**  
   Early trajectory and failure discovery (stored under `Papers/`).

2) **Trust-Recovery Audit (`final_audit/`)**  
   Formal verification archive after a mismatch crisis; defines the trusted position.

3) **Projects 4–10 (post-audit core program)**  
   Diagnostics, decomposition, interpretability, local-to-global bridge, architecture design, and theory-building under adversarial pressure.

4) **Project 11 (packaged mechanism + sampling results)**  
   Reader-friendly packaged tables and evidence matrix under `project_11/packaging/`.

5) **Project 12 (validation + paper bundle, Phase 1)**  
   Converts claims into reproducible evidence (Phase 1 validates P11 + P4), and produces a paper-ready bundle (draft + figures + checklist + PDF build).

---

## Quick verification (one command)
Everything working?
```bash
python tools/verify_platform_p0.py
```

Run this first after cloning or updating.

---

## Start here (fast paths)

### Path A — "Validated evidence only" (recommended)
If you want the cleanest, most trustworthy entry:
1) `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
2) `project_12/docs/PAPER_DRAFT_PHASE1.md`
3) `project_12/docs/SUBMISSION_CHECKLIST_PHASE1.md`

Optional (PDF build instructions):
- `project_12/paper_build/README.md`

### Path B — "Project 11 packaged takeaways"
If you want the Project 11 story in packaged form:
1) `project_11/packaging/EXECUTIVE_ABSTRACT.md`
2) `project_11/packaging/PACKAGING_INDEX.md`
3) `project_11/packaging/out/EVIDENCE_MATRIX.md`
4) `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md`
5) `project_11/packaging/out/FIG_F2_SAMPLE_EFFICIENCY.md`
6) `project_11/packaging/out/FIG_F3_RATIO_KNN.md`

### Path C — "Why this matters" (high-level)
1) `WHY_THIS_PROJECT_MATTERS.md`

### Path D — "Final verification-aligned position" (audit-first)
1) `final_audit/README.md`
2) `final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md`

### Path E — "Historical research story"
1) `Papers/README.md`

---

## What is the strongest repository-wide message (Phase 1)?
A concise Phase 1 synthesis (validated in Project 12):

- Standard evaluations can look strong while structured families expose failures.
- Boundary behavior and discontinuities can dominate "who wins" near transitions (Project 11).
- Absolute numeric thresholds can be brittle under holdout-seed variation, while mechanism-based criteria can remain robust (Project 11: C07 → C07R).
- Adversarial training can yield **narrow transfer** (improvements on seen families) with **negative transfer** on held-out structure (Project 4).

For evidence-first summaries:
- `project_12/docs/VALIDATED_RESULTS_P11_PROJECT12.md`
- `project_12/docs/VALIDATED_RESULTS_P4_PROJECT12.md`

---

## Where are the paper-ready materials?
Phase 1 paper bundle:
- Draft: `project_12/docs/PAPER_DRAFT_PHASE1.md`
- Figures/tables: `project_12/paper_assets/`
- Integrity gate: `project_12/reports/PAPER_DRAFT_INTEGRITY_CHECK.md`
- Submission checklist: `project_12/docs/SUBMISSION_CHECKLIST_PHASE1.md`
- PDF build: `project_12/paper_build/README.md`

---

## If you only have 60 seconds
Read these three files:
1) `project_12/docs/VALIDATED_RESULTS_MASTER_PHASE1.md`
2) `project_12/docs/PAPER_DRAFT_PHASE1.md`
3) `project_11/packaging/EXECUTIVE_ABSTRACT.md`

---

## Final note
This repository is best understood as a complete arc:
research → hidden weakness → audit → diagnostic reconstruction → mechanism/sampling studies → **validation into evidence** (Project 12 Phase 1).

If you are evaluating claims, prefer Project 12 snapshots and reports, not narrative summaries.

