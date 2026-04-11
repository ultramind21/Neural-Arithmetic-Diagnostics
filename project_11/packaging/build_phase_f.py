from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P11 = ROOT / "project_11"

OUT_DIR = P11 / "packaging" / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

INPUTS = {
    "D_resolution": P11 / "results" / "phase_d_soft_clamp" / "RESOLUTION_SWEEP_EXTENDED.md",
    "E1_report": P11 / "results" / "phase_e1_adaptive_nn" / "report.md",
    "E2_report": P11 / "results" / "phase_e2_sample_efficiency" / "report.md",
    "E2_analysis": P11 / "results" / "phase_e2_sample_efficiency" / "ANALYSIS.md",
    "E3_report": P11 / "results" / "phase_e3_ratio_knn" / "report.md",
    "E_synth": P11 / "results" / "PHASE_E_SYNTHESIS_V2.md",
}


def read_text(p: Path) -> str:
    if not p.exists():
        raise FileNotFoundError(str(p))
    return p.read_text(encoding="utf-8")


def write_text(name: str, text: str):
    (OUT_DIR / name).write_text(text, encoding="utf-8")


def main():
    d_res = read_text(INPUTS["D_resolution"])
    e1 = read_text(INPUTS["E1_report"])
    e2 = read_text(INPUTS["E2_report"])
    e2a = read_text(INPUTS["E2_analysis"])
    e3 = read_text(INPUTS["E3_report"])

    # Figure tables (copied blocks)
    write_text("FIG_F1_NN_RESOLUTION.md", d_res)
    write_text("FIG_F2_SAMPLE_EFFICIENCY.md", e2)
    write_text("FIG_F3_RATIO_KNN.md", e3)

    # Evidence matrix (human-readable summary)
    evidence = []
    evidence.append("# PROJECT 11 — EVIDENCE MATRIX (Phase D/E)")
    evidence.append("")
    evidence.append("## Core results (soft labels, k=15)")
    evidence.append("")
    evidence.append("| Item | Best setting | Metric | Value | Source |")
    evidence.append("|---|---|---:|---:|---|")
    evidence.append("| Rule baseline | V3.1 | macroF1_present | 0.9353 | Phase D resolution sweep |")
    evidence.append("| Dense NN | NN81 (6561 pts) | macroF1_present | 0.9847 | Phase D resolution sweep |")
    evidence.append("| Dense NN (mid) | NN41 (1681 pts) | macroF1_present | 0.9674 | Phase D resolution sweep |")
    evidence.append("| Adaptive NN | N=2000 (1000 uniform + 1000 boundary) | macroF1_present | 0.9752 | Phase E1 report |")
    evidence.append("| Sample-efficiency peak | N=1000 mixed | macroF1_present (mean over seeds) | 0.9780 | Phase E2 report/analysis |")
    evidence.append("| Ratio sweep best | N=1500, frac=0.5, 1-NN | macroF1_present (mean over seeds) | 0.9747 | Phase E3 report |")
    evidence.append("")
    write_text("EVIDENCE_MATRIX.md", "\n".join(evidence))

    # Key claims (short, copyable)
    claims = []
    claims.append("# PROJECT 11 — KEY CLAIMS (copyable)")
    claims.append("")
    claims.append("1) Hard clamp creates discontinuity artifacts that concentrate errors near boundaries; soft clamp restores smoother regime structure.")
    claims.append("2) Under soft labels (k=15), an interpretable rule baseline (V3.1) becomes competitive (macroF1_present=0.9353).")
    claims.append("3) Dense local interpolation (NN) improves with resolution and remains the top performer at high resolution (NN81=0.9847), but at increased reference cost.")
    claims.append("4) Structure-guided sampling (uniform+boundary) yields strong sample efficiency: N=1000 mixed reaches macroF1_present≈0.9780 (mean over seeds), close to NN81 with far fewer reference points.")
    claims.append("5) Boundary-only sampling fails; global coverage is necessary.")
    claims.append("")
    write_text("KEY_CLAIMS.md", "\n".join(claims))

    print("\n=== PHASE F BUILD COMPLETE ===")
    print(f"Outputs in: {OUT_DIR}\n")


if __name__ == "__main__":
    main()
