# Project 12 Phase 1 Paper Build

This directory contains scripts and instructions for building and distributing the Phase 1 paper.

## Quick Start

```bash
cd neural_arithmetic_diagnostics
python project_12/scripts/build_phase1_pdf.py
```

Output: `project_12/paper_build/Project12_Phase1.pdf`

## Requirements

- **Pandoc 3.0+** — Markdown to PDF conversion engine
  - Windows: Install from [pandoc.org](https://pandoc.org/installing.html)
  - Linux: `apt install pandoc`
  - macOS: `brew install pandoc`

- **LaTeX / xelatex** — PDF rendering backend
  - Windows: [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/)
  - Linux: `apt install texlive-xetex`
  - macOS: `brew install basictex` (or full MacTeX)

## Build Options

### Standard (recommended)
```bash
python project_12/scripts/build_phase1_pdf.py
```
- Uses xelatex PDF engine (best typography)
- Generates table of contents
- Styled margins (1 inch) and spacing (1.5x)

### Manual Pandoc (if script fails)
```bash
pandoc project_12/docs/PAPER_DRAFT_PHASE1.md \
  -o project_12/paper_build/Project12_Phase1.pdf \
  --resource-path=project_12 \
  --pdf-engine=xelatex \
  --toc --toc-depth=2
```

### Alternative PDF engines
If xelatex fails, try:
- `--pdf-engine=pdflatex` (faster, fewer dependencies)
- `--pdf-engine=lualatex` (good Unicode support)

## Outputs

| File | Purpose |
|------|---------|
| `Project12_Phase1.pdf` | Main paper (final). |
| `Project12_Phase1_release.zip` (optional) | Reproducible bundle: PDF + Markdown + figures + evidence. |

## Troubleshooting

### "pandoc not found"
- Install pandoc from [pandoc.org](https://pandoc.org/installing.html)
- Verify: `pandoc --version`

### "xelatex not found"
- Install MiKTeX (Windows) or TeX Live (Linux/macOS)
- Verify: `xelatex --version`

### "Font not found" or LaTeX errors
- Run MiKTeX Package Manager or `tlmgr update --all` (TeX Live)
- Fonts needed: Computer Modern (default), which is included

### PDF is blank or images missing
- Check `--resource-path` points to correct project root
- Verify figures exist in `project_12/paper_assets/`
- Run integrity check: `python project_12/scripts/paper_draft_integrity_check.py`

## Release Checklist

Before distribution:

- [ ] PDF builds without errors
- [ ] All 6 figures visible in PDF
- [ ] Tables readable and properly formatted
- [ ] Table of contents links work
- [ ] Check page count and layout
- [ ] Verify metadata (title, date, author if needed)

## Files Involved

**Source:**
- `project_12/docs/PAPER_DRAFT_PHASE1.md` — Paper text (Markdown)
- `project_12/paper_assets/fig*.png` — Figures (6 publication-ready PNGs)
- `project_12/paper_assets/table*.md` — Tables (Markdown format)
- `project_12/paper_assets/captions/*.md` — Figure captions

**Scripts:**
- `project_12/scripts/build_phase1_pdf.py` — PDF build automation
- `project_12/scripts/paper_draft_integrity_check.py` — Validation check

**Build output:**
- `project_12/paper_build/Project12_Phase1.pdf` — Final PDF (not in git)

## Version History

| Date | Event |
|------|-------|
| 2026-04-11 | Phase 1 paper draft complete; PDF build scripts created (Sprint 9-10) |
