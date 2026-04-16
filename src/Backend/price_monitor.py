from database import Session, JogoMonitorado
import requests
import time
import threading
import json
import os


token = "8736406764:AAE9X2LkYU165xZz0XcI0ZbQhYRnY4W2pEQ"

def search_game(name):
    url = "https://store.steampowered.com/api/storesearch/"
    params = {"term": name, "l": "portuguese", "cc": "br"}
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if data["items"]:
            game = data["items"][0]
            return str(game["id"]), game["name"]
    except Exception as e:
        print(f"Erro na busca: {e}")
    return None, None

def get_game_info(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=br"
    try:
        response = requests.get(url)
        data = response.json()
        game_data = data.get(str(appid), {}).get("data")
        if not game_data or "price_overview" not in game_data:
            return 0.0
        return float(game_data["price_overview"]["final"] / 100)
    except:
        return 0.0
    
def enviar_telegram(mensagem, chat_id_destino):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id_destino, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except:
        print("Erro ao enviar mensagem no Telegram.")

def monitor_prices():
    while True:
        session = Session()
        try:
            jogos = session.query(JogoMonitorado).all()
            print(f"\n--- Verificando {len(jogos)} jogos no banco: {time.strftime('%H:%M:%S')} ---")

            for jogo in jogos:
                atual = get_game_info(jogo.appid_steam)

                if atual > 0:
                    # Se houver queda de preço
                    if jogo.ultimo_preco and atual < jogo.ultimo_preco:
                        chat_id = jogo.dono.chat_id_telegram
                        if chat_id:
                            msg = f"🔥 *PROMOÇÃO!* {jogo.nome_jogo} caiu de R${jogo.ultimo_preco:.2f} para R${atual:.2f}!"
                            enviar_telegram(msg, chat_id)
                    
                    jogo.ultimo_preco = atual 
            
            session.commit() 
        except Exception as e:
            print(f"Erro no monitor: {e}")
            session.rollback()
        finally:
            session.close()
        time.sleep(60)