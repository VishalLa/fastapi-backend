import os
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_DIR = BASE_DIR / "db"
DB_FILE = DB_DIR / "test.sqlite3"

DB_DIR.mkdir(parents=True, exist_ok=True)

if not DB_FILE.exists():
    DB_FILE.touch()

class Settings(BaseSettings):
    DEBUG: bool = False 

    SQLALCHEMY_SYNC_DATABASE_URI: str = (
        f"sqlite:///{DB_FILE.as_posix()}"
    )

    SQLALCHEMY_ASYNC_DATABASE_URI: Optional[str] = (
        f"sqlite+aiosqlite:///{DB_FILE.as_posix()}"
    )

    API_BASE: Optional[str] = None
    API_SERVER_URL: Optional[str] = None

    SCHEDULER_API_ENABLED: bool = True 

    LOG_FILE: str = "debug.log"
    LOG_FORMAT: str = "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

def _normalize_sqlite_uri(uri: str | None) -> str | None:
    if not uri:
        return uri
    # get the path after the first ':///' (handles sqlite+driver too)
    if ':///' in uri:
        _prefix, _sep, tail = uri.partition(':///')
        db_path = tail
    else:
        return uri

    p = Path(db_path)
    if not p.is_absolute():
        p = BASE_DIR / p

    try:
        p.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    try:
        if not p.exists():
            p.touch()
    except Exception:
        pass

    return f"{_prefix}:///{p.as_posix()}"

try:
    settings.SQLALCHEMY_SYNC_DATABASE_URI = _normalize_sqlite_uri(
        getattr(settings, 'SQLALCHEMY_SYNC_DATABASE_URI', None)
    )
except Exception:
    pass

try:
    settings.SQLALCHEMY_ASYNC_DATABASE_URI = _normalize_sqlite_uri(
        getattr(settings, 'SQLALCHEMY_ASYNC_DATABASE_URI', None)
    )
except Exception:
    pass
