from typing import List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from app.engine import get_session
from app.secutiry import get_current_user
from app.models import (
    TrellosoUser,
    TrellosoTag, 
    # TagCreate, 
    TrellosoTagRead, 
    # TagUpdate, 
    TrellosoTagReadWithCards
)

router = APIRouter()


@router.get("/", response_model=List[TrellosoTagRead])
def read_tags(
    *,
    session: Session = Depends(get_session),
    current_user: TrellosoUser = Depends(get_current_user)
):
    db_tags= session.exec(select(TrellosoTag)).all()
    return db_tags


# As tags são controladas pelo sistema e os usuários devem usar apenas as que existem
# Criar um usuário admin para acessar esses endpoints
# @router.get("/{tag_id}", response_model=TagReadWithCards)
# def read_tag(
#     *, 
#     tag_id: int, 
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user)
# ):
#     db_tag = session.get(Tag, tag_id)
#     if not db_tag:
#         raise HTTPException(status_code=404, detail="Tag not found")
#     return db_tag


# @router.post("/", response_model=TagRead)
# def create_tag(
#     *, 
#     session: Session = Depends(get_session), 
#     tag_in: TagCreate,
#     current_user: User = Depends(get_current_user)
# ):
#     db_tag = Tag.model_validate(tag_in)
#     session.add(db_tag)
#     session.commit()
#     session.refresh(db_tag)
#     return db_tag


# @router.patch("/{tag_id}", response_model=TagRead)
# def update_tag(
#     *,
#     session: Session = Depends(get_session),
#     tag_id: int,
#     tag_in: TagUpdate,
#     current_user: User = Depends(get_current_user)
# ):
#     db_tag = session.get(Tag, tag_id)
#     if not db_tag:
#         raise HTTPException(status_code=404, detail="Tag not found")
#     tag_in_data = tag_in.model_dump(exclude_unset=True)
#     for key, value in tag_in_data.items():
#         setattr(db_tag, key, value)
#     session.add(db_tag)
#     session.commit()
#     session.refresh(db_tag)
#     return db_tag


# @router.delete("/{tag_id}")
# def delete_tag(
#     *, 
#     session: Session = Depends(get_session), 
#     tag_id: int,
#     current_user: User = Depends(get_current_user)
# ):
#     db_tag = session.get(Tag, tag_id)
#     if not db_tag:
#         raise HTTPException(status_code=404, detail="Tag not found")
#     session.delete(db_tag)
#     session.commit()
#     return {"ok": True}