import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "kamu-tidak-akan-menebak"
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL") or f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
