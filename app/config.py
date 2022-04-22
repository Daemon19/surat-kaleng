import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Memastikan templates otomatis dimuat ulang
    TEMPLATES_AUTO_RELOAD = True

    # Mengatur sesi agar menggunakan filesystem (bukan signed cookies)
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL", "").replace("://", "ql://", 1)
        or "sqlite:///surat_kaleng.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
