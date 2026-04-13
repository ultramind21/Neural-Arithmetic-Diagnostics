# CHECKPOINT — Formal Project Documentation (Sprint P1 Closure Report)

**Date:** 2026-04-13  
**Repository:** ultramind21/Neural-Arithmetic-Diagnostics  
**Default Branch:** main (origin/HEAD → origin/main)  
**System Philosophy:** Evidence-first engineering. Project 12 = Claim Authority Layer.  
**Authority Policy:** `project_12/docs/CLAIM_AUTHORITY.md`

---

## Executive Summary

Sprint P1 ("Repro Hardening + Docs + CI matrix") is **CLOSED**. All objectives met:
- ✅ Multi-platform CI (Ubuntu + Windows) passing
- ✅ Requirements ledger (`requirements.lock.txt`)
- ✅ Hash-based authority integrity ledgers
- ✅ Reproducibility documentation
- ✅ Windows encoding fixes (emoji → ASCII)
- ✅ PR #1 merged to main

**Merge Evidence:**
- Merge commit: `089464d71b99034c32e4790295cc3fe970f0392a`
- Timestamp: 2026-04-13 20:58:32 UTC
- CI result on main: **SUCCESS** (both Ubuntu + Windows jobs)

---

## Completed Work by Sprint

### P0 (Stability Fixes)
**Status:** ✅ Merged to main  
**Objective:** Fix critical bugs in `src/` without breaking validation.

**Changes:**
- `src/env/soroban_env.py`: Added unknown action guard → illegal + terminate.
- `src/env/encode.py`: Made observation encoding shape-agnostic (no fixed feature count).
- `src/teacher/dataset_gen.py`: Changed silent skipping to fail-fast on dataset errors.
- Docstring alignment for observation shapes.

**Key commit:**
- `8473f19` — P0: guard unknown actions, shape-agnostic observations, fail-fast dataset

---

### Platform P0 (Packaging + One-Command Verify)
**Status:** ✅ Merged to main  
**Objective:** Convert repository into a runnable toolkit without touching research layer.

**Deliverables:**
1. **Packaging infrastructure:**
   - `pyproject.toml` for package distribution
   - `nad/` package with CLIs: `nad-check-links`, `nad-diff-gate`

2. **Testing framework:**
   - `pytest.ini` restricting discovery to `tests/`, ignoring `archive_optional/`
   - `tests/test_pytest_smoke.py` pytest wrappers for legacy tests

3. **Documentation:**
   - `CONTRIBUTING.md` with developer guidelines
   - `project_12/docs/CLAIM_AUTHORITY.md` authority policy

4. **Continuous integration:**
   - `.github/workflows/ci.yml` with multi-platform matrix (Ubuntu + Windows)
   - `tools/verify_platform_p0.py` — One-command verification script

5. **Versioning:**
   - Tag `platform-p0-2026-04-11` (snapshot at commit `8c9c07d`)

**Platform P0 integration:** Merged to main via earlier merge commits (chronologically documented).

---

