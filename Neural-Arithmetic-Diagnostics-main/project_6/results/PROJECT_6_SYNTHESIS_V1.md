# PROJECT 6 SYNTHESIS V1
## Mechanistic Interpretability Sandbox — Current Scientific Position

**Date:** April 2026  
**Project:** 6  
**Status:** ACTIVE SYNTHESIS  
**Scope:** interim synthesis, not final closure

---

## 1. Purpose

This document records the first strong synthesis point of Project 6.

Project 6 was launched to investigate a simple but important internal question:

> Where and how is arithmetic-relevant information represented inside the model?

The project has now accumulated enough accepted probes to support a coherent mechanistic narrative.

---

## 2. The Current Probe Arc

Project 6 currently contains five accepted interpretability probes.

### Probe 1 — Carry Selectivity
The first probe showed that carry-related information is measurably represented in hidden activations, and that the carry-conditioned local architecture exhibits stronger carry selectivity than the simpler local baseline.

This established the first internal signal.

### Probe 2 — Success vs Failure Contrast
The second probe showed that successful and failing local arithmetic cases are strongly distinguishable in hidden activation space.

This established that internal structure tracks behavioral correctness.

### Probe 3 — Top Unit Ablation
The third probe showed that ablating top diagnostic units substantially degrades digit/exact performance while leaving carry performance unchanged.

This provided the first strong causal-style signal that at least some of the identified units are functionally important.

### Probe 4 — Family-Level Link
The fourth probe showed that the same internal units vary meaningfully across higher-level arithmetic family conditions.

This established the first bridge between:
- local internal structure
- and family-level arithmetic behavior

### Probe 5 — Digit-vs-Carry Dissociation
The fifth probe showed a complete dissociation between the top units most relevant to digit-related success and those most relevant to carry-related internal selectivity.

This is the strongest current internal specialization result.

---

## 3. What Project 6 Has Now Established

Taken together, the current probes establish the following:

1. carry-related information is represented internally
2. success and failure are internally distinguishable
3. some units are not merely correlated with performance but functionally important under ablation
4. local internal structure links meaningfully to higher-level family behavior
5. digit-related and carry-related signals can be sharply dissociated at the top-unit level

This is already a strong mechanistic profile.

---

## 4. The Emerging Mechanistic Story

Project 6 now supports a coherent intermediate interpretability story.

The strongest current version of that story is:

> arithmetic-relevant information inside the model is structured rather than diffuse in a meaningless way.

More specifically:
- carry information is represented
- behaviorally successful and failing cases occupy distinguishable internal regions
- some units matter causally for digit-related local performance
- and top digit-relevant units are dissociated from top carry-relevant units

This does not yet amount to a full arithmetic circuit explanation.
But it is already much stronger than simply saying that "the model has interesting hidden states."

---

## 5. Why This Matters

The importance of Project 6 is that it moves the research line one step beyond behavioral diagnostics.

Projects 4 and 5 established:
- where the models fail
- where interventions help
- and where structural bottlenecks remain

Project 6 now begins to explain how some of these behavioral distinctions appear internally.

This is scientifically valuable because it creates a bridge between:
- robustness analysis
and
- mechanistic interpretation

That bridge is often missing in empirical work.

---

## 6. What This Does NOT Yet Establish

Project 6 still does not establish:

- a full arithmetic circuit
- a complete causal account of all family-level failures
- a proof that the identified units are sufficient to explain all behavior
- a global decomposition of the entire model into solved functional submodules
- final closure of the interpretability question

These remain open.

---

## 7. Strongest Current Scientific Position

The strongest current Project 6 position is:

> the arithmetic sandbox now supports a real mechanistic interpretability program: carry-sensitive internal structure exists, successful and failing local cases are internally separable, some units are causally important for digit behavior, and digit-vs-carry functional specialization is visible at the top-unit level.

This is a substantial result.

---

## 8. Why This Is More Than a Probe Collection

The five probes are not just isolated diagnostics.

They form a structured sequence:

1. identify a representational signal
2. connect it to behavioral correctness
3. test causal importance
4. relate it to family-level behavior
5. test internal functional specialization

That sequence gives Project 6 a real arc rather than a pile of exploratory artifacts.

---

## 9. What the Sandbox Has Proven

The sandbox has already proven that:
- mechanistic analysis is tractable here
- meaningful internal contrasts can be extracted
- perturbation-based tests can reveal functionally important units
- the project is not limited to black-box behavioral interpretation alone

This justifies the sandbox framing itself.

---

## 10. Most Meaningful Next Step

The next meaningful step should now ask:

> How do the dissociated digit-relevant and carry-relevant units contribute to family-level failures and successes?

This is the natural next frontier because it would tighten the bridge between:
- unit-level internal structure
and
- family-level arithmetic behavior

That is the strongest next question available.

---

## 11. Current Status

**Project 6 status:** active  
**Synthesis level:** strong interim synthesis  
**Closure status:** not yet closed  
**Main contribution so far:** a coherent mechanistic bridge from carry selectivity to behavioral contrast, causal relevance, family-level linkage, and digit-vs-carry specialization

---
