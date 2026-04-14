# BASELINE_SPEC_PROJECT_11

**Purpose:** Complete specification of all baselines used in Project 11 (Phases D, E2, E3), extracted directly from protocols and experiment scripts without interpretation.

**Date:** 2026-04-11  
**Extracted from:** Project 11 docs/ + experiments/  

---

## (1) Task / Labels Definition

### What is macroF1_present?

**Definition:** Macro-averaged F1 score computed across **only the label classes present in the true holdout labels**.

Where:
- **Classes:** 3 region types:
  - "family-aware region"
  - "transition region"
  - "universal region"
- **Computation:** For each present class, compute:
  - TP = true positives
  - FP = false positives (predicted this class, but ground truth is different)
  - FN = false negatives (ground truth is this class, but predicted different)
  - Precision = TP / (TP + FP) if denominator > 0 else 0
  - Recall = TP / (TP + FN) if denominator > 0 else 0
  - F1 = 2 * Prec * Rec / (Prec + Rec) if denominator > 0 else 0
  - Then macro-average F1 across present classes only

**Why "present"?** Because not all 3 region types appear in every subset (e.g., test holdout). This prevents penalizing the model for not predicting classes that don't exist in that subset.

**Source:**
- `project_11/experiments/phase_d_resolution_sweep_extended.py` lines 84–99
- `project_11/experiments/phase_e2_sample_efficiency.py` lines 53–69
- `project_11/experiments/phase_e3_ratio_knn.py` lines 65–81

**Code reference:**
```python
def macro_f1_present(y_true: List[str], y_pred: List[str]) -> float:
    supports = dist_counts(y_true)  # count how many of each class in true labels
    present = [k for k, v in supports.items() if v > 0]  # only classes with count > 0
    if not present:
        return 0.0
    f1s = []
    for lbl in present:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == lbl and p == lbl)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != lbl and p == lbl)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == lbl and p != lbl)
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
        f1s.append(f1)
    return sum(f1s) / len(f1s)
```

### Ground truth labels (soft-clamp regime)

**Source of ground truth:** Computed per test point (H, P) using the system definitions + soft clamp.

**Soft clamp formula:**
```
soft_clamp(x; k=15) = clamp01(softplus(kx) / k - softplus(k(x-1)) / k)
```
where:
- softplus(u) = log(1 + exp(u))
- clamp01(v) = max(0, min(1, v))

This is used to compute "universal_score" and "family_aware_score" for each family, which then determine the region label.

**Source:**
- `project_11/docs/PHASE_D_SOFT_CLAMP_PROTOCOL.md` Section 2 ("What changes")
- `project_11/experiments/phase_d_resolution_sweep_extended.py` lines 62–75

---

## (2) Soft Clamp Definition

### Parameter: k

**Value:** k = 15 (LOCKED)

### Where soft clamp is applied

**Context:** Phase D introduces soft clamp to replace hard clamp in ground truth label computation.

**Hard clamp (baseline):** `clamp01(x) = max(0, min(1, x))`  
**Soft clamp (Phase D):** `soft_clamp(x; k=15) = clamp01(softplus(kx)/k - softplus(k(x-1))/k)`

### Function definitions in code

**Source: `project_11/experiments/phase_d_resolution_sweep_extended.py` lines 52–75**

```python
def softplus(x: float) -> float:
    import math
    if x > 50:
        return x
    return math.log1p(math.exp(x))

def soft_clamp_softplus(x: float, k: float) -> float:
    # matches audit recompute formulation
    return clamp01(softplus(k * x) / k - softplus(k * (x - 1.0)) / k)
```

### Ground truth computation using soft clamp

For each family family:
1. Compute base_global (from system definition)
2. Compute shared_failure (from system definition)
3. universal_score = soft_clamp(base_global + P * shared_failure; k=15)
4. family_aware_score = soft_clamp(base_global + 0.30 * shared_failure + 0.80 * H; k=15)
5. Compare scores using thresholds to determine region label

