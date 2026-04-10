import numpy as np

# =========================
# System Definition (V0.1)
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


def U(u_power: float) -> float:
    """Universal intervention function (monotonic, diminishing returns)."""
    return 1 - np.exp(-u_power)


def compute_metrics(h_scale: float, u_power: float):
    """
    Compute:
      - P = mean_f(Δ_uni_f)
      - H = Var_f(Δ_fam_f)

    V0.1 fix:
      - Heterogeneity is SIGNED (no abs), so families receive different gains/losses.
    """
    G_base = []
    G_uni = []
    G_fam = []

    for f in BASE:
        base = BASE[f]
        sign = SIGNS[f]

        # Base
        g_base = base

        # Universal (same functional form for all families)
        g_uni = g_base + U(u_power)

        # Heterogeneity (SIGNED)  <-- critical fix vs V0
        residual = sign * h_scale
        g_fam = g_uni + residual

        G_base.append(g_base)
        G_uni.append(g_uni)
        G_fam.append(g_fam)

    G_base = np.array(G_base, dtype=float)
    G_uni = np.array(G_uni, dtype=float)
    G_fam = np.array(G_fam, dtype=float)

    # Per-family gains
    delta_uni = G_uni - G_base
    delta_fam = G_fam - G_uni

    # Metrics
    P = float(np.mean(delta_uni))
    H = float(np.var(delta_fam))  # note: with signed residuals, H ~ h_scale^2

    return P, H


# =========================
# Sweeps
# =========================

h_values = np.linspace(0.0, 0.02, 10)
u_values = np.linspace(0.1, 0.5, 10)

results = []
for h in h_values:
    for u in u_values:
        P, H = compute_metrics(h, u)
        results.append((h, u, P, H))


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


# Independence check (correct definition: near-constant, not monotonic)
print("\n=== Independence Check (V0.1) ===")

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