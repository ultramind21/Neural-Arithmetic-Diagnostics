from __future__ import annotations

import difflib
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _canon_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def diff_gate(original: str, repro: str) -> bool:
    """
    Returns True if identical (after canonicalization for JSON), else False (and prints unified diff).
    """
    a = Path(original)
    b = Path(repro)

    if not a.exists() or not b.exists():
        print(f"ERROR: missing file(s): original_exists={a.exists()} repro_exists={b.exists()}")
        return False

    if a.suffix.lower() == ".json" and b.suffix.lower() == ".json":
        a_txt = _canon_json(_load_json(a))
        b_txt = _canon_json(_load_json(b))
    else:
        a_txt = a.read_text(encoding="utf-8", errors="replace")
        b_txt = b.read_text(encoding="utf-8", errors="replace")

    if a_txt == b_txt:
        print("OK: files are identical")
        return True

    diff = difflib.unified_diff(
        a_txt.splitlines(True),
        b_txt.splitlines(True),
        fromfile=str(a),
        tofile=str(b),
    )
    print("".join(diff))
    return False
