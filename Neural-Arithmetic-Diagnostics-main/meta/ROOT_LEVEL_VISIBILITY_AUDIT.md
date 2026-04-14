# ROOT LEVEL VISIBILITY AUDIT
## Neural-Arithmetic-Diagnostics

**Date:** April 2026  
**Purpose:** Decide which root-level files should remain visible, be moved, or be archived

---

## 1. Goal

The root of the repository should remain readable and attractive.

It should expose only the files that are most useful for:
- first-time visitors
- scientific orientation
- navigation
- and repository identity

Not every useful file should remain root-visible.

---

## 2. Root-Level Files to Keep Visible (Current Recommendation)

These files should remain prominently visible at root:

### Core public-facing files
- `README.md`
- `GETTING_STARTED_FAST.md`
- `WHY_THIS_PROJECT_MATTERS.md`
- `PROJECT_STRUCTURE.md`
- `requirements.txt`
- `LICENSE`

### Strategic visibility files
- `STRATEGIC_RESEARCH_MAP.md`

These files together provide:
- identity
- fast entry
- motivation
- navigation
- legal clarity
- and strategic overview

---

## 3. Root-Level Files to Move into a Meta / Docs Layer

The following files are useful, but too process-oriented to remain root-prominent forever:

- `GITHUB_REPOSITORY_REORGANIZATION_PLAN.md`
- `REPOSITORY_NAMING_AND_PRESENTATION_PLAN.md`
- `REPOSITORY_REORGANIZATION_EXECUTION_CHECKLIST.md`
- `REPOSITORY_VISUAL_ASSET_PLAN.md`
- `PHASE2_REPOSITORY_CLEANUP_PLAN.md`

These should likely move into a future folder such as:
- `meta/`
or
- `docs/repository_governance/`

---

## 4. Root-Level Files to Review for Archive

These files should be reviewed carefully and may be moved to archive or secondary visibility:

- `START_HERE.md`
- `FINAL_DELIVERABLES_OFFICIAL.md`
- `PRE_REORGANIZATION_AUDIT_CHECKLIST.md`
- `POST_REORGANIZATION_VERIFICATION_CHECKLIST.md`
- `REORGANIZATION_PLAN.md`
- `_FOR_MODEL_CONTEXT_FULL_SESSION.md`

These are not necessarily unimportant, but they are unlikely to be the best first-facing entry points for GitHub visitors.

---

## 5. Root-Level Files Likely Not Meant for Public Front Visibility

These should likely move out of root if not needed there:

- `generate_diagram.py`
- `project_tree.py`
- `neural_arithmetic_diagnostics.md`
- `unnamed.png`

They may still be useful, but they weaken the clarity of the top-level presentation.

---

## 6. Immediate Classification Rule

At root level, a file should remain visible only if it satisfies at least one of:

1. first-visit orientation
2. core project identity
3. essential repository navigation
4. legally or operationally essential visibility
5. strong strategic summary value

If it is mainly:
- transitional
- technical
- archival
- or process-governance focused

it should usually move out of root.

---

## 7. Immediate Next Step

The next step is:

> decide the destination folder for process/meta/governance files, then execute the first root-level file move batch

---
