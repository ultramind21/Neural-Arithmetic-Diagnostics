# PROJECT 6 FIRST EXPERIMENT PLAN
## Carry Selectivity Probe

**Date:** April 2026  
**Project:** 6  
**Status:** ACTIVE EXPERIMENT PLAN

---

## 1. Purpose

This document defines the first interpretability experiment in Project 6.

The goal is to begin with the smallest meaningful mechanistic contrast already grounded in previous results.

---

## 2. First Core Question

The first interpretability question is:

> **Can we identify internal representation differences between local cases with `carry_out = 0` and local cases with `carry_out = 1`?**

This is the cleanest starting point because:
- it is simple
- it is directly tied to Project 5 findings
- it targets a known important arithmetic variable
- it does not require broad circuit claims immediately

---

## 3. Why This Experiment First

Project 5 established that:
- local carry prediction can be easy
- local digit prediction can fail in carry-conditioned ways
- explicit carry-conditioned representation can dramatically improve local behavior

This means carry is already known to be a central variable.

Project 6 should therefore begin by asking:
- whether carry is visibly encoded in internal activations
- and whether that encoding is separable, localized, or distributed

---

## 4. Initial Target Models

The first experiment should focus on small local models from Project 5, especially:

- the simple learned local processor
- the explicit carry-conditioned local processor
- optionally later: the transition-aware local architecture

The first comparison should remain local and controlled.

---

## 5. Comparison Setup

The core contrast should be:

- cases with `carry_out = 0`
vs
- cases with `carry_out = 1`

Optional secondary contrasts:
- correct vs incorrect digit prediction
- rescued-family local cases vs failing-family local cases

But the first run should stay focused on carry selectivity.

---

## 6. What to Measure

The first experiment should extract and compare:

- hidden activations from intermediate layers
- representation differences between the two carry classes
- simple separability indicators
- candidate carry-selective units if they exist

This should begin with small, interpretable statistics rather than complex tooling.

---

## 7. What Counts as a Useful Result

A useful first result could be any of the following:

- hidden activations clearly separate carry_out = 0 from carry_out = 1
- a small subset of units appears strongly carry-selective
- carry information is present but distributed
- carry information is weak or entangled with digit information

Any of these would already be informative.

---

## 8. Non-Goals

This first experiment does NOT aim to:
- prove a full arithmetic circuit
- explain every failure mode
- identify all important neurons
- complete mechanistic interpretability in one step

It is only the first contrastive probe.

---

## 9. Immediate Next Step

The next implementation step is:

- `project_6/experiments/project_6_carry_selectivity_probe_v1.py`

---
