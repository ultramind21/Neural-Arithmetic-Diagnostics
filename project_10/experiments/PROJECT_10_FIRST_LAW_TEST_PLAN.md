# PROJECT 10 FIRST LAW TEST PLAN
## Testing Candidate Law 3

**Date:** April 2026  
**Project:** 10  
**Status:** ACTIVE LAW TEST PLAN

---

## Target Law

### Candidate Law 3
**Rescue Mechanisms Are Family-Sensitive Rather Than Universal**

### Current informal statement
A rescue mechanism may improve one family strongly while failing to generalize uniformly across other family types.

---

## Why This Law First

This is the strongest candidate to test first because:

1. it already has support from multiple earlier projects
2. it is narrower and more testable than some broader law candidates
3. it can be challenged directly through architecture and rescue experiments
4. if it fails, it fails clearly
5. if it survives, it becomes one of the strongest program-level laws

---

## What This Law Predicts

If the law is true, then:

- rescue mechanisms should not behave uniformly across all families
- one family may improve strongly
- another may remain unchanged
- another may worsen under the same rescue logic
- family-aware rescue should outperform naive universal rescue

---

## What Would Count Against the Law

The law would be weakened or falsified if we found:

- one rescue mechanism that works broadly and consistently across all family types
- no meaningful family differentiation under rescue
- or strong evidence that family sensitivity disappears under better design

---

## Core Test Strategy

The first law test should compare:

1. naive rescue
2. family-aware rescue
3. integrated rescue
4. any broader candidate "universal" rescue if available

across:
- multiple known family types
- and, where possible, across both linear and higher-dimensional settings

---

## Minimal Evidence to Review

The law test should use already available evidence from:
- Project 4 adversarial-training transfer limits
- Project 7 trigger-correctable vs trigger-insensitive family difference
- Project 8 family-sensitive architecture rescue
- Project 9 family-sensitive 3D rescue behavior

This means the first law test can begin as a synthesis-driven stress test, not from zero.

---

## Desired Outcome of the First Law Test

A strong outcome would be one of:

### If the law survives
- evidence from multiple projects converges on family-sensitive rescue
- universal rescue remains unsupported
- law becomes stronger

### If the law fails
- a counterexample appears
- we refine the law boundary
- the theory becomes more precise

Both outcomes are useful.

---

## Immediate Next Step

The next implementation step is:

- `project_10/experiments/project_10_law3_family_sensitive_rescue_test_v1.py`

This script should build the first explicit cross-project law test for Candidate Law 3.

---
