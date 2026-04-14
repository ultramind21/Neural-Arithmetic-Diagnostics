# PROJECT 5 REENTRY PLAN
## Decomposition Robustness Exploration

**Date:** April 2026  
**Status:** ACTIVE REENTRY PLAN

---

## 1. Current Position

Project 5 is currently:

- open
- paused
- and re-entering from a clean stopping point

### Accepted core results
1. structural decomposition with exact local oracle works
2. learned local processor shows a carry-conditioned digit bottleneck
3. simple loss reweighting does not rescue the bottleneck
4. explicit carry-conditioned representation strongly improves local behavior
5. explicit carry-conditioned representation rescues `full_propagation_chain`
6. robustness remains incomplete across all families

### Exploratory-only
- selective-failure diagnostic note
- not yet treated as a locked formal result

---

## 2. Core Research Question Now

The strongest current Project 5 question is:

> Why does explicit carry-conditioned representation rescue `full_propagation_chain` but fail to rescue `alternating_carry` and `block_boundary_stress`?

This is the correct reentry question.

---

## 3. Immediate Research Goal

The next goal is not broad expansion.
It is a focused follow-up:

- identify what structural condition still separates the rescued family from the unrecovered ones

---

## 4. Next Experiment Type

The next experiment should be a **clean follow-up diagnostic**, not a broad new architecture family.

Priority:
1. test the role of chunk size
2. test the role of local context width
3. test whether failures depend on boundary placement or pattern periodicity

---

## 5. Immediate Next Step

The first reentry experiment should be:

> **chunk-size sensitivity under the explicit carry-conditioned local processor**

This directly tests whether:
- the current failures are tied to the decomposition scale itself
- or whether they persist even when block granularity changes

---

## 6. Planned Next File

- `project_5/experiments/project_5_chunk_size_sensitivity_v1.py`

---

## 7. Interpretation Rule

No new Project 5 result should be treated as final closure.

Project 5 remains:
- exploratory
- hypothesis-driven
- and open until a later explicit closure decision

---
