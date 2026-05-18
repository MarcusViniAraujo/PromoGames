import { Navigate } from "react-router-dom";

// Envolve qualquer rota que exige login.
// Se não houver usuário no localStorage, redireciona para "/" imediatamente,
// sem piscar a página protegida.
export default function ProtectedRoute({ children }) {
  const user = localStorage.getItem("promogames_user");

  if (!user) {
    return <Navigate to="/" replace />;
  }

  return children;
}
