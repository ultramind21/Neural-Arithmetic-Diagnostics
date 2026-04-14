# PROJECT 5 EXPLORATION FRAMEWORK
## Decomposition Robustness Exploration

**Date:** April 2026  
**Status:** ACTIVE EXPLORATION  
**Relation to previous work:** Post-Project-4 exploratory branch

---

## 1. Core Question

Project 5 asks a focused structural question:

> **Does decomposition improve structural robustness in neural arithmetic?**

More specifically:
- if arithmetic inputs are decomposed into smaller units or blocks,
- and local computation is combined through some carry-transfer logic,
- does the resulting system become more robust under structured stress?

---

## 2. Why This Is a New Project

Project 4 already closed with:
- a diagnostic framework
- a stable baseline matrix
- a stable first intervention signal
- and an unresolved first blockwise branch

That unresolved blockwise branch suggested that decomposition may be important, but it did not produce a clean accepted scientific result.

Project 5 therefore starts fresh as a new exploration project rather than re-opening Project 4.

---

## 3. Main Hypothesis

### Working hypothesis
Some forms of decomposition may improve structural robustness by reducing global processing burden and localizing computation.

### Counter-hypothesis
Decomposition may merely relocate the problem:
- from full-sequence processing
to
- carry-interface failure across chunks

Project 5 is designed to distinguish between these possibilities.

---

## 4. Exploration Philosophy

Project 5 is not initially an optimization race.

Its first goal is diagnostic exploration:
- detect whether decomposition yields any real robustness signal
- identify which decomposition variants fail immediately
- identify whether chunk boundaries are the main weakness

Only after that should stronger claims or larger-scale experiments be considered.

---

## 5. Initial Variants to Explore

### Variant A — Digit-wise decomposition
Treat each position as a local unit, with explicit carry transfer.

### Variant B — Small-block decomposition
Use small chunk sizes (e.g. 2, 3, 5 digits) with carry passed across blocks.

### Variant C — Interface-aware chunking
Chunked processing with explicit carry-in / carry-out interface between blocks.

### Variant D — Hierarchical decomposition
Two-level processing:
- local chunk computation
- higher-level recomposition

---

## 6. Core Evaluation Families

Project 5 should begin by testing decomposition variants against the same structured families that proved diagnostic in Project 4:

- alternating carry
- full propagation chain
- block-boundary stress

These should be treated as the minimum structural test suite.

---

## 7. Key Diagnostic Goal

The first and most important thing to determine is:

- does decomposition improve only one family?
- does it worsen another family?
- does chunk-boundary handling become the dominant failure mode?
- or is there any sign of broader structural gain?

---

## 8. Immediate Success Criterion

Project 5 does not require a complete new model.

A successful early Project 5 outcome may simply be:

- a clean decomposition experiment
- with interpretable results
- showing whether decomposition helps, hurts, or redistributes failure

That alone would already be useful research progress.

---

## 9. First Planned Outputs

Initial outputs should include:

- a decomposition exploration plan
- one bounded decomposition experiment script
- one first result summary
- clear documentation of what is and is not concluded

---

## 10. Immediate Next Step

The next step is:

> define the first bounded decomposition experiment cleanly before running it

No execution should happen before that first experiment design is explicitly written.

---
