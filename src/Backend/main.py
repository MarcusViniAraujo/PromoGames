import threading
from database import JogoMonitorado, Session, criar_banco
from auth import login_usuario, cadastrar_usuario
from price_monitor import monitor_prices, search_game, get_game_info

def menu_logado(usuario):
    # Abrimos uma única sessão para o menu ou gerenciamos dentro de cada opção
    while True:
        print(f"\n--- 🎮 Menu de {usuario.nome} ---")
        print("1. Adicionar Jogo para Monitorar")
        print("2. Listar Meus Jogos")
        print("3. Sair")
        
        op = input("Escolha: ")
        session = Session() # Abre a conexão

        if op == "1":
            nome_busca = input("Nome do jogo: ")
            appid, nome_steam = search_game(nome_busca)
            if appid:
                # Evitar duplicatas para o mesmo usuário
                existe = session.query(JogoMonitorado).filter_by(usuario_id=usuario.id, appid_steam=appid).first()
                if not existe:
                    novo_jogo = JogoMonitorado(
                        usuario_id=usuario.id,
                        appid_steam=appid,
                        nome_jogo=nome_steam,
                        ultimo_preco=get_game_info(appid),
                        preco_alvo=0.0 
                    )
                    session.add(novo_jogo)
                    session.commit()
                    print(f" {nome_steam} adicionado!")
                else:
                    print(" Você já monitora este jogo.")
            else:
                print(" Jogo não encontrado.")

        elif op == "2":
            meus_jogos = session.query(JogoMonitorado).filter_by(usuario_id=usuario.id).all()
            if not meus_jogos:
                print("Você ainda não monitora nenhum jogo.")
            for j in meus_jogos:
                print(f"- {j.nome_jogo}: R${j.ultimo_preco:.2f}")

        elif op == "3":
            session.close()
            break
        
        session.close() # Sempre fecha para não travar o SQLite

def main():
    criar_banco() # Garante que o .db existe
    
    # Inicia o monitor em segundo plano
    # IMPORTANTE: Mudei o nome para 'monitor_prices' conforme criamos antes
    t = threading.Thread(target=monitor_prices, daemon=True)
    t.start()

    while True:
        print("\n=== VIGIA STEAM PRO ===")
        print("1. Login")
        print("2. Cadastro")
        print("3. Sair")
        
        escolha = input("Opção: ")
        
        if escolha == "1":
            email = input("Email: ")
            senha = input("Senha: ")
            user = login_usuario(email, senha)
            if user:
                menu_logado(user)
            else:
                print("Credenciais inválidas.")
        
        elif escolha == "2":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            cid = input("Chat ID Telegram: ")
            cadastrar_usuario(nome, email, senha, cid)
            
        elif escolha == "3":
            break

if __name__ == "__main__":
    main()