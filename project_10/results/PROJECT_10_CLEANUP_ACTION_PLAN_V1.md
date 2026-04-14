# PROJECT 10 CLEANUP ACTION PLAN V1
## Execution Sequence for Curated Cleanup

**Date:** April 2026  
**Project:** 10  
**Status:** ACTIVE CLEANUP ACTION PLAN

---

## 1. Purpose

This document converts the cleanup classification into a concrete action sequence.

The goal is to execute cleanup safely and in a controlled order.

The cleanup should preserve:
- scientific integrity
- canonical visibility
- and historical recoverability where needed

---

## 2. Execution Principle

Cleanup should proceed in this order:

1. create destination folders
2. move superseded files
3. move unreviewed agent outputs
4. move tools/archive files
5. review delete candidate one final time
6. delete only if still confirmed unnecessary

This order minimizes risk.

---

## 3. Step 1 — Create Destination Folders

The following folders should be created first:

- `project_10/results/superseded/`
- `project_10/results/unreviewed_agent_outputs/`
- `project_10/tools/`

No files should move before these folders exist.

---

## 4. Step 2 — Move Superseded Files

Move the following into:
- `project_10/results/superseded/`

Files:
- `PROJECT_10_SYNTHESIS_V1.md`
- `PROJECT_10_PHASE_2_SYNTHESIS_V1.md`
- `PROJECT_10_PRESENTATION_SUMMARY_V1.md`

These remain useful historically but should leave the canonical results surface.

---

## 5. Step 3 — Move Unreviewed Agent Outputs

Move the following into:
- `project_10/results/unreviewed_agent_outputs/`

Files:
- `PROJECT_10_ADVERSARIAL_FALSIFICATION_COMPLETE.md`
- `PROJECT_10_ADVERSARIAL_FALSIFICATION_PHASE_STATUS.md`
- `PROJECT_10_HIGHER_ORDER_CANDIDATE_STATUS_UPDATE_REGIME_B.md`
- `PROJECT_10_REGIME_B_V1_RESULTS.md`
- `PROJECT_10_REGIME_C_V1_RESULTS.md`

These should remain preserved, but clearly marked as non-canonical.

---

## 6. Step 4 — Move Utility Files

Move the following into:
- `project_10/tools/`

Files:
- `generate_diagram.py`
- `merge_files.py`
- `project_tree.py`

These should not remain in the main Project 10 surface.

---

## 7. Step 5 — Final Review of Delete Candidate

The following file should be reviewed once more before deletion:

- `neural_arithmetic_diagnosticss.md`

If confirmed to be:
- a local merged dump
- a redundant artifact
- or not part of the scientific/project-facing surface

then it can be deleted.

If not confirmed, it should be moved to an archive location instead.

---

## 8. Step 6 — Post-Cleanup Verification

After all moves are complete, Project 10 should be checked to confirm:

1. canonical core files remain visible
2. superseded files are no longer in the main results surface
3. unreviewed outputs are separated
4. tools are separated
5. no canonical experiment/result was accidentally removed

This verification is required.

---

## 9. Immediate Next Step

The next step is:

- execute Step 1 only

No moves or deletions should happen before the destination folders are created and confirmed.

---
