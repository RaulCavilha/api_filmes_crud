from fastapi import FastAPI, APIRouter, Depends, HTTPException
from modelos.modelos import Filme, Usuario, FilmePatch, FilmeDelete, UsuarioDelete, UsuarioPatch
from typing import Annotated
from sqlmodel import Session, select, update, delete
from database.database import get_session
from uuid import uuid4, UUID

router = APIRouter(tags=["Users"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get(path="/users", response_model=Usuario)
async def mostra_usuarios(session: SessionDep):
    ...

@router.get(path="/users/{user_id}", response_model=Usuario)
async def mostra_usuario(session: SessionDep, user_id: UUID):
    ...

@router.post(path="/users", response_model=Usuario)
async def adiciona_usuario(session: SessionDep):
    ...
    
@router.patch(path="/users/{user_id}", response_model=Usuario)
async def atualiza_usuario(session: SessionDep):
    ...

@router.delete(path="/users/{user_id}", response_model=UsuarioDelete)
async def deleta_usuario(session: SessionDep):
    ...