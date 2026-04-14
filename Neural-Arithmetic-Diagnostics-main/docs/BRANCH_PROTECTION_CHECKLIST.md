# Branch protection checklist (main)

Recommended GitHub settings for `main`:
- Require pull requests before merging
- Require status checks to pass:
  - CI workflow (ubuntu-latest + windows-latest)
- Require branches to be up to date before merging
- (Optional) Require review approval
- (Optional) Restrict who can push to main
