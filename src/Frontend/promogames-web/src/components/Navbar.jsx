import { Link, useLocation } from "react-router-dom";
import logo from "../assets/favicon1.svg";
import usericon from "../assets/usericon.svg";

export default function Navbar() {
  const location = useLocation();
  const isLoginPage = location.pathname === "/";
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
      <div className="flex items-center gap-6">
        {!isLoginPage && (
          <Link
            to="/"
            className="cursor-pointer hover:opacity-80 transition-opacity"
          >
            <img className="w-8 h-8" src={usericon} alt="Ícone do Usuário" />
          </Link>
        )}
      </div>
    </nav>
  );
}
