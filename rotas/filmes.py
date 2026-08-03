from fastapi import FastAPI, APIRouter, Depends, HTTPException
from modelos.modelos import Filme, FilmePatch, FilmeDelete, FilmePublic, FilmePut
from typing import Annotated
from sqlmodel import Session, delete, select, update
from database.database import get_session
from uuid import UUID, uuid4
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/filmes", tags=["Filmes"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.get(path="/", response_model=Filme)
async def mostra_filmes(session: SessionDep):
    ...

@router.get(path="/{filme_id}", response_model=FilmePublic)
async def mostra_filme(session: SessionDep, filme_id: UUID) -> Filme:
    if filme := session.exec(select(Filme).where(Filme.uuid == filme_id)).first():
        return filme
    raise HTTPException(status_code=404, detail="Livro não encontrado")

@router.post(path="/", response_model=FilmePublic)
async def adiciona_filme(session: SessionDep, filme: Filme):
    novo_uuid = uuid4()
    new_filme = Filme(
        uuid=novo_uuid,
        titulo=filme.titulo,
        sinopse=filme.sinopse,
        ano=filme.ano,
        nota_media=filme.nota_media,
        popularidade=filme.popularidade
    )

    session.add(new_filme)
    session.commit()
    session.refresh(new_filme)
    
    return new_filme
    
@router.patch(path="/{filme_id}", response_model=FilmePublic)
async def atualiza_filme_parcial(session: SessionDep, filme: FilmePatch, filme_id: UUID):
    if query := session.exec(select(Filme).where(Filme.uuid == filme_id)).first():
        user_data = filme.model_dump(exclude_unset=True)
        for chave, valor in user_data.items():
            setattr(query, chave, valor)

        session.add(query)
        session.commit()
        session.refresh(query)

        return FilmePublic.model_validate(query)
    else:
        raise HTTPException(status_code=404, detail="Livro não encotrado!")

@router.put(path="/{filme_id}", response_model=FilmePut)
async def atualiza_filme(session: SessionDep, filme_id: UUID, filme: Filme):
    if query := session.exec(select(Filme).where(Filme.uuid == filme_id)).first():
        json_data = filme.model_dump()
        for chave, valor in json_data.items():
            setattr(query, chave, valor)

        session.add(query)
        session.commit()
        session.refresh(query)

        return query
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado!")


@router.delete(path="/{filme_id}", response_model=FilmeDelete)
async def deleta_filme(session: SessionDep, filme_id: UUID):
    if filme := session.exec(select(Filme).where(Filme.uuid == filme_id)).first():
        session.delete(filme)
        session.commit()
        return f"Filme deletado com sucesso -> {filme}"
    else:
        raise Exception("Filme não encontrado!")