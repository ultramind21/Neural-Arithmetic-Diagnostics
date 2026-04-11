# GITHUB REPOSITORY REORGANIZATION PLAN
## Project 03 Abacus — Repository-Wide Publication Structure

**Date:** March 31, 2026  
**Purpose:** Prepare the entire repository for clean, public GitHub publication

---

## 1. Goal

This plan defines how to reorganize the repository so that it becomes:

- easier to navigate
- easier to understand for outside readers
- cleaner at the top level
- archival without being chaotic
- publication-friendly without losing research or audit history

This is a **repository-wide plan**, not a Project 4-only plan.

---

## 2. Repository Identity

The repository should present itself as a complete research line with three major layers:

### A. Research Line Foundation
Projects 1–3 and their closure documents

### B. Trust-Recovery Audit
Phases 1–6 and the verification archive

### C. Post-Audit Development
Project 4 as the first structured post-audit framework project

This allows the GitHub repository to reflect the actual intellectual history of the work.

---

## 3. Main Published Layers

The public-facing repository should clearly expose four major areas:

### 1) Core code
- `src/`
- `tests/`
- `checkpoints/`

### 2) Research narratives and historical project closures
- `papers/`

### 3) Audit archive
- `final_audit/`

### 4) Post-audit framework work
- `project_4/`

---

## 4. Top-Level Reading Path

A new visitor should be able to understand the repository in this order:

1. `README.md`
2. `PROJECT_STRUCTURE.md`
3. `papers/README.md`
4. `final_audit/README.md`
5. `project_4/README.md`

This should make the repository readable as:
- a research program
- an audited archive
- and a forward-looking framework effort

---

## 5. Folder-Level Roles

### `papers/`
Purpose:
- preserve the research narrative and closure position of Projects 1–3
- store historical final judgments and project closure documents
- remain visible as the conceptual foundation of the work

### `final_audit/`
Purpose:
- preserve the trust-recovery audit archive
- expose the final executive summaries and phase closure summaries
- keep verification code and raw outputs available but organized

### `project_4/`
Purpose:
- contain the post-audit diagnostic framework project
- separate framework work from historical audit material

### `src/`
Purpose:
- contain original core training/model code

---

## 6. Planned Structural Improvements

### 6.1 Normalize naming
Use `papers/` consistently as the canonical folder name.

Avoid mixed casing or duplicated naming conventions.

### 6.2 Add local README files
Create:
- `papers/README.md`
- `final_audit/README.md`
- `project_4/README.md`

### 6.3 Archive legacy handoff files
Create:
- `final_audit/archive_legacy_handoffs/`

Move there:
- `FILES_TO_SEND_TO_NEW_MODEL.md`
- `FORMAL_HANDOFF_FOR_NEW_MODEL.md`
- `HANDOFF_COMPLETE_CONTEXT_TO_NEW_MODEL.md`
- `HANDOFF_PACKAGE_COMPLETE.md`
- `MESSAGE_TO_NEW_MODEL.md`
- `QUICK_INDEX_FOR_NEW_MODEL.md`
- `SESSION_HANDOFF_READY.md`

These files remain useful historically, but should not dominate the public-facing audit view.

### 6.4 Group template files
Create:
- `final_audit/templates/`

Move there:
- `LOGICAL_VALIDATION_TEMPLATE.md`
- `TEMPLATE.md`
- `CROSS_CHECKS_TEMPLATE.md`
- `DATA_INTEGRITY_TEMPLATE.md`
- `DOCUMENTATION_ALIGNMENT_TEMPLATE.md`
- `REPRODUCTION_TEMPLATE.md`

### 6.5 Move optional debug/helper clutter
Create:
- `archive_optional/debug/`

Move there selected non-core helper/debug files, for example:
- `debug_alternating.py`
- `test_parser_fix.py`
- `diagnose_phase26c_timeout.py`

These may still be useful, but should not clutter the public-facing root or audit view.

---

## 7. Files That Must Remain Prominent

### Root
- `README.md`
- `PROJECT_STRUCTURE.md`
- `requirements.txt`

### papers
Must remain easy to find:
- Project 1 closure
- Project 2 closure
- Project 3 closure/index
- killer-test verdict
- final judgment / narrative documents

### final_audit
Must remain easy to find:
- executive summaries
- phase closure summaries
- master audit summary
- integrity check
- limitations note

### project_4
Must remain easy to find:
- framework
- validation protocol
- diagnostics
- baseline summaries
- intervention summaries
- closure documents

---

## 8. Public-Facing Narrative

The GitHub repository should communicate the following story:

### Layer 1 — Projects 1–3
The original research line and its major findings

### Layer 2 — Audit
A formal trust-recovery process that revalidated, corrected, or qualified earlier claims

### Layer 3 — Project 4
A post-audit methodological advance focused on diagnostic arithmetic reasoning

This is the correct narrative architecture of the repository.

---

## 9. What This Plan Avoids

This plan avoids two bad repository outcomes:

### Bad outcome A
A repository that looks like raw internal clutter with no readable front door

### Bad outcome B
A repository that over-centers Project 4 and makes Projects 1–3 look like obsolete leftovers

The actual repository should show continuity, not replacement.

---

## 10. Execution Order

### Step 1
Create local README files:
- `papers/README.md`
- `final_audit/README.md`
- `project_4/README.md`

### Step 2
Archive handoff files

### Step 3
Group templates

### Step 4
Move optional debug/helper clutter

### Step 5
Review root-level visibility and remove anything that confuses the public-facing entry point

---

## 11. Final Goal State

After reorganization, the repository should feel like:

- a serious research repository
- with a clear historical foundation
- with a rigorous audit archive
- with a clean post-audit project area
- and with minimal confusion for first-time GitHub visitors

---

## 12. Final Principle

This repository should not present itself as:
- "just a collection of experiments"

It should present itself as:
- **a coherent research line**
- **an audited scientific archive**
- **and a structured forward path after trust recovery**

---
