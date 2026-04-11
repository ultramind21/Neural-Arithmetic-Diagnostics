# PROJECT 7 FIRST EXPERIMENT PLAN
## Stepwise Composition Trace Experiment

**Date:** April 2026  
**Project:** 7  
**Status:** ACTIVE EXPERIMENT PLAN

---

## 1. Purpose

This document defines the first experiment in Project 7.

The purpose of this experiment is to trace, step by step, how local arithmetic competence does or does not translate into successful global composition.

---

## 2. Core Question

The experiment asks:

> At what point does local arithmetic competence fail to scale into global sequence success?

This is the first direct bridge experiment in Project 7.

---

## 3. Why This Experiment First

Project 5 and Project 6 already established:

- local arithmetic competence can become strong
- internal arithmetic structure can be meaningful
- family-level failure can still remain
- and simple explanations have already been ruled out

The next step must therefore directly observe the local-to-global transition itself.

That is why this experiment should be first.

---

## 4. Main Design

The experiment should execute arithmetic composition step by step and log, at each position:

- local input
- local carry-in
- predicted digit
- predicted carry
- hidden-state summary
- correctness of the local step
- cumulative state of the sequence so far

This creates a compositional trace rather than only a final score.

---

## 5. Families to Compare

The first bridge experiment should compare at least:

- `full_propagation_chain`
- `alternating_carry`
- `block_boundary_stress`

These three families are the minimum because they already define the strongest Project 5 and 6 contrast set.

---

## 6. What to Look For

The experiment should ask:

1. Does the first error appear early or late?
2. Does one wrong local step trigger a chain of later failures?
3. Does hidden-state behavior change before the first visible arithmetic mistake?
4. Do successful and failing families differ in how quickly local errors accumulate?
5. Does the model remain locally accurate for several steps before composition collapses?

---

## 7. Why This Is Important

This experiment is critical because it tests the central Project 7 hypothesis:

- perhaps the true gap is not local arithmetic competence itself
- but the transition from local competence to stable composition over time

This would provide a direct bridge between:
- Project 5 decomposition findings
- and Project 6 interpretability findings

---

## 8. Non-Goals

This experiment does NOT aim to:
- solve the whole project in one run
- provide a full mechanistic theory immediately
- replace later causal interventions

Its role is narrower:
- identify where local-to-global breakdown actually begins

---

## 9. Immediate Next Step

The next implementation step is:

- `project_7/experiments/project_7_stepwise_composition_trace_v1.py`

---
