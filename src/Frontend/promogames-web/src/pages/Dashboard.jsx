import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

const BASE_URL = "http://localhost:8000";

export default function Dashboard() {
  const navigate = useNavigate();
  const [usuario, setUsuario] = useState(null);
  const [jogos, setJogos] = useState([]);
  const [topDeals, setTopDeals] = useState([]);
  const [loadingDeals, setLoadingDeals] = useState(true);
  const [busca, setBusca] = useState("");
  const [resultado, setResultado] = useState(null);
  const [precoResultado, setPrecoResultado] = useState(null);
  const [loadingBusca, setLoadingBusca] = useState(false);
  const [loadingAdicionar, setLoadingAdicionar] = useState(false);
  const [loadingJogos, setLoadingJogos] = useState(true);
  const [erroMsg, setErroMsg] = useState("");
  const [sucessoMsg, setSucessoMsg] = useState("");
  const [removendoId, setRemovendoId] = useState(null);

  // Filtro de pesquisa nos jogos monitorados
  const [filtroJogos, setFiltroJogos] = useState("");

  // Ref e estado do carrossel
  const carrosselRef = useRef(null);
  const [podeScrollEsq, setPodeScrollEsq] = useState(false);
  const [podeScrollDir, setPodeScrollDir] = useState(true);

  // 1. Verifica login ao entrar na página
  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("promogames_user") || "null");
    if (!user) {
      navigate("/");
      return;
    }
    setUsuario(user);
  }, [navigate]);

  // 2. Busca jogos monitorados e promoções quando o usuário for definido
  useEffect(() => {
    if (usuario) {
      carregarJogos();
      carregarMelhoresPromocoes();
    }
  }, [usuario]);

  // Atualiza disponibilidade dos botões de scroll
  function atualizarBotoesScroll() {
    const el = carrosselRef.current;
    if (!el) return;
    setPodeScrollEsq(el.scrollLeft > 4);
    setPodeScrollDir(el.scrollLeft + el.clientWidth < el.scrollWidth - 4);
  }

  function scrollCarrossel(direcao) {
    const el = carrosselRef.current;
    if (!el) return;
    el.scrollBy({ left: direcao * 220, behavior: "smooth" });
    // Atualiza botões após animação terminar
    setTimeout(atualizarBotoesScroll, 350);
  }

  async function carregarJogos() {
    setLoadingJogos(true);
    try {
      const res = await fetch(`${BASE_URL}/listar_jogos/${usuario.id}`);
      const data = await res.json();
      setJogos(data);
    } catch {
      setErroMsg("Erro ao carregar jogos.");
    } finally {
      setLoadingJogos(false);
    }
  }

  async function carregarMelhoresPromocoes() {
    setLoadingDeals(true);
    try {
      const res = await fetch(`${BASE_URL}/api/top-deals`);
      if (!res.ok) throw new Error();
      const data = await res.json();
      setTopDeals(data);
    } catch {
      setTopDeals([]);
    } finally {
      setLoadingDeals(false);
    }
  }

  async function handleBuscar() {
    if (!busca.trim()) return;
    setErroMsg("");
    setSucessoMsg("");
    setResultado(null);
    setPrecoResultado(null);
    setLoadingBusca(true);

    try {
      const res = await fetch(
        `${BASE_URL}/search_game?name=${encodeURIComponent(busca)}`,
      );
      if (!res.ok) throw new Error();
      const data = await res.json();
      setResultado(data);
      buscarPrecoSteam(data.appid);
    } catch {
      setErroMsg("Jogo não encontrado na Steam.");
    } finally {
      setLoadingBusca(false);
    }
  }

  async function buscarPrecoSteam(appid) {
    try {
      const res = await fetch(
        `https://store.steampowered.com/api/appdetails?appids=${appid}&cc=br`,
      );
      const data = await res.json();
      const info = data[String(appid)]?.data;
      if (info?.price_overview) {
        setPrecoResultado((info.price_overview.final / 100).toFixed(2));
      } else {
        setPrecoResultado("0.00");
      }
    } catch {
      setPrecoResultado(null);
    }
  }

  async function handleAdicionar() {
    if (!resultado) return;
    setLoadingAdicionar(true);
    setErroMsg("");

    try {
      const res = await fetch(`${BASE_URL}/adicionar_jogo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: usuario.id,
          appid: resultado.appid,
          nome: resultado.name,
        }),
      });

      if (!res.ok) throw new Error();

      setSucessoMsg(`"${resultado.name}" adicionado com sucesso!`);
      setResultado(null);
      setBusca("");
      setPrecoResultado(null);
      await carregarJogos();
      setTimeout(() => setSucessoMsg(""), 3000);
    } catch {
      setErroMsg("Erro ao adicionar jogo. Tente novamente.");
    } finally {
      setLoadingAdicionar(false);
    }
  }

  async function handleRemover(jogoId, nomeJogo) {
    setRemovendoId(jogoId);
    setErroMsg("");

    try {
      const res = await fetch(`${BASE_URL}/remover_jogo/${jogoId}`, {
        method: "DELETE",
      });

      if (!res.ok) throw new Error();

      setJogos((prev) => prev.filter((j) => j.id !== jogoId));
      setSucessoMsg(`"${nomeJogo}" removido.`);
      setTimeout(() => setSucessoMsg(""), 3000);
    } catch {
      setErroMsg("Erro ao remover jogo. Tente novamente.");
    } finally {
      setRemovendoId(null);
    }
  }

  // Jogos filtrados pela pesquisa
  const jogosFiltrados = jogos.filter((j) =>
    j.nome?.toLowerCase().includes(filtroJogos.toLowerCase()),
  );

  return (
    <div className="min-h-screen bg-[var(--bg)] p-6">
      <div className="max-w-6xl mx-auto flex flex-col gap-8">
        {/* SEÇÃO 1: SAUDAÇÃO */}
        <div>
          <h1 className="text-3xl font-bold text-[var(--text-h)]">
            Olá, {usuario?.nome?.split(" ")[0]} 👋
          </h1>
          <p className="text-sm mt-1 text-[var(--text)]">
            Gerencie seus jogos monitorados e fique de olho nas promoções!
          </p>
        </div>

        {/* SEÇÃO 2: ADICIONAR JOGO */}
        <div className="rounded-xl border border-[var(--border)] shadow-[var(--shadow)] bg-[var(--bg)] p-6 flex flex-col gap-4">
          <h2 className="font-bold text-[var(--text-h)] text-base">
            Adicionar Novo Jogo
          </h2>

          {erroMsg && (
            <div className="px-3 py-2 rounded-md text-xs font-medium text-center bg-red-500/10 border border-red-500/30 text-red-400">
              {erroMsg}
            </div>
          )}

          {sucessoMsg && (
            <div className="px-3 py-2 rounded-md text-xs font-medium text-center bg-green-500/10 border border-green-500/30 text-green-400">
              {sucessoMsg}
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-3">
            <input
              className="flex-1 p-3 rounded-md border border-[var(--border)] bg-[var(--bg)] text-[var(--text)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
              placeholder="Nome do jogo..."
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleBuscar()}
            />
            <button
              onClick={handleBuscar}
              disabled={loadingBusca}
              className="sm:w-48 bg-[var(--accent)] text-white p-3 rounded-md font-semibold text-sm hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
            >
              {loadingBusca ? "Buscando..." : "Buscar na Steam"}
            </button>
          </div>

          {/* Card de Resultado da Busca */}
          {resultado && (
            <div className="rounded-lg border border-[var(--border)] bg-[var(--accent-bg)] mt-2 flex flex-col sm:flex-row items-center justify-between p-4 gap-4">
              <div className="flex items-center gap-4 w-full sm:w-auto">
                <img
                  src={`https://cdn.akamai.steamstatic.com/steam/apps/${resultado.appid}/header.jpg`}
                  alt={resultado.name}
                  className="rounded-md object-cover w-24 h-14 flex-shrink-0"
                  onError={(e) => e.target.classList.add("hidden")}
                />
                <div className="min-w-0">
                  <p className="font-semibold text-sm text-[var(--text-h)] truncate">
                    {resultado.name}
                  </p>
                  <p className="text-xs text-[var(--text)] mt-0.5">
                    {precoResultado === null
                      ? "Buscando preço..."
                      : precoResultado === "0.00"
                        ? "Grátis"
                        : `R$ ${precoResultado}`}
                  </p>
                </div>
              </div>
              <button
                onClick={handleAdicionar}
                disabled={loadingAdicionar}
                className="w-full sm:w-auto bg-[var(--accent)] text-white px-4 py-2 rounded-md text-xs font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
              >
                {loadingAdicionar ? "Adicionando..." : "+ Adicionar à lista"}
              </button>
            </div>
          )}
        </div>

        {/* SEÇÃO 3: CARROSSEL DE MELHORES PROMOÇÕES */}
        <div className="flex flex-col gap-4">
          <h2 className="font-bold text-[var(--text-h)] text-lg flex items-center gap-2">
            <span>🔥</span> Melhores Promoções do Momento
          </h2>

          {loadingDeals ? (
            <div className="flex gap-4 overflow-hidden py-2 animate-pulse">
              {[1, 2, 3, 4].map((n) => (
                <div
                  key={n}
                  className="w-48 h-56 bg-[var(--border)] rounded-xl flex-shrink-0 opacity-50"
                />
              ))}
            </div>
          ) : topDeals.length === 0 ? (
            <p className="text-sm text-[var(--text)] italic">
              Não há promoções externas disponíveis no momento.
            </p>
          ) : (
            /* Container relativo para posicionar os botões sobre o carrossel */
            <div className="relative group/carousel">
              {/* Botão ESQUERDA */}
              <button
                onClick={() => scrollCarrossel(-1)}
                disabled={!podeScrollEsq}
                aria-label="Rolar para a esquerda"
                className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-3 z-10
                           w-8 h-8 rounded-full flex items-center justify-center
                           bg-[var(--bg)] border border-[var(--border)] shadow-[var(--shadow)]
                           text-[var(--text-h)] text-sm
                           opacity-0 group-hover/carousel:opacity-100
                           transition-all duration-200
                           hover:border-[var(--accent-border)] hover:text-[var(--accent)]
                           disabled:opacity-0 disabled:pointer-events-none"
              >
                ‹
              </button>

              {/* Trilha do carrossel */}
              <div
                ref={carrosselRef}
                onScroll={atualizarBotoesScroll}
                className="flex overflow-x-auto gap-4 pb-3 pt-1 px-1 snap-x scroll-smooth [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
              >
                {topDeals.map((deal) => (
                  <div
                    key={deal.id}
                    className="w-48 bg-[var(--bg)] border border-[var(--border)] rounded-xl overflow-hidden shadow-[var(--shadow)] flex flex-col flex-shrink-0 snap-start hover:border-[var(--accent-border)] transition-all transform hover:-translate-y-1"
                  >
                    {/* Imagem clicável → abre na Steam */}
                    <a
                      href={`https://store.steampowered.com/app/${deal.id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      title="Ver na Steam"
                      className="relative block overflow-hidden group/card"
                    >
                      <img
                        src={deal.thumb}
                        alt={deal.titulo}
                        className="w-full h-24 object-cover transition-transform duration-300 group-hover/card:scale-105"
                      />
                      <div className="absolute inset-0 bg-black/0 group-hover/card:bg-black/40 transition-all duration-200 flex items-center justify-center">
                        <span className="text-white text-[10px] font-semibold opacity-0 group-hover/card:opacity-100 transition-opacity duration-200 drop-shadow">
                          Ver na Steam
                        </span>
                      </div>
                    </a>

                    <div className="p-3 flex flex-col flex-grow justify-between gap-2">
                      <h3 className="font-bold text-[var(--text-h)] text-xs line-clamp-2 min-h-[32px]">
                        {deal.titulo}
                      </h3>
                      <div className="flex items-center justify-between mt-auto">
                        <span className="bg-green-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">
                          -{deal.desconto}%
                        </span>
                        <div className="text-right">
                          <p className="line-through text-[10px] text-gray-400">
                            R${" "}
                            {(
                              deal.preco_promocao /
                              (1 - deal.desconto / 100)
                            ).toFixed(2)}
                          </p>
                          <p className="font-bold text-[var(--accent)] text-sm">
                            R$ {deal.preco_promocao}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Botão DIREITA */}
              <button
                onClick={() => scrollCarrossel(1)}
                disabled={!podeScrollDir}
                aria-label="Rolar para a direita"
                className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-3 z-10
                           w-8 h-8 rounded-full flex items-center justify-center
                           bg-[var(--bg)] border border-[var(--border)] shadow-[var(--shadow)]
                           text-[var(--text-h)] text-sm
                           opacity-0 group-hover/carousel:opacity-100
                           transition-all duration-200
                           hover:border-[var(--accent-border)] hover:text-[var(--accent)]
                           disabled:opacity-0 disabled:pointer-events-none"
              >
                ›
              </button>
            </div>
          )}
        </div>

        {/* SEÇÃO 4: JOGOS MONITORADOS */}
        <div className="rounded-xl border border-[var(--border)] shadow-[var(--shadow)] bg-[var(--bg)] p-6 flex flex-col min-h-[300px]">
          {/* Cabeçalho + campo de pesquisa */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
            <h2 className="font-bold text-[var(--text-h)] text-base whitespace-nowrap">
              Meus Jogos Monitorados ({jogos.length})
            </h2>

            {/* Campo de filtro — só aparece quando há jogos */}
            {!loadingJogos && jogos.length > 0 && (
              <div className="relative w-full sm:w-64">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--text)] text-xs pointer-events-none select-none">
                  🔍
                </span>
                <input
                  className="w-full pl-8 pr-3 py-2 rounded-md border border-[var(--border)] bg-[var(--bg)] text-[var(--text)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
                  placeholder="Pesquisar jogo..."
                  value={filtroJogos}
                  onChange={(e) => setFiltroJogos(e.target.value)}
                />
              </div>
            )}
          </div>

          {loadingJogos ? (
            <div className="flex items-center justify-center flex-1">
              <p className="text-sm text-[var(--text)]">
                Carregando seus jogos...
              </p>
            </div>
          ) : jogos.length === 0 ? (
            <div className="flex flex-col items-center justify-center flex-1 gap-3 opacity-60 py-8">
              <span className="text-4xl">🎮</span>
              <p className="text-sm text-center text-[var(--text)]">
                Nenhum jogo monitorado ainda.
                <br />
                Utilize o campo de busca acima para começar a rastrear preços.
              </p>
            </div>
          ) : jogosFiltrados.length === 0 ? (
            /* Nenhum resultado para o filtro */
            <div className="flex flex-col items-center justify-center flex-1 gap-3 opacity-60 py-8">
              <span className="text-3xl">🔍</span>
              <p className="text-sm text-center text-[var(--text)]">
                Nenhum jogo encontrado para "{filtroJogos}".
              </p>
            </div>
          ) : (
            <div className="flex flex-col gap-3 h-96 overflow-y-auto pr-1">
              {jogosFiltrados.map((jogo, index) => (
                <div
                  key={jogo.id ?? index}
                  className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-lg border border-[var(--border)] bg-[var(--accent-bg)] hover:border-[var(--accent-border)] transition-colors group"
                >
                  <div className="flex items-center gap-4 min-w-0">
                    <div
                      className="relative flex-shrink-0 cursor-pointer overflow-hidden rounded-md"
                      onClick={() =>
                        window.open(
                          `https://store.steampowered.com/app/${jogo.appid}`,
                          "_blank",
                        )
                      }
                    >
                      <img
                        src={`https://cdn.akamai.steamstatic.com/steam/apps/${jogo.appid}/header.jpg`}
                        alt={jogo.nome}
                        className="object-cover w-[100px] h-[56px] group-hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity bg-black/40">
                        <span className="text-white text-[10px] font-medium">
                          Ver na Steam
                        </span>
                      </div>
                    </div>

                    <div className="min-w-0">
                      <p className="font-semibold text-sm text-[var(--text-h)] truncate">
                        {jogo.nome}
                      </p>
                      <p className="text-xs mt-0.5 text-[var(--text)]">
                        AppID: {jogo.appid || "—"}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between sm:justify-end gap-6 flex-shrink-0">
                    <div className="text-right">
                      {/* Se o preço atual for menor que o preço original, significa que está em promoção */}
                      {jogo.preco_original &&
                      jogo.preco < jogo.preco_original ? (
                        <div className="flex flex-col items-end">
                          {/* Preço cheio (rasurado e menor) */}
                          <span className="text-xs line-through text-gray-400">
                            R$ {Number(jogo.preco_original).toFixed(2)}
                          </span>
                          {/* Preço atual em promoção (em destaque com a cor de sotaque) */}
                          <p className="font-bold text-base text-[var(--accent)] animate-pulse-subtle">
                            R$ {Number(jogo.preco).toFixed(2)}
                          </p>
                        </div>
                      ) : (
                        /* Caso não esteja em promoção, mostra apenas o preço normal */
                        <p className="font-bold text-base text-[var(--text)]">
                          {jogo.preco === 0 || jogo.preco === null
                            ? "Grátis"
                            : `R$ ${Number(jogo.preco).toFixed(2)}`}
                        </p>
                      )}
                    </div>

                    {/* Botão de Remover (mantém igual ao seu) */}
                    <button
                      onClick={() => handleRemover(jogo.id, jogo.nome)}
                      disabled={removendoId === jogo.id}
                      title="Remover jogo"
                      className="text-xs w-7 h-7 flex items-center justify-center rounded border bg-transparent text-[var(--text)] border-[var(--border)] transition-all hover:text-red-400 hover:border-red-500/50 hover:bg-red-500/10 disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                      {removendoId === jogo.id ? "…" : "✕"}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
