# GETTING STARTED FAST
## Neural-Arithmetic-Diagnostics in 2 Minutes

If you are new to this repository, this is the fastest way to understand what it contains.

---

## What is this repository?

This repository documents a full research line on **arithmetic reasoning in neural networks**.

It contains three major layers:

1. **Projects 1–3** — the original research line  
2. **Trust-Recovery Audit** — the formal verification archive  
3. **Project 4** — a post-audit diagnostic framework for distinguishing narrow gains from broader structural robustness

---

## The main idea in one sentence

> High arithmetic accuracy alone is not enough to claim robust reasoning.

That is the central lesson of the repository.

---

## What should I read first?

### If you want the shortest possible path
1. [`README.md`](README.md)
2. [`final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md`](final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md)
3. [`project_4/results/PROJECT_4_FINAL_JUDGMENT.md`](project_4/results/PROJECT_4_FINAL_JUDGMENT.md)

### If you want the historical research story
4. [`papers/README.md`](papers/README.md)

### If you want the verification layer
5. [`final_audit/README.md`](final_audit/README.md)

### If you want the post-audit framework
6. [`project_4/README.md`](project_4/README.md)

---

## What is the strongest result here?

The strongest repository-wide message is:

- models can look strong on standard arithmetic tests
- but structured adversarial diagnostics can reveal important weaknesses
- and intervention gains do not automatically imply robust transfer

---

## What is Project 4?

Project 4 is the post-audit framework project.

Its role is to distinguish between:
- distribution-bound fit
- bounded compositional competence
- stronger algorithm-like behavior

It is a diagnostic project, not just an accuracy project.

---

## What is the audit?

The audit is the repository's trust-recovery backbone.

It rechecked the earlier projects after a model/source mismatch crisis and documented:
- what passed
- what failed
- what remained qualified
- and what could no longer be claimed strongly

---

## Where is the final verified position?

Start here:
- [`final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md`](final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md)
- [`final_audit/documentation/executive_summaries/MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md`](final_audit/documentation/executive_summaries/MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md)

---

## Final note

This repository is best understood not as a single benchmark result, but as a complete arc:

- research
- failure
- audit
- reconstruction
- and diagnostic methodology

---
