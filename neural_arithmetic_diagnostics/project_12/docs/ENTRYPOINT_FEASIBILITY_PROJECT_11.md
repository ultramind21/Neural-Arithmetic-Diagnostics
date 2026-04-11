# ENTRYPOINT_FEASIBILITY_PROJECT_11

**Purpose:** Analyze the internal structure of Project 11 experiment scripts to determine the optimal strategy for creating Project 12 entrypoints with minimal modifications.

**Date:** 2026-04-11  
**Analysis scope:** 3 core reproduction scripts from Project 11

---

## PHASE D: Resolution Sweep Extended

**File:** `project_11/experiments/phase_d_resolution_sweep_extended.py`

### A) Execution Style

**Has `if __name__ == "__main__":`?** ✅ Yes (line 464)

```python
if __name__ == "__main__":
    main()
```

**Has `main()` function?** ✅ Yes (lines 193–463)

**Argument parsing?** ❌ No. All parameters are hardcoded as module-level constants:
- SYSTEM_HARD_PATH, SYSTEM_SOFT_PATH, HOLDOUT_PATH
- H_MIN, H_MAX, P_MIN, P_MAX
- NN resolutions: 11, 21, 41, 81

### B) Output Routing (Critical)

**Output path tracking:**

```python
# Line 15-17: Constants (hardcoded)
R = ROOT / "project_11" / "results"
OUT_DIR = R / "phase_d_soft_clamp"
OUT_MD = OUT_DIR / "RESOLUTION_SWEEP_EXTENDED.md"
OUT_JSON = OUT_DIR / "RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json"
```

**How outputs are written:**
- Line 334: `save_json(OUT_JSON, artifact)` — saves artifact dict as JSON
- Line 387: `save_text(OUT_MD, "\n".join(lines))` — saves markdown report

**Output directory injection:** ⚠️ Requires modification
- Currently: `OUT_DIR = R / "phase_d_soft_clamp"` (hardcoded)
- To divert to Project 12: Must replace line 15 to make `R` parameterizable or modify `OUT_DIR` directly

**Files created:**
- `RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json` (dictionary with k, points, true_dist, rules, nn, nn_grid_build)
- `RESOLUTION_SWEEP_EXTENDED.md` (markdown summary table)

### C) Inputs Used

**Holdout:**
- Line 12: `HOLDOUT_PATH = R / "phase_c3_sat_margin" / "holdout_points.json"` (hardcoded)
- Line 202: `holdout = load_json(HOLDOUT_PATH); pts = holdout["points"]`
- Read-only; no generation step

**Pool:** Not used in Phase D (deterministic, no sampling)

**Seeds:** 
- Deterministic run; holdout seed is locked (223311) in the JSON file itself

### D) Core Functions We Must Reuse

Critical functions (no need for external dependencies if copied):

| Function | Lines | Purpose |
|---|---|---|
| `softplus(x)` | 54–58 | Smooth approximation to max(x, 0) for soft clamp |
| `soft_clamp_softplus(x, k)` | 61–64 | Main soft clamp formula |
| `ground_truth_soft(system, H, P)` | 109–155 | Assign region label via soft clamp |
| `v3_predict(system, H, P, ...)` | 157–168 | V3 rule prediction |
| `v31_predict(system, H, P)` | 171–179 | V3.1 rule prediction |
| `nn_label(H, P, grid)` | 103–109 | 1-NN inference on grid |
| `macro_f1_present(y_true, y_pred)` | 79–96 | Metric computation |
| `eval_metrics(y_true, y_pred)` | 182–188 | Full metric dict |
| `subset(y_true, y_pred, mask)` | 191–200 | Subset evaluation |

All utility functions (`load_json`, `save_json`, `save_text`, `linspace`, `merge_system`, `accuracy`, etc.) are self-contained and have no external dependencies beyond standard Python.

### E) Minimal Reproduction Strategy Recommendation

**Recommended: Strategy 2 — "Copy into project_12/scripts + patch output_dir only"**

