from pathlib import Path
from sqlmodel import Field, SQLModel, create_engine, Session 
from models.models import Filme, Usuario
FILE_PATH = Path("dadosfilmes.db")
SQLITE_URL = f"sqlite:///{FILE_PATH}"
CONNECT_ARGS = {"check_same_thread":False}

engine = create_engine(url=SQLITE_URL, connect_args=CONNECT_ARGS, echo=True)

def criar_banco_de_dados():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session