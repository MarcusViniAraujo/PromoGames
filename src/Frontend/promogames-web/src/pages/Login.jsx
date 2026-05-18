import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/favicon1.svg";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(e) {
    e.preventDefault();
    setErro("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha }),
      });

      const data = await res.json();

      if (!res.ok) {
        setErro(data.detail || "Erro ao fazer login.");
        return;
      }

      // Salva o usuário logado para uso no Dashboard
      localStorage.setItem("promogames_user", JSON.stringify(data));
      navigate("/dashboard");
    } catch {
      setErro("Não foi possível conectar ao servidor.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col items-center justify-start p-4 bg-[var(--bg)] pt-32">
      <div className="w-full max-w-sm flex flex-col items-center gap-5 p-8 rounded-xl border border-[var(--border)] shadow-[var(--shadow)] bg-[var(--bg)]">
        <img className="w-20 h-20" src={logo} alt="Logo do PromoGames" />

        <h1 className="text-2xl font-bold text-[var(--text-h)]">Login</h1>

        {/* Mensagem de erro */}
        {erro && (
          <div
            className="w-full px-4 py-3 rounded-md text-sm font-medium text-center"
            style={{
              background: "rgba(239,68,68,0.1)",
              border: "1px solid rgba(239,68,68,0.35)",
              color: "#f87171",
            }}
          >
            {erro}
          </div>
        )}

        <input
          className="w-full p-3 rounded-md border border-[var(--border)] bg-[var(--bg)] text-[var(--text)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleLogin(e)}
        />

        <input
          className="w-full p-3 rounded-md border border-[var(--border)] bg-[var(--bg)] text-[var(--text)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
          placeholder="Senha"
          type="password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleLogin(e)}
        />

        <button
          onClick={handleLogin}
          disabled={loading}
          className="w-full bg-[var(--accent)] text-white p-3 rounded-md font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>

        <p className="text-sm text-[var(--text)]">
          Não tem uma conta?{" "}
          <Link
            to="/register"
            className="text-[var(--accent)] hover:underline font-semibold"
          >
            Cadastrar-se
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