### Sprint P1 (Reproducibility Hardening + Docs + CI Matrix)
**Status:** ✅ Merged to main (PR #1)  
**Objective:** Elevate reproducibility from engineering best-practice to documented + verifiable standard.

#### 1.1 Dependency Ledger
- **File:** `requirements.lock.txt`
- **Generated from:** Clean venv using `requirements.txt`
- **Purpose:** Audit trail of dependencies at freeze moment
- **Limitation:** Not universal cross-OS/CUDA guarantee (especially Torch); Python version + platform-specific

#### 1.2 Authority Ledgers (Hash-Based Integrity)
- **Files:**
  - `project_12/results/_hashes/p12_docs_sha256.json` — Hash tree of `project_12/docs/`
  - `project_12/results/_hashes/p12_results_sha256.json` — Hash tree of `project_12/results/`
- **Generator:** `tools/hash_tree.py` (SHA256 tree hash)
- **Self-exclusion:** Hash ledgers ignore `_hashes/` directory to prevent self-reference

#### 1.3 Report Generation
- **Script:** `tools/verify_platform_p0.py`
- **Output (gitignored):**
  - `tools/verify_reports/pip_freeze.txt` — Environment snapshot
  - `tools/verify_reports/platform_p0_report.json` — Gate results (compile, tests, links, diff-gate)
- **Gitignore rationale:** Prevent churn; reports are ephemeral verification artifacts

#### 1.4 CI Architecture Upgrade
- **From:** Single-platform (implicit Ubuntu) runs
- **To:** Matrix CI targeting:
  - `ubuntu-latest`
  - `windows-latest`
- **Pipeline steps:**
  - Install dependencies
  - Python compilation (`compileall` on `src/`, `nad/`)
  - PyTest smoke gate
  - Legacy integration test execution
  - CLI sniff tests (`nad-check-links`, `nad-diff-gate`)
  - `tools/verify_platform_p0.py` full gate
  - Large file guard (≤20MB per file)
  - **Windows fix:** Large file check uses `shell: bash` to work on Windows runners

#### 1.5 Documentation
- **File:** `docs/REPRODUCIBILITY.md`
  - Comprehensive reproducibility guide
  - Lists what IS reproducible (engineering reproducibility)
  - Lists what is NOT (scientific reproducibility awaiting full freeze)
  - Links to `project_12/docs/CLAIM_AUTHORITY.md`

- **Updated:** `README.md`, `CONTRIBUTING.md` with reproducibility references

#### 1.6 Windows CI Fix (Emoji Encoding)
**Root cause:** Windows PowerShell uses cp1252 encoding; emoji `✅` (U+2705) cannot be encoded.

**Affected files:**
- `tests/test_env.py` — 10 emoji instances
- `tests/test_rules.py` — 12 emoji instances
- `tests/test_teacher.py` — 4 emoji instances

**Fix:** Replace all `✅` with ASCII `[OK]` for cross-platform compatibility.

**Commits (P1):**
- `1eed548` — Fix emoji in test_env.py
- `f84b341` — Fix emoji in test_rules.py
- `2c73b1e` — Fix emoji in test_teacher.py

#### 1.7 PR Merge
- **PR #1:** "Merge pull request #1 from ultramind21/sprint-p1-repro-hardening"
- **Merge-to:** `main` branch
- **Merge commit:** `089464d71b99034c32e4790295cc3fe970f0392a`
- **Merged at:** 2026-04-13 20:58:32 UTC
- **Merged by:** ultramind21
- **Post-merge CI:** ✅ **SUCCESS** (both Windows + Ubuntu jobs)
- **Branch deleted:** `sprint-p1-repro-hardening` (as expected)

---

## Verification (How to Check Status)

### Quick smoke test (30 seconds)
```bash
python tools/verify_platform_p0.py
```

### Run pytest only
```bash
python -m pytest -q
```

### Regenerate authority ledgers
```bash
python tools/hash_tree.py project_12/docs > project_12/results/_hashes/p12_docs_sha256.json
python tools/hash_tree.py project_12/results > project_12/results/_hashes/p12_results_sha256.json
```

### Check CI history
```bash
gh run list --repo ultramind21/Neural-Arithmetic-Diagnostics --workflow ci --branch main --limit 5
```

---

## What Is NOT "Scientifically Frozen" Yet?

Important distinction:
- **Current state:** Engineering reproducibility + CI determinism + ledger audit trail
- **NOT included:**
  - Dependency hash lock with verified hashes (pip-tools `--generate-hashes` or `uv lock`)
  - Signed commits/tags (GPG)
  - Branch protection rules enforced
  - Official release tag (e.g., v0.1.0) with signed release notes
  - Cross-platform CUDA/hardware certification

These are in **Sprint P2** scope.

---

## Important Operational Notes

1. **`requirements.lock.txt` semantics:**
   - Records exact versions from clean environment build
   - Useful for audit and historical reference
   - NOT a guarantee of bit-identical reproducibility across OS/hardware/GPU
   - Torch especially is hardware-sensitive

2. **`tools/verify_reports/` is gitignored:**
   - By design—reports are ephemeral verification outputs
   - Prevents report churn from cluttering git history
   - Can be regenerated anytime via `verify_platform_p0.py`

3. **Temporary files purged:**
   - Removed untracked debug files multiple times (e.g., `project_tree.py` artifacts, `replace_emoji.py` workarounds)
   - Protocol: No scripts/artifacts left behind after completion

---

## Project 12 Authority Layer

**Policy file:** `project_12/docs/CLAIM_AUTHORITY.md`  
**Core principle:** Any claim marked "publishable" must pass through Project 12 gates:
- Authorship chain (git history)
- Artifact integrity (hash ledgers)
- Reproducibility gates (verify script)
- CI certification (GitHub Actions)

---

## Roadmap: Sprint P2 (Next)

**Objective:** Elevate reproducibility from engineering ledger to cryptographically locked state + governance.

**Scope:**
1. **Dependency hash lock:**
   - Option A: `pip-tools` → `requirements.lock.txt` with `--generate-hashes`
   - Option B: `uv lock` (modern, faster)
   - Goal: Verify download integrity + prevent supply-chain tampering

2. **Branch protections:**
   - Require CI checks on pull requests
   - Block direct pushes to main
   - Require pull request reviews (minimum 1)

3. **Release engineering:**
   - Tag `v0.1.0-alpha` (or `v0.1.0`) on current main
   - Write CHANGELOG.md summarizing P0 + P1
   - Optionally: GitHub release with artifacts

4. **(Future) Multi-platform CI:**
   - Add macOS runner to matrix
   - Test Apple Silicon compatibility

---

## Operational Protocol (for Future Agent Sessions)

- **Minimal diffs:** Any change must be explained with `git diff` + gate evidence
- **No temp scripts inside repo:** Workarounds must be external or deleted after use
- **No snippet execution as primary tool:** Caused commit misdirection in past iterations
- **Evidence before merge:** Always provide GitHub Actions run IDs or `gh` command output

---

## Timeline (Key Timestamps)

| Date/Time (UTC) | Event |
|----------------------|-------|
| 2026-04-11 T16:52 | Platform P0 merged to main (commit 5bb5b4d) |
| 2026-04-11 T00:00+ | P1 work: hashes, ledgers, docs, CI matrix |
| 2026-04-13 T18:00+ | Windows emoji fixes (3 commits: 1eed548, f84b341, 2c73b1e) |
| 2026-04-13 T20:24 | PR #1 CI triggered (test_teacher.py emoji fix commit 2c73b1e) |
| 2026-04-13 T20:25 | PR #1 CI completed: Windows + Ubuntu both SUCCESS |
| 2026-04-13 T20:58:32 | PR #1 merged to main (merge commit 089464d) |
| 2026-04-13 T20:58:35 | Post-merge CI on main triggered and completed: SUCCESS |

---

## References

- **Authority policy:** [project_12/docs/CLAIM_AUTHORITY.md](../project_12/docs/CLAIM_AUTHORITY.md)
- **Reproducibility guide:** [docs/REPRODUCIBILITY.md](../docs/REPRODUCIBILITY.md)
- **Contributing guide:** [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Verify script:** [tools/verify_platform_p0.py](../tools/verify_platform_p0.py)
- **Hash generator:** [tools/hash_tree.py](../tools/hash_tree.py)
- **CI workflow:** [.github/workflows/ci.yml](../.github/workflows/ci.yml)

---

**Document Status:** Final (Sprint P1 Closure)  
**Author/Generated:** Arena AI Agent (2026-04-13)  
**Next Review:** Sprint P2 kickoff
