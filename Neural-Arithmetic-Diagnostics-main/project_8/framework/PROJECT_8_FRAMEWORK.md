# PROJECT 8 FRAMEWORK
## Composition Stabilization Architectures

**Date:** April 2026  
**Status:** ACTIVE FRAMEWORK  
**Relation to previous work:** New project after Projects 5–7

---

## 1. Core Question

Project 8 asks:

> How can local arithmetic competence be turned into globally robust compositional behavior?

This is now the central design question of the research line.

---

## 2. Why This Project Exists

Project 5 showed that:
- decomposition can work in principle
- but learned local decomposition can fail selectively

Project 6 showed that:
- meaningful internal arithmetic structure exists
- some internal signals are causally important
- but local mechanistic structure alone does not solve the full problem

Project 7 showed that:
- local-to-global failure is not mechanistically uniform
- some family-level failures are trigger-correctable
- others are not

Project 8 begins where these findings converge:
- local competence exists
- but robust composition still fails
- therefore the next step is explicit architecture/interface design

---

## 3. Main Project Goal

The goal of Project 8 is not to produce another diagnostic only.

It is to design and test architectures or interfaces that can:
- preserve local arithmetic competence
- maintain global consistency
- and reduce family-level compositional failure

Project 8 is therefore the first major design-oriented project built on the post-audit and post-interpretability foundation.

---

## 4. Main Strategic Direction

Project 8 will begin conservatively.

### Phase 1 focus
Only two branches are active at the start:

#### Branch A — Composition Interface
Explicit interface carrying:
- carry_in
- carry_out
- optional confidence / consistency information

#### Branch D — Global Controller
A simple controller that:
- monitors sequence behavior
- detects obvious inconsistency
- and can apply limited correction or override

No other branches are active in Phase 1.

---

## 5. Why This Controlled Start Matters

We do not want to mix all possible solutions at once.

The first experiment should isolate the question:

> Is the missing ingredient mainly the composition interface, the global controller, both, or neither?

This keeps the project scientifically interpretable.

---

## 6. Core Evaluation Families

Project 8 should begin using the same minimum family set that proved most diagnostic in Projects 5–7:

- alternating_carry
- full_propagation_chain
- block_boundary_stress

These are the minimum required families.

---

## 7. Main Evaluation Rule

The first design-stage experiment must report:

- exact_match per family
- direct comparison across variants
- no average-only reporting

The key question is:
- which family improves
- which family remains broken
- and whether successful families are preserved

---

## 8. Immediate Next Step

The next step is not coding everything at once.

The next step is:

- `project_8/framework/PROJECT_8_FIRST_EXPERIMENT_PLAN.md`

This file should define the first bounded experiment clearly before implementation begins.

---
