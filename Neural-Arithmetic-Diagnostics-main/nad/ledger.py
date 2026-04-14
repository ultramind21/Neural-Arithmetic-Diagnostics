from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Iterable, Tuple


def _sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _norm_rel(rel: str) -> str:
    # ledger uses posix style
    return rel.replace("\\", "/").lstrip("./")


def ledger_check(root: str, ledger_rel: str = "project_12/results/_hashes/p12_results_sha256.json") -> Tuple[int, int, int, Dict[str, str]]:
    """
    Returns (entries, missing_count, mismatch_count, samples_dict)
    samples_dict may contain keys:
      - missing_sample
      - mismatch_sample
    """
    root_p = Path(root).resolve()
    ledger_path = (root_p / ledger_rel).resolve()

    if not ledger_path.exists():
        raise FileNotFoundError(f"Ledger not found: {ledger_path}")

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    if not isinstance(ledger, dict):
        raise ValueError("Ledger JSON must be an object/dict")

    results_root = (root_p / "project_12" / "results").resolve()

    missing = []
    mismatch = []

    for rel, expected in ledger.items():
        rel = _norm_rel(rel)
        target = (results_root / Path(rel)).resolve()
        if not target.exists():
            missing.append(rel)
            continue
        got = _sha256_file(target)
        if got.lower() != str(expected).lower():
            mismatch.append((rel, str(expected), got))

    samples: Dict[str, str] = {}
    if missing:
        samples["missing_sample"] = "\n".join(missing[:20])
    if mismatch:
        lines = []
        for rel, exp, got in mismatch[:10]:
            lines.append(f"{rel}\n  expected: {exp}\n  got:      {got}")
        samples["mismatch_sample"] = "\n".join(lines)

    return len(ledger), len(missing), len(mismatch), samples
