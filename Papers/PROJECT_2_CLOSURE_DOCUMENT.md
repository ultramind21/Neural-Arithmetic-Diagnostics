# PROJECT 2 CLOSURE DOCUMENT
## Audit-Aligned Final Position

---

## Introduction

Project 2 was launched as a follow-up to Project 1 to test whether explicitly constrained state representations might improve arithmetic generalization.

The specific tested idea was to impose finite-state-style bottlenecks and compare their behavior against a less constrained baseline. The purpose of this document is to preserve the most defensible audit-aligned interpretation of that project after Phase 3 audit.

**Audit qualification (March 31, 2026):**  
Phase 3 audit identified a critical comparability issue in:

- `src/train/phase_27c_architecture_audit.py`

Specifically:
- cross-architecture test-pair distribution was biased
- same-trial comparisons were not methodologically clean
- bounded official reproduction remained incomplete

This caveat must remain locked into any use of Project 2 comparative conclusions.

---

## Project 2 Scope

Within its audited scope, Project 2 should be understood as:

- a test of a specific family of constrained-state variants
- under a setup later found to carry a cross-architecture comparability caveat
- with semantics and metric logic independently verified
- but without clean architecture-to-architecture fairness at the held-out pair level

This means Project 2 remains informative, but not fully clean as a comparative benchmark.

---

## What the Audit Actually Established

### Phase 3 audit outcome
For `phase_27c_architecture_audit.py`, the audit established:

- **3A:** PASS
- **3B:** **FAIL / BIASED**
- **3C:** PASS
- **3D:** PASS
- **3E:** **INCOMPLETE / TIMEOUT**

### What this means
The audit supports the following:
- source/setup is transparent enough for audit
- target semantics are correct
- metric logic is correct

But it also established that:
- architecture comparisons are not methodologically clean at the split level
- bounded official reproduction was not completed

---

## Audit-Aligned Interpretation of Project 2

The most defensible Project 2 position is:

> The tested FSM-style constrained variants did not provide audit-clean evidence of improvement over the baseline in the audited Project 2 setup.

This is narrower and more defensible than claiming:
- that the constraints definitively worsen arithmetic generalization in all relevant senses
- or that the baseline-vs-FSM gap is conclusively controlled

---

## Historical Comparative Results (With Locked Caveat)

Historical reported Project 2 values indicated approximately:

- baseline near the upper ~60s
- constrained FSM-style variants near the low ~50s

However, these values must be interpreted under the locked Phase 3 caveat:

> the compared architectures did not receive identical same-trial held-out test-pair sets

Therefore, these historical comparative numbers may still be cited as **reported values**, but not as a fully clean architecture-to-architecture comparison.

---

## What Project 2 Defensibly Supports

The following claims remain defensible in audit-aligned form:

### 1. The tested FSM-style variants did not show audited evidence of benefit
Under the audited Project 2 setup, the constrained variants did not produce a cleanly established improvement over the baseline.

### 2. The comparison remains qualified, not clean
Because of the Phase 3 shuffle-order bias, the relative ranking between architectures must remain caveated.

### 3. The negative outcome still has value
Even with the caveat, Project 2 remains useful because it does **not** provide encouraging evidence that this specific constrained-state approach solved the generalization problem under the tested setup.

---

## What Project 2 Does NOT Defensibly Prove

Project 2 should **not** be used to claim:

- that all explicit state constraints are ineffective
- that FSM-style ideas are inherently harmful
- that the exact magnitude of the baseline-vs-FSM gap is conclusively established
- that a specific internal failure mechanism has been proven
- that this project alone settles the future of structured-state approaches

---

## Why Project 2 Is Considered Closed

Project 2 is considered closed because its central tested idea has been explored far enough to support a stable negative-or-non-supportive result, but with explicit audit qualification.

### Closure basis
1. the source/setup was audited
2. semantics were verified
3. metrics were verified
4. a critical comparability caveat was discovered and locked
5. no audit-clean evidence of improvement emerged from the tested constrained variants

This is sufficient to close Project 2 in its audited form.

---

## Final Project 2 Position

The most defensible final position is:

> Project 2 did not produce audit-clean evidence that the tested FSM-style state constraints improve arithmetic generalization.
>
> Historical reported results were consistent with weaker performance for the constrained variants, but the architecture comparison carries a permanent Phase 3 comparability caveat due to biased test-pair distribution.

This is the correct audited use of Project 2.

---

## Locked Phase 3 Caveat

Any future use of Project 2 results should retain this qualification:

> Project 2 architecture comparisons were conducted under a setup later shown to have biased cross-architecture test-pair distribution. Therefore, relative architecture performance should be treated as suggestive rather than as a fully controlled comparison.

---

## Recommended Use Going Forward

Project 2 should be cited as:
- an audit-qualified negative result
- showing no clean evidence of benefit for the tested FSM-style approach
- without overgeneralizing to all constrained-state or hybrid methods

Any future exploration of explicit state or memory mechanisms should be treated as a new project.

---

## Formal Closure

**Status:** CLOSED — AUDIT-QUALIFIED  
**Audit Qualification Date:** March 31, 2026  
**Project 2 Position:** no audit-clean evidence of benefit for the tested FSM-style variants

---

## Appendix: Phase 3 Audit Anchor

### Audit target
- `src/train/phase_27c_architecture_audit.py`

### Locked Phase 3 result
- architecture comparability bias at the held-out pair level
- semantics verified
- metrics verified
- bounded reproduction incomplete

This appendix is included only to anchor Project 2 closure in the audited record.

---