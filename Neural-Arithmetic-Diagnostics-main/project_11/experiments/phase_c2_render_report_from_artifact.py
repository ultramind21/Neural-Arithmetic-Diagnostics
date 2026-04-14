from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "project_11" / "results" / "phase_c2_noise"
ARTIFACT = OUT_DIR / "artifact.json"
REPORT = OUT_DIR / "report.md"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    a = load_json(ARTIFACT)
    results = a["results"]

    # stable sort
    results = sorted(results, key=lambda r: (float(r["sigma_H"]), float(r["sigma_P"])))

    lines = []
    lines.append("# PROJECT 11 — PHASE C2 NOISE-AWARE REPORT (V3-MC)")
    lines.append("")
    lines.append(f"- points: 500 (from locked T4-Large holdout)")
    lines.append(f"- reps per setting: {a.get('reps', 'unknown')}")
    lines.append(f"- MC samples per point (K): {a.get('K_mc', 'unknown')}")
    lines.append("")
    lines.append("## Results (means ± sd)")
    lines.append("")
    lines.append("| sigma_H | sigma_P | V3-hard F1 | V3-MC F1 | NN11 F1 |")
    lines.append("|---:|---:|---:|---:|---:|")

    for r in results:
        lines.append(
            f"| {float(r['sigma_H']):.4f} | {float(r['sigma_P']):.4f} | "
            f"{r['v3_hard']['macro_f1_mean']:.4f} ± {r['v3_hard']['macro_f1_sd']:.4f} | "
            f"{r['v3_mc']['macro_f1_mean']:.4f} ± {r['v3_mc']['macro_f1_sd']:.4f} | "
            f"{r['nn11']['macro_f1_mean']:.4f} ± {r['nn11']['macro_f1_sd']:.4f} |"
        )

    lines.append("")
    lines.append("Artifacts:")
    lines.append(f"- `{ARTIFACT.as_posix()}`")

    save_text(REPORT, "\n".join(lines))
    print("\n=== PHASE C2 REPORT RE-RENDERED FROM ARTIFACT ===")
    print(f"Artifact: {ARTIFACT}")
    print(f"Report:   {REPORT}\n")


if __name__ == "__main__":
    main()
