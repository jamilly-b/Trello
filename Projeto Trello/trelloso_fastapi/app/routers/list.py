from datetime import datetime
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.engine import get_session
from app.secutiry import get_current_user
from app.models import (
    TrellosoUser,
    TrellosoList,
    TrellosoListCreate, 
    TrellosoListRead, 
    TrellosoListUpdate, 
    TrellosoListReadWithDetails,
    TrellosoCard,
    TrellosoCardReadFromList,
    TrellosoBoard
)


router = APIRouter()

@router.post("/", response_model=TrellosoListRead)
def create_list(
    *, 
    session: Session = Depends(get_session), 
    list_in: TrellosoListCreate,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_board = session.get(TrellosoBoard, list_in.board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Quadro não encontrado!")
    if db_board.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a criar uma Lista para esse Quadro!")
    db_list = TrellosoList.model_validate(list_in)
    db_list.user_id = current_user.id
    session.add(db_list)
    session.commit()
    session.refresh(db_list)
    return db_list


@router.get("/{list_id}", response_model=TrellosoListReadWithDetails)
def read_list(
    *, 
    session: Session = Depends(get_session), 
    list_id: int, 
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_list = session.get(TrellosoList, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="Lista não encontrada!")
    if db_list.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a acessar essa Lista!")
    return db_list        


@router.patch("/{list_id}", response_model=TrellosoListRead)
def update_list(
    *, 
    session: Session = Depends(get_session), 
    list_id: int, 
    list_in: TrellosoListUpdate,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_list = session.get(TrellosoList, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="Lista não encontrada!")
    if db_list.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a atualizar essa Lista!")
    list_in_data = list_in.model_dump(exclude_unset=True)

    if list_in.board_id:
        db_board = session.get(TrellosoBoard, list_in.board_id)
        if not db_board:
            raise HTTPException(status_code=404, detail="Quadro não encontrado!")
        if db_board.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="Você não está autorizado a mover essa lista para esse Quadro!")
        
    for key, value in list_in_data.items():
        setattr(db_list, key, value)
    db_list.updated_at = datetime.now()
    session.add(db_list)
    session.commit()
    session.refresh(db_list)
    return db_list      


@router.delete("/{list_id}")
def delete_list(
    *, 
    session: Session = Depends(get_session), 
    list_id: int,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_list = session.get(TrellosoList, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="Lista não encontrada!")
    if db_list.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a excluir essa Lista!")
    session.delete(db_list)
    session.commit()
    return {"ok": True}


@router.get("/{list_id}/cards", response_model=List[TrellosoCardReadFromList])
def get_list_cards(
    *, 
    session: Session = Depends(get_session), 
    list_id: int,
    current_user: TrellosoUser = Depends(get_current_user),
):
    db_list = session.get(TrellosoList, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="Lista não encontrada!")
    if db_list.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a recuperar os cards dessa Lista!")
    return db_list.cards
