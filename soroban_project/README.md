# Neural-Arithmetic-Diagnostics
## When High Arithmetic Accuracy Is Not Enough

**A research repository on arithmetic reasoning in neural networks, including audited baselines, adversarial diagnostics, and a post-audit framework for distinguishing narrow gains from structural robustness.**

---

## Why this repository matters

Neural models can achieve very high arithmetic accuracy and still fail badly on structured tests.

This repository documents a full research line that moved through:

- **Projects 1–3:** original arithmetic-learning experiments  
- **A full trust-recovery audit:** to determine what was truly supported  
- **Project 4:** a diagnostic framework for separating apparent improvement from genuine robustness

### Core message
> **High arithmetic accuracy alone is not sufficient evidence of robust reasoning.**

That is the central lesson of this repository.

---

## What makes this repository different

This is not just a code dump and not just a benchmark repository.

It contains:

- a **research line** (Projects 1–3)
- a **verification archive** (Phases 1–6 audit)
- a **post-audit framework project** (Project 4)
- and a repository structure designed to preserve:
  - historical claims
  - corrected verified positions
  - and new diagnostic methodology

---

## Key result in one paragraph

Across the research line, strong arithmetic performance on standard/random tests repeatedly turned out to be insufficient for strong reasoning claims. Structured adversarial tests revealed hidden weaknesses, the audit discovered and locked important caveats, and Project 4 then built a reproducible framework for distinguishing between **distribution-bound fit**, **bounded compositional competence**, and **stronger algorithm-like behavior**. The strongest current Project 4 result is that adversarial training can improve a specifically seen adversarial family **without** producing broad held-out robustness transfer.

---

## Repository at a glance

```text
soroban_project/
├── src/               # Core executable project code
├── papers/            # Historical research line (Projects 1–3)
├── final_audit/       # Trust-recovery verification archive
├── project_4/         # Post-audit diagnostic framework
├── tests/             # Test files
├── checkpoints/       # Original checkpoints
└── README.md
```

---

## The three layers of the repository

### 1) Projects 1–3 — Historical research line
Located in:
- [`papers/`](papers/)

This is where you find the original project closures, historical findings, and research narratives.

**Start here:**  
- [`papers/README.md`](papers/README.md)

---

### 2) Audit — Verification archive
Located in:
- [`final_audit/`](final_audit/)

This is where the project's trust was rebuilt after a critical model/source mismatch problem.

It contains:
- executive summaries
- phase closure summaries
- verification scripts
- bounded reproduction outputs
- locked caveats

**Start here:**  
- [`final_audit/README.md`](final_audit/README.md)

---

### 3) Project 4 — Post-audit framework
Located in:
- [`project_4/`](project_4/)

This is the first project built after the audit from a cleaner epistemic foundation.

Its role is methodological:
- diagnose
- compare
- stress-test
- and classify arithmetic behavior more rigorously

**Start here:**  
- [`project_4/README.md`](project_4/README.md)

---

## Current project status

### Projects 1–3
- complete
- historically preserved
- audit-qualified where needed

### Audit
- complete
- integrity-checked
- final trust position documented

### Project 4
- complete at MVP level
- framework built
- stable baselines obtained
- first intervention result obtained
- blockwise branch explicitly unresolved

---

## Fastest reading path

If you want to understand the repository quickly, read:

1. [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md)
2. [`final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md`](final_audit/documentation/executive_summaries/EXECUTIVE_SUMMARY_FINAL.md)
3. [`project_4/results/PROJECT_4_FINAL_JUDGMENT.md`](project_4/results/PROJECT_4_FINAL_JUDGMENT.md)
4. [`papers/THE_FINAL_JUDGMENT.md`](papers/THE_FINAL_JUDGMENT.md)

---

## Best entry points by reader type

### If you are a research reader
Start with:
- [`papers/README.md`](papers/README.md)
- then [`final_audit/README.md`](final_audit/README.md)

### If you are a verification-minded reader
Start with:
- [`final_audit/README.md`](final_audit/README.md)
- then [`final_audit/documentation/executive_summaries/MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md`](final_audit/documentation/executive_summaries/MASTER_AUDIT_SUMMARY_PHASES_1_TO_6.md)

### If you are interested in the new diagnostic methodology
Start with:
- [`project_4/README.md`](project_4/README.md)
- [`project_4/framework/PROJECT_4_DIAGNOSTIC_FRAMEWORK.md`](project_4/framework/PROJECT_4_DIAGNOSTIC_FRAMEWORK.md)
- [`project_4/results/PROJECT_4_RESULTS_SUMMARY.md`](project_4/results/PROJECT_4_RESULTS_SUMMARY.md)

---

## Current strongest audited position

The repository now supports this carefully bounded position:

> Neural arithmetic models can appear strong on standard evaluations while remaining fragile under structured stress.  
> Diagnostic testing, explicit validation, and post-audit discipline are required before interpreting such performance as robust reasoning.

---

## Final note

This repository should be read as a complete scientific arc:

- original research
- hidden weakness
- trust crisis
- rigorous audit
- and post-audit methodological reconstruction

That full arc — not any single isolated number — is the real contribution of the repository.

---

*Status: Research line complete | Audit complete | Project 4 complete*  
*Project identity: Neural-Arithmetic-Diagnostics*
