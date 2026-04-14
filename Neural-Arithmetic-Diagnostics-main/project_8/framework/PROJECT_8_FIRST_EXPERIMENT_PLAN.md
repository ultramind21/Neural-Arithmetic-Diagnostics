# PROJECT 8 FIRST EXPERIMENT PLAN
## Minimal Composition Architecture Design

**Date:** April 2026  
**Project:** 8  
**Status:** ACTIVE FIRST EXPERIMENT PLAN

---

## 1. Purpose

This document defines the first bounded experiment of Project 8.

The goal is to test the simplest serious design answer to the Project 8 question:

> How can local arithmetic competence be turned into globally robust compositional behavior?

---

## 2. Phase 1 Scope

Project 8 Phase 1 is intentionally narrow.

Only two design branches are active:

### Branch A — Composition Interface
Introduce an explicit interface carrying:
- carry_in
- carry_out
- optional consistency / confidence information

### Branch D — Global Controller
Introduce a simple controller that:
- monitors sequence behavior
- detects obvious inconsistency patterns
- and can apply limited correction or override

No other branches are active in Phase 1.

---

## 3. Why This Experiment First

Projects 5–7 already established that:
- local competence can exist
- local arithmetic structure can exist
- local interventions can help selectively
- family-level failure remains heterogeneous

This means the next logical step is not another diagnostic probe, but a first controlled architecture experiment.

The first design question should therefore be:

> Is the missing ingredient mainly the composition interface, the global controller, both, or neither?

---

## 4. Variants to Compare

The first experiment should compare four conditions:

### Variant 1 — Baseline Composition
Local composition without new interface or controller

### Variant 2 — Interface Only
Local composition with explicit interface improvements

### Variant 3 — Controller Only
Local composition with a simple global controller

### Variant 4 — Interface + Controller
Local composition with both interface and controller active

---

## 5. Core Evaluation Families

The first experiment must test at least:

- `alternating_carry`
- `full_propagation_chain`
- `block_boundary_stress`

These remain the minimum family set because they are already the strongest structural contrasts in the research line.

---

## 6. Main Metric

The main metric must be:

- **exact_match per family**

This is critical.

The experiment should not rely only on:
- local accuracy
- average performance
- or one aggregated score

The key question is:
- which family improves
- which family remains broken
- and whether already-successful families are preserved

---

## 7. Positive Result Criteria

A meaningful positive result would be any of the following:

- improvement on `alternating_carry`
- improvement on `block_boundary_stress`
- preservation of `full_propagation_chain`
- broader improvement across more than one difficult family

A stronger result would be:
- family-level rescue without collateral damage

---

## 8. Negative But Valuable Result

A scientifically valuable negative result would be:

- interface alone does not help
- controller alone does not help
- or both together still fail

This would still strongly constrain the next design step.

---

## 9. Key Design Rule

The first experiment must remain minimal and interpretable.

Do not:
- add many moving parts at once
- mix in unrelated architectural ideas
- or treat this as a general optimization race

The point is to identify whether:
- interface
- controller
- both
- or neither
changes the local-to-global failure picture.

---

## 10. Immediate Next Step

The next implementation step is:

- `project_8/experiments/project_8_minimal_composition_architecture_v1.py`

---