**Rationale:**
1. ✅ Script is fully self-contained (all utilities defined inline)
2. ✅ No external imports except `json`, `time`, `pathlib`, `typing`
3. ✅ Output directory is the only thing that must change (lines 15–17)
4. ⚠️ Input paths (SYSTEM_HARD_PATH, SYSTEM_SOFT_PATH, HOLDOUT_PATH) can remain pointing to `project_11/results/` (read-only)
5. ✅ Minimal patch: just replace `OUT_DIR = R / "phase_d_soft_clamp"` with `OUT_DIR = project_12_results / "repro/phase_d"`

**Implementation path:**
```
project_12/scripts/run_phase_d_repro.py
  — Copy phase_d_resolution_sweep_extended.py
  — Patch lines 15–17 to redirect OUT_DIR
  — Add metadata capture (git_hash, timestamp, environment)
  — Add manifest_execution_log.json writer
```

**Risk:** Very low. Input paths remain unchanged (OK for read-only reference). Output paths are diverted. No functional changes to logic.

---

## PHASE E2: Sample Efficiency

**File:** `project_11/experiments/phase_e2_sample_efficiency.py`

### A) Execution Style

**Has `if __name__ == "__main__":`?** ✅ Yes (line 340+)

**Has `main()` function?** ✅ Yes (starts around line 220)

**Argument parsing?** ❌ No. All parameters hardcoded:
- SEEDS = [101, 202, 303]
- SIZES = [250, 500, 1000, 1500, 2000]
- STRATS = ["uniform", "boundary", "mixed"]
- POOL_SIZE = 60000

### B) Output Routing

**Output path tracking:**

```python
# Lines 15-17: Hardcoded
R = ROOT / "project_11" / "results"
OUT_DIR = R / "phase_e2_sample_efficiency"
OUT_MD = OUT_DIR / "report.md"
OUT_JSON = OUT_DIR / "artifact.json"
```

**How outputs are written:**
- Line ~310: `save_json(OUT_JSON, artifact)`
- Line ~335: `save_text(OUT_MD, "\n".join(lines))`

**Output directory injection:** ⚠️ Requires modification
- Same pattern as Phase D: must patch `OUT_DIR`

**Files created:**
- `artifact.json` (dict with test, true_dist, v31, nn41, nn81, rows, elapsed_seconds)
- `report.md` (markdown summary with means over seeds)

### C) Inputs Used

**Holdout:**
- Line 12: `HOLDOUT_PATH = R / "phase_c3_sat_margin" / "holdout_points.json"` (hardcoded)
- Loaded and used; read-only

**Pool:**
- Line 20: `POOL_SIZE = 60000`
- Used implicitly in `build_reference()` (lines ~130–200):
  - Generates 60,000 random points
  - Scores by `boundary_score_v3()`
  - Selects top N for "boundary" strategy
  - Mixed strategy: N/2 uniform + N/2 from pool top

**Seeds:**
- Line 19: `SEEDS = [101, 202, 303]` (hardcoded)
- Used to seed RNG in `build_reference()` (line ~135):
  ```python
  rng = random.Random(1000000 + 1000 * seed + 7 * N + {"uniform": 1, "boundary": 2, "mixed": 3}[strat])
  ```

### D) Core Functions We Must Reuse

Critical functions:

| Function | Lines | Purpose |
|---|---|---|
| `build_reference(system, rng, N, strategy)` | ~88–170 | Generate reference set (uniform/boundary/mixed) |
| `boundary_score_v3(H, P, sfs)` | ~72–87 | Score for boundary band selection |
| `sample_uniform(rng)` | ~68–70 | Uniform random point in domain |
| `eval_one(system, holdout_HP, y_true, ref_grid)` | ~203–205 | Single reference set evaluation |
| `nn_grid(system, holdout_HP, y_true, n)` | ~207–214 | Dense NN baseline (grid size n) |
| `ground_truth_soft`, `v31_predict`, `nn_label` | (same as Phase D) | Prediction functions |
| `macro_f1_present`, `accuracy` | (same as Phase D) | Metrics |

