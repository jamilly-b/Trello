from sqlmodel import Session
from app.secutiry import get_password_hash
from app.models import (
    TrellosoUser, TrellosoUserCreate, 
    TrellosoBoard, TrellosoBoardCreate,
    TrellosoCard, TrellosoCardCreate,
    TrellosoList, TrellosoListCreate,
    TrellosoTag, TrellosoTagCreate,
    TrellosoCardMember, TrellosoCardMemberCreate,
    TrellosoCardComment, TrellosoCardCommentCreate
)
from app.engine import engine, get_settings


def _create_users(session: Session, user: dict):
    user = TrellosoUserCreate(**user)
    db_user = TrellosoUser.model_validate(user)
    session.add(db_user)
    session.commit()
    return db_user


def _create_tags(session: Session, tag: dict):
    tag = TrellosoTagCreate(**tag)
    db_tag = TrellosoTag.model_validate(tag)
    session.add(db_tag)
    session.commit()
    return db_tag


def _create_cards(session: Session, card: dict):
    card = TrellosoCardCreate(**card)
    db_card = TrellosoCard.model_validate(card)
    db_card.user_id = 1
    session.add(db_card)
    session.commit()
    return db_card


def insert_test_data():
    if get_settings().recreate_db_startup:
        with Session(engine) as session:    
            user_1 = _create_users(session, {'name': 'Usuário 1', 'username': 'user1', 'password': get_password_hash('123456')})
            user_2 = _create_users(session, {'name': 'Usuário 2', 'username': 'user2', 'password': get_password_hash('123456')})
            user_3 = _create_users(session, {'name': 'Usuário 3', 'username': 'user3', 'password': get_password_hash('123456')})

            new_board = TrellosoBoardCreate(name="Board1")
            db_board = TrellosoBoard.model_validate(new_board)
            db_board.user_id = 1
            session.add(db_board)
            session.commit()

            new_list = TrellosoListCreate(name="List1", board_id=db_board.id, position=1)
            db_list = TrellosoList.model_validate(new_list)
            db_list.user_id = 1
            session.add(db_list)
            session.commit()

            tag_1 = _create_tags(session, {'name': 'info', 'color': '#b8daff'})
            tag_2 = _create_tags(session, {'name': 'sucess', 'color': '#c3e6cb'})
            tag_3 = _create_tags(session, {'name': 'danger', 'color': '#f5c6cb'})
            tag_4 = _create_tags(session, {'name': 'warning', 'color': '#ffeeba'})

            card_1 = _create_cards(session, {'name': 'Card 1', 'user_id': user_1.id, 'list_id':db_list.id, 'position': 1})
            card_2 = _create_cards(session, {'name': 'Card 2', 'user_id': user_1.id, 'list_id':db_list.id, 'position': 2})
            card_3 = _create_cards(session, {'name': 'Card 3', 'user_id': user_1.id, 'list_id':db_list.id, 'position': 3})
         
            card_tags = [
                {'card': card_1, 'tag': tag_1},
                {'card': card_1, 'tag': tag_2},
                {'card': card_2, 'tag': tag_3},
                {'card': card_3, 'tag': tag_1},
                {'card': card_3, 'tag': tag_3},
            ]
            for card_tag in card_tags:
                card_tag['card'].tags.append(card_tag['tag'])
                session.add(card_tag['card'])
            session.commit()

            card_members = [
                { 'card_id': 1, 'member_id': 2},
                { 'card_id': 1, 'member_id': 3},
            ]
            for card_member in card_members:
                new_card_member = TrellosoCardMemberCreate(**card_member)
                db_card_member = TrellosoCardMember.model_validate(new_card_member)
                session.add(db_card_member)
            session.commit()

            card_comments = [
                { 'card_id': 1, 'member_id': 2, 'comment': 'Muito bom!'},
                { 'card_id': 1, 'member_id': 3, 'comment': 'Acho que precisa melhorar!'},
            ]
            for card_comment in card_comments:
                new_card_comment = TrellosoCardCommentCreate(**card_comment)
                db_card_comment = TrellosoCardComment.model_validate(new_card_comment)
                db_card_comment.member_id = card_comment['member_id']
                session.add(db_card_comment)
            session.commit()
