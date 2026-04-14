# Reproducibility (Engineering Milestones)

This repository is a research-oriented codebase with an **evidence-first** workflow.
Passing checks means: *the engineering milestone is reproducible under the recorded setup*.
It does **not** automatically mean "scientific freeze" or "published claim".

## What is tracked
- `requirements.txt`: minimal direct dependencies (loose ranges).
- `requirements.lock.txt`: a **ledger** generated from a clean virtualenv created from `requirements.txt`.
  - Purpose: audit trail ("what was installed") for reproducibility checks.
  - Non-goal: universal cross-OS/CUDA installer.

## One-command verification (Platform P0)
Run:
```bash
python tools/verify_platform_p0.py
```

This performs:
1) compile checks (`src/` + `nad/`)
2) pytest smoke gate (wrappers under `tests/`)
3) legacy direct tests:
   - `python tests/test_env.py`
   - `python tests/test_rules.py`
   - `python tests/test_teacher.py`
4) link validation for Project 12 docs:
   - `nad-check-links project_12/docs`
5) diff gate self-test (JSON canonicalization)

## Verification reports (local, not committed)
`tools/verify_platform_p0.py` writes local outputs into:
- `tools/verify_reports/pip_freeze.txt`
- `tools/verify_reports/platform_p0_report.json`

These are intentionally **gitignored** to avoid churn.
If you need an audit attachment, copy them to a separate location and attach to an issue/PR.

## Hash ledgers (Project 12 authority layer)
We track sha256 ledgers for the claim authority layer:
- `project_12/results/_hashes/p12_docs_sha256.json`
- `project_12/results/_hashes/p12_results_sha256.json`

Generate/update:
```bash
python tools/hash_tree.py project_12/docs > project_12/results/_hashes/p12_docs_sha256.json
python tools/hash_tree.py project_12/results > project_12/results/_hashes/p12_results_sha256.json
```

`tools/hash_tree.py` intentionally skips `_hashes/` to avoid self-referential hashes.

## CI
CI runs the deterministic verify on:
- ubuntu-latest
- windows-latest

## What "freeze" would require (future)
To reach stronger release-grade reproducibility:
- dependency lock with hashes (pip-tools/uv)
- branch protection + required CI checks
- signed tags/commits (optional)
- formal release tag (e.g., `v0.1.0`)

---

## Integrity checklist (2026-04-14)
To verify ledger and artifact integrity without trusting automated reporting:

### 1) Verify ledger file hash (local vs reference)
```powershell
python -c "import hashlib, pathlib; 
p=pathlib.Path('project_12/results/_hashes/p12_results_sha256.json'); 
print('LOCAL_SHA256=', hashlib.sha256(p.read_bytes()).hexdigest())"

# Compare with reference clone or GitHub binary
```

### 2) Check for missing/corrupted files in results
```powershell
python -c "import json,hashlib,os; 
ledger=json.load(open('project_12/results/_hashes/p12_results_sha256.json',encoding='utf-8')); 
results_root='project_12/results'; 
missing=[]; mismatch=[]; 
for rel,exp in ledger.items():
    p=os.path.join(results_root, rel.replace('/', os.sep))
    if not os.path.exists(p): missing.append(rel); continue
    h=hashlib.sha256(open(p,'rb').read()).hexdigest()
    if h.lower()!=str(exp).lower(): mismatch.append(rel)
print('MISSING=',len(missing))
print('MISMATCH=',len(mismatch))"
```

**Expected:** `MISSING=0, MISMATCH=0`

### 3) Verify all artifacts are tracked in ledger
```powershell
python -c "import os,json,glob; 
ledger=json.load(open('project_12/results/_hashes/p12_results_sha256.json',encoding='utf-8')); 
results_root='project_12/results'; 
arts=glob.glob(os.path.join(results_root,'**','artifact.json'), recursive=True); 
bad=[]; 
for ap in arts: 
  rel=os.path.relpath(ap, results_root).replace(os.sep,'/'); 
  if rel not in ledger: bad.append(rel)
print('ARTIFACT_COUNT=',len(arts))
print('ARTIFACT_NOT_IN_LEDGER=',len(bad))"
```

**Expected:** `ARTIFACT_NOT_IN_LEDGER=0`

All three checks passing = all results integrity verified.

