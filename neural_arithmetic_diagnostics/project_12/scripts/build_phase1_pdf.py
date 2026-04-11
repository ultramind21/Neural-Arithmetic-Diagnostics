#!/usr/bin/env python3
"""
Sprint 10: Build Phase 1 Paper PDF
Converts PAPER_DRAFT_PHASE1.md to publication-ready PDF using Pandoc + xelatex.
"""

import subprocess
import sys
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJ12_ROOT = Path(__file__).resolve().parents[1]
DRAFT_MD = PROJ12_ROOT / "docs" / "PAPER_DRAFT_PHASE1.md"
BUILD_DIR = PROJ12_ROOT / "paper_build"
OUTPUT_PDF = BUILD_DIR / "Project12_Phase1.pdf"

# ============================================================================
# BUILD
# ============================================================================

def check_prerequisites():
    """Verify pandoc and xelatex are available."""
    checks = {
        "pandoc": ["pandoc", "--version"],
        "xelatex": ["xelatex", "--version"],
    }
    
    for tool, cmd in checks.items():
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ {tool} available")
            else:
                print(f"❌ {tool} check failed")
                return False
        except FileNotFoundError:
            print(f"❌ {tool} not found in PATH")
            return False
    
    return True

def build_pdf():
    """Build PDF from Markdown using pandoc."""
    if not DRAFT_MD.exists():
        print(f"❌ Draft not found: {DRAFT_MD}")
        return False
    
    print(f"\n📄 Building PDF from: {DRAFT_MD}")
    print(f"📁 Output: {OUTPUT_PDF}\n")
    
    # Pandoc command for Windows
    cmd = [
        "pandoc",
        str(DRAFT_MD),
        "-o", str(OUTPUT_PDF),
        f"--resource-path={PROJ12_ROOT}",
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=2",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "-V", "linestretch=1.5",
        "-V", "documentclass=article",
    ]
    
    print(f"🔨 Command: {' '.join(cmd[:4])}")
    print()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            if OUTPUT_PDF.exists():
                size_mb = OUTPUT_PDF.stat().st_size / (1024 * 1024)
                print(f"✅ PDF generated successfully")
                print(f"   Size: {size_mb:.2f} MB")
                print(f"   Path: {OUTPUT_PDF}")
                return True
            else:
                print(f"⚠️ Pandoc completed but PDF not found")
                return False
        else:
            print(f"❌ Pandoc error (exit code {result.returncode}):")
            if result.stderr:
                print(result.stderr)
            return False
    
    except subprocess.TimeoutExpired:
        print(f"❌ Pandoc timeout (60s)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("SPRINT 10: BUILD PHASE 1 PAPER PDF")
    print("="*80)
    
    # Check prerequisites
    print("\n[Prerequisites]")
    if not check_prerequisites():
        print("\n❌ Prerequisites failed. Install pandoc and xelatex.")
        return 1
    
    # Build PDF
    print("\n[Build]")
    if not build_pdf():
        return 1
    
    print("\n" + "="*80)
    print(f"✅ SUCCESS: PDF ready at {OUTPUT_PDF}")
    print("="*80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
