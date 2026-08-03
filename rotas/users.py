from fastapi import FastAPI, APIRouter, Depends, HTTPException
from modelos.modelos import Usuario, UsuarioDelete, UsuarioPatch, UsuarioPublic, UsuarioPut
from typing import Annotated
from sqlmodel import Session, select, update, delete
from database.database import get_session
from uuid import uuid4, UUID
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users" ,tags=["Users"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get(path="/", response_model=UsuarioPublic)
async def mostra_usuarios(session: SessionDep):
    ...

@router.get(path="/{user_id}", response_model=UsuarioPublic)
async def mostra_usuario(session: SessionDep, user_id: UUID):
    if user := session.exec(select(Usuario).where(Usuario.uuid == user_id)):
        return user
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")

@router.post(path="/", response_model=UsuarioPublic)
async def adiciona_usuario(session: SessionDep, usuario: Usuario):
    novo_uuid = uuid4()

    new_user = Usuario(
        uuid=novo_uuid,
        username=usuario.username,
        senha=usuario.senha,
        email=usuario.email
    )

    session.add(new_user)
    try:
        session.commit()
        session.refresh(new_user)
        return new_user
    
    except IntegrityError:
        # Dsefaz a operação: 
        session.rollback()

        # Mostra o erro ao usuário:
        raise HTTPException(
            status_code=409,
            detail="Username ou email já está em uso!"
        )

    
@router.patch(path="/{user_id}", response_model=UsuarioPublic)
async def atualiza_usuario_parcial(session: SessionDep, usuario: UsuarioPatch, user_id: UUID):
    if query := session.exec(select(Usuario).where(Usuario.uuid == user_id)).first():
        json_data = usuario.model_dump(exclude_unset=True)
        for chave, valor in json_data.items():
            setattr(query, chave, valor)

        session.add(query)
        session.commit()
        session.refresh(query)

        return UsuarioPublic.model_validate(query)

    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")

@router.put(path="/{user_id}", response_model=UsuarioPublic)
async def atualiza_usuario(session: SessionDep, usuario: Usuario, user_id: UUID):
    if query := session.exec(select(Usuario).where(Usuario.uuid == user_id)).first():
        json_data = usuario.model_dump()
        for chave, valor in json_data.items():
            setattr(query, chave, valor)

        session.add(query)
        session.commit()
        session.refresh(query)

        return UsuarioPublic.model_validate(query)

    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")

@router.delete(path="/{user_id}", response_model=UsuarioDelete)
async def deleta_usuario(session: SessionDep, usuario: UsuarioDelete, user_id: UUID):
    if query := session.exec(select(Usuario).where(Usuario.uuid == user_id)).first():
        session.delete(query)
        session.commit()

        return f"Usuário -> {query.username} deletado com sucesso!"

    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")