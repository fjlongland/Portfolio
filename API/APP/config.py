from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_password: str = "localhost"
    database_username: str = "postgress"
    secret_key: str = "asgfsfg"

settings = Settings()