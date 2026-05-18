import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(diretorio_atual, 'PromoGames.db')

engine = create_engine(f'sqlite:///{caminho_banco}', connect_args={"check_same_thread": False})
Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(200), nullable=False)
    chat_id_telegram = Column(String(50))

    jogos = relationship("JogoMonitorado", back_populates="dono", cascade="all, delete-orphan")


class JogoMonitorado(Base):
    __tablename__ = 'jogos_monitorados'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    appid_steam = Column(String(20), nullable=False)
    nome_jogo = Column(String(200))
    preco_alvo = Column(Float, default=0.0)
    ultimo_preco = Column(Float)           # Preço atual (com desconto se estiver em promoção)
    preco_original = Column(Float)         # Preço cheio fora de promoção

    dono = relationship("Usuario", back_populates="jogos")


class HistoricoPreco(Base):
    __tablename__ = 'historico_precos'

    id = Column(Integer, primary_key=True)
    appid_steam = Column(String(20), nullable=False)
    preco = Column(Float, nullable=False)
    data_verificacao = Column(DateTime, default=datetime.now)


Session = sessionmaker(bind=engine)


def criar_banco():
    Base.metadata.create_all(engine)

    # Migração segura: adiciona preco_original se ainda não existir
    # (útil para bancos já existentes sem a coluna)
    with engine.connect() as conn:
        cols = [row[1] for row in conn.execute(text("PRAGMA table_info(jogos_monitorados)"))]
        if "preco_original" not in cols:
            conn.execute(text("ALTER TABLE jogos_monitorados ADD COLUMN preco_original REAL"))
            conn.commit()
            print("✅ Coluna 'preco_original' adicionada ao banco existente.")

    print("✅ Banco de dados inicializado com sucesso!")


if __name__ == "__main__":
    criar_banco()