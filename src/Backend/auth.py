import bcrypt
from database import Session, Usuario

def cadastrar_usuario(nome, email, senha, chat_id):
    session = Session()
    try:
        # Criptografando a senha para segurança
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            chat_id_telegram=chat_id
        )

        session.add(novo_usuario)
        session.commit()
        print(f"✅ Usuário {nome} cadastrado com sucesso!")
        return True
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao cadastrar: {e}")
        return False
    finally:
        session.close()

def login_usuario(email, senha):
    session = Session()
    try:
        usuario = session.query(Usuario).filter_by(email=email).first()
        
        # Verifica se o usuário existe e se a senha bate com o hash
        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario.senha_hash.encode('utf-8')):
            return usuario
        return None
    finally:
        session.close()