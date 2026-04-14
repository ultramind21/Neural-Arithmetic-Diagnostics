# PROJECT 6 SUBSPACE INTERVENTION PLAN
## Moving Beyond Single-Unit Interpretability

**Date:** April 2026  
**Project:** 6  
**Status:** ACTIVE EXPERIMENT PLAN

---

## 1. Purpose

This document defines the next major branch inside Project 6.

The goal is to move from:
- single-unit interpretability
to
- subspace-level causal analysis

The core question is:

> Are the important arithmetic signals better captured by internal subspaces or directions than by individual units alone?

---

## 2. Why This Branch Now

Project 6 already established:

- carry-related representation exists
- successful and failing cases are internally separable
- some units matter causally
- digit and carry can be dissociated
- family-level differences are real
- simple trajectory interventions are not sufficient

This means the project has likely reached the limit of purely unit-centric interpretation.

A stronger next step is to ask whether the relevant internal structure is actually distributed over meaningful low-dimensional subspaces.

---

## 3. Core Hypothesis

### Working hypothesis
The current arithmetic mechanisms may be represented not only in individual units, but in low-dimensional internal directions or subspaces.

### Expected value
If this is true, subspace interventions may:
- explain behavior more cleanly than unit ablations
- reveal structure missed by unit-level probes
- and offer a stronger causal language for arithmetic representation

---

## 4. First Type of Subspace Test

The first subspace branch should remain simple.

Initial candidates:
- principal directions separating carry classes
- principal directions separating success vs failure
- top linear discriminative directions between digit and carry conditions

The goal is not yet maximal sophistication, but a clean first proof of concept.

---

## 5. Why This Matters

Unit-level probes already gave meaningful signals.
But if the true mechanism is distributed, then:
- zero overlap at the unit level may still miss deeper geometric overlap
- family-level effects may depend on direction-level structure
- and local arithmetic competence may be encoded in ways that are better understood geometrically than neuron-by-neuron

This branch tests exactly that.

---

## 6. What a Useful Result Would Be

A useful result could be any of the following:

- a low-dimensional direction cleanly separates carry classes
- a different direction separates success vs failure
- subspace perturbation has clearer behavioral effects than unit ablation
- unit-level and subspace-level stories partially agree or diverge in informative ways

Any of these would be valuable.

---

## 7. Immediate Next Step

The next implementation step is:

- `project_6/experiments/project_6_subspace_probe_v1.py`

---
