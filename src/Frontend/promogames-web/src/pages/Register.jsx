import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/favicon1.svg";

const InputField = ({
  placeholder,
  type = "text",
  value,
  onChange,
  onKeyDown,
}) => (
  <input
    className="w-full p-3 rounded-md border border-[var(--border)] bg-[var(--bg)] text-[var(--text)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
    placeholder={placeholder}
    type={type}
    value={value}
    onChange={onChange}
    onKeyDown={onKeyDown}
  />
);

function Register() {
  const navigate = useNavigate();
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");
  const [chatId, setChatId] = useState("");
  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleCadastro(e) {
    e.preventDefault();
    setErro("");
    setSucesso("");

    // Validações no cliente
    if (!nome.trim()) return setErro("Informe seu nome.");
    if (!email.trim()) return setErro("Informe seu e-mail.");
    if (senha.length < 6)
      return setErro("A senha deve ter pelo menos 6 caracteres.");
    if (senha !== confirmarSenha) return setErro("As senhas não coincidem.");

    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/cadastro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, email, senha, chat_id: chatId }),
      });

      const data = await res.json();

      if (!res.ok) {
        setErro(data.detail || "Erro ao cadastrar.");
        return;
      }

      setSucesso("Conta criada com sucesso! Redirecionando...");
      setTimeout(() => navigate("/"), 1800);
    } catch {
      setErro("Não foi possível conectar ao servidor.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col items-center justify-start p-4 bg-[var(--bg)] pt-20">
      <div className="w-full max-w-sm flex flex-col items-center gap-5 p-8 rounded-xl border border-[var(--border)] shadow-[var(--shadow)] bg-[var(--bg)]">
        <img className="w-20 h-20" src={logo} alt="Logo do PromoGames" />

        <h1 className="text-2xl font-bold text-[var(--text-h)]">
          Cadastrar-se
        </h1>

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

        {/* Mensagem de sucesso */}
        {sucesso && (
          <div
            className="w-full px-4 py-3 rounded-md text-sm font-medium text-center"
            style={{
              background: "rgba(74,222,128,0.1)",
              border: "1px solid rgba(74,222,128,0.35)",
              color: "#4ade80",
            }}
          >
            {sucesso}
          </div>
        )}

        <InputField
          placeholder="Nome"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
        />

        <InputField
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <InputField
          placeholder="Senha"
          type="password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />

        <InputField
          placeholder="Confirmar Senha"
          type="password"
          value={confirmarSenha}
          onChange={(e) => setConfirmarSenha(e.target.value)}
        />

        {/* Campo opcional para Telegram */}
        <div className="w-full">
          <InputField
            placeholder="Chat ID do Telegram (opcional)"
            value={chatId}
            onChange={(e) => setChatId(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleCadastro(e)}
          />
          <p
            className="text-xs mt-1.5"
            style={{ color: "var(--text)", opacity: 0.6 }}
          >
            Necessário para receber alertas de promoção via Telegram.
          </p>
        </div>

        <button
          onClick={handleCadastro}
          disabled={loading}
          className="w-full bg-[var(--accent)] text-white p-3 rounded-md font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Criando conta..." : "Criar Conta"}
        </button>

        <p className="text-sm text-[var(--text)]">
          Já tem uma conta?{" "}
          <Link
            to="/"
            className="text-[var(--accent)] hover:underline font-semibold"
          >
            Entrar
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
