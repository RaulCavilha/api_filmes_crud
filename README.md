# 🎬 API de Gestão de Filmes

Uma API RESTful desenvolvida em Python para o gerenciamento de um catálogo de filmes e controle de usuários, com persistência de dados.

## 🚀 Tecnologias Utilizadas

* **Python 3**
* **FastAPI** (Framework web)
* **SQLModel** (ORM que une SQLAlchemy e Pydantic para banco de dados)
* **SQLite** (Banco de dados para desenvolvimento)
* **Uvicorn** (Servidor ASGI)

## ⚙️ Funcionalidades

* **Autenticação e Usuários:**
  * Criação de novos usuários com armazenamento seguro e validação de duplicidade.
  * Sistema de Login.
* **Catálogo de Filmes (CRUD):**
  * `POST`: Adicionar novos filmes ao banco de dados.
  * `GET`: Listar os filmes cadastrados ou buscar detalhes via UUID.
  * `DELETE`: Remoção segura de filmes do catálogo.
  * `PATCH`: Atualização parcial dos dados de filmes e usuários

## 🛠️ Como rodar o projeto na sua máquina

Siga os passos abaixo para executar a API localmente.

1. **Clone este repositório:**
```bash
git clone https://github.com/RaulCavilha/api_filmes_crud.git
```

2. Acesse a pasta do projeto:
```bash
cd api_filmes_crud
```

3. Crie o ambiente virtual:
```bash
python -m venv venv
```

4. Ative o ambiente virtual (Windows):
```bash
.\venv\Scripts\activate
```
5. Instale as dependências:
```bash
pip install -r requirements.txt
```
6. Rode a API:
```bash
fastapi dev main.py
```
