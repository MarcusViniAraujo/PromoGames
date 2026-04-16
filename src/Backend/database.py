import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(diretorio_atual, 'PromoGames.db')

# O engine agora usa o caminho completo
engine = create_engine(f'sqlite:///{caminho_banco}', connect_args={"check_same_thread": False})
Base = declarative_base()

# 2. Definição da Tabela de Usuários
class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(200), nullable=False)
    chat_id_telegram = Column(String(50))
    
    # Relacionamento: Permite acessar os jogos do usuário com user.jogos
    jogos = relationship("JogoMonitorado", back_populates="dono", cascade="all, delete-orphan")

# 3. Definição da Tabela de Jogos
class JogoMonitorado(Base):
    __tablename__ = 'jogos_monitorados'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    appid_steam = Column(String(20), nullable=False)
    nome_jogo = Column(String(200))
    preco_alvo = Column(Float, default=0.0) # Alerta se baixar desse valor
    ultimo_preco = Column(Float) # Último preço registrado
    
    # Liga o jogo de volta ao objeto Usuario
    dono = relationship("Usuario", back_populates="jogos")

# 4. Tabela de Histórico (Opcional, mas ótimo para gráficos futuros)
class HistoricoPreco(Base):
    __tablename__ = 'historico_precos'
    
    id = Column(Integer, primary_key=True)
    appid_steam = Column(String(20), nullable=False)
    preco = Column(Float, nullable=False)
    data_verificacao = Column(DateTime, default=datetime.now)

# 5. Configuração da Sessão
# A Session é o que você usará nos outros arquivos para ler/escrever dados
Session = sessionmaker(bind=engine)

def criar_banco():
    Base.metadata.create_all(engine)
    print("✅ Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    criar_banco()