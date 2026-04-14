# PROJECT 7 CONTEXT-TRIGGER INTERVENTION PLAN
## Targeting Recurring Local Failure Contexts

**Date:** April 2026  
**Project:** 7  
**Status:** ACTIVE EXPERIMENT PLAN

---

## 1. Purpose

This document defines the next Project 7 experiment.

Its purpose is to move from:
- identifying recurring local failure contexts

to:
- directly intervening on those contexts

The new question is:

> If the recurring local failure contexts are corrected or stabilized directly, does family-level behavior improve?

---

## 2. Why This Experiment Now

The first Project 7 result showed that the current family-level failures are not best described as uniform collapse across all positions.

Instead, they appear to involve:
- recurring
- localized
- structurally specific
local decision failures.

This makes context-trigger intervention the strongest next step.

---

## 3. Core Hypothesis

### Working hypothesis
A small number of recurring local trigger contexts may be disproportionately responsible for family-level failure.

### Prediction
If those trigger contexts are corrected, stabilized, or replaced, the family-level failure may improve substantially even without changing the entire model.

---

## 4. Initial Intervention Type

The first context-trigger intervention should remain simple and explicit.

Possible v1 intervention form:
- detect the known recurring local trigger pattern
- replace the local prediction with:
  - oracle value
  - or constrained corrected value
- leave all other positions unchanged

This provides a clean test of whether the trigger contexts are causally central.

---

## 5. Immediate Families to Target

Priority families:
- `alternating_carry`
- `block_boundary_stress`

These are the two strongest current failure families with recurring local trigger structure.

`full_propagation_chain` can remain a control family.

---

## 6. What Would Count as a Strong Result

A strong result would be any of the following:

- correcting the trigger contexts rescues family-level exact-match substantially
- partial correction produces substantial partial recovery
- different families respond differently to the same trigger intervention
- trigger correction rescues behavior more effectively than generic smoothing

Any of these would be highly informative.

---

## 7. What Would Count as a Negative But Valuable Result

A negative result would still be valuable if:
- correcting known local trigger contexts does not rescue the family
- or rescue is much smaller than expected

That would show that the trigger contexts are not sufficient by themselves, even if they are highly visible.

---

## 8. Why This Is Important

This experiment is important because it is more precise than:
- generic trajectory smoothing
- broad hidden-state intervention
- or additional descriptive probing

It tests a very sharp causal idea:
- whether family-level failure is locally trigger-driven

This is exactly the kind of bridge Project 7 should build.

---

## 9. Immediate Next Step

The next implementation step is:

- `project_7/experiments/project_7_context_trigger_intervention_v1.py`

---
