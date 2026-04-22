# 🎮 PromoGames - Monitor Inteligente de Preços Steam

O **PromoGames** é uma solução completa para monitoramento de preços de jogos na Steam. Com uma arquitetura moderna baseada em **Cliente-Servidor (FastAPI)**, o sistema permite que múltiplos usuários gerenciem suas listas de desejos de forma privada, com notificações em tempo real enviadas diretamente via Telegram.

---

## 🏗️ Arquitetura do Projeto

O sistema foi redesenhado para separar as responsabilidades:
* **Servidor (`server.py`):** Gerencia a API, autenticação, persistência de dados e a execução do monitor de preços em segundo plano (background thread).
* **Cliente (`main.py`):** Interface de linha de comando para o usuário interagir com o sistema, realizar buscas e gerenciar jogos.

---

## 🚀 Funcionalidades Principais

- **Arquitetura Cliente-Servidor:** Separação clara entre a lógica de negócio (servidor) e a interação com o usuário (cliente).
- **Autenticação Segura:** Sistema de login com hashing de senhas.
- **Monitoramento Robusto:** Processamento assíncrono via *Threading* para checagens 24/7 sem interrupções.
- **Configuração via Variáveis de Ambiente:** Uso de `.env` para proteger tokens e credenciais.
- **Integração Telegram:** Notificações instantâneas de promoções.
- **Banco de Dados Relacional:** ORM completo utilizando SQLAlchemy.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** [Python 3.13+](https://www.python.org/)
- **Framework Web (API):** [FastAPI](https://fastapi.tiangolo.com/)
- **Banco de Dados:** SQLite
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Variáveis de Ambiente:** [python-dotenv](https://pypi.org/project/python-dotenv/)
- **Segurança:** [Bcrypt](https://pypi.org/project/bcrypt/)
- **Consumo de API:** [Requests](https://requests.readthedocs.io/)

---
