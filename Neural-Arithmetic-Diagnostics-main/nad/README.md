# NAD Toolkit

## What is NAD?

**NAD** (Neural Arithmetic Diagnostics) is a lightweight toolkit for validating research outputs in the neural arithmetic diagnostics repository.

Core purpose:
- Check Markdown documentation links are valid
- Compare artifacts/files for reproducibility (with canonical JSON diffing)
- Provide CLI interfaces for validation gates

NAD is **not** a research tool — it's infrastructure that wraps results from `project_*` folders.

## Install

```bash
pip install -e .
```

This installs the `nad` package and registers two CLI commands: `nad-check-links` and `nad-diff-gate`.

## CLI Reference

### nad-check-links

Recursively scan a Markdown file or directory for broken relative links.

```bash
nad-check-links PATH
```

**Arguments:**
- `PATH`: A `.md` file, or a directory to scan recursively.

**Example:**
```bash
nad-check-links project_12/docs
nad-check-links README.md
```

**Output:** Returns exit code 0 if all relative links exist; 1 and prints missing links if any are broken.

### nad-diff-gate

Compare two files for reproducibility. For JSON files, uses canonical formatting.

```bash
nad-diff-gate --original ORIGINAL_FILE --repro REPRO_FILE
```

**Arguments:**
- `--original`: Path to reference artifact.
- `--repro`: Path to reproduced artifact.

**Example:**
```bash
nad-diff-gate --original project_12/results/baseline_v1.json --repro project_12/results/baseline_repro.json
```

**Output:** 
- Exit code 0 and "OK: files are identical" if they match (after canonicalization).
- Exit code 1 and unified diff if they differ.

## Scope & Limitations

- **In scope:** Link validation, file diffing, artifact comparison.
- **Out of scope:** Running experiments, training models, or modifying research code.
- Reference for research logic: See `project_12/docs/CLAIM_AUTHORITY.md`.

## Integration with Project 12

NAD tools are used in `project_12/scripts/` validation gates and optionally in CI workflows (`.github/workflows/ci.yml`).

For authority on validated claims, see: [`project_12/docs/CLAIM_AUTHORITY.md`](../docs/CLAIM_AUTHORITY.md)
