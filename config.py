import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    POSTGRES_SERVER: str = (
        f'{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}'
    )
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URL")


settings = Settings()