**Source:** `project_11/experiments/phase_d_resolution_sweep_extended.py` lines 160–200

---

## (3) Holdout and Pool

### Holdout (800 test points, locked)

**File:** `project_11/results/phase_c3_sat_margin/holdout_points.json`  
**Size:** 800 points  
**seed:** 223311 (locked)  
**SHA256:** 4ede0bb89dd3f4f72b983018956b94a53bda3da74e1e258ddf56118d3812607c  

**Points stored as:** List of [H, P] tuples  
**Never edited:** This holdout is shared across all Phases D, E2, E3

**Load in code:**
```python
HOLDOUT_PATH = R / "phase_c3_sat_margin" / "holdout_points.json"
holdout_data = json.loads(HOLDOUT_PATH.read_text(encoding="utf-8"))
# holdout_data is a list of [H, P] coordinates
```

**Source:**
- `project_11/docs/PHASE_D_SOFT_CLAMP_PROTOCOL.md` Section 1 ("Locked inputs")
- `project_11/experiments/phase_d_resolution_sweep_extended.py` lines 11–13

### Pool (60,000 boundary candidate points, for sampling)

**Pool size:** 60,000 points  
**Used in:** Phase E2 (sample efficiency) and Phase E3 (ratio + kNN)  
**Purpose:** Generate boundary-only and mixed sampling strategies

**How pool is built (per seed, in Phase E2/E3):**
1. For each strategy, generate random points in domain [H_MIN, H_MAX] × [P_MIN, P_MAX]
2. Score each point using V3 boundary score
3. Rank points by boundary score (descending)
4. For boundary-only strategy: select N highest-scoring points
5. For uniform strategy: select N uniformly random points
6. For mixed strategy: half uniform + half boundary-only

**Code reference:** `project_11/experiments/phase_e2_sample_efficiency.py` lines ~150–200 (handling of pool scoring and selection)

**Source:**
- `project_11/docs/PHASE_E2_SAMPLE_EFFICIENCY_PROTOCOL.md` Section 1
- `project_11/docs/PHASE_E3_RATIO_KNN_PROTOCOL.md` Section 1

---

## (4) Dense NN Baseline

### NN Grid Definition

**What is NN_k?**  
A nearest-neighbor predictor built on a k×k regular grid of points in the (H, P) domain.

**Grid sizes used:** 11, 21, 41, 81  
(i.e., NN11, NN21, NN41, NN81)

### Grid bounds and resolution

**Domain ranges:**
- H: [0.0010, 0.0200] (H_MIN to H_MAX)
- P: [0.2600, 0.4200] (P_MIN to P_MAX)

**Grid construction (linspace):**
For NN_k (e.g., k=81):
- H_grid = linspace(H_MIN=0.0010, H_MAX=0.0200, n=81)
- P_grid = linspace(P_MIN=0.2600, P_MAX=0.4200, n=81)
- Total points: 81 × 81 = 6,561 points (for NN81)

**Source:** `project_11/experiments/phase_d_resolution_sweep_extended.py` lines 33–34 + lines 181–189

```python
def linspace(a: float, b: float, n: int) -> List[float]:
    step = (b - a) / (n - 1)
    return [a + i * step for i in range(n)]

# Grid construction example:
H_grid = linspace(H_MIN, H_MAX, n=81)
P_grid = linspace(P_MIN, P_MAX, n=81)
grid = [(h, p, ground_truth_soft(system, h, p)) for h in H_grid for p in P_grid]
```

### NN Inference

**Nearest neighbor computation:**
1. For a test point (H_test, P_test), compute normalized distances to all grid points:
   - H_range = 0.015 - 0.003 = 0.012
   - P_range = 0.42 - 0.30 = 0.12
   - normalized_distance = sqrt(((H - H_test) / H_range)² + ((P - P_test) / P_range)²)
2. Find grid point with minimum distance
3. Return the label of that grid point

