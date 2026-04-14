# PROJECT 11 — KEY CLAIMS (copyable)

1) Hard clamp creates discontinuity artifacts that concentrate errors near boundaries; soft clamp restores smoother regime structure.
2) Under soft labels (k=15), an interpretable rule baseline (V3.1) becomes competitive (macroF1_present=0.9353).
3) Dense local interpolation (NN) improves with resolution and remains the top performer at high resolution (NN81=0.9847), but at increased reference cost.
4) Structure-guided sampling (uniform+boundary) yields strong sample efficiency: N=1000 mixed reaches macroF1_present≈0.9780 (mean over seeds), close to NN81 with far fewer reference points.
5) Boundary-only sampling fails; global coverage is necessary.
