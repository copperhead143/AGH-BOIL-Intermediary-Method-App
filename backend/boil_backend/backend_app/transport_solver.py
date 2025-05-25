import numpy as np
from scipy.optimize import linprog

import numpy as np
from scipy.optimize import linprog

def solve_transport_problem(data):
    a = np.array(data["a"], dtype=float) #podaz
    b = np.array(data["b"], dtype=float) #popyt
    kz = np.array(data["kz"], dtype=float) #koszty zakupu
    c = np.array(data["c"], dtype=float) #cena sprzedazy
    kt = np.array(data["kt"], dtype=float) #koszty transportu

    m, n = len(a), len(b)

    # Zrównoważenie problemu (jeśli jest niezbilansowany)
    if sum(a) > sum(b):
        diff = sum(a) - sum(b)
        b.append(diff)
        c.append(0)
        for i in range(len(kt)):
            kt[i].append(0)
    elif sum(a) < sum(b):
        diff = sum(b) - sum(a)
        a.append(diff)
        kz.append(0)
        kt.append([0] * len(b))

    # Aktualizacja wymiarów
    m, n = len(a), len(b)

    # Obliczanie zysku jednostkowego
    zij = [[c[j] - kz[i] - kt[i][j] for j in range(n)] for i in range(m)]
    zij_flat = [-zij[i][j] for i in range(m) for j in range(n)]

    # Ograniczenia
    A_eq = []
    b_eq = []

    # Dostawcy
    for i in range(m):
        row = [1 if k // n == i else 0 for k in range(m * n)]
        A_eq.append(row)
        b_eq.append(a[i])

    # Odbiorcy
    for j in range(n):
        row = [1 if k % n == j else 0 for k in range(m * n)]
        A_eq.append(row)
        b_eq.append(b[j])

    bounds = [(0, None)] * (m * n)

    result = linprog(
        c=zij_flat,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="highs"
    )

    if result.success:
        x = result.x.reshape((m, n))
        total_profit = -result.fun
        return {
            "success": True,
            "xij": x.tolist(),
            "total_profit": total_profit
        }
    else:
        return {
            "success": False,
            "message": result.message
        }
