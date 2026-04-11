# PROJECT 10 REGIME A V2 SPEC
## Symmetric Forced Universal Rescue Regime

**Date:** April 2026  
**Project:** 10  
**Status:** ACTIVE REGIME V2 SPEC

---

## 1. Why V2 Exists

Regime A V1 was informative, but not yet clean enough as an adversarial falsification test.

The main issue was:
- universal rescue and family-aware rescue were not defined symmetrically enough

This means the result could still be influenced by the regime design itself rather than by the deeper theory question.

Regime A V2 exists to correct that.

---

## 2. Core Goal

Regime A V2 should test the same core question as V1:

> can a universal rescue succeed when multiple nominal families share a more aligned underlying failure structure?

But it must do so under a cleaner comparison.

---

## 3. Design Principle

In V2:

- universal rescue and family-aware rescue should start from the same base gain logic
- neither should receive an arbitrary built-in advantage
- differences should arise only from how each rescue interacts with the regime structure

This is the central design correction.

---

## 4. Required Symmetry

The following should be symmetric across rescue types:

- base gain scale
- access to shared failure factor
- performance floor and ceiling logic

The following may differ legitimately:

- whether rescue responds only to shared structure
- whether rescue can also respond to residual family-specific structure

That difference is the real scientific variable.

---

## 5. Construction Requirement

The regime should still preserve:

- strong local competence
- multiple nominal families
- weak/failing global robustness
- partially aligned deeper failure structure

But now the residual family-specific structure should be handled in a way that does not automatically hard-code the outcome.

---

## 6. What Counts as a Stronger Test

V2 becomes a stronger test if:

- universal rescue is genuinely given a fair chance
- family-aware rescue only wins when residual structure truly matters
- near-ties are possible
- universal wins are possible
- family-aware wins are possible

This makes the regime scientifically meaningful.

---

## 7. What Would Count Against the Higher-Order Candidate

Any of the following in V2 would weaken the higher-order candidate:

- universal rescue broadly matches or exceeds family-aware rescue
- universal rescue wins across most aligned families
- family-specific adaptation no longer matters materially once the deeper structure is aligned

---

## 8. What Would Count in Favor of the Higher-Order Candidate

Any of the following in V2 would support the higher-order candidate:

- family-aware rescue still clearly outperforms universal rescue
- residual family-specific structure remains causally important
- aligned deep structure is still insufficient to make universal rescue broadly competitive

---

## 9. Immediate Next Step

The next implementation step is:

- `project_10/experiments/project_10_regime_a_forced_universal_rescue_v2.py`

This file should implement the symmetric V2 version of Regime A.

---
