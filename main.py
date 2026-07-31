from database.database import criar_banco_de_dados
from contextlib import asynccontextmanager
from fastapi import FastAPI
from rotas import filmes, users

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Antes da API iniciar
    print("⏳ Criando banco de dados...")
    criar_banco_de_dados()
    print("✅ Banco pronto!")
    yield
    # Depois da API desligar
    print("🛑 Desligando servidor...")

app = FastAPI(lifespan=lifespan, title="API Filmes")
app.include_router(filmes.router)
app.include_router(users.router)
