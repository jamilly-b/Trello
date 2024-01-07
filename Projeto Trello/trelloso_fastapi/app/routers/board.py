from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.engine import get_session
from app.models import (
    TrellosoUser,
    TrellosoBoard, 
    TrellosoBoardCreate, 
    TrellosoBoardRead, 
    TrellosoBoardUpdate, 
    TrellosoBoardReadWithDetails,
    TrellosoList,
    TrellosoListReadWithDetails
)
from app.secutiry import get_current_user


router = APIRouter()

@router.post("/", response_model=TrellosoBoardRead)
def create_board(
    *, 
    session: Session = Depends(get_session), 
    board_in: TrellosoBoardCreate,
    current_user: TrellosoUser = Depends(get_current_user)
):
    db_board = TrellosoBoard.model_validate(board_in)
    db_board.user_id = current_user.id
    session.add(db_board)
    session.commit()
    session.refresh(db_board)
    return db_board


@router.get("/{board_id}", response_model=TrellosoBoardReadWithDetails)
def read_board(
    *, 
    session: Session = Depends(get_session), 
    board_id: int,
    current_user: TrellosoUser = Depends(get_current_user)
):
    db_board = session.get(TrellosoBoard, board_id)        
    if not db_board:
        raise HTTPException(status_code=404, detail="Quadro não encontrado!")
    if db_board.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a acessar esse Quadro!")
    return db_board        


@router.patch("/{board_id}", response_model=TrellosoBoardRead)
def update_board(
    *, 
    session: Session = Depends(get_session), 
    board_id: int, 
    board_in: TrellosoBoardUpdate,
    current_user: TrellosoUser = Depends(get_current_user)
):
    db_board = session.get(TrellosoBoard, board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Quadro não encontrado!")
    if db_board.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a atualizar esse Quadro!")
    board_in_data = board_in.model_dump(exclude_unset=True)
    for key, value in board_in_data.items():
        setattr(db_board, key, value)
    db_board.updated_at = datetime.now()
    session.add(db_board)
    session.commit()
    session.refresh(db_board)
    return db_board      


@router.delete("/{board_id}")
def delete_board(
    *, 
    session: Session = Depends(get_session), 
    board_id: int,
    current_user: TrellosoUser = Depends(get_current_user)
):
    db_board = session.get(TrellosoBoard, board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Quadro não encontrado!")
    if db_board.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a excluir esse Quadro!")
    session.delete(db_board)
    session.commit()
    return {"ok": True}


@router.get("/{board_id}/lists", response_model=List[TrellosoListReadWithDetails])
def get_board_lists(
    *, 
    session: Session = Depends(get_session), 
    board_id: int,
    current_user: TrellosoUser = Depends(get_current_user),
):
    db_board = session.get(TrellosoBoard, board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Quadro não encontrado!")
    if db_board.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a recuperar as listas desse quadro!")
    return db_board.lists
