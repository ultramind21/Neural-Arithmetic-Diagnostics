# PROJECT 4 RESULTS SUMMARY
## Diagnostic Arithmetic Reasoning — MVP Synthesis

**Date:** March 31, 2026  
**Project:** 4  
**Status:** MVP SYNTHESIS ACTIVE

---

## 1. Purpose

This document synthesizes the main results obtained so far in Project 4.

It combines:

- the Project 4 framework position
- the stable baseline matrix
- the first stable intervention signal
- and the current blockwise status

The purpose is not to overstate final theory, but to define the strongest
current Project 4 position that is actually supported by the evidence.

---

## 2. Framework Position

Project 4 was designed to move beyond raw arithmetic accuracy and toward a
diagnostic distinction between:

1. **distribution-bound fit**
2. **bounded compositional competence**
3. **stronger algorithm-like behavior**

The project's role is therefore diagnostic, not merely benchmark-optimizing.

---

## 3. Stable Baseline Matrix

### Stable baseline status
The following baseline families now have repeated-run stability under the current bounded Project 4 path:

- **MLP** → STABLE
- **LSTM** → STABLE
- **Transformer** → STABLE

This means the baseline patterns below are stable empirical signals, not one-off runs.

---

### Baseline matrix summary

| Dimension | MLP | LSTM | Transformer |
|----------|-----|------|-------------|
| Validation status | STABLE | STABLE | STABLE |
| In-distribution exact-match | low | low | low |
| Alternating carry | collapse | collapse | collapse |
| Full propagation chain | collapse | collapse | collapse |
| Block-boundary stress | success | collapse | success |

---

### Baseline interpretation
The current baseline matrix supports the following:

- all three baseline families remain weak in exact-match terms under the current bounded path
- all three fail on some structured adversarial conditions
- the strongest current architecture-dependent split appears on:
  - `block_boundary_stress`
- under this pattern:
  - **MLP succeeds**
  - **Transformer succeeds**
  - **LSTM fails**

This is the clearest stable cross-model diagnostic difference currently available.

---

## 4. First MVP Intervention: Adversarial Training

### Intervention result status
**PASS WITH QUALIFICATIONS**

### What was observed
The first adversarial-training intervention produced a stable result pattern:

- strong gain on a **seen adversarial family**
- no meaningful gain on another difficult family
- failure on a **held-out adversarial family**

### What this supports
This supports the following bounded interpretation:

> adversarial training can improve performance on specifically seen structured families, but this does not automatically translate into broad structural robustness.

In other words:
- the intervention produced a real effect
- but the effect is currently more consistent with **narrow transfer** than with generalized robustness

This is one of the most important current findings of Project 4.

---

## 5. Blockwise Decomposition Status

A first blockwise decomposition attempt was executed, but the implementation path drifted away from the originally intended experimental semantics during debugging.

Therefore:

- the first blockwise result is **not accepted** as part of the Project 4 scientific core
- it is recorded as:
  - **INCOMPLETE / METHODOLOGICALLY UNRESOLVED**

This means blockwise decomposition remains an open extension path, not an accepted Project 4 result at this stage.

---

## 6. What Project 4 Has Already Established

Even before any further extension, Project 4 has already established:

### A. A working diagnostic framework
Project 4 now has a concrete framework for measuring:
- in-distribution accuracy
- structured adversarial robustness
- length behavior
- rounding sensitivity
- carry corruption sensitivity

### B. A stable baseline comparison matrix
The project can now compare multiple architectures under one framework with actual repeated-run stability.

### C. A stable intervention signal
The project has already shown that:
- intervention gains can be family-specific
- and that "improvement" must be tested against held-out structured families

This is scientifically meaningful.

---

## 7. Current Strongest Supported Project 4 Statement

The most defensible current statement is:

> Project 4 has successfully built a diagnostic arithmetic reasoning framework and used it to obtain both a stable baseline matrix and a stable first intervention signal.
>
> The baseline matrix reveals a meaningful architecture-dependent difference on block-boundary stress, while the first intervention result shows that adversarial training can improve a seen adversarial family without yielding broad robustness transfer.

This is the current strongest supported synthesis.

---

## 8. What Project 4 Does NOT Yet Claim

Project 4 does **not** yet claim:

- that any tested model has reached Regime 3
- that adversarial training produces robust general arithmetic reasoning
- that the blockwise intervention has succeeded or failed scientifically
- that all framework dimensions are already fully mature
- that final Project 4 closure has been reached

---

## 9. Current Strategic Position

The current best strategic position is:

### GO WITH MVP CONSOLIDATION

This means:
- the project already has a meaningful MVP contribution
- the current baseline + intervention evidence is worth consolidating
- unresolved blockwise work should not contaminate the accepted MVP narrative

---

## 10. Recommended Next Step

The next step should be one of the following:

### Preferred next step
Prepare the formal closure-facing Project 4 documents:
- closure summary
- executive summary
- quick reference

### Optional later extension
Return later to blockwise decomposition only after redesigning its semantics cleanly.

---

## 11. Formal Status

**Project 4 status:** MVP-level synthesis established  
**Current best decision:** GO WITH MVP CONSOLIDATION  
**Strongest stable signal:** architecture-dependent block-boundary split + narrow adversarial-training transfer

---
