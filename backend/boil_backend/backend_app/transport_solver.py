import numpy as np
from scipy.optimize import linprog

def solve_transport_problem(data):
    """
    data powinno zawierać:
      - a: list<float>   # podaż od każdego dostawcy
      - b: list<float>   # popyt każdego odbiorcy
      - kz: list<float>  # koszt zakupu u każdego dostawcy
      - c: list<float>   # cena sprzedaży u każdego odbiorcy
      - kt: list[list<float>]  # koszty transportu od i do j
    """
    # 1) Parsowanie wejścia
    a  = np.array(data["a"], dtype=float)
    b  = np.array(data["b"], dtype=float)
    kz = np.array(data["kz"], dtype=float)
    c  = np.array(data["c"], dtype=float)
    kt = np.array(data["kt"], dtype=float)

    m, n = len(a), len(b)

    # 2) Wektor funkcji celu: minimalizujemy (kz_i + kt_ij - c_j) * x_ij
    C = (kz.reshape(-1,1) + kt - c.reshape(1,-1)).reshape(-1)

    # 3) Macierz ograniczeń równości (podaż + popyt)
    A_eq = []
    #   ∑_j x_ij = a_i
    for i in range(m):
        row = np.zeros(m * n)
        row[i*n:(i+1)*n] = 1
        A_eq.append(row)
    #   ∑_i x_ij = b_j
    for j in range(n):
        row = np.zeros(m * n)
        row[j::n] = 1
        A_eq.append(row)

    A_eq = np.vstack(A_eq)
    b_eq = np.concatenate([a, b])

    # 4) Granice: x_ij ≥ 0
    bounds = [(0, None)] * (m * n)

    # 5) Rozwiązanie
    result = linprog(C,
                     A_eq=A_eq,
                     b_eq=b_eq,
                     bounds=bounds,
                     method="highs")

    # 6) Parsowanie wyniku
    if result.success:
        x = result.x.reshape((m, n))
        # ← tak jak było: total_profit = -result.fun
        total_profit = -result.fun

        # ───── dodatkowe metryki ────────────────────────────────────────
        #  a) macierz jednostkowych zysków p_ij = c_j - kz_i - kt_ij
        unit_profits = (c.reshape(1,-1) - kz.reshape(-1,1) - kt)

        #  b) sumaryczne wartości
        revenue_total        = float((x * c.reshape(1,-1)).sum())
        purchase_cost_total  = float((x * kz.reshape(-1,1)).sum())
        transport_cost_total = float((x * kt).sum())
        cost_total           = purchase_cost_total + transport_cost_total
        # ────────────────────────────────────────────────────────────────

        return {
            "success": True,
            "xij": x.tolist(),
            "unit_profits": unit_profits.tolist(),
            "cost_total": cost_total,
            "revenue_total": revenue_total,
            "total_profit": total_profit
        }
    else:
        return {
            "success": False,
            "message": result.message
        }
