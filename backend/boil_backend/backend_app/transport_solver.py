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

    steps = []

    # ─── 1) Parsowanie wejścia ───────────────────────────────────────────────
    a  = np.array(data["a"], dtype=float)
    b  = np.array(data["b"], dtype=float)
    kz = np.array(data["kz"], dtype=float)
    c  = np.array(data["c"], dtype=float)
    kt = np.array(data["kt"], dtype=float)
    steps.append({
        "step": "parsed_input",
        "a": a.tolist(),
        "b": b.tolist(),
        "kz": kz.tolist(),
        "c": c.tolist(),
        "kt": kt.tolist(),
    })

    orig_m, orig_n = len(a), len(b)
    orig_kz, orig_c, orig_kt = kz.copy(), c.copy(), kt.copy()

    # ─── 2) Automatyczne balansowanie ────────────────────────────────────────
    total_supply = a.sum()
    total_demand = b.sum()
    steps.append({
        "step": "initial_totals",
        "total_supply": float(total_supply),
        "total_demand": float(total_demand),
    })

    if total_demand > total_supply:
        diff = total_demand - total_supply
        a  = np.append(a, diff)
        kz = np.append(kz, 0.0)
        kt = np.vstack([kt, orig_c])
        steps.append({
            "step": "add_dummy_supplier",
            "dummy_amount": float(diff),
            "new_a": a.tolist(),
            "new_kz": kz.tolist(),
            "new_kt_last_row": orig_c.tolist(),
        })

    elif total_supply > total_demand:
        diff = total_supply - total_demand
        b = np.append(b, diff)
        c = np.append(c, 0.0)
        dummy_col = np.zeros((len(a), 1))
        kt = np.hstack([kt, dummy_col])
        steps.append({
            "step": "add_dummy_consumer",
            "dummy_amount": float(diff),
            "new_b": b.tolist(),
            "new_c": c.tolist(),
            "new_kt_last_col": dummy_col.flatten().tolist(),
        })

    # ─── 3) Wektor funkcji celu ──────────────────────────────────────────────
    m, n = len(a), len(b)
    C = (kz.reshape(-1, 1) + kt - c.reshape(1, -1)).reshape(-1)
    steps.append({
        "step": "build_cost_vector",
        "C": C.tolist(),
        "shape": [m, n]
    })

    # ─── 4) Macierz ograniczeń równości ─────────────────────────────────────
    A_eq = []
    for i in range(m):
        row = np.zeros(m * n)
        row[i*n:(i+1)*n] = 1
        A_eq.append(row)
    for j in range(n):
        row = np.zeros(m * n)
        row[j::n] = 1
        A_eq.append(row)
    A_eq = np.vstack(A_eq)
    b_eq = np.concatenate([a, b])
    steps.append({
        "step": "build_constraints",
        "A_eq_rows": len(A_eq),
        "A_eq_cols": len(A_eq[0]),
        "b_eq": b_eq.tolist()
    })

    # ─── 5) Bounds ───────────────────────────────────────────────────────────
    bounds = [(0, None)] * (m * n)
    steps.append({
        "step": "set_bounds",
        "bounds_for_each_variable": "x_ij >= 0",
        "num_variables": m * n
    })

    # ─── 6) Rozwiązanie ──────────────────────────────────────────────────────
    result = linprog(
        C,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="simplex"
    )
    steps.append({
        "step": "linprog_result",
        "success": result.success,
        "status": result.message,
        "fun": result.fun if result.success else None
    })

    if not result.success:
        return {
            "success": False,
            "message": result.message,
            "steps": steps
        }

    # ─── 7) Parsowanie wyniku ────────────────────────────────────────────────
    x_full = result.x.reshape((m, n))
    steps.append({
        "step": "reshape_solution",
        "x_full_shape": [m, n],
        "x_full": x_full.tolist()
    })

    x = x_full[:orig_m, :orig_n]
    unit_profits = (orig_c.reshape(1, -1) - orig_kz.reshape(-1, 1) - orig_kt)
    steps.append({
        "step": "trim_solution_and_compute_unit_profits",
        "x_trimmed_shape": [orig_m, orig_n],
        "unit_profits": unit_profits.tolist()
    })

    # ─── 8) Metryki finansowe ────────────────────────────────────────────────
    revenue_total        = float((x * orig_c.reshape(1, -1)).sum())
    purchase_cost_total  = float((x * orig_kz.reshape(-1, 1)).sum())
    transport_cost_total = float((x * orig_kt).sum())
    cost_total           = purchase_cost_total + transport_cost_total
    total_profit         = revenue_total - cost_total
    steps.append({
        "step": "compute_totals",
        "revenue_total": revenue_total,
        "purchase_cost_total": purchase_cost_total,
        "transport_cost_total": transport_cost_total,
        "cost_total": cost_total,
        "total_profit": total_profit
    })

    # ─── 9) Zwracamy wynik wraz z krokami ────────────────────────────────────
    return {
        "success": True,
        "xij": x.tolist(),
        "unit_profits": unit_profits.tolist(),
        "cost_total": cost_total,
        "revenue_total": revenue_total,
        "total_profit": total_profit,
        "steps": steps
    }
