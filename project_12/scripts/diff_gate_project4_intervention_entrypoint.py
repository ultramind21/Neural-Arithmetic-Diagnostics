"""
================================================================================
DIFF_GATE_PROJECT4_INTERVENTION_ENTRYPOINT.PY
================================================================================

PURPOSE:
  Measure similarity between Project 4 original intervention entrypoint
  and P12 reproduction entrypoint to enforce copy+patch discipline.

PASS CRITERIA:
  - Similarity >= 0.85 (SequenceMatcher ratio)
  OR
  - Lines added/modified <= 80 lines

OUTPUT:
  project_12/reports/DIFF_GATE_P4_INTERVENTION_ENTRYPOINT.md

================================================================================
"""

import difflib
from pathlib import Path


def load_file_lines(path: Path):
    """Load file and return lines."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def compute_similarity(original_lines, modified_lines):
    """Compute SequenceMatcher similarity ratio."""
    matcher = difflib.SequenceMatcher(None, original_lines, modified_lines)
    return matcher.ratio()


def count_diff_lines(original_lines, modified_lines):
    """Count lines that were added or modified."""
    diff = list(difflib.unified_diff(original_lines, modified_lines, lineterm=''))
    # unified_diff output: lines starting with '+' are additions, '-' are deletions
    added = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
    deleted = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))
    return added, deleted, len(diff)


def main():
    original_path = Path("project_4/interventions/adversarial_training/project_4_adversarial_training.py")
    modified_path = Path("project_12/scripts/p4/run_p4_adversarial_training_repro.py")
    report_path = Path("project_12/reports/DIFF_GATE_P4_INTERVENTION_ENTRYPOINT.md")
    
    print(f"\n{'=' * 80}")
    print("DIFF GATE — Project 4 Intervention Entrypoint Minimal-Change Verification")
    print(f"{'=' * 80}")
    print(f"Original: {original_path}")
    print(f"Modified: {modified_path}")
    
    try:
        original_lines = load_file_lines(original_path)
        modified_lines = load_file_lines(modified_path)
        print(f"✓ Files loaded")
    except Exception as e:
        print(f"❌ Failed to load files: {e}")
        return
    
    # Compute metrics
    original_count = len(original_lines)
    modified_count = len(modified_lines)
    similarity = compute_similarity(original_lines, modified_lines)
    added, deleted, total_diff = count_diff_lines(original_lines, modified_lines)
    
    # Pass criteria
    SIMILARITY_THRESHOLD = 0.85
    LINE_CHANGE_THRESHOLD = 80
    
    similarity_pass = similarity >= SIMILARITY_THRESHOLD
    line_change_pass = (added + deleted) <= LINE_CHANGE_THRESHOLD
    overall_pass = similarity_pass or line_change_pass
    
    print(f"\nMetrics:")
    print(f"  Original lines: {original_count}")
    print(f"  Modified lines: {modified_count}")
    print(f"  Lines added: {added}")
    print(f"  Lines deleted: {deleted}")
    print(f"  Lines modified/total diff: {total_diff}")
    print(f"  Similarity ratio: {similarity:.4f}")
    
    print(f"\nPass Criteria:")
    print(f"  1. Similarity >= {SIMILARITY_THRESHOLD}: {similarity:.4f} {'✅ PASS' if similarity_pass else '❌ FAIL'}")
    print(f"  2. Lines changed (add+del) <= {LINE_CHANGE_THRESHOLD}: {added + deleted} {'✅ PASS' if line_change_pass else '❌ FAIL'}")
    print(f"\nOverall: {'✅ PASS (copy+patch discipline maintained)' if overall_pass else '❌ FAIL (rewrite detected — rebuild minimally)'}")
    
    # Generate report
    report_lines = [
        "# DIFF_GATE_P4_INTERVENTION_ENTRYPOINT — Minimal-Change Verification",
        "",
        "**Purpose:** Verify that P12 entrypoint is a true copy+patch of Project 4, not a major rewrite.",
        "",
        "---",
        "",
        "## Files Compared",
        "",
        f"- **Original:** `{original_path}`",
        f"- **Modified:** `{modified_path}`",
        "",
        "---",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Original lines | {original_count} |",
        f"| Modified lines | {modified_count} |",
        f"| Lines added | {added} |",
        f"| Lines deleted | {deleted} |",
        f"| Lines added + deleted | {added + deleted} |",
        f"| Similarity ratio (SequenceMatcher) | {similarity:.4f} |",
        "",
        "---",
        "",
        "## Pass Criteria",
        "",
        f"**Criterion 1:** Similarity >= {SIMILARITY_THRESHOLD}",
        f"- Result: {similarity:.4f} {'✅ PASS' if similarity_pass else '❌ FAIL'}",
        "",
        f"**Criterion 2:** Lines changed (added + deleted) <= {LINE_CHANGE_THRESHOLD}",
        f"- Result: {added + deleted} {'✅ PASS' if line_change_pass else '❌ FAIL'}",
        "",
        f"**Criterion 3:** Either Criterion 1 OR Criterion 2 passes",
        f"- Result: {'✅ PASS' if overall_pass else '❌ FAIL'}",
        "",
        "---",
        "",
        "## Verdict",
        "",
    ]
    
    if overall_pass:
        report_lines.extend([
            "✅ **PASS — Copy+Patch Discipline Maintained**",
            "",
            "The modified entrypoint maintains sufficient similarity to Project 4 original,",
            "indicating that it is a true copy+patch operation with minimal changes.",
            "",
            "Safe to proceed to Sprint 4B.2D (intervention training execution).",
        ])
    else:
        report_lines.extend([
            "❌ **FAIL — Major Rewrite Detected**",
            "",
            "The modified entrypoint diverges significantly from Project 4 original.",
            "This suggests a major rewrite rather than a minimal copy+patch operation.",
            "",
            "**Action Required:**",
            "1. Rebuild `project_12/scripts/p4/run_p4_adversarial_training_repro.py` by copying Project 4 entrypoint",
            "2. Apply ONLY the following minimal patches:",
            "   - Add `--manifest` argument to argparse",
            "   - Redirect `output_dir` based on manifest",
            "   - Load baseline artifact and compute gains",
            "   - Add `p12_metadata` to output artifact",
            "   - Add safety checks (output_dir within project_12, baseline exists)",
            "3. Avoid modifying any training logic, data generation, evaluation functions",
            "4. Re-run diff gate to verify minimal-change principle",
        ])
    
    report_lines.extend([
        "",
        "---",
        "",
        "**Generated by:** `project_12/scripts/diff_gate_project4_intervention_entrypoint.py`",
        "",
    ])
    
    report_text = "\n".join(report_lines)
    
    try:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_text, encoding="utf-8")
        print(f"\n✓ Report saved to: {report_path}")
    except Exception as e:
        print(f"❌ Failed to save report: {e}")
        return
    
    print(f"\n{'=' * 80}")


if __name__ == "__main__":
    main()
