import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, check=True):
    print(f"\n$ {' '.join(cmd)}")
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.stdout:
        print(p.stdout)
    if p.stderr:
        print(p.stderr, file=sys.stderr)
    if check and p.returncode != 0:
        raise SystemExit(p.returncode)
    return p.returncode


def main():
    # 0) compile gates
    run([sys.executable, "-m", "compileall", "-q", "src", "nad"])

    # 1) pytest gate (note: this repo uses smoke wrappers currently)
    run([sys.executable, "-m", "pytest", "-q"])

    # 2) run legacy direct tests too (stronger than smoke signal)
    run([sys.executable, "tests/test_env.py"])
    run([sys.executable, "tests/test_rules.py"])
    run([sys.executable, "tests/test_teacher.py"])

    # 3) nad-check-links on Project 12 docs (authority layer)
    run(["nad-check-links", "project_12/docs"])

    # 4) diff gate self-test (JSON canonicalization)
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        a = d / "a.json"
        b = d / "b.json"
        a.write_text('{"b": 2, "a": 1}\n', encoding="utf-8")
        b.write_text('{"a": 1, "b": 2}\n', encoding="utf-8")
        run(["nad-diff-gate", "--original", str(a), "--repro", str(b)])

        b.write_text('{"a": 1, "b": 3}\n', encoding="utf-8")
        # Expect non-zero exit here; do NOT fail the whole verify run, just confirm it fails.
        rc = run(["nad-diff-gate", "--original", str(a), "--repro", str(b)], check=False)
        if rc == 0:
            print("ERROR: diff gate should have failed but returned 0")
            raise SystemExit(1)
        print("OK: diff gate fails on mismatch as expected")

    print("\nP0_STATUS = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
