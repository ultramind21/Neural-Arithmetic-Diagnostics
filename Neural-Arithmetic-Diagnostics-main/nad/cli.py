import argparse
import sys

from .links import check_links
from .diff_gate import diff_gate
from .ledger import ledger_check


def check_links_main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="nad-check-links", description="Check Markdown relative links resolve to real files.")
    p.add_argument("path", help="Path to a .md file or a directory to scan recursively.")
    args = p.parse_args(argv)

    missing = check_links(args.path)
    if missing:
        for item in missing:
            print(item)
        return 1
    print("OK: no missing relative links found")
    return 0


def diff_gate_main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="nad-diff-gate", description="Fail if two artifacts/files differ (canonical JSON diff if .json).")
    p.add_argument("--original", required=True, help="Original artifact/file path")
    p.add_argument("--repro", required=True, help="Reproduced artifact/file path")
    args = p.parse_args(argv)

    ok = diff_gate(args.original, args.repro)
    return 0 if ok else 1


def ledger_check_main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="nad-ledger-check", description="Verify Project 12 results against sha256 ledger.")
    p.add_argument("--root", default=".", help="Repo root (default: .)")
    p.add_argument("--ledger", default="project_12/results/_hashes/p12_results_sha256.json", help="Ledger path relative to root")
    args = p.parse_args(argv)

    try:
        entries, missing, mismatch, samples = ledger_check(args.root, args.ledger)
    except Exception as e:
        print(f"ERROR: {e}")
        return 2

    print(f"LEDGER_ENTRIES={entries}")
    print(f"MISSING={missing}")
    print(f"MISMATCH={mismatch}")
    if samples.get("missing_sample"):
        print("MISSING_SAMPLE:")
        print(samples["missing_sample"])
    if samples.get("mismatch_sample"):
        print("MISMATCH_SAMPLE:")
        print(samples["mismatch_sample"])

    return 0 if (missing == 0 and mismatch == 0) else 1


def repro_check_main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="nad-repro-check", description="Run deterministic repo verification + ledger check.")
    p.add_argument("--root", default=".", help="Repo root (default: .)")
    args = p.parse_args(argv)

    # 1) run deterministic verify
    import subprocess
    r = subprocess.run([sys.executable, "tools/verify_platform_p0.py"], cwd=args.root)
    if r.returncode != 0:
        print(f"FAIL: verify_platform_p0.py exit={r.returncode}")
        return r.returncode

    # 2) run ledger check
    return ledger_check_main(["--root", args.root])


def _main():
    # Not used by console_scripts; useful for manual debugging.
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
