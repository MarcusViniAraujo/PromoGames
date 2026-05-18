# teste.py — rode com: python teste.py
from price_monitor import get_game_info, enviar_telegram
from database import Session, JogoMonitorado

print("\n=== 1. TESTANDO BUSCA DE PREÇO ===")
# Cyberpunk 2077 — appid conhecido
preco = get_game_info("1091500")
print(f"Preço retornado: R${preco:.2f}")
if preco > 0:
    print("✅ Busca de preço OK")
else:
    print("❌ Retornou 0.0 — problema na API da Steam ou jogo gratuito")

print("\n=== 2. TESTANDO BANCO DE DADOS ===")
session = Session()
jogos = session.query(JogoMonitorado).all()
print(f"Jogos no banco: {len(jogos)}")
for j in jogos:
    print(f"  - {j.nome_jogo} | appid: {j.appid_steam} | preço: {j.ultimo_preco} | chat_id: {j.dono.chat_id_telegram}")
session.close()

if not jogos:
    print("⚠️  Nenhum jogo cadastrado — adicione um jogo pelo frontend primeiro")

print("\n=== 3. TESTANDO ENVIO TELEGRAM ===")
# Substitua pelo seu chat_id real
MEU_CHAT_ID = "7241286397"

enviar_telegram(
    chat_id_destino=MEU_CHAT_ID,
    nome="Cyberpunk 2077",
    appid="1091500",
    preco_antigo=199.90,
    preco_atual=59.90,
)