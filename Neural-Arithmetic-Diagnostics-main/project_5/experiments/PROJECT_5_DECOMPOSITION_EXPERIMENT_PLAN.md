# PROJECT 5 DECOMPOSITION EXPERIMENT PLAN
## First Bounded Experiment

**Date:** April 2026  
**Project:** 5  
**Status:** ACTIVE EXPERIMENT PLAN

---

## 1. Purpose

This document defines the first bounded experiment in Project 5.

Its goal is to test a clean version of the question:

> **Does decomposition improve structural robustness in neural arithmetic?**

This first experiment is intentionally narrow and diagnostic.

---

## 2. First Variant to Test

### Variant Name
**Small-block decomposition with explicit carry interface**

### Description
The arithmetic sequence is divided into small fixed-size blocks.
Each block:
- receives a carry-in
- processes its local digits
- emits a carry-out

This is the simplest decomposition variant that still treats carry transfer explicitly.

---

## 3. Why This Variant First

This variant is chosen first because:

- it is more meaningful than naive chunking without carry transfer
- it is simpler than a full hierarchical design
- it directly tests whether carry-interface structure helps or fails
- it aligns naturally with the Project 4 block-boundary question

---

## 4. Baseline Comparison Target

The first decomposition experiment must be compared against the already established Project 4 baseline context.

Minimum comparison targets:
- Phase 30 MLP baseline artifact
- stable Project 4 baseline matrix summary
- especially block-boundary-stress behavior

The decomposition variant should not be interpreted in isolation.

---

## 5. Minimum Evaluation Families

The first experiment must test at least:

1. **alternating carry**
2. **full propagation chain**
3. **block-boundary stress**

These are the minimum structural stress families for Project 5 v1.0.

Optional:
- one in-distribution random evaluation condition

---

## 6. Main Questions

The first experiment should answer these questions:

1. Does decomposition improve any structured family at all?
2. Does it improve one family while harming another?
3. Does explicit carry interface help or merely move the failure to block boundaries?
4. Is the resulting behavior more robust, or just differently fragile?

---

## 7. Success / Failure Interpretation

### A useful result is NOT only "improvement"
This experiment is already useful if it shows any of the following:

- improvement on one family
- collapse on another family
- strong chunk-boundary sensitivity
- no meaningful gain at all
- redistribution of failure rather than reduction of failure

Any of these is scientifically informative.

### What would count as a promising signal?
A promising signal would be:
- improvement on at least one hard family
- without catastrophic collapse on the others
- especially if block-boundary stress remains stable

### What would count as a warning signal?
A warning signal would be:
- gain on local patterns
- but severe degradation once carry must cross block boundaries

---

## 8. Reporting Requirements

The experiment result must report at minimum:

- pattern-wise exact-match accuracy
- mean performance across tested families
- worst-case family performance
- explicit notes about carry-interface behavior
- explicit qualification if the experiment remains a bounded surrogate

No average alone is sufficient.

---

## 9. Non-Goals of This First Experiment

This experiment does NOT aim to:

- solve Project 5 completely
- prove that decomposition is the right long-term answer
- establish a final architectural theory
- replace full-sequence models entirely

It is only the first clean empirical probe.

---

## 10. Immediate Next Step

The next implementation step is:

> create the first bounded decomposition experiment script

Suggested filename:
- `project_5/experiments/project_5_decomposition_blockwise_v1.py`

---
