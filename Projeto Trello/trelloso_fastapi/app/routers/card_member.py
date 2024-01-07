from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.engine import get_session
from app.models import (
    TrellosoUser,
    TrellosoCardMember,
    TrellosoCardMemberCreate, 
    TrellosoCardMemberRead, 
    TrellosoCardMemberUpdate,
    TrellosoCard
)
from app.secutiry import get_current_user


router = APIRouter()

@router.post("/", response_model=TrellosoCardMemberRead)
def create_card_member(
    *, 
    session: Session = Depends(get_session), 
    card_member_in: TrellosoCardMemberCreate,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_card = session.get(TrellosoCard, card_member_in.card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    if db_card.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a adicionar um Membro nesse Cartão!")
    db_card_member = TrellosoCardMember.model_validate(card_member_in)
    session.add(db_card_member)
    session.commit()
    session.refresh(db_card_member)
    return db_card_member


@router.get("/{card_member_id}", response_model=TrellosoCardMemberRead)
def read_card_member(
    *, 
    session: Session = Depends(get_session), 
    card_member_id: int,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_card_member = session.get(TrellosoCardMember, card_member_id)
    if not db_card_member:
        raise HTTPException(status_code=404, detail="Membro não encontrado para esse Cartão!")
    return db_card_member        


@router.delete("/{card_member_id}")
def delete_card_member(
    *, 
    session: Session = Depends(get_session), 
    card_member_id: int,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_card_member = session.get(TrellosoCardMember, card_member_id)
    if not db_card_member:
        raise HTTPException(status_code=404, detail="Membro não encontrado para esse Cartão!")
    if db_card_member.member_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a excluir esse Membro desse Cartão!")
    session.delete(db_card_member)
    session.commit()
    return {"ok": True}