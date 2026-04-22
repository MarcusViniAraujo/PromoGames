import os
import threading
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Imports do seu projeto
from database import Session, JogoMonitorado, Usuario, criar_banco
from auth import cadastrar_usuario, login_usuario
# Adicionei a importação que estava faltando abaixo:
from price_monitor import monitor_prices, search_game, get_game_info

load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")

app = FastAPI()
criar_banco()

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
        preco_inicial = get_game_info(dados.appid)
        novo = JogoMonitorado(
            usuario_id=dados.user_id,
            appid_steam=dados.appid,
            nome_jogo=dados.nome,
            ultimo_preco=preco_inicial
        )
        session.add(novo)
        session.commit()
        return {"status": "adicionado"}
    finally:
        session.close()

@app.get("/listar_jogos/{user_id}")
def listar_jogos(user_id: int):
    session = Session()
    try:
        jogos = session.query(JogoMonitorado).filter_by(usuario_id=user_id).all()
        return [{"nome": j.nome_jogo, "preco": j.ultimo_preco} for j in jogos]
    finally:
        session.close()

if __name__ == "__main__":
    # Inicia a thread apenas se rodar este arquivo diretamente
    threading.Thread(target=monitor_prices, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
#python -m uvicorn server:app --reload