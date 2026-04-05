# GETTING STARTED FAST
## Neural-Arithmetic-Diagnostics in 2 Minutes

If you are new to this repository, this is the fastest way to understand what it contains.

---

## What is this repository?

This repository documents a full research line on **arithmetic reasoning in neural networks**.

It now contains four main layers:

1. **Projects 1–3** — the original research line  
2. **Trust-Recovery Audit** — the formal verification archive  
3. **Project 4** — the post-audit diagnostic framework  
4. **Projects 5–7** — advanced research branches on decomposition, mechanistic interpretability, and local-to-global failure

---

## The main idea in one sentence

> High arithmetic accuracy alone is not enough to justify strong claims about robust reasoning.

That is the central lesson of the repository.

---

## What should I read first?

### If you want the shortest possible path
1. [`README.md`](README.md)
2. [`WHY_THIS_PROJECT_MATTERS.md`](WHY_THIS_PROJECT_MATTERS.md)
3. [`STRATEGIC_RESEARCH_MAP.md`](STRATEGIC_RESEARCH_MAP.md)

### If you want the final verification-aligned position
4. [`final_audit/README.md`](final_audit/README.md)
5. [`final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md`](final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md)

### If you want the historical research story
6. [`papers/README.md`](papers/README.md)

### If you want the post-audit framework
7. [`project_4/README.md`](project_4/README.md)

### If you want the strongest current mechanistic branch
8. [`project_6/results/PROJECT_6_SYNTHESIS_FINAL.md`](project_6/results/PROJECT_6_SYNTHESIS_FINAL.md)

### If you want the strongest current local-to-global bridge branch
9. [`project_7/results/PROJECT_7_SYNTHESIS_V1.md`](project_7/results/PROJECT_7_SYNTHESIS_V1.md)

---

## What is the strongest result here?

The strongest repository-wide message is:

- models can look strong on standard arithmetic tests
- but structured adversarial diagnostics can reveal important weaknesses
- local competence does not automatically scale into global compositional robustness
- and internal arithmetic structure can be real without yielding a simple one-mechanism explanation of all failures

---

## What is the audit?

The audit is the repository's trust-recovery backbone.

It rechecked the earlier projects after a model/source mismatch crisis and documented:
- what passed
- what failed
- what remained qualified
- and what could no longer be claimed strongly

---

## What is Project 4?

Project 4 is the first post-audit framework project.

Its role is to distinguish between:
- distribution-bound fit
- bounded compositional competence
- stronger algorithm-like behavior

It is a diagnostic project, not just an accuracy project.

---

## What came after Project 4?

### Project 5
- decomposition robustness exploration
- asks why local competence may fail to scale globally

### Project 6
- mechanistic interpretability sandbox
- asks where arithmetic-relevant internal structure lives

### Project 7
- local-to-global failure bridge
- asks why different families fail through different mechanisms

---

## Where is the final verified position?

Start here:
- [`final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md`](final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md)
- [`final_audit/documentation/executive_summaries/MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md`](final_audit/documentation/executive_summaries/MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md)

---

## Final note

This repository is best understood not as a single benchmark result, but as a complete arc:

- research
- hidden weakness
- audit
- diagnostic reconstruction
- decomposition analysis
- mechanistic interpretability
- and local-to-global bridge discovery

---