**Code reference:**
```python
def normalized_distance(aH: float, aP: float, bH: float, bP: float) -> float:
    H_range = 0.015 - 0.003
    P_range = 0.42 - 0.30
    return (((aH - bH) / H_range) ** 2 + ((aP - bP) / P_range) ** 2) ** 0.5

def nn_label(H: float, P: float, grid: List[Tuple[float, float, str]]) -> str:
    best_lbl, best_d = None, None
    for gH, gP, glbl in grid:
        d = normalized_distance(H, P, gH, gP)
        if best_d is None or d < best_d:
            best_d, best_lbl = d, glbl
    return best_lbl
```

**Source:**
- `project_11/experiments/phase_d_resolution_sweep_extended.py` lines 120–134
- `project_11/experiments/phase_e2_sample_efficiency.py` lines 72–84

### Build Time

**Example (NN81 reported in Phase D):**  
Build time: 0.0527 seconds (single deterministic run)

**Source:** `project_11/packaging/out/FIG_F1_NN_RESOLUTION.md` (build_seconds column)

---

## (5) Sampling Strategies (E2/E3)

### Strategy definitions

#### 5.1 Uniform-only

**Definition:** N random points sampled uniformly from the domain [H_MIN, H_MAX] × [P_MIN, P_MAX].

**Code:**
```python
# Uniform: random.seed(seed)
# Then generate N random (H, P) from the bounds
uniform_points = [(random.uniform(H_MIN, H_MAX), random.uniform(P_MIN, P_MAX)) 
                  for _ in range(N)]
```

**Source:** `project_11/experiments/phase_e2_sample_efficiency.py` lines ~140–150

#### 5.2 Boundary-only

**Definition:** N points selected from a fixed pool (60,000 points) scored by V3 boundary score, taking the N points with **highest** boundary score.

**Boundary score (from V3 rule):**  
Defined in `project_11/src/predictors/compressed_deltas_rule_v3.py` (or similar).  
Represents how "boundary-like" a point is (closer to decision boundary = higher score).

**Selection:**
1. Generate pool of 60,000 random points in domain
2. Score each with V3 boundary score
3. Rank descending by score
4. Take top N points

**Source:** `project_11/experiments/phase_e2_sample_efficiency.py` lines ~145–160

#### 5.3 Mixed (50/50 uniform + boundary)

**Definition:** N points total:
- n_uniform = N / 2 (rounded)
- n_boundary = N - n_uniform
- Concatenate both lists

**Code:**
```python
n_uniform = N // 2  # or round(N * 0.5)
n_boundary = N - n_uniform
mixed_points = uniform_points[:n_uniform] + boundary_points[:n_boundary]
```

**Source:** `project_11/experiments/phase_e2_sample_efficiency.py` lines ~163–170 (implicit in loop logic)

**Also explicit in Phase E3:**
`project_11/docs/PHASE_E3_RATIO_KNN_PROTOCOL.md` Section 2:
> For each (seed, N, uniform_fraction):
> - n_uniform = round(N * uniform_fraction)
> - n_boundary = N - n_uniform

---

## (6) kNN Ratio Sweep (E3)

### Uniform fraction sweep

**Parameter:** uniform_fraction ∈ {0.2, 0.5, 0.8}

**Conversion to counts:**
```python
uniform_fracs = [0.2, 0.5, 0.8]
for frac in uniform_fracs:
    n_uniform = round(N * frac)
    n_boundary = N - n_uniform
    # Build mixed reference set
```

**Source:**
- `project_11/docs/PHASE_E3_RATIO_KNN_PROTOCOL.md` Section 2
- `project_11/experiments/phase_e3_ratio_knn.py` lines ~200–250

### 1-NN vs 3-NN

**1-NN (k=1):** Return label of single nearest neighbor  
**3-NN (k=3):** Majority vote among 3 nearest neighbors

