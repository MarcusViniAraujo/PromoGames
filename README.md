# 🎮 PromoGames - Monitor Inteligente de Preços Steam

O **PromoGames** é uma solução Full-Stack completa para monitoramento de preços de jogos na Steam. O sistema permite que usuários gerenciem suas listas de desejos e recebam notificações instantâneas quando um jogo atingir um valor desejado, garantindo economia e praticidade.



## 🏗️ Arquitetura do Projeto

O projeto adota uma arquitetura de separação de responsabilidades (Separation of Concerns):

* **Frontend:** Interface Web moderna desenvolvida com **React (Vite)** e **Tailwind CSS**. Focada em uma experiência de usuário (UX) fluida e responsiva.
* **Backend:** API RESTful robusta desenvolvida em **FastAPI (Python)**. Gerencia a autenticação, persistência de dados e a lógica de monitoramento.
* **Banco de Dados:** Utiliza **SQLite** com o ORM **SQLAlchemy**, garantindo integridade e simplicidade na gestão dos dados.

## 🚀 Funcionalidades

- **Monitoramento em tempo real:** Verificação automática de preços na Steam.
- **Autenticação Segura:** Sistema de login e cadastro com armazenamento de senhas hashadas.
- **Notificações:** Integração com Telegram Bot para alertas de promoções.
- **Interface Responsiva:** Dashboard intuitivo para gerenciamento de jogos monitorados.

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
| :--- | :--- |
| **Frontend** | React, Vite, Tailwind CSS, React Router |
| **Backend** | Python 3.13, FastAPI, SQLAlchemy, Bcrypt |
| **Outros** | SQLite, python-dotenv, Requests |
