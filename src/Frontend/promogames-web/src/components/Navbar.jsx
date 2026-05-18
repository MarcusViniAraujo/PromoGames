import { Link, useLocation, useNavigate } from "react-router-dom";
import logo from "../assets/favicon1.svg";
import usericon from "../assets/usericon.svg";

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const isLoginPage = location.pathname === "/";
  const isNewUserPage = location.pathname === "/register";

  const handleLogout = () => {
    localStorage.removeItem("promogames_user"); // Remove os dados do usuário
    navigate("/"); // Manda de volta para o login
  };

  return (
    <nav className="flex justify-between items-center p-4 border-b border-[var(--border)]">
      <Link
        to="/dashboard"
        className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
      >
        <img className="w-10 h-10" src={logo} alt="Logo do PromoGames" />
        <h2 className="text-[var(--text-h)] font-bold">PromoGames</h2>
      </Link>

      {/* Grupo da Direita */}
      <div className="flex items-center gap-4">
        {!isLoginPage && !isNewUserPage && (
          <>
            {/* Ícone do Perfil */}
            <Link
              to="/perfil"
              className="cursor-pointer hover:opacity-80 transition-opacity"
            >
              <img className="w-8 h-8" src={usericon} alt="Ícone do Usuário" />
            </Link>

            {/* Botão de Sair */}
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-red-500 border border-red-500/30 rounded-md hover:bg-red-500/10 transition-colors"
            >
              Sair
            </button>
          </>
        )}
      </div>
    </nav>
  );
}
