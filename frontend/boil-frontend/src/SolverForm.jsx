import React, { useState } from "react";
import axios from "axios";

const SolverForm = () => {
    // Ustawienie stanu początkowego dla wszystkich danych
    const [supply, setSupply] = useState([20, 30]);  // Wartości dla podaży
    const [demand, setDemand] = useState([10, 28, 27]);  // Wartości dla popytu
    const [purchaseCosts, setPurchaseCosts] = useState([10, 12]);  // Wartości kosztów zakupu
    const [sellingPrices, setSellingPrices] = useState([30, 25, 30]);  // Ceny sprzedaży
    const [transportCosts, setTransportCosts] = useState([
        [8, 14, 17],
        [12, 9, 19],
    ]);  // Koszty transportu (macierz)

    const [result, setResult] = useState(null);
    const [error, setError] = useState("");

    // Funkcja obsługująca zmianę danych w macierzy kosztów transportu
    const handleTransportChange = (i, j, value) => {
        const updatedCosts = [...transportCosts];
        updatedCosts[i][j] = parseFloat(value);
        setTransportCosts(updatedCosts);
    };

    // Funkcja do wysyłania danych na serwer
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

            console.log("Wysyłam dane:", payload);  // Dodaj logi, by zobaczyć, co jest wysyłane

            const res = await axios.post("http://localhost:8000/api/solve/", payload);

            console.log("Odpowiedź z serwera:", res.data);  // Dodaj logi odpowiedzi serwera
            setResult(res.data);
            setError("");  // Wyczyść poprzedni błąd
        } catch (err) {
            console.error("Błąd podczas wysyłania:", err);
            setError("Błąd podczas przetwarzania danych.");
        }
    };


    return (
        <div className="bg-white shadow-md rounded p-6 max-w-3xl mx-auto">
            <form onSubmit={handleSubmit}>
                <div className="p-4">
                    <table className="table-auto border border-gray-400">
                        <thead>
                        <tr>
                            <th></th>
                            <th>\/PODAŻ | POPYT{">"}</th>
                            {demand.map((_, j) => (
                                <th key={j}>
                                    Odbiorca {j + 1}
                                    <br />
                                    <input
                                        type="number"
                                        placeholder="cj"
                                        value={sellingPrices[j]}
                                        onChange={(e) => {
                                            const updated = [...sellingPrices];
                                            updated[j] = parseFloat(e.target.value);``
                                            setSellingPrices(updated);
                                        }}
                                        className="w-16 border"
                                    />
                                </th>
                            ))}
                            <th>Koszt zakupu</th>
                        </tr>
                        </thead>
                        <tbody>
                        {supply.map((_, i) => (
                            <tr key={i}>
                                <td>Dostawca {i + 1}</td>
                                <td>
                                    <input
                                        type="number"
                                        placeholder="ai"
                                        value={supply[i]}
                                        onChange={(e) => {
                                            const updated = [...supply];
                                            updated[i] = e.target.value;
                                            setSupply(updated);
                                        }}
                                        className="w-16 border"
                                    />
                                </td>
                                {demand.map((_, j) => (
                                    <td key={j}>
                                        <input
                                            type="number"
                                            value={transportCosts[i][j]}
                                            onChange={(e) => handleTransportChange(i, j, e.target.value)}
                                            className="w-16 border"
                                        />
                                    </td>
                                ))}
                                <td>
                                    <input
                                        type="number"
                                        placeholder="kz"
                                        value={purchaseCosts[i]}
                                        onChange={(e) => {
                                            const updated = [...purchaseCosts];
                                            updated[i] = e.target.value;
                                            setPurchaseCosts(updated);
                                        }}
                                        className="w-16 border"
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
                                        placeholder="bj"
                                        value={demand[j]}
                                        onChange={(e) => {
                                            const updated = [...demand];
                                            updated[j] = e.target.value;
                                            setDemand(updated);
                                        }}
                                        className="w-16 border"
                                    />
                                </td>
                            ))}
                            <td colSpan={2}></td>
                        </tr>
                        </tbody>
                    </table>
                </div>

                <button
                    type="submit"
                    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                    Oblicz
                </button>
            </form>

            {/* Wyświetlanie komunikatu o błędzie */}
            {error && <p className="text-red-500 mt-4">{error}</p>}

            {/* Wyświetlanie wyników */}
            {result && result.success && (
                <div className="mt-6">
                    <h2 className="text-xl font-bold mb-2">Wynik:</h2>
                    <p><strong>Zysk całkowity:</strong> {result.total_profit.toFixed(2)}</p>
                    <p className="mt-2 font-semibold">Macierz x<sub>ij</sub>:</p>
                    <table className="mt-1 border-collapse border">
                        <tbody>
                        {result.xij.map((row, i) => (
                            <tr key={i}>
                                {row.map((val, j) => (
                                    <td
                                        key={j}
                                        className="border px-3 py-1 text-center"
                                    >
                                        {val.toFixed(2)}
                                    </td>
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
