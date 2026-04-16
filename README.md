# 🎮 PromoGames - Monitor Inteligente de Preços Steam

O **PromoGames** é uma aplicação robusta desenvolvida em Python para monitorar preços de jogos na plataforma Steam. O sistema automatiza a busca por promoções e notifica usuários individualmente via Telegram assim que os preços atingem os critérios desejados.

---

## 🚀 Funcionalidades Principais

- **Autenticação Segura:** Sistema de login e cadastro com armazenamento de senhas criptografadas (Hashing com Bcrypt).
- **Monitoramento Multiusuário:** Diferente de scripts simples, o PromoGames suporta múltiplos usuários simultâneos, cada um com sua lista de desejos privada.
- **Notificações em Tempo Real:** Integração com a API do Telegram para alertas instantâneos de queda de preço.
- **Banco de Dados Relacional:** Persistência de dados utilizando SQLite e SQLAlchemy (ORM), garantindo integridade e escalabilidade.
- **Processamento Assíncrono:** Utiliza *Threading* para manter o monitoramento em segundo plano sem interromper a navegação do usuário no terminal.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** [Python 3.13+](https://www.python.org/)
- **Banco de Dados:** SQLite
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Segurança:** [Bcrypt](https://pypi.org/project/bcrypt/) (Criptografia de senhas)
- **Consumo de API:** [Requests](https://requests.readthedocs.io/)
- **Integrações:** Steam Store API & Telegram Bot API
