import React, { useState } from "react";
import axios from "axios";

const SolverForm = () => {
  // stany na wartości wejściowe
  const [supply, setSupply] = useState([20, 30]);
  const [demand, setDemand] = useState([10, 28, 27]);
  const [purchaseCosts, setPurchaseCosts] = useState([10, 12]);
  const [sellingPrices, setSellingPrices] = useState([30, 25, 30]);
  const [transportCosts, setTransportCosts] = useState([
    [8, 14, 17],
    [12, 9, 19],
  ]);

  // stan na wynik i ewentualny błąd
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // 1) Przygotuj payload
    const payload = {
      a: supply,
      b: demand,
      kz: purchaseCosts,
      c: sellingPrices,
      kt: transportCosts,
    };
    console.log("📤 WYSYŁAM payload:", payload);

    try {
      // 2) Wyślij do /api/solve/ (proxy lub pełny URL)
      const res = await axios.post("/api/solve/", payload);
      console.log("✅ OTRZYMAŁEM odpowiedź:", res);
      setResult(res.data);
      setError("");
    } catch (err) {
      console.error("❌ BŁĄD HTTP", err);
      setError("Błąd podczas przetwarzania danych.");
    }
  };

  return (
    <div className="container">
      <h1 className="title center">Transport Solver</h1>

      <form onSubmit={handleSubmit}>
        <table className="transport-table">
          <thead>
            <tr>
              <th></th>
              <th>Podaż / Popyt</th>
              {demand.map((_, j) => (
                <th key={j}>
                  <div>Odbiorca {j + 1}</div>
                  <input
                    type="number"
                    value={sellingPrices[j]}
                    onChange={(e) => {
                      const upd = [...sellingPrices];
                      upd[j] = parseFloat(e.target.value);
                      setSellingPrices(upd);
                    }}
                  />
                </th>
              ))}
              <th>Zakup</th>
            </tr>
          </thead>
          <tbody>
            {supply.map((_, i) => (
              <tr key={i}>
                <td>Dostawca {i + 1}</td>
                <td>
                  <input
                    type="number"
                    value={supply[i]}
                    onChange={(e) => {
                      const upd = [...supply];
                      upd[i] = parseFloat(e.target.value);
                      setSupply(upd);
                    }}
                  />
                </td>
                {transportCosts[i].map((_, j) => (
                  <td key={j}>
                    <input
                      type="number"
                      value={transportCosts[i][j]}
                      onChange={(e) => {
                        const costs = transportCosts.map((r) => [...r]);
                        costs[i][j] = parseFloat(e.target.value);
                        setTransportCosts(costs);
                      }}
                    />
                  </td>
                ))}
                <td>
                  <input
                    type="number"
                    value={purchaseCosts[i]}
                    onChange={(e) => {
                      const upd = [...purchaseCosts];
                      upd[i] = parseFloat(e.target.value);
                      setPurchaseCosts(upd);
                    }}
                  />
                </td>
              </tr>
            ))}
            <tr>
              <td></td>
              <th>Demand</th>
              {demand.map((_, j) => (
                <td key={j}>
                  <input
                    type="number"
                    value={demand[j]}
                    onChange={(e) => {
                      const upd = [...demand];
                      upd[j] = parseFloat(e.target.value);
                      setDemand(upd);
                    }}
                  />
                </td>
              ))}
              <td></td>
            </tr>
          </tbody>
        </table>

        <button type="submit" className="btn submit-btn">
          Oblicz
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}

      {result && result.success && (
        <div className="section">
          <h2>Wynik pośrednika:</h2>
          <p>
            <strong>Koszt całkowity:</strong> {result.cost_total.toFixed(2)}
          </p>
          <p>
            <strong>Przychód całkowity:</strong>{" "}
            {result.revenue_total.toFixed(2)}
          </p>
          <p>
            <strong>Zysk pośrednika:</strong> {result.total_profit.toFixed(2)}
          </p>

          <h3>1. Macierz optymalnych przewozów (x<sub>ij</sub>):</h3>
          <table className="result-table">
            <tbody>
              {result.xij.map((row, i) => (
                <tr key={i}>
                  {row.map((val, j) => (
                    <td key={j}>{val.toFixed(2)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>

          <h3>2. Macierz jednostkowych zysków (p<sub>ij</sub>):</h3>
          <table className="result-table">
            <tbody>
              {result.unit_profits.map((row, i) => (
                <tr key={i}>
                  {row.map((p, j) => (
                    <td key={j}>{p.toFixed(2)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default SolverForm;
