from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.engine import get_session
from app.models import (
    TrellosoUser,
    TrellosoCardTag,
    TrellosoCardTagCreate, 
    TrellosoCardTagRead, 
    TrellosoCardTagUpdate
)
from app.secutiry import get_current_user

router = APIRouter()

@router.post("/", response_model=TrellosoCardTagRead)
def create_card_tag(
    *, 
    session: Session = Depends(get_session), 
    card_tag_in: TrellosoCardTagCreate,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_card_tag = session.get(TrellosoCardTag, (card_tag_in.card_id, card_tag_in.tag_id))
    if not db_card_tag:
        db_card_tag = TrellosoCardTag.model_validate(card_tag_in)
        session.add(db_card_tag)
        session.commit()
        session.refresh(db_card_tag)
    return db_card_tag


@router.get("/{card_id}/{tag_id}", response_model=TrellosoCardTagRead)
def read_card_tag(
    *, 
    session: Session = Depends(get_session), 
    card_id: int,
    tag_id: int,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_card_tag = session.get(TrellosoCardTag, (card_id, tag_id))
    if not db_card_tag:
        raise HTTPException(status_code=404, detail="Tag não encontrada para esse Cartão")
    return db_card_tag        


@router.delete("/{card_id}/{tag_id}")
def delete_card_tag(
    *, 
    session: Session = Depends(get_session), 
    card_id: int,
    tag_id: int,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_card_tag = session.get(TrellosoCardTag, (card_id, tag_id))
    if not db_card_tag:
        raise HTTPException(status_code=404, detail="Tag não encontrada para esse Cartão")
    session.delete(db_card_tag)
    session.commit()
    return {"ok": True}
