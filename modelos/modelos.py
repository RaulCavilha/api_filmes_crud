from pydantic import BaseModel
from typing import Annotated
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

"""
Os modelos serão usados como base para o que vai ser usado como tabela ou não. Temos que ter vários modelos. pois assim fica mais fácil de trabalhar
do que se tivessemos que resolver bugs e erros de um único só modelo com tabela.
"""

class FilmeBase(SQLModel):
    """
    Modelo que recebe parâmetros essenciais para criação da tabela
    """
    titulo: Annotated[str, Field(index=True)]
    nota_media: Annotated[float, Field(alias="notaMedia")] | None = None
    sinopse: str | None = None
    popularidade: float | None = None
    ano: str | None = None

class Filme(FilmeBase, table=True):
    """
    Modelo que será usado para criação da tabela em criar_banco_de_dados()
    """
    id: Annotated[int, Field(default=None, index=True, primary_key=True)]
    uuid: Annotated[UUID, Field(default_factory=uuid4, index=True, unique=True)]

class FilmePublic(FilmeBase):
    """
    Modelo que será utilizado para retornar ao usuário, herdando da classe FilmeBase
    """
    uuid: UUID

class FilmePut(FilmeBase):
    """
    Modelo que herda da classe FilmeBase para atulizações em filmes que já estão no Banco de Dados
    """
    ...

class FilmePatch(SQLModel):
    """
    Atualização de determinados parâmetros do modelo
    """
    titulo: Annotated[str, Field(index=True)] | None = None
    nota_media: Annotated[float, Field(le=10.0)] | None = None
    sinopse: str | None = None
    popularidade: float | None = None
    ano: str | None = None

class FilmeDelete(Filme):
    """
    Modelo que vai ser usado para deletar um determinado Filme
    """
    ...

class UsuarioBase(SQLModel):
    """
    Modelo que vai ser usado na criação de novos usuários
    """
    username: Annotated[str, Field(min_length=10, max_length=30, index=True, unique=True)]
    senha: Annotated[str, Field(min_length=8)]
    email: Annotated[str, Field(unique=True)]

class Usuario(UsuarioBase, table=True):
    """
    Modelo que herda de UsuarioBase e será usado como tabela
    """
    user_id: Annotated[int, Field(default=None, index=True, primary_key=True)]
    uuid: Annotated[UUID, Field(default_factory=uuid4, index=True)]

class UsuarioPublic(UsuarioBase):
    """
    Modelo que será usado para retornar ao usuário
    """
    uuid: UUID

class UsuarioPut(UsuarioBase):
    """
    Modelo que herda da classe FilmeBase para atulizações em filmes que já estão no Banco de Dados
    """
    ...

class UsuarioPatch(SQLModel):
    """
    Atualização de determinados parâmetros do modelo
    """
    username: Annotated[str, Field(min_length=10, max_length=30, index=True, unique=True)] | None = None
    senha: Annotated[str, Field(min_length=8, max_length=30)] | None = None
    email: Annotated[str, Field(unique=True)] | None = None

class UsuarioDelete(Usuario):
    """Modelo que vai ser usado para deletar um determinado Usuário
    """
    ...