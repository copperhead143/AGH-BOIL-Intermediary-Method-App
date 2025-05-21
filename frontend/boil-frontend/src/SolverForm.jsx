import React, { useState } from "react";
import axios from "axios";

const SolverForm = () => {
    const [supply, setSupply] = useState([20, 30]);
    const [demand, setDemand] = useState([10, 28, 27]);
    const [purchaseCosts, setPurchaseCosts] = useState([10, 12]);
    const [sellingPrices, setSellingPrices] = useState([30, 25, 30]);
    const [transportCosts, setTransportCosts] = useState([
        [8, 14, 17],
        [12, 9, 19],
    ]);

    const [result, setResult] = useState(null);
    const [error, setError] = useState("");

    const handleTransportChange = (i, j, value) => {
        const updatedCosts = [...transportCosts];
        updatedCosts[i][j] = parseFloat(value);
        setTransportCosts(updatedCosts);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const payload = {
                a: supply,
                b: demand,
                kz: purchaseCosts,
                c: sellingPrices,
                kt: transportCosts,
            };

            const res = await axios.post("http://localhost:8000/api/solve/", payload);
            setResult(res.data);
            setError("");
        } catch (err) {
            console.error("Błąd podczas wysyłania:", err);
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
                        <th className="title-header"></th>
                        <th className="title-header">\/PODAŻ | POPYT{">"}</th>
                        {demand.map((_, j) => (
                            <th key={j} className="popyt">
                                <div className="popyt-label">Odbiorca {j + 1}</div>
                                <input
                                    type="number"
                                    value={sellingPrices[j]}
                                    onChange={(e) => {
                                        const updated = [...sellingPrices];
                                        updated[j] = parseFloat(e.target.value);
                                        setSellingPrices(updated);
                                    }}
                                    className="popyt-input"
                                />
                            </th>
                        ))}
                        <th className="title-header">Koszt zakupu</th>
                    </tr>
                    </thead>

                    <tbody>
                    {supply.map((_, i) => (
                        <tr key={i}>
                            <td className="podaz-label">Dostawca {i + 1}</td>
                            <td>
                                <input
                                    type="number"
                                    value={supply[i]}
                                    onChange={(e) => {
                                        const updated = [...supply];
                                        updated[i] = e.target.value;
                                        setSupply(updated);
                                    }}
                                />
                            </td>
                            {demand.map((_, j) => (
                                <td key={j}>
                                    <input
                                        type="number"
                                        value={transportCosts[i][j]}
                                        onChange={(e) => handleTransportChange(i, j, e.target.value)}
                                    />
                                </td>
                            ))}
                            <td>
                                <input
                                    type="number"
                                    value={purchaseCosts[i]}
                                    onChange={(e) => {
                                        const updated = [...purchaseCosts];
                                        updated[i] = e.target.value;
                                        setPurchaseCosts(updated);
                                    }}
                                />
                            </td>
                        </tr>
                    ))}
                    <tr>
                        <td></td>
                        <th>Koszt Transportu</th>
                        {demand.map((_, j) => (
                            <td key={j}>
                                <input
                                    type="number"
                                    value={demand[j]}
                                    onChange={(e) => {
                                        const updated = [...demand];
                                        updated[j] = e.target.value;
                                        setDemand(updated);
                                    }}
                                />
                            </td>
                        ))}
                        <td colSpan={2}></td>
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
                    <h2 className="result-title">Wynik:</h2>
                    <p><strong>Zysk całkowity:</strong> {result.total_profit.toFixed(2)}</p>
                    <p className="critical-path">Macierz x<sub>ij</sub>:</p>
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
                </div>
            )}
        </div>
    );
};

export default SolverForm;
