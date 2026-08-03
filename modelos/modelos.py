from pydantic import BaseModel
from typing import Annotated
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class FilmeBase(SQLModel):
    titulo: Annotated[str, Field(index=True)]
    nota_media: Annotated[float, Field(alias="notaMedia")] | None = None
    sinopse: str | None = None
    popularidade: float | None = None
    ano: str | None = None

class Filme(FilmeBase, table=True):
    id: Annotated[int, Field(default=None, index=True, primary_key=True)]
    uuid: Annotated[UUID, Field(default_factory=uuid4, index=True, unique=True)]

class FilmePublic(FilmeBase):
    uuid: UUID

class FilmePut(FilmeBase):
    ...

class FilmePatch(SQLModel):
    titulo: Annotated[str, Field(index=True)] | None = None
    nota_media: Annotated[float, Field(le=10.0)] | None = None
    sinopse: str | None = None
    popularidade: float | None = None
    ano: str | None = None

class FilmeDelete(Filme):
    ...

class UsuarioBase(SQLModel):
    username: Annotated[str, Field(min_length=10, max_length=30, index=True, unique=True)]
    senha: Annotated[str, Field(min_length=8)]
    email: Annotated[str, Field(unique=True)]

class Usuario(UsuarioBase, table=True):
    user_id: Annotated[int, Field(default=None, index=True, primary_key=True)]
    uuid: Annotated[UUID, Field(default_factory=uuid4, index=True, unique=True)]

class UsuarioPublic(UsuarioBase):
    uuid: UUID

class UsuarioPut(UsuarioBase):
    ...

class UsuarioPatch(SQLModel):
    username: Annotated[str, Field(min_length=10, max_length=30, index=True, unique=True)] | None = None
    senha: Annotated[str, Field(min_length=8, max_length=30)] | None = None
    email: Annotated[str, Field(unique=True)] | None = None

class UsuarioDelete(Usuario):
    ...