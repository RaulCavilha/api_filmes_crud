from fastapi import FastAPI, APIRouter, Depends, HTTPException
from modelos.modelos import Filme, FilmePatch, FilmeDelete, FilmePublic, FilmePut
from typing import Annotated
from sqlmodel import Session, delete, select, update
from database.database import get_session
from uuid import UUID, uuid4

router = APIRouter(tags=["Filmes"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.get(path="/filmes", response_model=Filme)
async def mostra_filmes(session: SessionDep):
    ...

@router.get(path="/filmes/{filme_id}", response_model=FilmePublic)
async def mostra_filme(session: SessionDep, filme_id: UUID) -> Filme:
    if filme := session.exec(select(Filme).where(Filme.uuid == filme_id)).first():
        return filme
    raise HTTPException(status_code=404, detail="Livro não encontrado")

@router.post(path="/filmes", response_model=FilmePublic)
async def adiciona_filme(session: SessionDep, filme: FilmePut):
    novo_uuid = uuid4()

    novo_filme = Filme(
        uuid=novo_uuid,
        titulo=filme.titulo,
        nota_media=filme.nota_media,
        sinopse=filme.sinopse,
        ano=filme.ano
    )

    session.add(novo_filme)
    session.commit()

    return FilmePublic.model_validate(novo_filme)
    
@router.patch(path="/filmes/{filme_id}", response_model=FilmePublic)
async def atualiza_filme(session: SessionDep, filme: FilmePatch):
    ...

@router.delete(path="/filmes/{filme_id}", response_model=FilmeDelete)
async def deleta_filme(session: SessionDep, filme_id: UUID):
    if filme := session.exec(select(Filme).where(Filme.uuid == filme_id)).first():
        session.delete(filme)
        session.commit()
        return f"Filme deletado com sucesso -> {filme}"
    else:
        raise Exception("Filme não encontrado!")