# PROJECT 11 — T4-LARGE RUNBOOK (Rule V3)

## Rules
- No installs
- No venv
- No file deletions
- Do not edit generated JSON after SHA256 is printed

## Commands (run in order)

```powershell
cd "d:\Music\Project 03 Abacus\neural_arithmetic_diagnostics"
python project_11/experiments/transfer_t4_large_generate.py
python project_11/experiments/transfer_t4_large_rule_check.py
python project_11/experiments/transfer_t4_large_evaluate.py
type project_11\results\transfer_t4_large\report.md
```

## Output folder
- `project_11/results/transfer_t4_large/`

All artifacts (holdout, predictions, report, artifact.json) go there.

---

## Expected flow

1. **generate.py** creates JSON files + prints SHA256 hashes (LOCK)
2. **rule_check.py** verifies 0 mismatches (integrity)
3. **evaluate.py** computes metrics + generates report
4. **report.md** displayed (final results)

---

## Abort conditions

If any command fails:
- STOP immediately
- Do NOT proceed to next command
- Report error + exit code

---
