from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from functools import lru_cache
from .config import Settings

@lru_cache
def get_settings():
    return Settings()    

def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    if settings.recreate_db_startup:
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)


settings = get_settings()
postgres_url = \
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}" \
    f"@{settings.postgres_host}:{settings.postgres_port}/" \
    f"{settings.postgres_db}"
engine = create_engine(postgres_url, echo=True)
