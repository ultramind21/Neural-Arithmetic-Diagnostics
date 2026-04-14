# PROJECT 9 FIRST SANDBOX PLAN
## Small 3D Arithmetic Lattice Sandbox

**Date:** April 2026  
**Project:** 9  
**Status:** ACTIVE SANDBOX PLAN

---

## 1. Purpose

This document defines the first actual sandbox to be implemented in Project 9.

The goal is to create a higher-dimensional compositional environment that is:
- small
- controlled
- arithmetic-like
- and scientifically useful

---

## 2. Why a Small 3D Sandbox First

The first Project 9 sandbox must be small enough to remain interpretable.

We do not want:
- a giant high-dimensional world immediately
- or a visually impressive but analytically vague simulation

Instead, the first sandbox should be:
- simple enough to inspect
- rich enough to create local-to-global interaction
- and clear enough to support later diagnosis and intervention

---

## 3. Proposed First Structure

### Working shape
A small 3D lattice, for example:
- `2 × 2 × 2`
or
- `3 × 2 × 2`

This provides:
- local adjacency
- multiple directions of interaction
- non-linear composition pathways
- enough structure for global cascades without becoming too large

---

## 4. State Concept

Each cell in the lattice should carry a small arithmetic-like state.

At minimum, the local state may include:
- digit-like value
- carry-like value
- or a small bounded state tuple

The exact representation should remain simple in v1.

---

## 5. Local Update Logic

The first sandbox must define:
- how local cells interact
- how carry-like information passes
- how updates propagate
- and how local changes create global effects

The key design requirement is:

> local rules must be simple, but their global consequences must be nontrivial

---

## 6. Core Scientific Value

The sandbox should allow us to test a new class of question:

> Does local competence still fail to scale when composition is no longer confined to a linear sequence?

This is the central reason for Project 9.

---

## 7. First Evaluation Themes

The first sandbox should support at least these analyses:

1. local correctness
2. global consistency
3. propagation/cascade behavior
4. failure concentration
5. effect of local perturbation on global structure

This keeps continuity with Projects 5–8 while genuinely expanding the compositional world.

---

## 8. Design Rule

The first sandbox should remain:
- small
- legible
- controlled
- and explainable

Its first goal is not maximum complexity.
Its first goal is to create the **minimal higher-dimensional world** that can generate interesting local-to-global arithmetic behavior.

---

## 9. Immediate Next Step

The next step is:

- `project_9/experiments/project_9_small_3d_lattice_v1.py`

This will implement the first controlled sandbox.

---