### E) Minimal Reproduction Strategy Recommendation

**Recommended: Strategy 2 — "Copy into project_12/scripts + patch output_dir only"**

**Rationale:**
1. ✅ Fully self-contained (same as Phase D)
2. ✅ Stochastic seeds are parameterized in loops (SEEDS hardcoded but can be reused)
3. ✅ Pool size and sampling logic are self-contained
4. ⚠️ Must patch output directory (line 17)
5. ✅ Reuses all core utility functions from Phase D (can share a common utils module)

**Implementation path:**
```
project_12/scripts/run_phase_e2_repro.py
  — Copy phase_e2_sample_efficiency.py
  — Patch output directory
  — Keep SEEDS, SIZES, STRATS unchanged (for Sprint 2B reproduction fidelity)
  — Add metadata capture
```

**Risk:** Low. Seed values are locked (no flexibility needed for reproduction). All logic is self-contained.

---

## PHASE E3: Ratio + kNN

**File:** `project_11/experiments/phase_e3_ratio_knn.py`

### A) Execution Style

**Has `if __name__ == "__main__":`?** ✅ Yes (line 340+)

**Has `main()` function?** ✅ Yes

**Argument parsing?** ❌ No. Hardcoded sweep parameters:
- NS = [1000, 1500]
- FRACS = [0.2, 0.5, 0.8]
- SEEDS = [111, 222, 333, 444, 555]
- POOL_SIZE = 60000

### B) Output Routing

**Output path tracking:**

```python
# Lines 15-17: Hardcoded
R = ROOT / "project_11" / "results"
OUT_DIR = R / "phase_e3_ratio_knn"
OUT_MD = OUT_DIR / "report.md"
OUT_JSON = OUT_DIR / "artifact.json"
```

**How outputs are written:**
- Line ~280: `save_json(OUT_JSON, artifact)`
- Line ~312: `save_text(OUT_MD, "\n".join(lines))`

**Output directory injection:** ⚠️ Requires modification (same pattern)

**Files created:**
- `artifact.json` (dict with test, true_dist, baselines, rows, elapsed_seconds, pool_size, Ns, fracs, seeds)
- `report.md` (markdown summary)

**Important:** artifact.json **already contains metadata** (pool_size, Ns, fracs, seeds) — good practice we should copy for Project 12.

### C) Inputs Used

**Holdout:**
- Line 12: `HOLDOUT_PATH = R / "phase_c3_sat_margin" / "holdout_points.json"` (hardcoded, read-only)

**Pool:**
- Line 23: `POOL_SIZE = 60000` (constant, generated internally per seed+N+frac)
- Used in `build_reference()` (lines ~130–180):
  - Deterministic RNG per (seed, N, frac)
  ```python
  rng = random.Random(900000 + 13*seed + 17*N + int(frac*1000))
  ```

**Seeds:**
- Line 22: `SEEDS = [111, 222, 333, 444, 555]` (hardcoded)
- Used directly in main loop

### D) Core Functions We Must Reuse

Critical functions:

| Function | Lines | Purpose |
|---|---|---|
| `build_reference(system, seed, N, frac_uniform)` | ~114–176 | Generate mixed reference with deterministic RNG |
| `knn_label(H, P, ref, k)` | ~86–101 | k-NN inference (k ∈ {1,3}) with tie-break |
| `boundary_score_v3` | (same as E2) | Boundary scoring |
| `sample_uniform` | (same as E2) | Uniform sampling |
| `nn_grid(system, holdout_HP, y_true, n)` | ~203–208 | Dense NN baseline using knn_label with k=1 |
| Metric/prediction functions | (same as D/E2) | Shared utilities |

**Difference from E2:**
- Uses `knn_label()` instead of `nn_label()` for k-NN flexibility
- RNG is deterministic per (seed, N, frac) rather than per (seed, N, strategy)

