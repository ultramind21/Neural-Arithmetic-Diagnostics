import argparse
import sys

from .links import check_links
from .diff_gate import diff_gate


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


def _main():
    # Not used by console_scripts; useful for manual debugging.
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
