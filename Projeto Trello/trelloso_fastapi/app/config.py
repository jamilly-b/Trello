from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    recreate_db_startup: int
    fastapi_title: str
    api_router_prefix: str
    api_router_token: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int