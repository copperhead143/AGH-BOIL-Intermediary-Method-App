import numpy as np
from scipy.optimize import linprog

def solve_transport_problem(data):
    """
    data powinno zawierać:
      - a:   list<float>         # podaż od każdego dostawcy
      - b:   list<float>         # popyt każdego odbiorcy
      - kz:  list<float>         # koszt zakupu u każdego dostawcy
      - c:   list<float>         # cena sprzedaży u każdego odbiorcy
      - kt:  list[list<float>]   # koszty transportu od i do j
    """

    # ─── 1) Parsowanie i zapamiętanie oryginałów ─────────────────────────────
    a  = np.array(data["a"], dtype=float)
    b  = np.array(data["b"], dtype=float)
    kz = np.array(data["kz"], dtype=float)
    c  = np.array(data["c"], dtype=float)
    kt = np.array(data["kt"], dtype=float)

    orig_m, orig_n = len(a), len(b)
    orig_kz       = kz.copy()
    orig_c        = c.copy()
    orig_kt       = kt.copy()

    # ─── 2) Automatyczne balansowanie supply/demand ──────────────────────────
    total_supply = a.sum()
    total_demand = b.sum()

    if total_demand > total_supply:
        # dodajemy "fikcyjnego dostawcę"
        diff = total_demand - total_supply
        a  = np.append(a, diff)
        kz = np.append(kz, 0.0)
        # koszty transportu z fikcyjnego dostawcy = cena sprzedaży,
        # by profit z tych x_ij był 0
        kt = np.vstack([kt, orig_c])
    elif total_supply > total_demand:
        # dodajemy "fikcyjnego odbiorcę"
        diff = total_supply - total_demand
        b = np.append(b, diff)
        c = np.append(c, 0.0)
        # koszty transportu do fikcyjnego odbiorcy = 0,
        # by profit = -kz (czyli strata zakupu bez sprzedaży)
        dummy_col = np.zeros((len(a), 1))
        kt = np.hstack([kt, dummy_col])

    # nowe wymiary
    m, n = len(a), len(b)

    # ─── 3) Wektor funkcji celu: minimalizujemy (kz_i + kt_ij - c_j) * x_ij ───
    C = (kz.reshape(-1, 1) + kt - c.reshape(1, -1)).reshape(-1)

    # ─── 4) Macierz ograniczeń równości (podaż + popyt) ──────────────────────
    A_eq = []

    # ∑_j x_ij = a_i
    for i in range(m):
        row = np.zeros(m * n)
        row[i * n:(i + 1) * n] = 1
        A_eq.append(row)

    # ∑_i x_ij = b_j
    for j in range(n):
        row = np.zeros(m * n)
        row[j::n] = 1
        A_eq.append(row)

    A_eq = np.vstack(A_eq)
    b_eq = np.concatenate([a, b])

    # ─── 5) Bounds: x_ij ≥ 0 ────────────────────────────────────────────────
    bounds = [(0, None)] * (m * n)

    # ─── 6) Rozwiązanie za pomocą HiGHS ───────────────────────────────────
    result = linprog(
        C,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="highs"
    )

    # ─── 7) Parsowanie i przycinanie wyników ───────────────────────────────
    if not result.success:
        return {
            "success": False,
            "message": result.message
        }

    # pełna macierz x (m × n)
    x_full = result.x.reshape((m, n))

    # obcinamy do oryginalnych wymiarów
    x             = x_full[:orig_m, :orig_n]
    unit_profits  = (
        (orig_c.reshape(1, -1) - orig_kz.reshape(-1, 1) - orig_kt)
    )

    # ─── 8) Metryki biznesowe ────────────────────────────────────────────────
    revenue_total        = float((x * orig_c.reshape(1, -1)).sum())
    purchase_cost_total  = float((x * orig_kz.reshape(-1, 1)).sum())
    transport_cost_total = float((x * orig_kt).sum())
    cost_total           = purchase_cost_total + transport_cost_total
    total_profit         = revenue_total - cost_total

    # ─── 9) Zwracamy gotowe dane ───────────────────────────────────────────
    return {
        "success": True,
        "xij": x.tolist(),
        "unit_profits": unit_profits.tolist(),
        "cost_total": cost_total,
        "revenue_total": revenue_total,
        "total_profit": total_profit
    }
