"""
Sprint 9: Paper Draft Integrity Check
Validates that all figures, tables, and evidence paths referenced in PAPER_DRAFT_PHASE1.md exist.
"""

import re
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJ12_ROOT = Path(__file__).resolve().parents[1]
PAPER_DRAFT = PROJ12_ROOT / "docs" / "PAPER_DRAFT_PHASE1.md"
ASSETS_DIR = PROJ12_ROOT / "paper_assets"
DOCS_DIR = PROJ12_ROOT / "docs"
REPORTS_DIR = PROJ12_ROOT / "reports"

REQUIRED_FIGURES = {
    "fig1_nn_resolution.png": "NN resolution sweep (P11-C02)",
    "fig2_sample_efficiency.png": "Sample efficiency (P11-C03/C04/C06)",
    "fig3_c07_sweep_distribution.png": "C07 sweep distribution (P11-C07 rejection)",
    "fig4_p4_baseline_family_table.png": "P4 baseline family table (P4-C02/C03/C05)",
    "fig5_p4_pre_post_intervention.png": "P4 pre/post intervention (P4-C04)",
    "fig6_p4_seed_sweep_summary.png": "P4 3-seed smoke check (P4-C04)",
}

REQUIRED_TABLES = {
    "table1_protocol_checklist.md": "Protocol checklist (12 steps)",
    "table2_p11_evidence_summary.md": "P11 evidence summary (9 claims)",
}

REQUIRED_CAPTIONS = {
    "fig1_nn_resolution.md": "Fig1 caption",
    "fig2_sample_efficiency.md": "Fig2 caption",
    "fig3_c07_sweep_distribution.md": "Fig3 caption",
    "fig4_p4_baseline_family_table.md": "Fig4 caption",
    "fig5_p4_pre_post_intervention.md": "Fig5 caption",
    "fig6_p4_seed_sweep_summary.md": "Fig6 caption",
}

REQUIRED_EVIDENCE_FILES = {
    "VALIDATED_RESULTS_MASTER_PHASE1.md": "Master snapshot",
    "VALIDATED_RESULTS_P11_PROJECT12.md": "P11 snapshot",
    "VALIDATED_RESULTS_P4_PROJECT12.md": "P4 snapshot",
    "PAPER_READY_PHASE1_THREATS_TO_VALIDITY.md": "Threats to validity reference",
    "PAPER_READY_PHASE1_EVIDENCE_INDEX.md": "Evidence index reference",
}

# ============================================================================
# CHECKS
# ============================================================================

def check_figures():
    """Verify all figure files exist and are readable."""
    results = []
    for fname, desc in REQUIRED_FIGURES.items():
        fpath = ASSETS_DIR / fname
        status = "✅ PASS" if fpath.exists() else "❌ MISSING"
        results.append(f"{status} | {fname:40s} | {desc}")
    return results

def check_tables():
    """Verify all table files exist."""
    results = []
    for fname, desc in REQUIRED_TABLES.items():
        fpath = ASSETS_DIR / fname
        status = "✅ PASS" if fpath.exists() else "❌ MISSING"
        results.append(f"{status} | {fname:40s} | {desc}")
    return results

def check_captions():
    """Verify all caption files exist."""
    results = []
    captions_dir = ASSETS_DIR / "captions"
    for fname, desc in REQUIRED_CAPTIONS.items():
        fpath = captions_dir / fname
        status = "✅ PASS" if fpath.exists() else "❌ MISSING"
        results.append(f"{status} | {fname:40s} | {desc}")
    return results

def check_evidence_files():
    """Verify all evidence/support files referenced exist."""
    results = []
    for fname, desc in REQUIRED_EVIDENCE_FILES.items():
        fpath = DOCS_DIR / fname
        status = "✅ PASS" if fpath.exists() else "❌ MISSING"
        results.append(f"{status} | {fname:40s} | {desc}")
    return results

def check_figure_refs_in_draft():
    """Extract all Fig/Table references from draft and verify they're in REQUIRED_FIGURES/TABLES."""
    if not PAPER_DRAFT.exists():
        return ["❌ Paper draft not found"]
    
    draft_text = PAPER_DRAFT.read_text()
    results = []
    
    # Find all Fig. N patterns (Fig. 1, Fig. 2, etc.)
    fig_refs = set(re.findall(r'\bFig\.\s+(\d+)', draft_text))
    for fig_num in sorted(fig_refs):
        expected_key = f"fig{fig_num}_"
        has_match = any(k.startswith(expected_key) for k in REQUIRED_FIGURES.keys())
        status = "✅ PASS" if has_match else "⚠️ WARNING"
        results.append(f"{status} | Fig. {fig_num:40s} | referenced in draft")
    
    # Find Table N patterns
    table_refs = set(re.findall(r'\bTable\s+(\d+)', draft_text))
    for table_num in sorted(table_refs):
        expected_key = f"table{table_num}_"
        has_match = any(k.startswith(expected_key) for k in REQUIRED_TABLES.keys())
        status = "✅ PASS" if has_match else "⚠️ WARNING"
        results.append(f"{status} | Table {table_num:40s} | referenced in draft")
    
    return results

def main():
    """Run all checks and generate report."""
    print("\n" + "="*100)
    print("SPRINT 9: PAPER DRAFT INTEGRITY CHECK")
    print("="*100)
    
    all_results = []
    
    print("\n[FIGURES]")
    fig_results = check_figures()
    for r in fig_results:
        print(r)
    all_results.extend(fig_results)
    
    print("\n[TABLES]")
    table_results = check_tables()
    for r in table_results:
        print(r)
    all_results.extend(table_results)
    
    print("\n[CAPTIONS]")
    caption_results = check_captions()
    for r in caption_results:
        print(r)
    all_results.extend(caption_results)
    
    print("\n[EVIDENCE & SUPPORT FILES]")
    evidence_results = check_evidence_files()
    for r in evidence_results:
        print(r)
    all_results.extend(evidence_results)
    
    print("\n[FIGURE/TABLE REFERENCES IN DRAFT]")
    ref_results = check_figure_refs_in_draft()
    for r in ref_results:
        print(r)
    all_results.extend(ref_results)
    
    # Count results
    passed = sum(1 for r in all_results if "✅ PASS" in r)
    warnings = sum(1 for r in all_results if "⚠️ WARNING" in r)
    failed = sum(1 for r in all_results if "❌ MISSING" in r)
    
    print("\n" + "="*100)
    print(f"RESULTS: {passed} ✅ PASS | {warnings} ⚠️ WARNING | {failed} ❌ MISSING")
    print("="*100)
    
    # Write report
    report_path = REPORTS_DIR / "PAPER_DRAFT_INTEGRITY_CHECK.md"
    report_text = f"""# Paper Draft Integrity Check Report
Date: 2026-04-11  
Project: Project 12 Phase 1  

## Summary
- ✅ PASS: {passed}
- ⚠️ WARNING: {warnings}
- ❌ MISSING: {failed}

**Status: {'🟢 PASS' if failed == 0 else '🔴 FAIL'}**

## Detailed Results

### Figures
""" + "\n".join(["- " + r for r in fig_results]) + "\n\n### Tables\n" + "\n".join(["- " + r for r in table_results]) + "\n\n### Captions\n" + "\n".join(["- " + r for r in caption_results]) + "\n\n### Evidence & Support Files\n" + "\n".join(["- " + r for r in evidence_results]) + "\n\n### Figure/Table References\n" + "\n".join(["- " + r for r in ref_results])
    
    with open(report_path, "w") as f:
        f.write(report_text)
    
    print(f"\n✅ Report written to: {report_path}")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit(main())
