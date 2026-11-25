from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from core.config import settings


if settings.DB_TYPE == "postgres":

    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL is required for PostgreSQL")

    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True
    )

elif settings.DB_TYPE == "sqlite":

    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

else:
    raise ValueError(
        "DB_TYPE must be either 'postgres' or 'sqlite'"
    )


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():

    if settings.DB_TYPE != "sqlite":
        return

    with SessionLocal() as db:

        db.execute(text("""
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(60) UNIQUE NOT NULL,
                class VARCHAR(3) NOT NULL,
                section VARCHAR(1) NOT NULL
            )
        """))

        db.commit()
