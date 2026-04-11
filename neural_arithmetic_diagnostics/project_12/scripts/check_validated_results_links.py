#!/usr/bin/env python3
"""
check_validated_results_links.py

Validates that all paths referenced in VALIDATED_RESULTS_P11_PROJECT12.md exist on disk.
Generates a report: VALIDATED_RESULTS_LINK_CHECK.md
"""

import re
import os
from pathlib import Path
from typing import List, Tuple

def extract_paths_from_markdown(md_file: Path) -> List[str]:
    """Extract all paths that look like project_12/ or project_11/ from markdown."""
    paths = set()
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: backticks or plain text paths starting with project_12/ or project_11/
    pattern = r'(?:project_1[12]/[^\s`\)]+)'
    matches = re.findall(pattern, content)
    paths.update(matches)
    
    return sorted(list(paths))

def check_paths(base_dir: Path, paths: List[str]) -> Tuple[List[str], List[str]]:
    """Check if paths exist relative to base_dir."""
    existing = []
    missing = []
    
    for path_str in paths:
        full_path = base_dir / path_str
        if full_path.exists():
            existing.append(path_str)
        else:
            missing.append(path_str)
    
    return existing, missing

def main():
    # Paths
    project_root = Path(__file__).parent.parent.parent  # neural_arithmetic_diagnostics/
    validated_results = project_root / "project_12" / "docs" / "VALIDATED_RESULTS_P11_PROJECT12.md"
    report_path = project_root / "project_12" / "reports" / "VALIDATED_RESULTS_LINK_CHECK.md"
    
    # Extract paths
    print(f"Reading: {validated_results}")
    if not validated_results.exists():
        print(f"ERROR: {validated_results} not found!")
        return
    
    paths = extract_paths_from_markdown(validated_results)
    print(f"Found {len(paths)} unique path references")
    
    # Check paths
    existing, missing = check_paths(project_root, paths)
    
    # Generate report
    report_lines = []
    report_lines.append("# VALIDATED_RESULTS_P11_PROJECT12.md — Link Integrity Check")
    report_lines.append("")
    report_lines.append(f"**Check Date:** {Path(validated_results).stat().st_mtime}")
    report_lines.append(f"**Total paths found:** {len(paths)}")
    report_lines.append(f"**Existing:** {len(existing)}")
    report_lines.append(f"**Missing:** {len(missing)}")
    report_lines.append("")
    
    if missing:
        report_lines.append("## ❌ MISSING PATHS")
        report_lines.append("")
        for path in missing:
            report_lines.append(f"- `{path}`")
        report_lines.append("")
    
    report_lines.append("## ✅ EXISTING PATHS")
    report_lines.append("")
    for path in existing:
        report_lines.append(f"- `{path}`")
    report_lines.append("")
    
    if missing:
        report_lines.append("---")
        report_lines.append("## STATUS: ❌ FAILED — Missing paths detected")
        report_lines.append("")
        report_lines.append("**Action required:** Update `VALIDATED_RESULTS_P11_PROJECT12.md` to correct or remove missing references.")
        status = "FAILED"
    else:
        report_lines.append("---")
        report_lines.append("## STATUS: ✅ PASSED — All referenced paths exist")
        report_lines.append("")
        report_lines.append("Evidence integrity verified. Ready for Sprint 2E.")
        status = "PASSED"
    
    # Write report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
    
    print(f"\n✅ Report written to: {report_path}")
    print(f"Status: {status}")
    print(f"Missing: {len(missing)}")
    print(f"Existing: {len(existing)}")

if __name__ == "__main__":
    main()
