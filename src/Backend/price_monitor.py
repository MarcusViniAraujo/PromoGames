import os
import re
import time
import requests
from dotenv import load_dotenv
from database import Session, JogoMonitorado, HistoricoPreco

load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")
if not token:
    print("ERRO: TELEGRAM_TOKEN não configurado no .env!")


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


def fetch_top_deals():
    """Busca as melhores ofertas na Steam e calcula o preço original real usando o desconto."""
    url = "https://store.steampowered.com/api/featuredcategories?cc=br&l=portuguese"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        specials = data.get("specials", {}).get("items", [])
        
        promocoes = []
        for item in specials[:10]:
            final_raw = item.get("final_price", 0)
            desconto = item.get("discount_percent", 0)
            
            preco_promocao = float(final_raw) / 100
            
            # Engenharia reversa para corrigir inconsistências da API da Steam
            if 0 < desconto < 100:
                preco_original = preco_promocao / (1 - (desconto / 100))
            elif desconto == 100:
                initial_raw = item.get("initial_price", 0)
                preco_original = float(initial_raw) / 100 if initial_raw > 0 else 0.0
            else:
                preco_original = preco_promocao
            
            promocoes.append({
                "id": str(item["id"]),
                "titulo": item["name"],
                "preco_original": f"{preco_original:.2f}",
                "preco_promocao": f"{preco_promocao:.2f}",
                "desconto": desconto,
                "thumb": item["large_capsule_image"]
            })
        return promocoes
    except Exception as e:
        print(f"Erro ao buscar ofertas na Steam: {e}")
        return None


def get_game_info(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=br"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        game_data = data.get(str(appid), {}).get("data")
        if not game_data or "price_overview" not in game_data:
            return 0.0, 0.0
        po = game_data["price_overview"]
        preco_atual    = float(po["final"])   / 100
        preco_original = float(po["initial"]) / 100
        return preco_atual, preco_original
    except Exception as e:
        print(f"Erro ao buscar preço do appid {appid}: {e}")
        return 0.0, 0.0


def escapar_markdown(texto):
    caracteres = r"\_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(caracteres)}])", r"\\\1", str(texto))


def enviar_telegram(chat_id_destino, nome, appid, preco_antigo, preco_atual):
    imagem_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"
    link_steam = f"https://store.steampowered.com/app/{appid}"
    desconto = round(((preco_antigo - preco_atual) / preco_antigo) * 100)

    nome_e         = escapar_markdown(nome)
    preco_antigo_e = escapar_markdown(f"{preco_antigo:.2f}")
    preco_atual_e  = escapar_markdown(f"{preco_atual:.2f}")
    desconto_e     = escapar_markdown(desconto)

    legenda = (
        f"🔥 *PROMOÇÃO DETECTADA\!*\n\n"
        f"🎮 *{nome_e}*\n\n"
        f"~R\${preco_antigo_e}~ → 🟢 *R\${preco_atual_e}*\n"
        f"📉 Queda de *{desconto_e}%*\n\n"
        f"[👉 Ver na Steam]({link_steam})"
    )

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": chat_id_destino,
        "photo": imagem_url,
        "caption": legenda,
        "parse_mode": "MarkdownV2",
    }

    try:
        response = requests.post(url, data=payload)
        if response.ok:
            print(f"  ✅ Telegram enviado para chat_id {chat_id_destino}")
        else:
            print(f"  ❌ Erro Telegram ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"  ❌ Erro ao enviar Telegram: {e}")


def monitor_prices():
    while True:
        print(f"\n--- Iniciando ciclo de checagem: {time.strftime('%H:%M:%S')} ---")
        
        # 1. Abre uma sessão rápida apenas para listar os registros atuais
        session = Session()
        try:
            jogos_info = [(j.id, j.appid_steam, j.nome_jogo) for j in session.query(JogoMonitorado).all()]
        except Exception as e:
            print(f"Erro ao listar jogos do banco: {e}")
            jogos_info = []
        finally:
            session.close()  # Fecha imediatamente para não prender o SQLite

        print(f"Verificando {len(jogos_info)} jogos mapeados...")

        # 2. Varre os jogos fazendo requisições HTTP fora de sessões persistentes
        for jogo_id, appid, nome in jogos_info:
            try:
                atual, original = get_game_info(appid)
                
                if atual > 0:
                    # 3. Abre uma sub-sessão cirúrgica apenas para atualizar este jogo
                    sub_session = Session()
                    try:
                        db_jogo = sub_session.query(JogoMonitorado).get(jogo_id)
                        if db_jogo:
                            preco_anterior = db_jogo.ultimo_preco
                            print(f"  {nome}: R${atual:.2f} (cheio: R${original:.2f} | anterior: {preco_anterior})")

                            # Se o preço caiu em relação ao registro anterior, envia o alerta
                            if preco_anterior is not None and atual < preco_anterior:
                                chat_id = db_jogo.dono.chat_id_telegram
                                if chat_id:
                                    print(f"  🔥 Queda detectada! Disparando Telegram...")
                                    enviar_telegram(chat_id, nome, appid, preco_anterior, atual)
                                else:
                                    print(f"  ⚠️ Telegram omitido: chat_id vazio para o dono de '{nome}'")

                            # Grava as modificações de estado
                            db_jogo.ultimo_preco = atual
                            if original > 0:
                                db_jogo.preco_original = original

                            sub_session.add(HistoricoPreco(appid_steam=appid, preco=atual))
                            sub_session.commit()
                    except Exception as err_db:
                        sub_session.rollback()
                        print(f"  ❌ Erro de persistência para '{nome}': {err_db}")
                    finally:
                        sub_session.close()

            except Exception as e:
                print(f"  ❌ Falha crítica ao processar o fluxo de '{nome}': {e}")
                continue

        time.sleep(7200)  # Aguarda 2 horas até o próximo ciclo