import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DATABASE_USER')}:"
    f"{os.getenv('DATABASE_PASSWORD')}@"
    f"{os.getenv('DATABASE_HOST')}:"
    f"{os.getenv('DATABASE_PORT')}/"
    f"{os.getenv('DATABASE_NAME')}"
)


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
