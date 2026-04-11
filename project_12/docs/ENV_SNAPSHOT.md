# ENV_SNAPSHOT — Project 12 Validation (Sprint 2A)

**Frozen at:** 2026-04-11 (April 11, 2026)  
**Git branch:** project12-validation  
**Git tag:** v0.12-claims-locked  
**Commit hash:** 9b7051fe7e35c77afe05ec06a6aba87aeed92a11  

---

## System Information

| Component | Value |
|---|---|
| **OS** | Windows 10+ |
| **Python version** | 3.12.0 |
| **Python executable** | C:\Users\med\AppData\Local\Programs\Python\Python312\python.exe |
| **Torch version** | 2.5.1+cu121 |
| **GPU available** | Yes (CUDA 12.1 compute support) |
| **Virtual environment** | `.venv` (active) |

---

## Validation Gate

This snapshot locks the environment at the point where **all 8 Project 11 claims are extracted and validated for scientific rigor** (Sprint 1.6 complete).

**What this snapshot captures:**
- ✅ FORMAL_CLAIMS.md: 8 claims with Observed + Validation targets (separated)
- ✅ CLAIM_LOCK_STATUS.md: Claims marked `untested (Project 12)`
- ✅ TRACEABILITY_PROJECT_11.md: claim ↔ source artifact mapping
- ✅ Type reassessment: 3 strong, 3 medium, 2 weak

**What this snapshot does NOT allow:**
- ❌ No modifications to legacy projects (4–11) except critical bug fixes
- ❌ No execution of Project 12 grid runs until Sprint 2A completes
- ❌ No inference/prediction code until baselines verified

---

## Next Steps (Sprint 2A)

1. Baseline specification extraction (BASELINE_SPEC_PROJECT_11.md)
2. Artifact metadata inspection (inspect_project11_artifacts.py + report)
3. Manifest specification and templates (MANIFEST_SPEC.md + 3 JSON manifests)
4. Finalize traceability (review TRACEABILITY_PROJECT_11.md for accuracy)

After Sprint 2A completes:
- Sprint 2B: Entrypoint script derivation (reproduce Phase D/E2/E3 without modifying Project 11)
- Sprint 2C: Re-validation with new seeds (independent holdout/pool)

---

## Reproducibility Note

To restore this exact environment later:
```powershell
git checkout v0.12-claims-locked
git checkout -b project12-validation origin/project12-validation
# Ensure Python packages match (requirements.txt TBD)
```

