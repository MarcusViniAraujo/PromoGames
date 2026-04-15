import requests
import time
import threading
import json
import os


token = "8736406764:AAE9X2LkYU165xZz0XcI0ZbQhYRnY4W2pEQ"
chat_id = "7241286397"
ARQUIVO_DADOS = "meus_jogos.json"
games = {}
prices = {}

if os.path.exists(ARQUIVO_DADOS):
    try:
        with open(ARQUIVO_DADOS, 'r') as f:
            dados_salvos = json.load(f)
            games = dados_salvos.get("games", {})
            prices_brutos = dados_salvos.get("prices", {})
            for k, v in prices_brutos.items():
                if isinstance(v, dict): 
                    prices[k] = float(v.get("final", 0))
                else:
                    prices[k] = float(v)
    except:
        print("Aviso: Erro ao ler JSON. Iniciando com dados vazios.")

def salvar_dados():
    with open(ARQUIVO_DADOS, 'w') as f:
        json.dump({"games": games, "prices": prices}, f)

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

        price_data = game_data.get("price_overview")
        return float(price_data["final"] / 100)
    except:
        return 0.0
    
def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")

def monitor_prices():
    while True:
        items = list(games.items())
        if not items:
            time.sleep(10)
            continue

        print(f"\n--- Verificando preços: {time.strftime('%H:%M:%S')} ---")
        for appid, name in items:
            appid_str = str(appid)
            atual = get_game_info(appid_str)
            
            if atual <= 0: 
                continue

            if appid_str in prices:
                preco_salvo = prices[appid_str]
                
                if isinstance(preco_salvo, dict):
                    preco_salvo = float(preco_salvo.get("final", 0))

                if atual < preco_salvo:
                    msg = f"🔥 *PROMOÇÃO!* {name} caiu de R${preco_salvo:.2f} para R${atual:.2f}!"
                    enviar_telegram(msg)
                    print(f"\n[ALERTA] {msg}")

            prices[appid_str] = atual
        
        salvar_dados()
        time.sleep(60)

if __name__ == "__main__":
    print("=== VIGIA STEAM PRO ATIVADO ===")
    
    thread_monitor = threading.Thread(target=monitor_prices, daemon=True)
    thread_monitor.start()

    while True:
        novo_jogo = input("Nome do jogo (ou 'listar'/'sair'): ")
        
        if novo_jogo.lower() == 'sair':
            break
            
        if novo_jogo.lower() == 'listar':
            print("\n--- Jogos sendo vigiados ---")
            for id, n in games.items():
                p = prices.get(str(id), 0.0)
                if isinstance(p, dict): p = p.get("final", 0)
                print(f"ID: {id} | Nome: {n} | Preço: R${float(p):.2f}")
            continue

        appid, name = search_game(novo_jogo)

        if appid:
            appid_str = str(appid)
            if appid_str not in games:
                games[appid_str] = name
                print(f"✅ Adicionado: {name}")
                enviar_telegram(f"📌 Novo jogo monitorado: {name}")
                prices[appid_str] = get_game_info(appid_str)
                salvar_dados()
            else:
                print("⚠️ Este jogo já está na lista!")
        else:
            print("❌ Jogo não encontrado.")