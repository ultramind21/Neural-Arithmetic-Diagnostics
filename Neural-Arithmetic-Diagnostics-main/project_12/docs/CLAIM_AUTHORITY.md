# Claim Authority Policy (Project 12)

Project 12 is the **final authority** for claim status in this repository.

## Status meanings
- **validated**: backed by Project 12 artifacts + gates + traceable evidence pointers.
- **rejected-as-stated**: falsified under the specified protocol.
- **revised**: original statement adjusted; revised claim must have its own evidence pointers.

## Policy
- Results in `project_*` folders are **not** considered validated claims by default.
- Any publishable claim must have:
  1) claim text in `FORMAL_CLAIMS.md` (or linked addendum),
  2) manifests that reproduce the evidence,
  3) artifacts + metadata,
  4) gates passing,
  5) inclusion in a master validated snapshot document.
