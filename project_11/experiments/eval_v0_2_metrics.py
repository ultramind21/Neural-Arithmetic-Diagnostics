import numpy as np

# =========================
# System Definition (V0.2)
# Robustness variant: per-family heterogeneity weights
# =========================

BASE = {
    "A": 0.50,
    "B": 0.48,
    "C": 0.47,
    "D": 0.49,
}

SIGNS = {
    "A": 1,
    "B": -1,
    "C": 1,
    "D": -1,
}

# V0.2 addition: families respond with different magnitudes to heterogeneity
# (asymmetric on purpose, to test robustness of H)
WEIGHTS = {
    "A": 0.25,
    "B": 1.00,
    "C": 1.60,
    "D": 0.55,
}


def U(u_power: float) -> float:
    """Universal intervention function (monotonic, diminishing returns)."""
    return 1 - np.exp(-u_power)


def compute_metrics(h_scale: float, u_power: float):
    """
    Compute:
      - P = mean_f(Δ_uni_f)
      - H = Var_f(Δ_fam_f)

    V0.2 heterogeneity:
      residual_f = sign_f * weight_f * h_scale
      G_fam_f = G_uni_f + residual_f

    Expectations:
      - P increases with u_power, independent of h_scale
      - H increases with h_scale, independent of u_power
      - With variance metric, H should scale ~ h_scale^2
    """
    G_base = []
    G_uni = []
    G_fam = []
    delta_fam_list = []

    for f in BASE:
        g_base = BASE[f]
        g_uni = g_base + U(u_power)

        residual = SIGNS[f] * WEIGHTS[f] * h_scale
        g_fam = g_uni + residual

        G_base.append(g_base)
        G_uni.append(g_uni)
        G_fam.append(g_fam)

        # store heterogeneity gain explicitly
        delta_fam_list.append(residual)

    G_base = np.array(G_base, dtype=float)
    G_uni = np.array(G_uni, dtype=float)

    delta_uni = G_uni - G_base
    delta_fam = np.array(delta_fam_list, dtype=float)  # equals G_fam - G_uni by construction

    P = float(np.mean(delta_uni))
    H = float(np.var(delta_fam))

    return P, H


# =========================
# Sweeps
# =========================

h_values = np.linspace(0.0, 0.02, 10)
u_values = np.linspace(0.1, 0.5, 10)


# =========================
# Analysis Helpers
# =========================

def is_monotonic(values):
    return all(x <= y for x, y in zip(values, values[1:]))


def almost_constant(values, tol=1e-12):
    values = np.array(values, dtype=float)
    return (np.max(values) - np.min(values)) < tol


# =========================
# Checks
# =========================

print("\n==============================")
print("PROJECT 11 — FOUNDATION")
print("V0.2 ROBUSTNESS CHECK")
print("==============================\n")

print("WEIGHTS:", WEIGHTS)

# P vs u_power (fix h)
print("\n=== P vs u_power (fixed h=0.01) ===")
P_list = []
for u in u_values:
    P, _ = compute_metrics(0.01, u)
    P_list.append(P)
    print(f"u={u:.3f} -> P={P:.6f}")
print("Monotonic:", is_monotonic(P_list))

# H vs h_scale (fix u)
print("\n=== H vs h_scale (fixed u=0.3) ===")
H_list = []
for h in h_values:
    _, H = compute_metrics(h, 0.3)
    H_list.append(H)
    print(f"h={h:.4f} -> H={H:.12f}")
print("Monotonic:", is_monotonic(H_list))

# Independence check
print("\n=== Independence Check (V0.2) ===")

# H vs u_power (fix h)
H_vs_u = []
for u in u_values:
    _, H = compute_metrics(0.01, u)
    H_vs_u.append(H)
print(f"H range across u (h=0.01): {min(H_vs_u):.12f} .. {max(H_vs_u):.12f}")
print("H independent of u_power:", almost_constant(H_vs_u, tol=1e-12))

# P vs h_scale (fix u)
P_vs_h = []
for h in h_values:
    P, _ = compute_metrics(h, 0.3)
    P_vs_h.append(P)
print(f"P range across h (u=0.3): {min(P_vs_h):.12f} .. {max(P_vs_h):.12f}")
print("P independent of h_scale:", almost_constant(P_vs_h, tol=1e-12))

# Quadratic scaling sanity check: H / h^2 should be ~ constant (for h > 0)
print("\n=== Quadratic Scaling Sanity (H ~ h^2) ===")
unit_residuals = np.array([SIGNS[f] * WEIGHTS[f] for f in BASE], dtype=float)  # residuals when h_scale=1
expected_coeff = float(np.var(unit_residuals))
print(f"Expected coefficient Var(sign*weight) = {expected_coeff:.12f}")

ratios = []
for h in h_values:
    if h == 0:
        continue
    _, H = compute_metrics(h, 0.3)
    ratios.append(H / (h * h))

print(f"Observed H/h^2 range: {min(ratios):.12f} .. {max(ratios):.12f}")
print("H/h^2 almost constant:", almost_constant(ratios, tol=1e-10))
