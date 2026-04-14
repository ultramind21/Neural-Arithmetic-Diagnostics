# PROJECT 8 REDESIGN V2 PLAN
## Controlled Local Error Injection

**Date:** April 2026  
**Project:** 8  
**Status:** ACTIVE REDESIGN PLAN

---

## 1. Why Redesign Is Needed

The first Project 8 experiment executed successfully but did not produce a discriminative architecture comparison.

All variants behaved identically on the tested families, which means the setup was not challenging enough to expose the role of:
- interface
- controller
- or their combination

Therefore Project 8 should continue, but under a sharper experiment design.

---

## 2. Core Redesign Principle

The new experiment should not rely on a local processor that is already too successful for the tested setup.

Instead, it should create a controlled regime in which:
- local failures exist
- they are structurally meaningful
- and interface/controller mechanisms have a real opportunity to help

---

## 3. New Core Strategy

### Controlled Local Error Injection
Introduce controlled local prediction errors into the composition process.

This allows Project 8 to ask:

> When local errors are present, can interface/controller structure prevent them from becoming global failure?

This is a much better direct test of the Project 8 question.

---

## 4. Why This Is Better

This redesign directly tests:
- local-to-global protection
rather than
- performance in a regime where nothing is failing

It therefore creates the missing discriminative environment.

---

## 5. Variants to Compare

The same four variants remain valid:

1. baseline composition
2. interface only
3. controller only
4. interface + controller

The difference is that now they will be evaluated under a controlled local-error regime.

---

## 6. Main Evaluation Question

The new question becomes:

> Which variant best prevents local errors from amplifying into family-level exact-match failure?

This is a more direct architectural test than the original v1 setup.

---

## 7. Immediate Next Step

The next implementation step is:

- `project_8/experiments/project_8_minimal_composition_architecture_v2.py`

---
