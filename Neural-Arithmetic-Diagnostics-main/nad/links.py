from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def _iter_md_files(root: Path) -> Iterable[Path]:
    if root.is_file() and root.suffix.lower() == ".md":
        yield root
        return
    if root.is_dir():
        for p in root.rglob("*.md"):
            yield p


def _is_external(href: str) -> bool:
    href = href.strip()
    return href.startswith(("http://", "https://", "mailto:"))


def _strip_anchor(href: str) -> str:
    # "file.md#section" -> "file.md"
    return href.split("#", 1)[0].strip()


def check_links(path: str) -> List[str]:
    """
    Returns a list of human-readable missing link messages.
    Only checks relative (local) links in markdown.
    """
    root = Path(path)
    if not root.exists():
        return [f"ERROR: path not found: {path}"]

    missing: List[str] = []
    for md in _iter_md_files(root):
        text = md.read_text(encoding="utf-8", errors="replace")
        for m in _LINK_RE.finditer(text):
            href = m.group(1).strip()
            if not href or _is_external(href) or href.startswith("#"):
                continue

            href_no_anchor = _strip_anchor(href)
            if not href_no_anchor:
                continue

            # Ignore pure query-like weirdness (rare), keep strict otherwise.
            target = (md.parent / href_no_anchor).resolve()
            if not target.exists():
                missing.append(f"MISSING: {md} -> {href}")

    return missing
