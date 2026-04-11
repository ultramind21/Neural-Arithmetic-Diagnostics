# RESULT VALIDATION PROTOCOL
## Project 4 Execution Discipline Layer

**Date:** March 31, 2026  
**Status:** ACTIVE  
**Scope:** Project 4 experimental runs and diagnostic outputs

---

## 1. Purpose

This document defines the execution-discipline rules for Project 4.

Project 4 is not only a framework for diagnosing models; it must also diagnose
the reliability of its own reported results.

Therefore, no important Project 4 result should be treated as stable solely
because it appeared once.

---

## 2. Core Principle

> A result is not treated as stable merely because it is interesting.
> It must also satisfy minimum replay and consistency conditions.

---

## 3. Validation Levels

### Level 0 — Single Run
- one run completed successfully
- useful for debugging, prototyping, and rapid inspection
- **not sufficient** for strong result claims

### Level 1 — Repeat Check
- same configuration re-run at least once
- used to detect accidental one-off behavior

### Level 2 — Stability Check
- same configuration run across at least **3 runs**
- aggregate mean and spread recorded
- minimum requirement for reporting a result as **validated** in Project 4 MVP

### Level 3 — Extended Stability
- used only for especially important or surprising findings
- larger rerun set, or broader seed variation, or stress-repeat protocol

---

## 4. Minimum Validation Rule for Core Claims

A Project 4 result should be considered **validated** only if:

1. it is reproduced across **at least 3 runs**
2. the reporting pipeline is consistent across those runs
3. the result remains interpretable under variance
4. raw outputs are saved
5. recomputed summary values match the raw outputs at the checked level

---

## 5. Required Reporting for Validated Results

Every validated Project 4 result must report:

- configuration identifier
- number of runs
- central value (mean or equivalent)
- spread (std, range, or both)
- whether the result passed validation threshold
- location of raw outputs

---

## 6. Initial Working Stability Policy

These are **initial working rules**, not immutable scientific laws.

### For core scalar metrics
- report at least:
  - mean
  - standard deviation
  - run count

### Initial interpretation
- very low spread → stronger stability
- moderate spread → usable with qualification
- large spread → unstable, interpret cautiously

---

## 7. Failure Conditions

A result should be marked **UNSTABLE** if any of the following occur:

- repeated runs produce materially inconsistent conclusions
- parser/reporting pipeline changes the apparent result
- recomputed metrics do not match saved outputs
- result classification changes across reruns without clear explanation

---

## 8. Role of Validation in Regime Classification

Regime classification should not rely on a single unvalidated run.

At minimum:
- the core evidence used for regime assignment should satisfy **Level 2**
- borderline regime assignments should be marked explicitly as provisional if stability is weak

---

## 9. MVP Rule

For Project 4 MVP:

- exploratory runs are allowed
- but any result elevated into a conclusion, comparison, or regime claim must pass the minimum validation rule above

---

## 10. Planned Supporting Tool

A future validation utility may be added, for example:

- `validate_run_stability.py`

Its role would be:
- rerun same configuration multiple times
- aggregate outputs
- compute spread
- emit a simple stability verdict

This tool is optional at framework birth, but the protocol itself is mandatory.

---

## 11. Final Principle

Project 4 is not only about detecting model weaknesses.

It must also detect:
- weak evidence
- unstable runs
- and accidental conclusions

That is why validation is part of the framework, not an afterthought.

---

# END OF RESULT VALIDATION PROTOCOL
