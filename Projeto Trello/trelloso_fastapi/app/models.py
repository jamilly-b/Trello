from pydantic import BaseModel

from datetime import datetime

from typing import List, Optional, ClassVar

from sqlmodel import Field, Relationship, SQLModel

# Para os campos calculados! Não encontrei uma solução nativa do SQLModel
from sqlalchemy.orm import column_property
from sqlalchemy import select, func
from sqlalchemy.sql import text

class Token(BaseModel):
    access_token: str
    token_type: str

#TRELLOSO CARDMEMBER#############################################################

class TrellosoCardMemberBase(SQLModel):
    card_id: Optional[int] = Field(default=None, foreign_key="card.id")
    member_id: Optional[int] = Field(default=None, foreign_key="user.id")


class TrellosoCardMember(TrellosoCardMemberBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    card: Optional["TrellosoCard"] = Relationship(back_populates="cardmembers")
    member: Optional["TrellosoUser"] = Relationship(back_populates="cardmembers")

    __tablename__ = "cardmember"


class TrellosoCardMemberCreate(TrellosoCardMemberBase):
    pass


class TrellosoCardMemberRead(TrellosoCardMemberBase):
    id: int


class TrellosoCardMemberUpdate(SQLModel):
    card_id: Optional[int] = None
    member_id: Optional[int] = None    

#TRELLOSO USER#############################################################

class TrellosoUserBase(SQLModel):
    name: str = Field(index=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    avatar_url: Optional[str] = Field(default=None, nullable=True)


class TrellosoUser(TrellosoUserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    cards: List["TrellosoCard"] = Relationship(back_populates="members", link_model=TrellosoCardMember)

    boards: List["TrellosoBoard"] = Relationship(back_populates="user")
    lists: List["TrellosoList"] = Relationship(back_populates="user")
    cardcomments: List["TrellosoCardComment"] = Relationship(back_populates="member")
    cardmembers: List["TrellosoCardMember"] = Relationship(back_populates="member")
    
    __tablename__ = "user"


class TrellosoUserCreate(TrellosoUserBase):
    password: str


class TrellosoUserRead(TrellosoUserBase):
    id: int


class TrellosoUserUpdate(SQLModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None


#TRELLOSO CARDCOMMENT########################################################

class TrellosoCardCommentBase(SQLModel):
    comment: str = Field(nullable=False)
    card_id: Optional[int] = Field(default=None, foreign_key="card.id")


class TrellosoCardComment(TrellosoCardCommentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Usuário que fez o comentário!
    member_id: int = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    member: Optional[TrellosoUser] = Relationship(back_populates="cardcomments")
    card: Optional["TrellosoCard"] = Relationship(back_populates="cardcomments")

    __tablename__ = "cardcomment"


class TrellosoCardCommentCreate(TrellosoCardCommentBase):
    pass


class TrellosoCardCommentRead(TrellosoCardCommentBase):
    id: int


class TrellosoCardCommentUpdate(SQLModel):
    comment: Optional[str] = None


#TRELLOSO BOARD############################################################
    
class TrellosoBoardBase(SQLModel):
    name: str = Field(index=True, nullable=False)
    color: str = Field(default='#FFFFF')
    favorito: bool = Field(default=False)


class TrellosoBoard(TrellosoBoardBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    user: Optional[TrellosoUser] = Relationship(back_populates="boards")
    
    lists: List["TrellosoList"] = Relationship(
        back_populates="board",
        sa_relationship_kwargs={"order_by": "asc(TrellosoList.position)"}        
    )    

    __tablename__ = "board"


class TrellosoBoardCreate(TrellosoBoardBase):
    pass


class TrellosoBoardRead(TrellosoBoardBase):
    id: int


class TrellosoBoardUpdate(SQLModel):
    name: Optional[str] = None
    color: Optional[str] = None
    favorito: Optional[bool] = None


#TRELLOSO LIST############################################################

class TrellosoListBase(SQLModel):
    name: str = Field(index=True, nullable=False)
    board_id: int = Field(default=None, foreign_key="board.id")
    position: int = Field(nullable=False)


class TrellosoList(TrellosoListBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    user: Optional[TrellosoUser] = Relationship(back_populates="lists")
    board: Optional[TrellosoBoard] = Relationship(back_populates="lists")

    cards: List["TrellosoCard"] = Relationship(
        back_populates="list",
        sa_relationship_kwargs={"order_by": "asc(TrellosoCard.position)"}        
    )

    __tablename__ = "list"


class TrellosoListCreate(TrellosoListBase):
    pass


class TrellosoListRead(TrellosoListBase):
    id: int


class TrellosoListUpdate(SQLModel):
    name: Optional[str] = None
    board_id: Optional[int] = None


#TRELLOSO CARDTAG##########################################################

class TrellosoCardTagBase(SQLModel):
    card_id: Optional[int] = Field(
        default=None, foreign_key="card.id", primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )


class TrellosoCardTag(TrellosoCardTagBase, table=True):
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    card: Optional["TrellosoCard"] = Relationship(back_populates="cardtags")
    tag: Optional["TrellosoTag"] = Relationship(back_populates="cardtags")

    __tablename__ = "cardtag"


class TrellosoCardTagCreate(TrellosoCardTagBase):
    pass


class TrellosoCardTagRead(TrellosoCardTagBase):
    pass


class TrellosoCardTagUpdate(SQLModel):
    card_id: Optional[int] = None
    tag_id: Optional[int] = None

#TRELLOSO CARD############################################################

class TrellosoCardBase(SQLModel):
    name: str = Field(index=True, nullable=False)
    date: Optional[datetime] = Field(default=None, nullable=True)
    list_id: Optional[int] = Field(default=None, foreign_key="list.id")
    position: int = Field(nullable=False)


class TrellosoCard(TrellosoCardBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    tags: List["TrellosoTag"] = Relationship(back_populates="cards", link_model=TrellosoCardTag)
    members: List["TrellosoUser"] = Relationship(back_populates="cards", link_model=TrellosoCardMember)

    user: Optional[TrellosoUser] = Relationship(back_populates="cards")
    list: Optional[TrellosoList] = Relationship(back_populates="cards")

    cardcomments: List["TrellosoCardComment"] = Relationship(
        back_populates="card",
        sa_relationship_kwargs={"order_by": "asc(TrellosoCardComment.id)"}
    )
    cardmembers: List["TrellosoCardMember"] = Relationship(back_populates="card")
    cardtags: List["TrellosoCardTag"] = Relationship(back_populates="card")

    cardcomments_count: ClassVar = column_property(
        select(func.count(TrellosoCardComment.id))
        .where(TrellosoCardComment.card_id == text("card.id"))
        .scalar_subquery()
    )

    cardmembers_count: ClassVar = column_property(
        select(func.count(TrellosoCardMember.id))
        .where(TrellosoCardMember.card_id == text("card.id"))
        .scalar_subquery()
    )

    __tablename__ = "card"


class TrellosoCardCreate(TrellosoCardBase):
    pass


class TrellosoCardRead(TrellosoCardBase):
    id: int


class TrellosoCardUpdate(SQLModel):
    name: Optional[str] = None
    date: Optional[datetime] = None
    list_id: Optional[int] = None

#TRELLOSO TAG#############################################################

class TrellosoTagBase(SQLModel):
    name: str = Field(index=True, nullable=False)
    color: str = Field(nullable=False)


class TrellosoTag(TrellosoTagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

    cards: List[TrellosoCard] = Relationship(back_populates="tags", link_model=TrellosoCardTag)

    cardtags: List["TrellosoCardTag"] = Relationship(back_populates="tag")


    __tablename__ = "tag"


class TrellosoTagCreate(TrellosoTagBase):
    pass


class TrellosoTagRead(TrellosoTagBase):
    id: int


class TrellosoTagUpdate(SQLModel):
    name: Optional[str] = None
    color: Optional[str] = None
   
#TRELLOSO READ WITH DETAILS####################################################
    
class TrellosoUserReadWithDetails(TrellosoUserRead):
    boards: List[TrellosoBoard] = []
    # lists: List[ListT] = []
    # cards: List[Card] = []
    # cardcomments: List[CardComment] = []
    # cardmembers: List[CardMember] = []
    # cardtags: List[CardTag] = []


class TrellosoTagReadWithCards(TrellosoTagRead):
    cards: List[TrellosoCardRead] = []


class TrellosoBoardReadWithDetails(TrellosoBoardRead):
    lists: List[TrellosoListRead] = []


class TrellosoCardTagWithDetails(TrellosoCardTagRead):
    tag: TrellosoTag


class TrellosoCardReadFromList(TrellosoCardRead):
    cardcomments_count: int = 0
    cardmembers_count: int = 0
    tags: List[TrellosoTagRead] = []     


class TrellosoCardReadWithDetails(TrellosoCardRead):
    cardcomments: List[TrellosoCardComment] = []
    cardmembers: List[TrellosoCardMember] = []
    tags: List[TrellosoTagRead] = []     


class TrellosoListReadWithDetails(TrellosoListRead):
    cards: List[TrellosoCardReadFromList] = []


class TrellosoCardMemberReadWithDetails(TrellosoCardMemberRead):
    # card: TrellosoCard
    member: TrellosoUser


class TrellosoCardTagReadWithDetails(TrellosoCardTagRead):
    # card: TrellosoCard
    tag: TrellosoTag