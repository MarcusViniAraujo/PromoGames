import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [jogos, setJogos] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/listar_jogos/1")
      .then((res) => setJogos(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1 style={{ color: "var(--text-h)" }}>Meus Jogos Monitorados</h1>
      <div style={{ display: "grid", gap: "1rem" }}>
        {jogos.map((jogo, index) => (
          <div key={index} className="card">
            <h3 style={{ color: "var(--text-h)" }}>{jogo.nome}</h3>
            <p>
              Preço atual: <strong>R$ {jogo.preco}</strong>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
