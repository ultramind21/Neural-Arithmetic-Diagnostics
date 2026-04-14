# Where we are now — Snapshot (deterministic resume)

> Goal: make project state understandable **without chat context**.
> This is an **engineering snapshot** + reproducibility contract, not a scientific "freeze".

## 1) Snapshot metadata (fill-in at update time)
- Date (UTC): 2026-04-14
- Repo (GitHub): ultramind21/Neural-Arithmetic-Diagnostics
- Branch: main
- Commit (main HEAD): 4f348418f99c9ecdfeb4b6921326e08a2c979b72
- Python: 3.12.0
- OS: Windows-11-10.0.28000-SP0

### Update instructions (1 minute)
Run from repo root:
- `git rev-parse HEAD`
- `python tools/verify_platform_p0.py`
- `python -m pytest -q`
- ledger integrity check (section 3)

Then update the metadata above.

---

## 2) The one command that defines "repo is OK"
From repo root:

```bash
python tools/verify_platform_p0.py
```

Expected:
- ends with `P0_STATUS = PASS`
- exit code `0`

Quick tests:
```bash
python -m pytest -q
```

---

## 3) Results integrity (Project 12 authority layer)
The integrity source-of-truth is the sha256 ledger:

- `project_12/results/_hashes/p12_results_sha256.json`

### Deterministic integrity check (no trust in humans)
Run this from repo root (PowerShell or bash):

```bash
python -c "import json,hashlib,os; \
LEDGER='project_12/results/_hashes/p12_results_sha256.json'; \
RESULTS_ROOT='project_12/results'; \
d=json.load(open(LEDGER,encoding='utf-8')); \
missing=[]; mismatch=[]; \
for rel,exp in d.items(): \
    p=os.path.join(RESULTS_ROOT, rel.replace('/', os.sep)); \
    if not os.path.exists(p): missing.append(rel); continue; \
    h=hashlib.sha256(open(p,'rb').read()).hexdigest(); \
    if h.lower()!=str(exp).lower(): mismatch.append(rel); \
print('LEDGER_ENTRIES=',len(d)); \
print('MISSING=',len(missing)); \
print('MISMATCH=',len(mismatch)); \
print('MISSING_SAMPLE=',missing[:20]);"
```

**Interpretation:**
- `MISMATCH=0` ⇒ no corruption / no silent edits to results.
- `MISSING=0` ⇒ results fully present (per ledger).
- If missing/mismatch appears: do **not** guess. Re-clone reference and compare.

### Reference clone rule (Windows-safe)
Do not rely on ZIP extraction for deep results paths.
Use a short-path clone as reference:

```bash
git config --global core.longpaths true
git clone https://github.com/ultramind21/Neural-Arithmetic-Diagnostics.git C:\NAD_REF
```

---

## 4) Claim authority (non-negotiable)
**Project 12 is the claim authority layer.**
- Claims are governed by Project 12 docs + manifests + artifacts + gates.
- Policy: `project_12/docs/CLAIM_AUTHORITY.md`

Anything outside Project 12 is hypothesis/narrative until validated via Project 12 evidence.

---

## 5) Current capabilities implemented (high-level)
### Tooling / Platform
- Installable package skeleton (`pyproject.toml`) with `nad/` toolkit
- CLI:
  - `nad-check-links`
  - `nad-diff-gate`
- CI (GitHub Actions):
  - ubuntu-latest + windows-latest
  - runs deterministic verify + pytest
- Security guardrails in CONTRIBUTING:
  - never embed tokens in git URLs
  - no force pushes unless explicitly approved

### Research baselines (Project 12 results exist)
Artifacts/reports are under:
- `project_12/results/`

Key families of runs include:
- Phase 2 Transformer (addition): smoke + real run
- Phase 3 addition diversification: carry-heavy vs no-carry + cross-eval
- Subtraction: MVP env/teacher + smoke artifact
- Subtraction: modes + cross-eval (no_borrow vs borrow_heavy)

(Exact runs and their metrics live in each `artifact.json` under `project_12/results/**/artifact.json`.)

---

## 6) Where to look (paths)
### Core code
- Env: `src/env/`
- Teacher: `src/teacher/`
- Models/eval: `src/models/`, `src/eval/`
- Verify runner: `tools/verify_platform_p0.py`
- Hashing tool: `tools/hash_tree.py`

### Project 12 (authority + evidence)
- Docs: `project_12/docs/`
- Manifests: `project_12/manifests/`
- Results: `project_12/results/`
- Results ledger: `project_12/results/_hashes/p12_results_sha256.json`

---

## 7) How to resume work safely (workflow)
1) Create a clean branch from main:
   - `git checkout main && git pull`
   - `git checkout -b <new-branch>`
2) Before any "results" commit:
   - commit code first
   - then generate artifacts/results so `artifact.git_commit == code commit`
3) Update hash ledgers after results changes:
   - `python tools/hash_tree.py project_12/results > project_12/results/_hashes/p12_results_sha256.json`
4) PR only, no direct pushes to main (recommended once branch protections are enabled).

---

## 8) Known constraints (important)
- This is **not** a scientific freeze/release:
  - no signed tags/commits requirement
  - dependency locking is "stronger" but not perfect for torch/CUDA variants
- Windows path length can drop files silently when using ZIP/extract.
  - prefer `git clone` under a short path (e.g., `C:\NAD_REF`)

---

## 9) "If something looks missing" rule
Do not trust narratives. Trust only:
- `tools/verify_platform_p0.py` (PASS/FAIL)
- `pytest` result
- ledger integrity check (missing/mismatch)
- reference clone comparison
