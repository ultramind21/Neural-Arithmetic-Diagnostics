# REPOSITORY REORGANIZATION EXECUTION CHECKLIST
## Project 03 Abacus

**Date:** March 31, 2026  
**Purpose:** Track execution of the GitHub publication cleanup plan

---

## 1. Goal

This checklist turns the repository reorganization plan into an executable step-by-step process.

Use it to ensure that:
- no important file is lost
- no structural change is forgotten
- no public-facing confusion remains in the final GitHub version

---

## 2. Directory Creation

### Create archive / organization folders
- [ ] `final_audit/archive_legacy_handoffs/`
- [ ] `final_audit/templates/`
- [ ] `archive_optional/`
- [ ] `archive_optional/debug/`

---

## 3. README Layer

### Confirm public-facing README files exist
- [x] `papers/README.md`
- [x] `final_audit/README.md`
- [x] `project_4/README.md`

### Root visibility files
- [ ] review root `README.md`
- [ ] review `PROJECT_STRUCTURE.md`
- [ ] ensure top-level entry path is clear for GitHub visitors

---

## 4. Handoff Archive Moves

Move legacy handoff files into:
- `final_audit/archive_legacy_handoffs/`

Files:
- [ ] `FILES_TO_SEND_TO_NEW_MODEL.md`
- [ ] `FORMAL_HANDOFF_FOR_NEW_MODEL.md`
- [ ] `HANDOFF_COMPLETE_CONTEXT_TO_NEW_MODEL.md`
- [ ] `HANDOFF_PACKAGE_COMPLETE.md`
- [ ] `MESSAGE_TO_NEW_MODEL.md`
- [ ] `QUICK_INDEX_FOR_NEW_MODEL.md`
- [ ] `SESSION_HANDOFF_READY.md`

---

## 5. Template Grouping

Move template files into:
- `final_audit/templates/`

Files:
- [ ] `LOGICAL_VALIDATION_TEMPLATE.md`
- [ ] `TEMPLATE.md`
- [ ] `CROSS_CHECKS_TEMPLATE.md`
- [ ] `DATA_INTEGRITY_TEMPLATE.md`
- [ ] `DOCUMENTATION_ALIGNMENT_TEMPLATE.md`
- [ ] `REPRODUCTION_TEMPLATE.md`

---

## 6. Debug / Helper Cleanup

Move optional helper/debug files into:
- `archive_optional/debug/`

Candidate files:
- [ ] `debug_alternating.py`
- [ ] `test_parser_fix.py`
- [ ] `diagnose_phase26c_timeout.py`

Optional review candidates:
- [ ] `killer_test_carry_followup.py`
- [ ] `killer_test_test4_frequency.py`

---

## 7. Folder Naming Consistency

### Papers naming
- [ ] confirm canonical use of `papers/`
- [ ] ensure no parallel naming confusion remains

---

## 8. Public-Facing Visibility Review

### `papers/`
- [ ] key closure docs remain visible
- [ ] historical documents are still discoverable
- [ ] folder does not look like an unsorted dump

### `final_audit/`
- [ ] executive summaries easy to find
- [ ] phase summaries easy to find
- [ ] code_audit remains accessible but not confusing
- [ ] limitations note easy to find

### `project_4/`
- [ ] framework easy to find
- [ ] diagnostics easy to find
- [ ] validation easy to find
- [ ] baseline/intervention/results path understandable

---

## 9. GitHub Readability Check

Before publication, confirm:
- [ ] a new visitor can understand the repository from the root
- [ ] a research reader can find Projects 1–3
- [ ] an audit reader can find the final verification position
- [ ] a technical reader can find Project 4 framework and outputs
- [ ] legacy transition material no longer dominates the first impression

---

## 10. Final Publication Readiness Gate

Repository should be considered GitHub-ready only if:
- [ ] structure matches the reorganization plan
- [ ] all major README files are in place
- [ ] legacy clutter is archived
- [ ] official summaries are easy to find
- [ ] no critical file path confusion remains

---

## 11. Final Note

This checklist is not a scientific result document.

It is a repository-governance tool used to make sure the public GitHub version
reflects the actual quality and maturity of the work already completed.

---
