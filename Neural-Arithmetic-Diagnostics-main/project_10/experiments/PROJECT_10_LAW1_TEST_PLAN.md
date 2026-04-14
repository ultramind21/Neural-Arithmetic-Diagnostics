# PROJECT 10 LAW 1 TEST PLAN
## Testing Candidate Law 1

**Date:** April 2026  
**Project:** 10  
**Status:** ACTIVE LAW TEST PLAN

---

## Target Law

### Candidate Law 1
**Local competence is not sufficient for global robustness.**

### Current informal statement
A system may exhibit strong local arithmetic competence while still failing to produce globally robust compositional behavior.

---

## Why This Law Matters

This is one of the deepest recurring findings in the entire program.

If this law becomes strongly supported, it would help explain why:
- local arithmetic performance
- local internal structure
- and even local causal relevance

do not automatically scale into:
- family-level
- sequence-level
- or globally compositional robustness

This law is therefore foundational.

---

## Why Test It Now

Candidate Law 3 has now reached strong support.

The next strongest law candidate is Candidate Law 1, because:
- it appears repeatedly across Projects 5–9
- it links behavioral, mechanistic, and architectural layers
- and it can be tested through structured cross-project evidence

---

## What This Law Predicts

If the law is true, then:

- local competence should often coexist with global failure
- local representation quality should not guarantee family-level success
- local causal improvements should not automatically rescue global composition
- architecture support may still be required even after local competence is strong

---

## What Would Count Against the Law

The law would be weakened or falsified if we found a case where:

- local competence is clearly strong
- no additional support is introduced
- and the system still generalizes robustly at the global compositional level across difficult family conditions

That would count strongly against the law.

---

## Core Test Strategy

The first law test should compare evidence from:

- Project 5 local decomposition findings
- Project 6 local mechanistic findings
- Project 7 local-to-global bridge findings
- Project 8 architecture rescue results
- Project 9 higher-dimensional propagation findings where relevant

The key question is:
- where does local success stop being enough?

---

## Expected Evidence Types

Relevant evidence may include:

1. local arithmetic success with global family failure
2. strong local internal structure without global rescue
3. local trigger correction that helps one family but not another
4. local architecture improvement that still needs higher-level integration
5. family-sensitive rescue as evidence that local competence alone is insufficient

---

## Desired Outcome of the Test

A strong result would show:

- broad support for the claim that local competence alone is not enough
- clear cross-project convergence
- strong boundary notes
- and no trivial counterexample in the current program

A weaker or mixed result would still be useful if it narrows the law's valid scope.

---

## Immediate Next Step

The next implementation step is:

- `project_10/experiments/project_10_law1_evidence_matrix_v1.py`

This should build the first structured evidence matrix for Candidate Law 1.

---
