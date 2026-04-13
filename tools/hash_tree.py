#!/usr/bin/env python3
"""
hash_tree.py — Generate SHA256 hashes of all files in a directory tree.

Usage: python tools/hash_tree.py <DIR>

Outputs JSON to stdout with:
- paths (POSIX-style, sorted)
- sha256 hashes (hex)
- excludes: .git, .venv, .venv_lock, __pycache__, _hashes, hidden files (.*).
"""

import sys
import json
import hashlib
from pathlib import Path


def hash_tree(root_path):
    """
    Walk tree, hash files, return sorted JSON-serializable dict.
    """
    root = Path(root_path).resolve()
    
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")
    
    # Exclusions
    SKIP_DIRS = {".git", ".venv", ".venv_lock", "__pycache__", "_hashes"}
    
    hashes = {}
    
    for file_path in sorted(root.rglob("*")):
        rel_path = file_path.relative_to(root)
        
        # Skip directories
        if file_path.is_dir():
            continue
        
        # Skip if within excluded directory
        parts = rel_path.parts
        if any(part in SKIP_DIRS for part in parts):
            continue
        
        # Skip hidden files
        if any(part.startswith(".") for part in parts):
            continue
        
        # Calculate hash
        sha256 = hashlib.sha256(file_path.read_bytes()).hexdigest()
        
        # Use POSIX-style path (forward slashes)
        posix_path = rel_path.as_posix()
        hashes[posix_path] = sha256
    
    return hashes


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hash_tree.py <DIR>", file=sys.stderr)
        sys.exit(1)
    
    target = sys.argv[1]
    try:
        result = hash_tree(target)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
