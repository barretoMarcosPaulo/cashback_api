from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    MANAGER_CPF: str
    CASHBACK_API: str
    CASHBACK_API_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()