### E) Minimal Reproduction Strategy Recommendation

**Recommended: Strategy 2 — "Copy into project_12/scripts + patch output_dir only"**

**Rationale:**
1. ✅ Fully self-contained
2. ✅ Deterministic RNG per configuration (reproducible)
3. ✅ Already includes metadata in artifact (pool_size, Ns, fracs, seeds)
4. ⚠️ Must patch output directory
5. ✅ Can reuse all utility functions from Phase D/E2

**Implementation path:**
```
project_12/scripts/run_phase_e3_repro.py
  — Copy phase_e3_ratio_knn.py
  — Patch output directory
  — Keep NS, FRACS, SEEDS unchanged (reproduction fidelity)
  — Add metadata capture (git_hash, timestamp, env)
```

**Risk:** Very low. All parameters locked for reproducibility.

---

## Decision Table

| Script | Recommended Strategy | Why | Risk | Minimal patches |
|---|---|---|---|---|
| **Phase D** | Strategy 2: Copy + patch OUT_DIR | Self-contained; input paths can remain read-only; deterministic | Very low | Line 17: `OUT_DIR` path redirect |
| **Phase E2** | Strategy 2: Copy + patch OUT_DIR | Self-contained; seed values hardcoded (OK); sampling logic independent | Low | Line 17: `OUT_DIR` path redirect |
| **Phase E3** | Strategy 2: Copy + patch OUT_DIR | Self-contained; deterministic RNG per config; already has metadata export | Very low | Line 17: `OUT_DIR` path redirect |

---

## Shared Utilities (Code Reuse Opportunity)

All three scripts have **overlapping core functions**. For efficiency, we can create:

**`project_12/scripts/entrypoint_shared.py`** (common module)

Extract and place here:
- `softplus()`, `soft_clamp_softplus()`, `clamp01()`, `clip()`
- `ground_truth_soft()`, `v3_predict()`, `v31_predict()`
- `nn_label()`, `knn_label()`
- `macro_f1_present()`, `macro_f1_fixed3()`, `accuracy()`, `dist_counts()`
- `eval_metrics()`, `subset()`
- `boundary_score_v3()`, `sample_uniform()`
- `linspace()`, `merge_system()`
- `load_json()`, `save_json()`, `save_text()`

Then each entrypoint script imports from `entrypoint_shared` and focuses on:
- Its specific sweep grid (NS, SIZES, SEEDS, FRACS)
- Its specific sampling/inference logic (Phase D grid sweep, E2 strategies, E3 knn)
- Artifact construction and metadata

**Code duplication reduction:** ~250 lines → ~80 lines per entrypoint (30% reduction)

---

## Implementation Checklist (Sprint 2B)

Before starting entrypoint code:

- [ ] Identify exact line numbers for `OUT_DIR` patch in each script
- [ ] Decide: single `entrypoint_shared.py` or keep utilities inline in each script?
- [ ] Define metadata structure to add (git_hash, timestamp, env, seeds, holdout_path, pool_config, manifest_hash)
- [ ] Create `manifest_execution_log.json` schema (start_timestamp, end_timestamp, executor, exit_code, etc.)
- [ ] Test import paths (can phase_d import from phase_e2?)
- [ ] Define output directory structure in project_12/results/repro/ (confirmed in manifests)

---

## Recommendation Summary

**All three scripts follow identical pattern:**
1. Hardcoded input paths (OK for read-only reference data)
2. Hardcoded output paths (must patch to divert to project_12)
3. Hardcoded sweep parameters (keep as-is for Sprint 2B reproduction fidelity)
4. Self-contained logic (no external dependencies)
5. Clean separation of concerns (utilities + specific logic)

**Optimal approach for Sprint 2B:**
- **Strategy 2 (copy + patch)** for all three scripts
- Option: Create shared utilities module to reduce duplication
- Minimal risk of breaking reproducibility
- Total effort: <2 hours for all three entrypoints + testing

