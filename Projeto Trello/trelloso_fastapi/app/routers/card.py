from datetime import datetime
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.engine import get_session
from app.models import (
    TrellosoUser,
    TrellosoCard,
    TrellosoCardCreate, 
    TrellosoCardRead, 
    TrellosoCardUpdate, 
    TrellosoCardReadWithDetails,
    TrellosoCardComment,
    TrellosoCardCommentRead,
    TrellosoTagRead,
    TrellosoList
)
from app.secutiry import get_current_user

router = APIRouter()

@router.post("/", response_model=TrellosoCardRead)
def create_card(
    *, 
    session: Session = Depends(get_session), 
    card_in: TrellosoCardCreate,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_list = session.get(TrellosoList, card_in.list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="Lista não encontrada!")
    if db_list.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a criar um card nessa Lista!")    
    db_card = TrellosoCard.model_validate(card_in)
    db_card.user_id = current_user.id
    session.add(db_card)
    session.commit()
    session.refresh(db_card)
    return db_card


@router.get("/{card_id}", response_model=TrellosoCardReadWithDetails)
def read_card(
    *, 
    session: Session = Depends(get_session), 
    card_id: int,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_card = session.get(TrellosoCard, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    return db_card        


@router.patch("/{card_id}", response_model=TrellosoCardRead)
def update_card(
    *, 
    session: Session = Depends(get_session), 
    card_id: int, 
    card_in: TrellosoCardUpdate,
    current_user: TrellosoUser = Depends(get_current_user)        
):
    db_card = session.get(TrellosoCard, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    if db_card.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a atualizar esse Cartão!")
    card_in_data = card_in.model_dump(exclude_unset=True)
    for key, value in card_in_data.items():
        setattr(db_card, key, value)
    db_card.updated_at = datetime.now()
    session.add(db_card)
    session.commit()
    session.refresh(db_card)
    return db_card      


@router.delete("/{card_id}")
def delete_card(
    *, 
    session: Session = Depends(get_session), 
    card_id: int,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_card = session.get(TrellosoCard, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    session.delete(db_card)
    session.commit()
    return {"ok": True}


@router.get("/{card_id}/comments", response_model=List[TrellosoCardCommentRead])
def read_card_comments(
    *, 
    session: Session = Depends(get_session), 
    card_id: int,
    current_user: TrellosoUser = Depends(get_current_user),
):
    db_card = session.get(TrellosoCard, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado!")
    if db_card.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a recuperar os Comentários desse Cartão!")

    return db_card.cardcomments


@router.get("/{card_id}/members", response_model=List[TrellosoUser])
def read_card_members(
    *, 
    session: Session = Depends(get_session), 
    card_id: int,
    current_user: TrellosoUser = Depends(get_current_user),
):
    db_card = session.get(TrellosoCard, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado!")
    if db_card.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a recuperar os Membros desse Cartão!")

    return db_card.members


@router.get("/{card_id}/tags", response_model=List[TrellosoTagRead])
def read_card_tags(
    *, 
    session: Session = Depends(get_session), 
    card_id: int,
    current_user: TrellosoUser = Depends(get_current_user),
):
    db_card = session.get(TrellosoCard, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado!")
    if db_card.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a recuperar as Tags desse Cartão!")

    return db_card.tags