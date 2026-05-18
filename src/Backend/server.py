import os
import threading
import uvicorn
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from database import Session, JogoMonitorado, Usuario, criar_banco
from auth import cadastrar_usuario, login_usuario
from price_monitor import monitor_prices, search_game, get_game_info, fetch_top_deals

load_dotenv()

# Gerenciador de Ciclo de Vida: Executa de forma segura mesmo com o --reload ativo
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Servidor iniciado! Ligando o monitor de preços em background thread...")
    threading.Thread(target=monitor_prices, daemon=True).start()
    yield
    print("⛔ Servidor encerrado.")

app = FastAPI(lifespan=lifespan)
criar_banco()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos de Dados ---
class LoginRequest(BaseModel):
    email: str
    senha: str

class CadastroRequest(BaseModel):
    nome: str
    email: str
    senha: str
    chat_id: str

class JogoRequest(BaseModel):
    user_id: int
    appid: str
    nome: str

# --- Rotas ---

@app.post("/login")
def login(dados: LoginRequest):
    usuario = login_usuario(dados.email, dados.senha)
    if usuario:
        return {"id": usuario.id, "nome": usuario.nome}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@app.post("/cadastro")
def rota_cadastro(dados: CadastroRequest):
    session = Session()
    existe = session.query(Usuario).filter_by(email=dados.email).first()
    session.close()

    if existe:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")

    sucesso = cadastrar_usuario(dados.nome, dados.email, dados.senha, dados.chat_id)
    if sucesso:
        return {"status": "sucesso"}

    raise HTTPException(status_code=500, detail="Erro interno no servidor.")

@app.get("/search_game")
def buscar_jogo(name: str):
    appid, nome_steam = search_game(name)
    if appid:
        return {"appid": appid, "name": nome_steam}
    raise HTTPException(status_code=404, detail="Jogo não encontrado na Steam.")

@app.post("/adicionar_jogo")
def adicionar(dados: JogoRequest):
    session = Session()
    try:
        preco_atual, preco_original = get_game_info(dados.appid)
        novo = JogoMonitorado(
            usuario_id=dados.user_id,
            appid_steam=dados.appid,
            nome_jogo=dados.nome,
            ultimo_preco=preco_atual,
            preco_original=preco_original if preco_original > 0 else preco_atual,
        )
        session.add(novo)
        session.commit()
        return {"status": "adicionado"}
    finally:
        session.close()

@app.delete("/remover_jogo/{jogo_id}")
def remover_jogo(jogo_id: int):
    session = Session()
    try:
        jogo = session.query(JogoMonitorado).filter_by(id=jogo_id).first()
        if not jogo:
            raise HTTPException(status_code=404, detail="Jogo não encontrado.")
        session.delete(jogo)
        session.commit()
        return {"status": "removido"}
    finally:
        session.close()

@app.get("/listar_jogos/{user_id}")
def listar_jogos(user_id: int):
    session = Session()
    try:
        jogos = session.query(JogoMonitorado).filter_by(usuario_id=user_id).all()
        return [
            {
                "id": j.id,
                "nome": j.nome_jogo,
                "appid": j.appid_steam,
                "preco": j.ultimo_preco,
                "preco_original": j.preco_original,
            }
            for j in jogos
        ]
    finally:
        session.close()

@app.get("/api/top-deals")
def top_deals():
    deals = fetch_top_deals()
    if deals is None:
        raise HTTPException(status_code=503, detail="Não foi possível buscar promoções.")
    return deals

if __name__ == "__main__":
    # Aqui o uvicorn só roda se você chamar direto via python server.py
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)