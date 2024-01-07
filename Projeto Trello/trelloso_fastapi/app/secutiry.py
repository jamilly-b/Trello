import logging

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.models import TrellosoUser
from app.engine import get_session, get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Para remover o warning do bcrypt com o passlib
logging.getLogger('passlib').setLevel(logging.ERROR)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_settings().api_router_token)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_settings().secret_key, algorithm=get_settings().algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=[get_settings().algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    statement = select(TrellosoUser).where(TrellosoUser.username == username)
    db_user = session.exec(statement).first()
    if db_user is None:
        raise credentials_exception   
    return db_user
