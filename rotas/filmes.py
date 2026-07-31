from fastapi import FastAPI, APIRouter, Depends, HTTPException
from modelos.modelos import Filme, FilmePatch, FilmeDelete, FilmePublic
from typing import Annotated
from sqlmodel import Session, delete, select, update
from database.database import get_session
from uuid import UUID

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

@router.post(path="/filmes", response_model=Filme)
async def adiciona_filme(session: SessionDep):
    ...
    
@router.patch(path="/filmes/{filme_id}", response_model=Filme)
async def atualiza_filme(session: SessionDep):
    ...

@router.delete(path="/filmes/{filme_id}", response_model=FilmeDelete)
async def deleta_filme(session: SessionDep):
    ...