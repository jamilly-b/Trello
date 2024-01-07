from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.engine import get_session, get_settings
from app.models import TrellosoUser, Token
from app.secutiry import (
    verify_password, 
    create_access_token
)


router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    *, session: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()
):
    
    statement = select(TrellosoUser).where(TrellosoUser.username == form_data.username)
    db_user = session.exec(statement).first()
    if (not db_user) or (not verify_password(form_data.password, db_user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=get_settings().access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


