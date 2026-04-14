# PROJECT 10 PHASE DIAGRAM REFINEMENT PLAN V1
## Sharpening Regions and Transition Bands

**Date:** April 2026  
**Project:** 10  
**Status:** ACTIVE PHASE-DIAGRAM REFINEMENT PLAN

---

## 1. Purpose

This document defines the first refinement plan for the current phase-diagram-style theory in Project 10.

The purpose is to sharpen the current coarse region map and make the transition bands more precise.

This is not a request for blind grid expansion.

It is a targeted refinement plan.

---

## 2. Why Refinement Is Needed

The current phase diagram already identifies:

- a family-aware advantage region
- a boundary / transition region
- a universal dominance region

It also includes first approximate transition bands.

However, these boundaries are still coarse.

To strengthen the theory, Project 10 now needs to ask:

> how sharp are these transitions, and where exactly do the region boundaries lie?

This is the refinement goal.

---

## 3. Main Refinement Targets

### Target A — Heterogeneity boundary
Current estimate:
- between **0.006**
and
- **0.0075**
at baseline universal power

This is the first heterogeneity transition band.

### Target B — Universal-power boundary
Current estimate:
- between **0.32**
and
- **0.34**
at medium/high heterogeneity

This is the first power transition band.

These are the two highest-priority refinement targets.

---

## 4. Refinement Strategy

The first refinement pass should:

- test additional points inside the current transition bands
- compare whether verdict changes are abrupt or gradual
- preserve simple interpretation
- and avoid expanding into a full dense grid before local threshold structure is understood

This is boundary-focused sharpening.

---

## 5. What the Refinement Should Clarify

The refinement should help answer:

1. does the heterogeneity transition behave sharply or smoothly?
2. does the universal-power transition behave sharply or smoothly?
3. are medium and high heterogeneity governed by the same power threshold?
4. is the current boundary region narrow or extended?

These are the key current questions.

---

## 6. Immediate Next Step

The next implementation step is:

- `project_10/experiments/project_10_phase_diagram_refinement_v1.py`

This script should probe the current transition bands more densely than the earlier threshold refinement pass.

---
