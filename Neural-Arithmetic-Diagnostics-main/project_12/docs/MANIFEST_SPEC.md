# MANIFEST_SPEC

**Purpose:** Define the schema and format for reproducible experiment manifests in Project 12.

**Format:** JSON (no external dependencies like YAML)

---

## JSON Schema

```json
{
  "manifest_version": "1.0",
  "experiment_id": "string (unique identifier)",
  "phase": "string (D | E2 | E3)",
  "sprint": "string (e.g., '2B' or '2C')",
  "claim_ids": ["list of claim IDs this validates", "e.g., ['P11-C01', 'P11-C02']"],
  
  "entrypoint": "string (path to script relative to project_12/, e.g., 'scripts/run_phase_d_repro.py')",
  
  "fixed_params": {
    "k": "integer (soft clamp parameter, typically 15)",
    "holdout_size": "integer (typically 800)",
    "holdout_path": "string (path to holdout JSON)",
    "pool_size": "integer or null (if not applicable)",
    "system_hard_path": "string (path to system definition JSON)",
    "system_soft_path": "string (path to soft clamp system JSON)"
  },
  
  "seeds": {
    "type": "string (deterministic | stochastic)",
    "values": ["list of integer seeds"]
  },
  
  "output_dir": "string (path relative to project_12/results/ where outputs go)",
  
  "expected_outputs": ["list of expected output files", "e.g., ['artifact.json', 'report.md']"],
  
  "notes": "string (any special instructions or caveats)",
  
  "validation_targets": {
    "claims_this_validates": ["claim IDs"],
    "acceptance_criteria": "string (reference to FORMAL_CLAIMS.md for thresholds)"
  }
}
```

---

## Field Definitions

| Field | Type | Required | Description |
|---|---|---|---|
| `manifest_version` | string | ✅ | Version of this schema (allows future evolution) |
| `experiment_id` | string | ✅ | Unique identifier e.g., "p11_phase_d_repro" |
| `phase` | string | ✅ | Which Project 11 phase is being reproduced: D, E2, or E3 |
| `sprint` | string | ✅ | Which Project 12 sprint: 2B (reproduction), 2C (re-validation), etc. |
| `claim_ids` | list | ✅ | Which claims this manifest validates |
| `entrypoint` | string | ✅ | Path to the run script (relative to project_12/) |
| `fixed_params` | object | ✅ | Immutable parameters for this experiment |
| `seeds` | object | ✅ | Seed specification: type + list of values |
| `output_dir` | string | ✅ | Where outputs are written (relative to project_12/results/) |
| `expected_outputs` | list | ✅ | What files should be created |
| `notes` | string | ⚠️ | Comments for humans (e.g., "Sprint 2B: repro with same seeds as P11") |
| `validation_targets` | object | ⚠️ | Link to acceptance criteria in FORMAL_CLAIMS.md |

---

## Example: Phase D Reproduction (Sprint 2B)

```json
{
  "manifest_version": "1.0",
  "experiment_id": "p11_phase_d_repro",
  "phase": "D",
  "sprint": "2B",
  "claim_ids": ["P11-C01", "P11-C02", "P11-C07"],
  
  "entrypoint": "scripts/run_phase_d_repro.py",
  
  "fixed_params": {
    "k": 15,
    "holdout_size": 800,
    "holdout_path": "../project_11/results/phase_c3_sat_margin/holdout_points.json",
    "pool_size": null,
    "system_hard_path": "../project_11/results/transfer_t4_system.json",
    "system_soft_path": "../project_11/results/phase_d_soft_clamp/system_soft_clamp.json"
  },
  
  "seeds": {
    "type": "deterministic",
    "values": [223311]
  },
  
  "output_dir": "repro/phase_d",
  
  "expected_outputs": [
    "RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json",
    "RESOLUTION_SWEEP_EXTENDED.md",
    "manifest_execution_log.json"
  ],
  
  "notes": "Sprint 2B reproduction: Run Phase D with identical parameters to Project 11. Outputs go to project_12/results/repro/phase_d/. Single deterministic run (seed 223311).",
  
  "validation_targets": {
    "claims_this_validates": ["P11-C01", "P11-C02", "P11-C07"],
    "acceptance_criteria": "See FORMAL_CLAIMS.md P11-C01, P11-C02, P11-C07 sections"
  }
}
```

---

## Manifest Discovery

All manifests are stored in: `project_12/manifests/`

Naming convention: `p11_phase_X_[sprint].json`

Examples:
- `p11_phase_d_repro.json` (Sprint 2B)
- `p11_phase_e2_repro.json` (Sprint 2B)
- `p11_phase_e3_repro.json` (Sprint 2B)
- `p11_phase_e2_revalidate.json` (Sprint 2C with new seeds)
- `p11_phase_d_extended.json` (if additional runs needed)

---

## Manifest Execution Lifecycle

1. **Manifest creation** (this doc)
2. **Entrypoint script creation** (Sprint 2B)
3. **Manifest validation** (check all required fields are present)
4. **Execution** (run entrypoint with manifest JSON as argument)
5. **Execution log capture** (create manifest_execution_log.json with:
   - start_timestamp
   - end_timestamp
   - executor (e.g., "agent" or "user")
   - entrypoint version (git hash)
   - exit_code
   - output_dir_created
   - files_written
)

---

## Future Extensions (Not Yet Used)

Reserved fields for future use:
- `dependencies`: list of script files this depends on
- `pre_checks`: list of pre-execution assertions (e.g., "holdout file must exist")
- `post_checks`: list of post-execution assertions (e.g., "output artifact.json must have 'rows' key")
- `timeout_seconds`: maximum runtime before hard stop
- `resource_limits`: memory, CPU, GPU specs

