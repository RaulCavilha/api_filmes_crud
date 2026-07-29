from fastapi import FastAPI, APIRouter, Depends
from models.models import Filme
from typing import Annotated
from sqlmodel import Session
from database.database import get_session

router = APIRouter(prefix='/filmes', tags=["filmes"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.get(path="/", response_model=Filme)
async def mostra_filmes(session: SessionDep):
    pass