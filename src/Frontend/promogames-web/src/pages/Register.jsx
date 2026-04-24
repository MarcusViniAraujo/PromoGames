import logo from "../assets/favicon1.svg";
import { Link } from "react-router-dom";

// Componente simples para reaproveitar o estilo do Input
const InputField = ({ placeholder, type = "text" }) => (
  <input
    className="w-full p-3 rounded-md border border-[var(--border)] bg-[var(--bg)] text-[var(--text)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
    placeholder={placeholder}
    type={type}
  />
);

function Register() {
  return (
    <div className="flex flex-col items-center justify-start  p-4 bg-[var(--bg)] pt-32">
      <div className="w-full max-w-sm flex flex-col items-center gap-6 p-8 rounded-xl border border-[var(--border)] shadow-[var(--shadow)] bg-[var(--bg)]">
        <img className="w-20 h-20" src={logo} alt="Logo do PromoGames" />

        <h1 className="text-2xl font-bold text-[var(--text-h)]">
          Cadastrar-se
        </h1>

        <InputField placeholder="Email" type="email" />
        <InputField placeholder="Senha" type="password" />
        <InputField placeholder="Confirmar Senha" type="password" />

        <button className="w-full bg-[var(--accent)] text-white p-3 rounded-md font-semibold hover:opacity-90 transition-opacity">
          Criar Conta
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
