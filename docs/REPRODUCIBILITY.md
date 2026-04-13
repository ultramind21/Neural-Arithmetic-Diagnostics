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
