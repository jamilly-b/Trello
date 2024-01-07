from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.engine import get_session
from app.models import (
    TrellosoUser, 
    TrellosoUserCreate, 
    TrellosoUserRead, 
    TrellosoUserUpdate, 
    TrellosoUserReadWithDetails,
    TrellosoBoard,
    TrellosoBoardRead
)
from app.secutiry import get_password_hash, get_current_user

router = APIRouter()


@router.get("/me", response_model=TrellosoUserRead)
async def show_me(current_user: TrellosoUser = Depends(get_current_user)):
    return current_user


@router.post("/", response_model=TrellosoUserRead)
def create_user(
    *, 
    session: Session = Depends(get_session), 
    user_in: TrellosoUserCreate
):
    db_user = (
        session.exec(
            select(TrellosoUser).
            where(TrellosoUser.username==user_in.username)
        ).first()
    )
    if db_user:
        raise HTTPException(status_code=409, detail="Já existe um usuário com esse username!")

    hashed_password = get_password_hash(user_in.password)
    user_in.password = hashed_password
    db_user = TrellosoUser.model_validate(user_in)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[TrellosoUserRead])
def read_users(
    *,
    session: Session = Depends(get_session)
):
    db_users= session.exec(select(TrellosoUser)).all()
    return db_users


@router.get("/{user_id}", response_model=TrellosoUserReadWithDetails)
def read_user(
    *, 
    user_id: int, 
    session: Session = Depends(get_session),
    current_user: TrellosoUser = Depends(get_current_user)
):
    db_user = session.get(TrellosoUser, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a acessar esse Usuário!")
    return db_user


@router.patch("/{user_id}", response_model=TrellosoUserRead)
def update_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
    user_in: TrellosoUserUpdate,
    current_user: TrellosoUser = Depends(get_current_user)
):
    db_user = session.get(TrellosoUser, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a alterar esse Usuário!")
    user_in_data = user_in.model_dump(exclude_unset=True)
    for key, value in user_in_data.items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.now()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(
    *, 
    session: Session = Depends(get_session), 
    user_id: int,
    current_user: TrellosoUser = Depends(get_current_user)
):
    db_user = session.get(TrellosoUser, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a excluir esse Usuário!")
    session.delete(db_user)
    session.commit()
    return {"ok": True}


@router.get("/me/boards", response_model=List[TrellosoBoardRead])
async def read_users_boards(
    *, 
    session: Session = Depends(get_session), 
    current_user: TrellosoUser = Depends(get_current_user)
):
    return current_user.boards