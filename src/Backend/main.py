import requests
import sys

# O endereço onde o servidor está rodando
BASE_URL = "http://127.0.0.1:8000"

# Variável para armazenar o usuário logado no cliente
usuario_logado = None

def fazer_login():
    global usuario_logado
    email = input("Email: ")
    senha = input("Senha: ")
    
    # Enviando dados para o servidor validar
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "senha": senha})
    
    if response.status_code == 200:
        usuario_logado = response.json() # Armazena os dados do usuário (ex: id, nome)
        print(f"👋 Bem-vindo, {usuario_logado['nome']}!")
        return True
    else:
        # Captura a mensagem de erro específica do servidor
        erro = response.json().get("detail", "Erro desconhecido")
        print(f"❌ {erro}") # Vai imprimir: "❌ E-mail ou senha incorretos."
        return False

def adicionar_jogo():
    nome = input("Nome do jogo: ")
    
    try:
        response = requests.get(f"{BASE_URL}/search_game", params={"name": nome})
        
        if response.status_code != 200:
            print("❌ Jogo não encontrado na Steam.")
            return
            
        dados = response.json()
        appid = dados['appid']
        nome_steam = dados['name']
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor. Ele está rodando?")
        return

    payload = {
        "user_id": usuario_logado['id'], 
        "appid": appid, 
        "nome": nome_steam
    }
    
    response = requests.post(f"{BASE_URL}/adicionar_jogo", json=payload)
    
    if response.status_code == 200:
        print(f"✅ {nome_steam} adicionado com sucesso!")
    else:
        erro = response.json().get("detail", "Erro desconhecido")
        print(f"❌ Erro ao adicionar: {erro}")

def listar_meus_jogos():
    response = requests.get(f"{BASE_URL}/listar_jogos/{usuario_logado['id']}")
    
    if response.status_code == 200:
        jogos = response.json()
        if not jogos:
            print("\nVocê ainda não possui jogos monitorados.")
        else:
            print("\n--- Meus Jogos ---")
            for j in jogos:
                print(f"- {j['nome']}: R${j['preco']:.2f}")

def fazer_cadastro():
    print("\n--- Novo Cadastro ---")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    cid = input("Chat ID Telegram: ")
    
    # Enviando para a API
    payload = {"nome": nome, "email": email, "senha": senha, "chat_id": cid}
    response = requests.post(f"{BASE_URL}/cadastro", json=payload)
    
    if response.status_code == 200:
        print("✅ Cadastro realizado com sucesso! Agora você pode logar.")

    else:
        # Captura a mensagem de erro do servidor
        erro = response.json().get("detail", "Erro desconhecido")
        print(f"❌ {erro}") # Vai imprimir: "❌ Este e-mail já está cadastrado."
def main():
    while True:
        print("\n=== VIGIA STEAM ===")
        print("1. Login")
        print("2. Cadastrar")
        print("3. Sair")
        
        escolha = input("Opção: ")
        
        if escolha == "1":
            if fazer_login():
                while True: # Menu Logado
                    print("\n1. Adicionar Jogo | 2. Listar | 3. Logout")
                    sub = input("Escolha: ")
                    if sub == "1": adicionar_jogo()
                    elif sub == "2": listar_meus_jogos()
                    elif sub == "3": break

        elif escolha == "2":
            fazer_cadastro()

        elif escolha == "3":
            sys.exit()

if __name__ == "__main__":
    main()