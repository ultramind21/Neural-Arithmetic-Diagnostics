# PROJECT 6 INTERPRETABILITY FRAMEWORK
## Mechanistic Interpretability Sandbox

**Date:** April 2026  
**Status:** ACTIVE FRAMEWORK  
**Relation to previous work:** New project after Project 5 checkpoint

---

## 1. Core Question

Project 6 asks:

> **Can a small arithmetic sandbox reveal where and how neural models represent carry, state transitions, and local computation structure?**

This is a mechanistic interpretability project, not a performance benchmark project.

---

## 2. Why This Project Exists

Projects 1–5 established strong behavioral findings about:
- arithmetic success
- structured failure
- adversarial robustness
- decomposition feasibility
- learned bottlenecks

What remains open is the internal side:

- where is carry represented?
- how is local state transformed?
- are there carry-selective neurons or transition-sensitive units?
- do different architectures implement arithmetic through visibly different internal structures?

Project 6 is designed to investigate these questions directly.

---

## 3. Why This Is a Good Sandbox

Arithmetic is especially suitable for mechanistic interpretability because:

- the task structure is explicit
- local state transitions are meaningful
- carry can be defined precisely
- adversarial families are already available
- earlier projects already identified behaviorally important contrasts

This makes Project 6 a controlled interpretability sandbox rather than a vague high-dimensional probe.

---

## 4. Main Project Direction

Project 6 will focus on three interpretability layers:

### Layer A — State Localization
Where is carry or carry-related information represented?

### Layer B — State Transition
How does carry-related information move across positions, layers, or computation steps?

### Layer C — Failure Linkage
Can structured failures be linked to identifiable internal representational weaknesses?

---

## 5. Initial Targets

The first targets should be small and controlled.

Recommended initial targets:
- local processors from Project 5
- simple successful vs failing family comparisons
- explicit carry-conditioned local architectures
- possibly later: comparison with broader model families

---

## 6. Initial Methods

Project 6 may use methods such as:
- activation extraction
- probing
- neuron selectivity analysis
- layerwise representation comparison
- contrastive analysis across pattern families
- simple circuit-style inspection where feasible

The project should begin with the smallest methods that can yield interpretable results.

---

## 7. Initial Comparison Logic

The first contrastive comparisons should focus on:
- successful vs failing local cases
- carry_out = 0 vs carry_out = 1
- rescued family vs unrecovered family
- structurally simple vs structurally diverse families

These are the most promising first interpretability contrasts because they are already grounded in previous behavioral results.

---

## 8. Non-Goals

Project 6 does not begin by:
- trying to interpret everything at once
- probing huge opaque systems immediately
- claiming mechanistic proof before contrastive evidence exists

It begins with:
- small contrasts
- explicit hypotheses
- interpretable local structures

---

## 9. Immediate Next Step

The first step is:

> define the first mechanistic interpretability experiment cleanly before running it

Suggested next file:
- `project_6/experiments/PROJECT_6_FIRST_EXPERIMENT_PLAN.md`

---