**Implementation:**
```python
def knn_label(H: float, P: float, ref: List[Tuple[float, float, str]], k: int) -> str:
    # Compute distances to all reference points
    dists = [(normalized_distance(H, P, rH, rP), lbl) for (rH, rP, lbl) in ref]
    dists.sort(key=lambda x: x[0])
    top = [lbl for _, lbl in dists[:k]]  # k nearest labels
    
    # Majority vote
    c = Counter(top)
    best = max(c.values())
    tied = [lab for lab, v in c.items() if v == best]
    
    # Deterministic tie-break: transition > universal > family-aware
    order = ["transition region", "universal region", "family-aware region"]
    for lab in order:
        if lab in tied:
            return lab
    return tied[0]
```

**Source:**
- `project_11/experiments/phase_e3_ratio_knn.py` lines 84–105
- `project_11/docs/PHASE_E3_RATIO_KNN_PROTOCOL.md` Section 2

---

## (7) Fixed Systems and Parameters

### System file (hard thresholds + family definitions)

**File:** `project_11/results/transfer_t4_system.json`

**Contains:**
- families: list of family definitions with base_global and shared_failure
- thresholds: dict with per_family_margin, region_family_aware_gap_gt, etc.

**Source:** Generated in earlier phases (Phases A–C); locked before Phase D

### Soft clamp system file

**File:** `project_11/results/phase_d_soft_clamp/system_soft_clamp.json`

**Contains:**
- Copy of families + thresholds from hard system
- soft_clamp parameter: {"k": 15}

**How merged:**
```python
def merge_system(hard: dict, soft: dict) -> dict:
    out = {}
    out["families"] = hard.get("families", [])
    out["thresholds"] = hard.get("thresholds", {})
    out["soft_clamp"] = soft.get("soft_clamp", {"k": 15})
    return out
```

**Source:**
- `project_11/experiments/phase_d_resolution_sweep_extended.py` lines 137–141
- `project_11/experiments/phase_e2_sample_efficiency.py` lines 118–123

---

## (8) Serialization and Artifact Format

### Output directory structure

**Phase D:** `project_11/results/phase_d_soft_clamp/`  
- `RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json`
- `RESOLUTION_SWEEP_EXTENDED.md`

**Phase E2:** `project_11/results/phase_e2_sample_efficiency/`  
- `artifact.json`
- `report.md`

**Phase E3:** `project_11/results/phase_e3_ratio_knn/`  
- `artifact.json`
- `report.md`

### JSON structure (minimal spec observed)

Each artifact.json contains:
- `results`: list of result objects
- Each result object has: N, seed, strategy, macroF1_present, accuracy, (seed list if stochastic), etc.

**No detailed reference point lists saved** (only aggregate metrics per configuration)

**Source:**
- `project_11/experiments/phase_d_resolution_sweep_extended.py` lines ~250–300 (save_json calls)
- `project_11/experiments/phase_e2_sample_efficiency.py` lines ~280–320 (save_json calls)

---

## Summary Table

| Component | Phase D | Phase E2 | Phase E3 | Source |
|---|---|---|---|---|
| **Holdout** | 800 pts (locked) | 800 pts (locked) | 800 pts (locked) | PHASE_*_PROTOCOL.md |
| **Clamp type** | soft (k=15) | soft (k=15) | soft (k=15) | PROTOCOL Section 2 |
| **Pool size** | N/A (grid based) | 60,000 | 60,000 | PROTOCOL Section 1 |
| **Strategies** | NN-grid | uniform/boundary/mixed | uniform_frac ∈ {0.2,0.5,0.8} | PROTOCOL Section 3 |
| **Grid sizes** | NN11..NN81 | NN41, NN81 (baselines) | 1-NN, 3-NN on refs | PROTOCOL / Script |
| **Seeds** | 1 (223311, fixed) | 3 ([101,202,303]) | 5 ([111,222,333,444,555]) | PROTOCOL Section 4/5 |
| **Metrics** | macroF1_present, accuracy | macroF1_present, accuracy | macroF1_present, accuracy | Script compute |
| **Reference files** | ~100 JSON files | 1 artifact.json | 1 artifact.json | Phase docs |

