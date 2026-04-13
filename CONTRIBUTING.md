# Contributing

## Ground rules
- **Project 12 is the claim authority layer.**
  - Any result outside `project_12/` is considered a hypothesis/narrative until validated via Project 12 artifacts + gates.
- Keep changes **minimal and reproducible**.
- Do not add large data files to git.

## Dev quickstart
```bash
python -m pip install -U pip
pip install -r requirements.txt
pip install -e .
pip install pytest
```

## Run checks
One-command verification (includes all checks):
```bash
python tools/verify_platform_p0.py
```

Or run individually:
```bash
python -m compileall -q src nad
python -m pytest -q
python tests/test_env.py
python tests/test_rules.py
python tests/test_teacher.py
```

Lock file (ledger of installed packages):
```bash
# Generated from requirements.txt in a clean venv
cat requirements.lock.txt
```

## Adding/Changing a claim
- Update claim text under `project_12/docs/`
- Add/update a manifest under `project_12/manifests/`
- Generate artifacts under `project_12/results/`
- Update validated status documents under `project_12/docs/` and/or `project_12/reports/`
