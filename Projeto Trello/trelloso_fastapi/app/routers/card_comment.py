from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.engine import get_session
from app.models import (
    TrellosoUser,
    TrellosoCardComment,
    TrellosoCardCommentCreate, 
    TrellosoCardCommentRead, 
    TrellosoCardCommentUpdate,
    TrellosoCard,
    TrellosoCardMember
)
from app.secutiry import get_current_user


router = APIRouter()

@router.post("/", response_model=TrellosoCardCommentRead)
def create_card_comment(
    *, 
    session: Session = Depends(get_session), 
    card_comment_in: TrellosoCardCommentCreate,
    current_user: TrellosoUser = Depends(get_current_user)
):
    
    db_card = session.get(TrellosoCard, card_comment_in.card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")

    # Tem um erro no modelo! O member_id deveria ser chave estrangeira de cardmember e não de user!
    db_member = (
        session.exec(
            select(TrellosoCardMember).
            where(TrellosoCardMember.member_id==current_user.id)
        ).first()
    )
    if not db_member and db_card.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Usuário não é Membro desse Cartão!")

    db_card_comment = TrellosoCardComment.model_validate(card_comment_in)
    db_card_comment.member_id = current_user.id
    session.add(db_card_comment)
    session.commit()
    session.refresh(db_card_comment)
    return db_card_comment


@router.get("/{card_cooment_id}", response_model=TrellosoCardCommentRead)
def read_card_comment(
    *, 
    session: Session = Depends(get_session), 
    card_cooment_id: int,
    current_user: TrellosoUser = Depends(get_current_user)
):
    db_card_comment = session.get(TrellosoCardComment, card_cooment_id)
    if not db_card_comment:
        raise HTTPException(status_code=404, detail="CardComment not found")
    return db_card_comment        


@router.patch("/{card_cooment_id}", response_model=TrellosoCardCommentRead)
def update_card_comment(
    *, 
    session: Session = Depends(get_session), 
    card_cooment_id: int, 
    card_comment_in: TrellosoCardCommentUpdate,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_card_comment = session.get(TrellosoCardComment, card_cooment_id)
    if not db_card_comment:
        raise HTTPException(status_code=404, detail="CardComment not found")
    if db_card_comment.member_id != current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a alterar esse Comentário!")
    card_comment_data = card_comment_in.model_dump(exclude_unset=True)
    for key, value in card_comment_data.items():
        setattr(db_card_comment, key, value)
    db_card_comment.updated_at = datetime.now()
    session.add(db_card_comment)
    session.commit()
    session.refresh(db_card_comment)
    return db_card_comment      


@router.delete("/{card_cooment_id}")
def delete_card_comment(
    *, 
    session: Session = Depends(get_session), 
    card_cooment_id: int,
    current_user: TrellosoUser = Depends(get_current_user)    
):
    db_card_comment = session.get(TrellosoCardComment, card_cooment_id)
    if not db_card_comment:
        raise HTTPException(status_code=404, detail="CardComment not found")
    if db_card_comment.member_id != current_user.id or db_card_comment.card.user_id!=current_user.id:
        raise HTTPException(status_code=401, detail="Você não está autorizado a alterar esse Comentário!")
    session.delete(db_card_comment)
    session.commit()
    return {"ok": True}
