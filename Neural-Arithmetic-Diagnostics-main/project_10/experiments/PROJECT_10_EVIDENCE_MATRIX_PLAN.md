# PROJECT 10 EVIDENCE MATRIX PLAN
## Structured Law Testing Backbone

**Date:** April 2026  
**Project:** 10  
**Status:** ACTIVE EVIDENCE PLAN

---

## 1. Purpose

This document defines the evidence-matrix structure that will support all later law testing in Project 10.

The purpose is to replace:
- loose summary-language matching

with:
- structured evidence evaluation

---

## 2. Core Principle

A candidate law should not be judged from narrative text alone.

It should be judged through a matrix that records:

1. what result exists
2. whether that result is relevant
3. whether it supports, weakens, or leaves the law undecided
4. whether it defines a boundary
5. whether it could count as a falsifier

This creates a much stronger theory-testing discipline.

---

## 3. Matrix Row Structure

Each row in the matrix should represent one evidence item.

Each row should contain at least:

- project name
- result identifier
- short result statement
- candidate law relevance
- evidence role:
  - support
  - partial support
  - no evidence
  - boundary
  - contradiction
  - falsification candidate
- confidence note
- short interpretation note

---

## 4. Matrix Column Logic

### Required Columns

1. `project`
2. `result_id`
3. `result_title`
4. `candidate_law`
5. `evidence_role`
6. `confidence_level`
7. `boundary_note`
8. `falsification_relevance`
9. `comments`

---

## 5. Evidence Role Definitions

### support
The result directly supports the candidate law.

### partial_support
The result supports the candidate law, but only under limited interpretation.

### no_evidence
The result does not meaningfully bear on the law.

### boundary
The result helps define where the law stops or becomes more qualified.

### contradiction
The result pushes against the law but is not yet strong enough to count as a direct falsifier.

### falsification_candidate
The result is of the kind that could genuinely falsify the law if confirmed cleanly.

---

## 6. Why This Is Better

This matrix approach is stronger because it prevents:

- casual wording from being mistaken for theory
- ambiguous support from being treated as strong support
- unrelated results from being overused
- and weak law tests from looking stronger than they are

This is exactly the discipline Project 10 needs.

---

## 7. Immediate Next Step

The next implementation step is:

- `project_10/experiments/project_10_law3_evidence_matrix_v1.py`

This file should build the first structured matrix for Candidate Law 3.

---
